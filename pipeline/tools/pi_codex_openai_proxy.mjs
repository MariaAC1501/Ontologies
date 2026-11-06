#!/usr/bin/env node
/**
 * Local OpenAI Chat Completions compatibility proxy backed by Pi's
 * ChatGPT Plus/Pro (Codex) OAuth credential.
 *
 * It intentionally binds to 127.0.0.1 only by default. The OAuth token never
 * leaves this process except in requests to the official Codex endpoint used by
 * Pi. The repository extraction flow does not use direct OpenAI API keys.
 */

import http from "node:http";
import { execFileSync } from "node:child_process";
import { constants as fsConstants } from "node:fs";
import { access, mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";
import { randomUUID } from "node:crypto";
import { pathToFileURL } from "node:url";

const host = process.env.PI_CODEX_PROXY_HOST || "127.0.0.1";
const port = Number.parseInt(process.env.PI_CODEX_PROXY_PORT || "8977", 10);
const modelId = process.env.PI_CODEX_MODEL || "gpt-5.6-luna";
const maxRequestBytes = 50 * 1024 * 1024;
const defaultAuthFile = join(
  process.env.USERPROFILE || process.env.HOME || ".",
  ".pi",
  "agent",
  "auth.json",
);
const authFile = process.env.PI_AUTH_FILE || defaultAuthFile;

async function fileExists(path) {
  try {
    await access(path, fsConstants.R_OK);
    return true;
  } catch {
    return false;
  }
}

function npmGlobalRoot() {
  try {
    const npm = process.platform === "win32" ? "npm.cmd" : "npm";
    return execFileSync(npm, ["root", "-g"], { encoding: "utf8" }).trim();
  } catch {
    return "";
  }
}

async function resolvePiAiCompatPath() {
  if (process.env.PI_AI_COMPAT_PATH) {
    return process.env.PI_AI_COMPAT_PATH;
  }

  const requireFromHere = createRequire(import.meta.url);
  try {
    return requireFromHere.resolve("@earendil-works/pi-ai/dist/compat.js");
  } catch {
    // The package is normally nested under the globally installed Pi agent.
  }

  const candidates = [];
  const globalRoot = npmGlobalRoot();
  if (globalRoot) {
    candidates.push(
      join(globalRoot, "@earendil-works", "pi-coding-agent", "node_modules", "@earendil-works", "pi-ai", "dist", "compat.js"),
      join(globalRoot, "@earendil-works", "pi-ai", "dist", "compat.js"),
    );
  }

  for (const candidate of candidates) {
    if (await fileExists(candidate)) return candidate;
  }

  throw new Error(
    "Could not locate @earendil-works/pi-ai/dist/compat.js. " +
      "Run this with Pi installed globally, or set PI_AI_COMPAT_PATH."
  );
}

const compatPath = await resolvePiAiCompatPath();
const oauthCandidates = [
  // Older pi-ai versions.
  join(dirname(compatPath), "utils", "oauth", "openai-codex.js"),
  // Current pi-ai versions.
  join(dirname(compatPath), "auth", "oauth", "openai-codex.js"),
];
let oauthPath = "";
for (const candidate of oauthCandidates) {
  if (await fileExists(candidate)) {
    oauthPath = candidate;
    break;
  }
}
if (!oauthPath) {
  throw new Error(`Could not locate OpenAI Codex OAuth helper. Tried: ${oauthCandidates.join(", ")}`);
}

const { openAICodexResponsesApi } = await import(pathToFileURL(compatPath).href);
const oauthModule = await import(pathToFileURL(oauthPath).href);
const refreshOpenAICodexToken = oauthModule.refreshOpenAICodexToken ||
  (async (refreshToken) => oauthModule.openaiCodexOAuth.refresh({ refresh: refreshToken }));

function log(message) {
  process.stdout.write(`[${new Date().toISOString()}] ${message}\n`);
}

function sendJson(response, status, body) {
  response.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
  });
  response.end(JSON.stringify(body));
}

function openAIError(response, status, message, type = "proxy_error") {
  sendJson(response, status, { error: { message, type } });
}

function toText(content) {
  if (typeof content === "string") return content;
  if (!Array.isArray(content)) return "";
  return content
    .map((part) => {
      if (typeof part === "string") return part;
      if (!part || typeof part !== "object") return "";
      if (typeof part.text === "string") return part.text;
      if (typeof part.content === "string") return part.content;
      return "";
    })
    .filter(Boolean)
    .join("\n");
}

async function readBody(request) {
  const chunks = [];
  let length = 0;
  for await (const chunk of request) {
    length += chunk.length;
    if (length > maxRequestBytes) {
      throw new Error("Request body exceeds 50 MiB.");
    }
    chunks.push(chunk);
  }
  return JSON.parse(Buffer.concat(chunks).toString("utf8"));
}

async function getOAuthCredential() {
  const data = JSON.parse(await readFile(authFile, "utf8"));
  const credential = data["openai-codex"];
  if (!credential?.access || !credential?.refresh || !credential?.expires) {
    throw new Error("Pi OpenAI Codex OAuth credentials are unavailable. Run /login and select ChatGPT Plus/Pro (Codex).");
  }

  // Refresh shortly before expiry and persist the refreshed credential in the
  // same Pi auth file. No OAuth material is logged.
  if (Number(credential.expires) <= Date.now() + 120_000) {
    const refreshed = await refreshOpenAICodexToken(credential.refresh);
    data["openai-codex"] = {
      ...credential,
      ...refreshed,
      type: "oauth",
    };
    await mkdir(dirname(authFile), { recursive: true });
    const temporary = `${authFile}.tmp-${process.pid}`;
    await writeFile(temporary, `${JSON.stringify(data, null, 2)}\n`, "utf8");
    await rename(temporary, authFile);
    return data["openai-codex"];
  }

  return credential;
}

function buildContext(messages) {
  const systemParts = [];
  const conversation = [];

  for (const message of Array.isArray(messages) ? messages : []) {
    const role = message?.role;
    const text = toText(message?.content);
    if (!text) continue;
    if (role === "system" || role === "developer") {
      systemParts.push(text);
    } else if (role === "user") {
      conversation.push({ role: "user", content: text, timestamp: Date.now() });
    } else if (role === "assistant") {
      // OntoCast sends a single user prompt. Preserve this fallback for normal
      // Chat Completions clients without requiring Pi-internal message shapes.
      conversation.push({
        role: "user",
        content: `[Previous assistant response]\n${text}`,
        timestamp: Date.now(),
      });
    }
  }

  if (conversation.length === 0) {
    throw new Error("A user message is required.");
  }
  return {
    ...(systemParts.length ? { systemPrompt: systemParts.join("\n\n") } : {}),
    messages: conversation,
  };
}

function textFromDoneMessage(message) {
  if (!message || !Array.isArray(message.content)) return "";
  return message.content
    .filter((block) => block?.type === "text")
    .map((block) => block.text || "")
    .join("");
}

async function complete(requestBody) {
  const credential = await getOAuthCredential();
  const context = buildContext(requestBody.messages);
  const requestedMaxTokens = Number(
    requestBody.max_completion_tokens ?? requestBody.max_tokens ?? 8192,
  );
  const maxTokens = Number.isFinite(requestedMaxTokens)
    ? Math.max(256, Math.min(Math.floor(requestedMaxTokens), 16384))
    : 8192;
  const model = {
    id: modelId,
    name: `Pi Codex ${modelId}`,
    api: "openai-codex-responses",
    provider: "openai-codex",
    baseUrl: "https://chatgpt.com/backend-api",
    reasoning: true,
    input: ["text"],
    cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
    contextWindow: 272000,
    maxTokens: 16384,
  };

  let text = "";
  let doneMessage;
  const stream = openAICodexResponsesApi().streamSimple(model, context, {
    apiKey: credential.access,
    maxTokens,
    transport: "sse",
    timeoutMs: 30 * 60 * 1000,
  });

  for await (const event of stream) {
    if (event.type === "text_delta") {
      text += event.delta;
    } else if (event.type === "error") {
      throw new Error(event.error?.errorMessage || "Pi Codex request failed.");
    } else if (event.type === "done") {
      doneMessage = event.message;
    }
  }

  if (!text) text = textFromDoneMessage(doneMessage);
  if (!text) throw new Error("Pi Codex returned an empty completion.");
  return { text, usage: doneMessage?.usage };
}

const server = http.createServer(async (request, response) => {
  const requestUrl = new URL(request.url || "/", `http://${host}:${port}`);
  if (request.method === "GET" && requestUrl.pathname === "/health") {
    return sendJson(response, 200, { status: "ok", provider: "openai-codex", model: modelId });
  }
  if (
    request.method !== "POST" ||
    !["/v1/chat/completions", "/chat/completions"].includes(requestUrl.pathname)
  ) {
    return openAIError(response, 404, "Only POST /v1/chat/completions is supported.", "not_found");
  }

  const started = Date.now();
  try {
    const requestBody = await readBody(request);
    if (requestBody.stream) {
      return openAIError(response, 400, "Streaming is not supported by this local compatibility proxy.", "unsupported_feature");
    }
    const { text, usage } = await complete(requestBody);
    const completionId = `chatcmpl-pi-codex-${randomUUID()}`;
    log(`completed in ${Date.now() - started} ms`);
    return sendJson(response, 200, {
      id: completionId,
      object: "chat.completion",
      created: Math.floor(Date.now() / 1000),
      model: requestBody.model || modelId,
      choices: [
        {
          index: 0,
          message: { role: "assistant", content: text },
          finish_reason: "stop",
        },
      ],
      usage: {
        prompt_tokens: usage?.input || 0,
        completion_tokens: usage?.output || 0,
        total_tokens: usage?.totalTokens || 0,
      },
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    log(`request failed: ${message.replaceAll(/\s+/g, " ").slice(0, 240)}`);
    return openAIError(response, 502, message, "pi_codex_error");
  }
});

server.listen(port, host, () => {
  log(`listening on http://${host}:${port}/v1/chat/completions using ${modelId}`);
});

function shutdown(signal) {
  log(`received ${signal}; shutting down`);
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(0), 5000).unref();
}

process.on("SIGINT", () => shutdown("SIGINT"));
process.on("SIGTERM", () => shutdown("SIGTERM"));
