"""Blank-form, reviewer-isolated held-out annotations. No model output is loaded here."""

from __future__ import annotations

import hashlib
import json
import re
import threading
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from pipeline.fulltext import (
    PAGE_MARKER_RE,
    load_corpus_manifest,
    resolve_pdf,
    validate_source_map,
)

ID = re.compile(r"[A-Za-z0-9_-]+\Z")
STATUSES = {"present", "not_reported", "unclear", "not_applicable", "extraction_failure"}
SCHEMA = "held-out-gold/v1"


class AnnotationError(ValueError):
    pass


def now() -> datetime:
    return datetime.now(timezone.utc)


def timestamp(value: datetime) -> str:
    return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def parse_time(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("timezone missing")
        return parsed
    except (ValueError, TypeError) as error:
        raise AnnotationError("Invalid timer timestamp") from error


def empty_annotation(corpus_id: str, reviewer: str, digest: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA, "corpus_id": corpus_id, "reviewer_id": reviewer,
        "source_sha256": digest, "cases": [], "zero_case_reason": "", "notes": "",
    }


def assert_keys(value: Any, keys: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != keys:
        raise AnnotationError(f"{label}: expected keys {', '.join(sorted(keys))}")


def text(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise AnnotationError(f"{label} must be text")
    return value


def validate_assertion(value: Any, label: str, pages: dict[int, tuple[int, str]], *, complete: bool) -> None:
    assert_keys(value, {"status", "raw", "normalized", "evidence"}, label)
    status = value["status"]
    if status not in STATUSES:
        raise AnnotationError(f"{label}: select a status")
    raw = text(value["raw"], f"{label}.raw")
    text(value["normalized"], f"{label}.normalized")
    evidence = value["evidence"]
    if not isinstance(evidence, list):
        raise AnnotationError(f"{label}.evidence must be a list")
    if status != "present" and (raw.strip() or value["normalized"].strip()):
        raise AnnotationError(f"{label}: non-present fields cannot contain a value")
    if complete and status == "present" and (not raw.strip() or not evidence):
        raise AnnotationError(f"{label}: a present value needs raw wording and evidence")
    if complete and status == "unclear" and not evidence:
        raise AnnotationError(f"{label}: unclear wording needs evidence")
    if status in {"not_reported", "not_applicable"} and evidence:
        raise AnnotationError(f"{label}: no evidence for an absent or inapplicable value")
    for index, entry in enumerate(evidence, 1):
        where = f"{label}.evidence[{index}]"
        assert_keys(entry, {"source", "page", "section", "quote", "start", "end"}, where)
        source = entry["source"]
        page = entry["page"]
        if source not in {"text", "pdf"} or type(page) is not int or page not in pages:
            raise AnnotationError(f"{where}: choose a valid source and PDF page")
        text(entry["section"], f"{where}.section")
        quote = text(entry["quote"], f"{where}.quote")
        if complete and not quote.strip():
            raise AnnotationError(f"{where}: quote the source exactly")
        start, end = entry["start"], entry["end"]
        if source == "text":
            _, body = pages[page]
            if not complete and start is None and end is None:
                continue  # Allow an unfinished quotation in a saved draft.
            if type(start) is not int or type(end) is not int or not (0 <= start <= end <= len(body)):
                raise AnnotationError(f"{where}: select an exact span on the text page")
            if body[start:end] != quote:
                raise AnnotationError(f"{where}: quote does not match the saved text span")
        elif start is not None or end is not None:
            raise AnnotationError(f"{where}: PDF quotes must not have text offsets")


def validate_annotation(value: Any, corpus_id: str, reviewer: str, digest: str,
                        pages: dict[int, tuple[int, str]], *, complete: bool = False) -> None:
    assert_keys(value, {"schema_version", "corpus_id", "reviewer_id", "source_sha256",
                        "cases", "zero_case_reason", "notes"}, "annotation")
    if (value["schema_version"], value["corpus_id"], value["reviewer_id"], value["source_sha256"]) != (
        SCHEMA, corpus_id, reviewer, digest
    ):
        raise AnnotationError("Annotation identity or source checksum differs from the frozen input")
    cases = value["cases"]
    if not isinstance(cases, list):
        raise AnnotationError("cases must be a list")
    text(value["notes"], "notes")
    reason = text(value["zero_case_reason"], "zero_case_reason")
    if cases and reason.strip():
        raise AnnotationError("A zero-case reason cannot accompany cases")
    if complete and not cases and not reason.strip():
        raise AnnotationError("Add a case, or explain why there are zero eligible cases")
    seen: set[str] = set()
    for case in cases:
        assert_keys(case, {"id", "boundary", "item", "function", "data", "models",
                           "configuration", "notes"}, "case")
        case_id = case["id"]
        if not isinstance(case_id, str) or not ID.fullmatch(case_id) or case_id in seen:
            raise AnnotationError("Case IDs must be unique safe identifiers")
        seen.add(case_id)
        text(case["notes"], f"{case_id}.notes")
        for key in ("boundary", "item", "function", "configuration"):
            validate_assertion(case[key], f"{case_id}.{key}", pages, complete=complete)
        if complete and case["boundary"]["status"] != "present":
            raise AnnotationError(f"{case_id}: case boundary must be supported")
        for kind in ("data", "models"):
            members = case[kind]
            if not isinstance(members, list) or (complete and not members):
                raise AnnotationError(f"{case_id}.{kind}: add at least one entry or an explicit absence")
            local: set[str] = set()
            for member in members:
                assert_keys(member, {"id", "value"}, f"{case_id}.{kind} entry")
                member_id = member["id"]
                if not isinstance(member_id, str) or not ID.fullmatch(member_id) or member_id in local:
                    raise AnnotationError(f"{case_id}.{kind}: IDs must be unique")
                local.add(member_id)
                validate_assertion(member["value"], f"{case_id}.{kind}.{member_id}", pages, complete=complete)
        if complete and case["configuration"]["status"] == "present":
            configuration = case["configuration"]["normalized"]
            if configuration not in {"single", "coordinated"}:
                raise AnnotationError(f"{case_id}: configuration must normalize to single or coordinated")
            model_count = sum(member["value"]["status"] == "present" for member in case["models"])
            if ((configuration == "single" and model_count != 1) or
                (configuration == "coordinated" and model_count < 2)):
                raise AnnotationError(f"{case_id}: configuration conflicts with the number of present models")


class GoldWorkspace:
    """One local reviewer per process; no read path for another reviewer's files."""

    def __init__(self, manifest: Path, prepared_dir: Path, output_dir: Path, reviewer: str):
        if not ID.fullmatch(reviewer):
            raise AnnotationError("Reviewer ID may contain letters, numbers, _ and - only")
        self.reviewer = reviewer
        self.lock = threading.RLock()
        self.output = output_dir.resolve() / reviewer
        base, records, raw = load_corpus_manifest(manifest, require_verified=False)
        if raw["partition_frozen"] is not True:
            raise AnnotationError("Freeze the partition before gold annotation")
        self.records = {key: record for key, record in records.items() if record.partition == "held_out"}
        if not self.records:
            raise AnnotationError("Manifest has no held-out articles")
        if any(record.bibliographic_status != "verified" for record in self.records.values()):
            raise AnnotationError("All held-out articles must have verified bibliographic identity")
        if any(not ID.fullmatch(key) for key in self.records):
            raise AnnotationError("Corpus IDs must contain letters, numbers, _ and - only")
        self.pdfs = {key: resolve_pdf(base, record) for key, record in self.records.items()}
        self.prepared_dir = prepared_dir.resolve()
        self.documents: dict[str, tuple[str, str, dict[int, tuple[int, str]]]] = {}
        for key, record in self.records.items():
            folder = self.prepared_dir / key
            if folder.is_symlink() or not folder.is_dir():
                raise AnnotationError(f"Missing prepared document for {key}: {folder}")
            md = folder / "document.md"
            source = folder / "source-map.json"
            identity = folder / "bibliographic-identity.json"
            quality = folder / "quality.json"
            if any(path.is_symlink() for path in (md, source, identity, quality)):
                raise AnnotationError(f"Prepared document contains a symbolic link: {key}")
            try:
                document = md.read_text(encoding="utf-8")
                source_map = json.loads(source.read_text(encoding="utf-8"))
                bibliography = json.loads(identity.read_text(encoding="utf-8"))
                quality_result = json.loads(quality.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, ValueError) as error:
                raise AnnotationError(f"Missing or invalid prepared output for {key}") from error
            validate_source_map(document, source_map)
            if (source_map.get("corpus_id") != key or bibliography.get("corpus_id") != key
                or bibliography.get("pdf_sha256") != record.pdf_sha256
                or bibliography.get("doi") != record.doi
                or bibliography.get("title") != record.title
                or bibliography.get("year") != record.year
                or bibliography.get("partition") != "held_out"
                or bibliography.get("manifest_partition_frozen") is not True
                or quality_result.get("status") != "pass"):
                raise AnnotationError(f"Prepared output does not match verified manifest for {key}")
            matches = list(PAGE_MARKER_RE.finditer(document))
            if not matches or [int(match.group(1)) for match in matches] != list(range(1, len(matches) + 1)):
                raise AnnotationError(f"Prepared pages are missing, repeated, or out of order for {key}")
            pages = {int(match.group(1)): (match.end(), document[match.end(): matches[i + 1].start() if i + 1 < len(matches) else len(document)])
                     for i, match in enumerate(matches)}
            self.documents[key] = (document, hashlib.sha256(document.encode("utf-8")).hexdigest(), pages)

    def _path(self, key: str) -> Path:
        if key not in self.records:
            raise AnnotationError("Unknown held-out article")
        return self.output / f"{key}.json"

    def _initial(self, key: str) -> dict[str, Any]:
        return {"revision": 0, "state": "draft", "annotation": empty_annotation(key, self.reviewer, self.documents[key][1]),
                "timer": {"seconds": 0.0, "running_since": None, "intervals": []},
                "created_at": None, "updated_at": None, "submitted_at": None}

    def get(self, key: str) -> dict[str, Any]:
        path = self._path(key)
        if not path.exists():
            return self._initial(key)
        return json.loads(path.read_text(encoding="utf-8"))

    def articles(self) -> list[dict[str, Any]]:
        with self.lock:
            return [{"corpus_id": key, "title": record.title, "doi": record.doi,
                     "year": record.year, "state": self.get(key)["state"]}
                    for key, record in sorted(self.records.items())]

    def article(self, key: str) -> dict[str, Any]:
        with self.lock:
            record = self.records[self._path(key).stem]
            document, digest, pages = self.documents[key]
            return {"corpus_id": key, "title": record.title, "doi": record.doi, "year": record.year,
                    "source_sha256": digest, "pages": [{"number": number, "text": body} for number, (_, body) in pages.items()],
                    "session": self.get(key)}

    def update(self, key: str, revision: int, *, annotation: Any = None,
               action: str | None = None) -> dict[str, Any]:
        with self.lock:
            session = self.get(key)
            if type(revision) is not int or revision != session["revision"]:
                raise AnnotationError("Revision conflict: reload the article before saving")
            if session["state"] == "submitted":
                raise AnnotationError("Submitted gold annotations cannot be edited")
            if annotation is not None:
                validate_annotation(annotation, key, self.reviewer, self.documents[key][1], self.documents[key][2],
                                    complete=action == "submit")
                session["annotation"] = annotation
            if action == "submit" and annotation is None:
                validate_annotation(session["annotation"], key, self.reviewer, self.documents[key][1],
                                    self.documents[key][2], complete=True)
            if action not in {None, "start", "pause", "submit"}:
                raise AnnotationError("Unknown action")
            clock = now()
            timer = session["timer"]
            if action == "start":
                if timer["running_since"] is not None:
                    raise AnnotationError("Timer is already running")
                timer["running_since"] = timestamp(clock)
            if action in {"pause", "submit"} and timer["running_since"] is not None:
                started = timer["running_since"]
                duration = max(0.0, (clock - parse_time(started)).total_seconds())
                timer["seconds"] += duration
                timer["intervals"].append({"start": started, "end": timestamp(clock), "seconds": duration})
                timer["running_since"] = None
            elif action == "pause":
                raise AnnotationError("Timer is not running")
            if action == "submit":
                if not timer["intervals"]:
                    raise AnnotationError("Start the timer to record manual annotation effort before submitting")
                session["state"] = "submitted"
                session["submitted_at"] = timestamp(clock)
            session["revision"] += 1
            session["created_at"] = session["created_at"] or timestamp(clock)
            session["updated_at"] = timestamp(clock)
            self.output.mkdir(parents=True, exist_ok=True)
            path = self._path(key)
            with NamedTemporaryFile("w", encoding="utf-8", dir=self.output, prefix=f".{key}.", delete=False) as file:
                temporary = Path(file.name)
                json.dump(session, file, ensure_ascii=False, indent=2)
                file.write("\n")
                file.flush()
                import os
                os.fsync(file.fileno())
            temporary.replace(path)
            return session
