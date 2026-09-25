"use strict";
let token, articles = [], current = null, session = null, annotation = null;
let page = 1, view = "text", searchTerm = "", searchIndex = 0;
let changed = 0, saved = 0, pending = null, saving = false;
const $ = id => document.getElementById(id);
function node(tag, attrs = {}, children = []) {
  const item = document.createElement(tag);
  for (const [key, val] of Object.entries(attrs)) {
    if (key === "class") item.className = val;
    else if (key === "text") item.textContent = val;
    else if (key === "onclick") item.addEventListener("click", val);
    else item.setAttribute(key, val);
  }
  for (const child of children) item.append(child);
  return item;
}
const btn = (label, click, css = "") => node("button", {type:"button", text:label, class:css, onclick:click});
const message = (value, error = false) => { $("save-status").textContent = value; $("save-status").classList.toggle("error", error); };
async function request(url, method = "GET", body = null) {
  const options = {method, headers:{"X-Annotation-Token":token || ""}};
  if (body) { options.headers["Content-Type"] = "application/json"; options.body = JSON.stringify(body); }
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data;
}
async function refreshList() {
  const data = await request("/api/articles");
  token = data.token; articles = data.articles;
  $("reviewer").textContent = `Reviewer: ${data.reviewer_id}`;
  const list = $("articles"); list.replaceChildren();
  for (const item of articles) {
    const b = btn("", () => openArticle(item.corpus_id), "article-link" + (current?.corpus_id === item.corpus_id ? " selected" : ""));
    b.append(node("small", {text:item.corpus_id + " · " + item.doi}), node("strong", {text:item.title}), node("small", {text:item.state}));
    list.append(b);
  }
}
function dirty() {
  changed++; message("Unsaved changes");
  clearTimeout(pending); pending = setTimeout(() => { save().catch(e => message(e.message, true)); }, 650);
}
async function save() {
  clearTimeout(pending); pending = null;
  if (saving) { while (saving) await new Promise(resolve => setTimeout(resolve, 50)); }
  if (!current || changed === saved || session.state === "submitted") return;
  saving = true;
  try {
    while (changed !== saved) {
      const version = changed, snapshot = structuredClone(annotation), id = current.corpus_id;
      const result = await request(`/api/article/${encodeURIComponent(id)}`, "PUT", {revision:session.revision, annotation:snapshot});
      if (current?.corpus_id !== id) throw new Error("Article changed while saving");
      session = result; saved = version;
      message(changed === saved ? "Draft saved" : "Saving…");
    }
  } finally { saving = false; }
}
async function action(kind) {
  try {
    await save();
    if (kind === "submit" && !confirm("Submit and lock this independent gold annotation? You will not be able to edit it.")) return;
    session = await request(`/api/article/${encodeURIComponent(current.corpus_id)}`, "POST", {revision:session.revision, action:kind});
    message(kind === "submit" ? "Submitted and locked" : kind === "start" ? "Timer running" : "Timer paused");
    renderToolbar();
    if (kind === "submit") { renderAnnotations(); await refreshList(); }
  } catch (e) { message(e.message, true); }
}
async function openArticle(id) {
  try {
    await save();
    current = await request(`/api/article/${encodeURIComponent(id)}`);
    session = current.session; annotation = session.annotation;
    changed = saved = 0; page = 1; view = "text"; searchTerm = ""; searchIndex = 0;
    render(); await refreshList(); message(session.state === "submitted" ? "Submitted and locked" : "Draft ready");
  } catch (e) { message(e.message, true); }
}
function render() {
  const workspace = $("workspace"); workspace.replaceChildren();
  workspace.append(node("div", {class:"article-head"}, [node("h2", {text:current.title}),
    node("div", {class:"muted", text:`${current.corpus_id} · ${current.doi} · ${current.year} · ${current.pages.length} PDF pages`})]));
  const toolbar = node("div", {class:"toolbar", id:"toolbar"}); workspace.append(toolbar);
  const columns = node("div", {class:"columns"});
  columns.append(node("section", {class:"panel source-panel", id:"source-panel"}), node("section", {class:"panel annotation-body", id:"annotation-panel"}));
  workspace.append(columns); renderToolbar(); renderSource(); renderAnnotations();
}
function renderToolbar() {
  if (!current) return;
  const bar = $("toolbar"); bar.replaceChildren();
  bar.append(node("span", {class:"badge " + session.state, text:session.state.toUpperCase()}),
    node("span", {id:"clock", text:"00:00:00"}));
  if (session.state !== "submitted") {
    bar.append(btn(session.timer.running_since ? "Pause timer" : "Start timer", () => action(session.timer.running_since ? "pause" : "start")),
      btn("Save draft", async () => {try { await save(); message("Draft saved"); } catch(e) {message(e.message, true);} }),
      btn("Submit gold record", () => action("submit"), "primary"));
  }
  bar.append(node("span", {class:"muted", text:"Pause the timer for breaks. Autosave does not stop it."}));
  updateClock();
}
function updateClock() {
  if (!session || !$("clock")) return;
  let seconds = session.timer.seconds;
  if (session.timer.running_since) seconds += Math.max(0, (Date.now() - Date.parse(session.timer.running_since))/1000);
  seconds = Math.floor(seconds);
  $("clock").textContent = [Math.floor(seconds/3600), Math.floor(seconds/60)%60, seconds%60].map(n => String(n).padStart(2,"0")).join(":");
}
setInterval(updateClock, 1000);
function findNext() {
  const query = searchTerm.trim().toLowerCase();
  if (!query) return;
  for (let n = 0; n < current.pages.length; n++) {
    const i = (page - 1 + n) % current.pages.length;
    const text = current.pages[i].text.toLowerCase();
    const at = text.indexOf(query, n === 0 ? searchIndex : 0);
    if (at >= 0) {
      page = i + 1; searchIndex = at + query.length; view = "text"; renderSource();
      const pre = $("page-text"), range = document.createRange(), selection = window.getSelection();
      range.setStart(pre.firstChild, at); range.setEnd(pre.firstChild, at + query.length);
      selection.removeAllRanges(); selection.addRange(range);
      const body = pre.parentElement;
      body.scrollTop += range.getBoundingClientRect().top - body.getBoundingClientRect().top - 70;
      message(`Found on PDF page ${page}`); return;
    }
  }
  message("No more matches; search again from the first page", true);
  searchIndex = 0;
}
function renderSource() {
  const panel = $("source-panel"); panel.replaceChildren(node("h3", {text:"Source article"}));
  const controls = node("div", {class:"source-controls"});
  controls.append(btn("Text", () => {view="text"; renderSource();}), btn("PDF", () => {view="pdf"; renderSource();}));
  const pageSelect = node("select", {"aria-label":"PDF page"});
  for (const entry of current.pages) pageSelect.append(node("option", {value:entry.number, text:`Page ${entry.number}`}));
  pageSelect.value = page;
  pageSelect.onchange = () => {page = Number(pageSelect.value); searchIndex=0; renderSource();};
  controls.append(pageSelect, btn("Previous", () => {if(page>1){page--;searchIndex=0;renderSource();}}), btn("Next", () => {if(page<current.pages.length){page++;searchIndex=0;renderSource();}}));
  panel.append(controls);
  const search = node("div",{class:"source-controls"});
  const searchField = node("input",{type:"search",placeholder:"Search all pages", "aria-label":"Search article text"});
  searchField.value=searchTerm;
  searchField.oninput=() => {searchTerm=searchField.value; searchIndex=0;};
  searchField.onkeydown=e => {if(e.key === "Enter"){e.preventDefault();findNext();}};
  search.append(searchField,btn("Find next",findNext));panel.append(search);
  const box = node("div", {class:"source-body"});
  if (view === "text") {
    box.append(node("pre", {id:"page-text", text:current.pages[page-1].text}));
    panel.append(node("div", {class:"help", text:"Select exact text on this page; then use ‘Use selection’ in an evidence row. Page numbers refer to the PDF."}));
  } else {
    box.append(node("iframe", {title:"Source PDF", src:`/api/article/${encodeURIComponent(current.corpus_id)}/pdf#page=${page}`}));
    panel.append(node("div", {class:"help", text:"For PDF-only evidence, enter the exact quotation and printed PDF page manually."}));
  }
  panel.append(box);
}
function newAssertion(status="present") { return {status, raw:"", normalized:"", evidence:[]}; }
function newMember() { return {id:"entry-"+crypto.randomUUID(), value:newAssertion()}; }
function newCase() {
  return {id:"case-"+crypto.randomUUID(), boundary:newAssertion(), item:newAssertion(), function:newAssertion(),
    data:[newMember()], models:[newMember()], configuration:newAssertion(), notes:""};
}
function input(label, value, onChange, opts={}) {
  const wrapper = node("label", {class:opts.full ? "full" : ""}, [document.createTextNode(label)]);
  const element = opts.multiline ? node("textarea", {rows:opts.rows || 2}) : node("input", {type:opts.type || "text", placeholder:opts.placeholder || ""});
  element.value = value;
  element.addEventListener("input", () => {onChange(element.value); dirty();});
  wrapper.append(element); return wrapper;
}
function select(label, value, options, onChange) {
  const wrapper = node("label", {}, [document.createTextNode(label)]);
  const el = node("select");
  for (const [key, title] of options) el.append(node("option", {value:key, text:title}));
  el.value = String(value);
  el.addEventListener("change", () => {onChange(el.value); dirty();});
  wrapper.append(el); return wrapper;
}
const statusOptions = [["present","Present"],["not_reported","Not reported"],["unclear","Unclear"],["not_applicable","Not applicable"],["extraction_failure","Text extraction failure"]];
function selectedQuote(entry) {
  const pre = $("page-text"), selection = window.getSelection();
  if (!pre || !selection || selection.isCollapsed || selection.rangeCount !== 1) {message("Select text in the current text page first", true); return;}
  const range = selection.getRangeAt(0);
  if (range.startContainer !== pre.firstChild || range.endContainer !== pre.firstChild) {message("Select within one text page", true);return;}
  entry.source = "text"; entry.page = page; entry.start = range.startOffset; entry.end = range.endOffset;
  entry.quote = pre.textContent.slice(entry.start, entry.end); dirty(); renderAnnotations();
}
function locateQuote(entry) {
  const body = current.pages[entry.page-1]?.text || "";
  const at = body.indexOf(entry.quote);
  if (!entry.quote.trim() || at < 0 || body.indexOf(entry.quote, at+1) >= 0) {
    message("Quote must match exactly once on that text page. Otherwise select the intended occurrence directly.", true); return;
  }
  entry.start = at; entry.end = at + entry.quote.length; dirty(); renderAnnotations();
}
function evidenceEditor(assertion, entry) {
  const box = node("div", {class:"evidence"});
  const fields = node("div", {class:"grid"});
  fields.append(select("Source",entry.source,[["text","Prepared text"],["pdf","PDF (manual verification)"]], val => {
    entry.source=val; entry.start=null; entry.end=null; renderAnnotations();
  }));
  const pageSelect = select("PDF page",entry.page,current.pages.map(p => [p.number,`Page ${p.number}`]),val => {
    entry.page=Number(val); entry.start=null; entry.end=null; page=entry.page; renderSource(); renderAnnotations();
  }); fields.append(pageSelect);
  fields.append(input("Section / table (optional)",entry.section,val => entry.section=val,{full:true}));
  fields.append(input("Exact quotation",entry.quote,val => {
    entry.quote=val;
    if (entry.source === "text") {
      const body=current.pages[entry.page-1].text, at=body.indexOf(val);
      if (val && at >= 0 && body.indexOf(val,at+1) < 0) {entry.start=at;entry.end=at+val.length;}
      else {entry.start=null;entry.end=null;}
    }
  },{full:true,multiline:true,rows:3})); box.append(fields);
  const actions = node("div", {class:"row"});
  actions.append(btn("Use selection", () => selectedQuote(entry)), btn("Find exact quote", () => locateQuote(entry)),
    btn("Remove quote", () => {assertion.evidence.splice(assertion.evidence.indexOf(entry),1);dirty();renderAnnotations();},"danger"));
  box.append(actions); return box;
}
function assertionEditor(title, assertion) {
  const box = node("div", {class:"assertion"}, [node("h4", {text:title})]);
  const fields = node("div", {class:"grid"});
  fields.append(select("Status",assertion.status,statusOptions,val => {
    assertion.status=val;
    if (val !== "present") {assertion.raw="";assertion.normalized="";}
    if (["not_reported","not_applicable"].includes(val)) assertion.evidence=[];
    renderAnnotations();
  }));
  fields.append(input("Raw wording",assertion.raw,val => assertion.raw=val,{placeholder:"As stated by the article"}),
    input("Normalized label (if supported)",assertion.normalized,val => assertion.normalized=val,{full:true}));
  box.append(fields);
  if (assertion.evidence.length) box.append(...assertion.evidence.map(e => evidenceEditor(assertion,e)));
  box.append(btn("+ Add evidence", () => {
    assertion.evidence.push({source:"text",page,section:"",quote:"",start:0,end:0});dirty();renderAnnotations();
  }));
  return box;
}
function memberEditor(caseRecord, kind, title) {
  const container = node("div", {class:"assertion"}, [node("h4",{text:title})]);
  for (const member of caseRecord[kind]) {
    const row = node("div", {class:"member"});
    row.append(btn("Remove entry", () => {caseRecord[kind].splice(caseRecord[kind].indexOf(member),1);dirty();renderAnnotations();},"danger"),
      assertionEditor(kind === "data" ? "Data modality / variables" : "Specific model / role", member.value));
    container.append(row);
  }
  container.append(btn("+ Add " + (kind === "data" ? "data" : "model"), () => {caseRecord[kind].push(newMember());dirty();renderAnnotations();}));
  return container;
}
function renderAnnotations() {
  const panel = $("annotation-panel"); panel.replaceChildren(node("h3",{text:"Independent case annotation"}),
    node("p",{class:"help",text:"One case per implemented function–item–data–model-set combination. Put independent alternatives in separate cases; group coordinated components within one model set. Use the frozen codebook for boundary decisions."}));
  const fields = node("fieldset"); fields.disabled = session.state === "submitted";
  fields.append(input("Article notes (optional)",annotation.notes,val => annotation.notes=val,{full:true,multiline:true}),
    input("If zero eligible cases, explain why",annotation.zero_case_reason,val => annotation.zero_case_reason=val,{full:true,multiline:true}));
  for (const [index, c] of annotation.cases.entries()) {
    const card = node("div",{class:"case"});
    card.append(node("div",{class:"case-title"},[node("strong",{text:`Case ${index+1} · ${c.id}`}),
      btn("Remove case", () => {if(confirm("Remove this case and its evidence?")){annotation.cases.splice(index,1);dirty();renderAnnotations();}},"danger")]));
    card.append(assertionEditor("Case boundary / why these components belong together",c.boundary),
      assertionEditor("Maintainable item",c.item), assertionEditor("Diagnostic or prognostic function",c.function),
      memberEditor(c,"data","Condition data (each input or modality)"),
      memberEditor(c,"models","Model set (each specific component)"),
      assertionEditor("Model configuration (normalize to single or coordinated)",c.configuration),
      input("Case notes / unresolved decisions",c.notes,val => c.notes=val,{full:true,multiline:true}));
    fields.append(card);
  }
  fields.append(btn("+ Add case", () => {annotation.zero_case_reason="";annotation.cases.push(newCase());dirty();renderAnnotations();},"primary"));
  panel.append(fields);
  panel.append(node("p",{class:"note",text:"Present values require raw wording and at least one exact quote with PDF page. Text quotes must match the selected page and saved character span. PDF quotes are recorded for manual checking, not automatically verified."}));
}
refreshList().then(() => message("Select an article")).catch(e => message(e.message,true));
