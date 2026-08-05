#!/usr/bin/env python3
"""Run no-OntoCast LLM JSON extraction baselines from evidence JSONL.

The CLI reads ``evidence.jsonl`` records and writes ``predictions.jsonl`` records
compatible with ``evaluate_extraction.py``.  In ``--dry-run`` mode it never calls
an API: it only saves prompt Markdown files and emits empty canonical predictions
with ``metadata.status == "dry-run"``.  The ``llm_schema`` condition can take a
generated schema file via ``--schema-context``.  Real execution uses an
OpenAI-compatible Chat Completions endpoint through the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


DEFAULT_EVIDENCE = Path("paper/experiments/evidence.jsonl")
DEFAULT_OUTPUT = Path("paper/experiments/predictions.jsonl")
DEFAULT_BASE_URL = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
DEFAULT_MODEL = os.environ.get("LLM_MODEL", "")
CONDITIONS = ("generic_json", "llm_schema", "llm_ontology")
ID_FIELDS = ("record_id", "corpus_id", "paper_id", "doc_id", "id")
CANONICAL_FIELDS = (
    "reference",
    "publication_year",
    "task",
    "case_study",
    "case_study_type",
    "input_for_model",
    "number_of_input_variables",
    "input_types",
    "data_preprocessing",
    "model_approach",
    "model_types",
    "models",
    "module_synchronization",
    "number_of_failure_modes",
    "performance_indicator",
    "performance",
    "complementary_notes",
    "study_title",
    "publication_identifier",
)
LIST_FIELDS = {"input_types", "model_types", "models"}
FIELD_SCHEMA: Tuple[Tuple[str, str, str], ...] = (
    ("reference", "string|null", "Compact citation/reference for the study."),
    ("publication_year", "string|number|null", "Publication year."),
    ("task", "string|null", "Maintenance/prognostics task, e.g. fault diagnosis, RUL, anomaly detection."),
    ("case_study", "string|null", "Asset/system/dataset/application case study."),
    ("case_study_type", "string|null", "Industrial, laboratory, benchmark, simulation, review, etc."),
    ("input_for_model", "string|null", "Signals, measurements, logs, images, or other model inputs."),
    ("number_of_input_variables", "string|number|null", "Number of model input variables if stated."),
    ("input_types", "array", "Input variable/data types; use [] if unknown."),
    ("data_preprocessing", "string|null", "Preprocessing, feature engineering, normalization, segmentation, etc."),
    ("model_approach", "string|null", "High-level modeling approach."),
    ("model_types", "array", "Model families/types; use [] if unknown."),
    ("models", "array", "Concrete model names/algorithms; use [] if unknown."),
    ("module_synchronization", "string|boolean|null", "Whether/which modules are synchronized or coordinated."),
    ("number_of_failure_modes", "string|number|null", "Number of failure modes/classes if stated."),
    ("performance_indicator", "string|null", "Metric names such as RMSE, F1, accuracy, MAE, AUC."),
    ("performance", "string|null", "Reported metric values/results."),
    ("complementary_notes", "string|null", "Important caveats or extra extracted information."),
    ("study_title", "string|null", "Paper title."),
    ("publication_identifier", "string|null", "DOI, EID, URL, or other publication identifier."),
)


class UserError(Exception):
    """Raised for user-facing CLI errors."""


def empty_prediction() -> Dict[str, Any]:
    return {field: ([] if field in LIST_FIELDS else None) for field in CANONICAL_FIELDS}


def read_jsonl(path: Path) -> List[Tuple[int, Dict[str, Any]]]:
    if not path.exists():
        raise UserError(f"evidence JSONL not found: {path}")
    if not path.is_file():
        raise UserError(f"evidence JSONL path is not a file: {path}")

    records: List[Tuple[int, Dict[str, Any]]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    obj = json.loads(stripped)
                except json.JSONDecodeError as exc:
                    raise UserError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
                if not isinstance(obj, dict):
                    raise UserError(f"{path}:{line_number}: expected a JSON object")
                records.append((line_number, obj))
    except UnicodeDecodeError as exc:
        raise UserError(f"could not decode evidence JSONL as UTF-8: {path}: {exc}") from exc
    except OSError as exc:
        raise UserError(f"could not read evidence JSONL {path}: {exc}") from exc

    if not records:
        raise UserError(f"evidence JSONL has no records: {path}")
    return records


def write_jsonl(path: Path, records: Sequence[Dict[str, Any]]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as exc:
        raise UserError(f"could not write predictions JSONL {path}: {exc}") from exc


def get_record_id(obj: Dict[str, Any], line_number: int) -> str:
    for key in ID_FIELDS:
        value = obj.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    metadata = obj.get("metadata")
    if isinstance(metadata, dict):
        for key in ID_FIELDS:
            value = metadata.get(key)
            if value is not None and str(value).strip():
                return str(value).strip()
    return f"line-{line_number}"


def safe_name(value: str, fallback: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip()).strip("-._")
    return cleaned or fallback


def display_path(path: Path) -> str:
    return path.as_posix()


def default_prompts_dir(output: Path) -> Path:
    return output.parent / "prompts"


def truncate_text(value: str, max_chars: int) -> str:
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 40].rstrip() + "\n...[truncated for prompt provenance]..."


def json_template() -> str:
    return json.dumps(empty_prediction(), ensure_ascii=False, indent=2)


def field_schema_text() -> str:
    lines = []
    for field, expected_type, description in FIELD_SCHEMA:
        lines.append(f"- `{field}` ({expected_type}): {description}")
    return "\n".join(lines)


def generic_condition_instructions() -> str:
    return (
        "Extract the requested maintenance/prognostics information from the evidence. "
        "Use only the evidence text and metadata. Do not infer facts that are not stated. "
        "Return null for unknown scalar fields and [] for unknown list fields."
    )


def schema_condition_instructions(schema_context: str = "") -> str:
    instructions = (
        "Extract according to the canonical 19-field schema below. Keep field names exact. "
        "Use null for missing scalar values, arrays for list fields, and concise strings for scalar fields.\n\n"
        + field_schema_text()
    )
    context = schema_context.strip()
    if context:
        instructions += (
            "\n\nAdditional LLM-generated schema context:\n"
            + context
            + "\n\nUse this generated schema context to interpret domain concepts, aliases, "
            "normalization guidance, and provenance/evidence requirements while still returning the exact "
            "19 canonical fields requested below."
        )
    return instructions


def ontology_condition_instructions(ontology_context: str) -> str:
    context = ontology_context.strip() or "No ontology context was provided."
    return (
        "Extract according to the canonical 19-field schema and align terms to the ontology labels/classes "
        "when the evidence supports doing so. Do not force an ontology term if the paper uses a clearer "
        "specific wording.\n\n"
        + field_schema_text()
        + "\n\nOntology context (brief label/class extract):\n"
        + context
    )


def metadata_preview(metadata: Any) -> str:
    if not isinstance(metadata, dict):
        return "{}"
    keep: Dict[str, Any] = {}
    for key in (
        "corpus_id",
        "pdf",
        "facts",
        "bibliographic",
        "keywords",
        "screening",
        "sample_manifest_fields",
    ):
        if key in metadata:
            keep[key] = metadata[key]
    if not keep:
        keep = metadata
    return json.dumps(keep, ensure_ascii=False, indent=2, sort_keys=True)


def build_prompt(
    evidence_record: Dict[str, Any],
    record_id: str,
    condition: str,
    ontology_context: str,
    schema_context: str = "",
) -> Tuple[str, str]:
    if condition == "generic_json":
        instructions = generic_condition_instructions()
    elif condition == "llm_schema":
        instructions = schema_condition_instructions(schema_context)
    elif condition == "llm_ontology":
        instructions = ontology_condition_instructions(ontology_context)
    else:  # argparse prevents this, but keep the function safe.
        raise UserError(f"unknown condition: {condition}")

    evidence_text = str(evidence_record.get("evidence_text", ""))
    scope = str(evidence_record.get("scope", ""))
    metadata = metadata_preview(evidence_record.get("metadata"))

    system = (
        "You are a careful information extraction system for predictive maintenance papers. "
        "Return only one valid JSON object. Do not include Markdown, code fences, explanations, or comments."
    )
    user = (
        f"Condition: {condition}\n"
        f"Record ID: {record_id}\n"
        f"Evidence scope: {scope}\n\n"
        f"Instructions:\n{instructions}\n\n"
        "Return exactly these 19 canonical fields. Keep every key present even when unknown:\n"
        f"```json\n{json_template()}\n```\n\n"
        "Evidence text:\n"
        f"```text\n{evidence_text}\n```\n\n"
        "Evidence metadata for provenance/disambiguation:\n"
        f"```json\n{metadata}\n```"
    )
    return system, user


def write_prompt_markdown(path: Path, record_id: str, condition: str, system: str, user: str) -> None:
    content = (
        f"# Prompt: {condition} / {record_id}\n\n"
        "## System\n\n"
        f"{system}\n\n"
        "## User\n\n"
        f"{user}\n"
    )
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    except OSError as exc:
        raise UserError(f"could not write prompt {path}: {exc}") from exc


def chat_completions_url(base_url: str) -> str:
    cleaned = base_url.strip().rstrip("/")
    if not cleaned:
        raise UserError("--base-url must not be empty for real execution")
    if cleaned.endswith("/chat/completions"):
        return cleaned
    return cleaned + "/chat/completions"


def read_api_key(env_name: str) -> str:
    if not env_name.strip():
        raise UserError("--api-key-env must not be empty")
    api_key = os.environ.get(env_name, "")
    if not api_key:
        raise UserError(f"environment variable {env_name!r} is not set")
    return api_key


def call_chat_completion(
    base_url: str,
    api_key: str,
    model: str,
    temperature: float,
    timeout: float,
    system: str,
    user: str,
) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
        "response_format": {"type": "json_object"},
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        chat_completions_url(base_url),
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        raise UserError(f"HTTP {exc.code} from chat completions endpoint: {body[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise UserError(f"chat completions request failed: {exc}") from exc
    except TimeoutError as exc:
        raise UserError(f"chat completions request timed out after {timeout} seconds") from exc

    try:
        response_obj = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise UserError(f"chat completions response was not valid JSON: {exc}") from exc

    try:
        content = response_obj["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise UserError(
            "chat completions response did not contain choices[0].message.content"
        ) from exc
    if not isinstance(content, str):
        raise UserError("choices[0].message.content was not a string")
    return content


def strip_markdown_fence(text: str) -> str:
    match = re.fullmatch(r"\s*```(?:json|JSON)?\s*(.*?)\s*```\s*", text, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def first_balanced_json_object(text: str) -> str:
    start = text.find("{")
    if start < 0:
        raise UserError("model response did not contain a JSON object")

    depth = 0
    in_string = False
    escape = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise UserError("model response contained an unterminated JSON object")


def parse_model_json(content: str) -> Dict[str, Any]:
    candidates = [content.strip(), strip_markdown_fence(content)]
    try:
        candidates.append(first_balanced_json_object(content))
    except UserError:
        pass

    errors: List[str] = []
    for candidate in candidates:
        if not candidate:
            continue
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError as exc:
            errors.append(str(exc))
            continue
        if not isinstance(parsed, dict):
            raise UserError("model JSON response must be an object")
        return parsed
    detail = "; ".join(errors[:3]) if errors else "no JSON object found"
    raise UserError(f"could not parse model response as JSON: {detail}")


def coerce_prediction(parsed: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    payload: Any = parsed.get("prediction") if isinstance(parsed.get("prediction"), dict) else parsed
    if not isinstance(payload, dict):
        raise UserError("parsed model JSON did not contain an object prediction")

    warnings: List[str] = []
    missing = [field for field in CANONICAL_FIELDS if field not in payload]
    if missing:
        warnings.append("missing fields filled with empty values: " + ", ".join(missing))
    extra = sorted(str(key) for key in payload.keys() if key not in CANONICAL_FIELDS)
    if extra:
        warnings.append("extra fields ignored: " + ", ".join(extra[:20]))

    prediction = empty_prediction()
    for field in CANONICAL_FIELDS:
        value = payload.get(field)
        if value is None or value == "":
            continue
        if field in LIST_FIELDS:
            prediction[field] = value if isinstance(value, list) else [value]
        else:
            prediction[field] = value
    return prediction, warnings


def turtle_literal_value(raw: str) -> str:
    value = raw.replace('\\"', '"').replace("\\n", " ").strip()
    return " ".join(value.split())


def local_name(subject: str) -> str:
    cleaned = subject.strip("<>")
    if "#" in cleaned:
        cleaned = cleaned.rsplit("#", 1)[-1]
    elif "/" in cleaned:
        cleaned = cleaned.rstrip("/").rsplit("/", 1)[-1]
    elif ":" in cleaned:
        cleaned = cleaned.rsplit(":", 1)[-1]
    return re.sub(r"[_-]+", " ", cleaned).strip() or subject


def is_subject_line(line: str) -> bool:
    if not line or line.startswith(("@prefix", "PREFIX", "#", ";", ".", "]")):
        return False
    return bool(re.match(r"^(?:<[^>]+>|[A-Za-z_][\w.-]*:[\w.-]+|:[\w.-]+)\s+", line))


def extract_ontology_context(path: Path, max_items: int = 60, max_chars: int = 5000) -> str:
    if not path.exists():
        raise UserError(f"ontology file not found: {path}")
    if not path.is_file():
        raise UserError(f"ontology path is not a file: {path}")

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise UserError(f"could not decode ontology as UTF-8: {path}: {exc}") from exc
    except OSError as exc:
        raise UserError(f"could not read ontology {path}: {exc}") from exc

    classes: Dict[str, Dict[str, str]] = {}
    labels: Dict[str, str] = {}
    current_subject = ""
    label_pattern = re.compile(r'rdfs:label\s+"((?:\\.|[^"\\])*)"')
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("@prefix"):
            continue
        if is_subject_line(line):
            current_subject = line.split(None, 1)[0]
        if current_subject and re.search(r"\b(?:a|rdf:type)\s+(?:owl:Class|rdfs:Class)\b", line):
            classes.setdefault(current_subject, {})
        match = label_pattern.search(line)
        if match and current_subject:
            labels[current_subject] = turtle_literal_value(match.group(1))

    for subject, label in labels.items():
        if subject in classes:
            classes[subject]["label"] = label

    def priority(item: Tuple[str, Dict[str, str]]) -> Tuple[int, str]:
        subject, info = item
        if subject.startswith(":"):
            group = 0
        elif subject.startswith("cco:"):
            group = 1
        elif subject.startswith("obo:"):
            group = 2
        else:
            group = 3
        return group, info.get("label") or local_name(subject)

    lines = []
    for subject, info in sorted(classes.items(), key=priority)[:max_items]:
        label = info.get("label") or local_name(subject)
        name = local_name(subject)
        if label.casefold() == name.casefold():
            lines.append(f"- {label} ({subject})")
        else:
            lines.append(f"- {label} ({subject}; local name: {name})")

    if not lines:
        return f"No owl:Class/rdfs:label extract could be parsed from {path}."
    return truncate_text("\n".join(lines), max_chars)


def read_schema_context(path: Path, max_chars: int = 12000) -> str:
    if not path.exists():
        raise UserError(f"schema context file not found: {path}")
    if not path.is_file():
        raise UserError(f"schema context path is not a file: {path}")
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise UserError(f"could not decode schema context as UTF-8: {path}: {exc}") from exc
    except OSError as exc:
        raise UserError(f"could not read schema context {path}: {exc}") from exc
    stripped = text.strip()
    return truncate_text(stripped, max_chars) if stripped else "Schema context file was empty."


def process_record(
    evidence_record: Dict[str, Any],
    line_number: int,
    index: int,
    args: argparse.Namespace,
    model: str,
    api_key: str,
    prompts_dir: Path,
    ontology_context: str,
    schema_context: str = "",
) -> Dict[str, Any]:
    record_id = get_record_id(evidence_record, line_number)
    system, user = build_prompt(evidence_record, record_id, args.condition, ontology_context, schema_context)
    prompt_name = f"{index + 1:04d}_{args.condition}_{safe_name(record_id, 'record')}.md"
    prompt_path = prompts_dir / prompt_name
    write_prompt_markdown(prompt_path, record_id, args.condition, system, user)

    schema_context_path = getattr(args, "schema_context", None)
    metadata: Dict[str, Any] = {
        "status": "dry-run" if args.dry_run else "pending",
        "condition": args.condition,
        "model": model,
        "temperature": args.temperature,
        "evidence_scope": evidence_record.get("scope"),
        "evidence_line_number": line_number,
        "prompt_file": display_path(prompt_path),
        "errors": [],
        "warnings": [],
    }
    if schema_context_path:
        metadata["schema_context_file"] = display_path(Path(schema_context_path))

    if args.dry_run:
        return {"record_id": record_id, "prediction": empty_prediction(), "metadata": metadata}

    started = time.time()
    try:
        content = call_chat_completion(
            base_url=args.base_url,
            api_key=api_key,
            model=model,
            temperature=args.temperature,
            timeout=args.timeout,
            system=system,
            user=user,
        )
        parsed = parse_model_json(content)
        prediction, warnings = coerce_prediction(parsed)
        metadata["status"] = "ok"
        metadata["warnings"] = warnings
        metadata["response_chars"] = len(content)
    except Exception as exc:  # Keep execution isolated per record.
        prediction = empty_prediction()
        metadata["status"] = "error"
        metadata["errors"] = [str(exc)]
    finally:
        metadata["elapsed_seconds"] = round(time.time() - started, 3)

    return {"record_id": record_id, "prediction": prediction, "metadata": metadata}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--evidence",
        type=Path,
        default=DEFAULT_EVIDENCE,
        help=f"Input evidence JSONL path (default: {DEFAULT_EVIDENCE}).",
    )
    parser.add_argument(
        "--condition",
        choices=CONDITIONS,
        required=True,
        help="LLM comparator condition to run.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output predictions JSONL path (default: {DEFAULT_OUTPUT}).",
    )
    parser.add_argument(
        "--prompts-dir",
        type=Path,
        help="Prompt Markdown output directory (default: OUTPUT_PARENT/prompts).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not call an API; save prompts and emit empty predictions with status=dry-run.",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=(
            "OpenAI-compatible base URL, or full /chat/completions URL "
            f"(default: env LLM_BASE_URL or {DEFAULT_BASE_URL})."
        ),
    )
    parser.add_argument(
        "--api-key-env",
        default="LLM_API_KEY",
        help="Environment variable containing the API key (default: LLM_API_KEY).",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Model name. Required for real execution; dry-run defaults to dry-run-model.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Sampling temperature for real execution (default: 0).",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        help="Optional maximum number of evidence records to process.",
    )
    parser.add_argument(
        "--ontology",
        type=Path,
        help="Seed ontology TTL used only by the llm_ontology condition.",
    )
    parser.add_argument(
        "--schema-context",
        type=Path,
        help="Generated schema JSON/Markdown context used only by the llm_schema condition.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="Per-record API timeout in seconds for real execution (default: 120).",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    if args.max_records is not None and args.max_records < 0:
        raise UserError("--max-records must be non-negative")
    if args.timeout <= 0:
        raise UserError("--timeout must be positive")

    records = read_jsonl(args.evidence)
    if args.max_records is not None:
        records = records[: args.max_records]
    if not records:
        raise UserError("no evidence records selected")

    model = args.model.strip() or ("dry-run-model" if args.dry_run else "")
    if not model:
        raise UserError("--model is required for real execution")

    api_key = ""
    if not args.dry_run:
        api_key = read_api_key(args.api_key_env)

    ontology_context = ""
    if args.condition == "llm_ontology":
        if args.ontology:
            ontology_context = extract_ontology_context(args.ontology)
        else:
            ontology_context = "No --ontology file was supplied."

    schema_context = ""
    schema_context_path = getattr(args, "schema_context", None)
    if args.condition == "llm_schema" and schema_context_path:
        schema_context = read_schema_context(Path(schema_context_path))

    prompts_dir = args.prompts_dir or default_prompts_dir(args.output)
    outputs: List[Dict[str, Any]] = []
    for index, (line_number, evidence_record) in enumerate(records):
        outputs.append(
            process_record(
                evidence_record=evidence_record,
                line_number=line_number,
                index=index,
                args=args,
                model=model,
                api_key=api_key,
                prompts_dir=prompts_dir,
                ontology_context=ontology_context,
                schema_context=schema_context,
            )
        )

    write_jsonl(args.output, outputs)
    status_counts: Dict[str, int] = {}
    for record in outputs:
        metadata = record.get("metadata", {})
        status = metadata.get("status", "unknown") if isinstance(metadata, dict) else "unknown"
        status_counts[str(status)] = status_counts.get(str(status), 0) + 1

    print("LLM JSON extraction complete")
    print(f"  condition: {args.condition}")
    print(f"  model: {model}")
    print(f"  records: {len(outputs)}")
    print(f"  statuses: {json.dumps(status_counts, sort_keys=True)}")
    print(f"  prompts: {prompts_dir}")
    print(f"  wrote: {args.output}")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except UserError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
