#!/usr/bin/env python3
"""Generate an LLM-designed extraction schema or ontology from evidence JSONL.

The CLI reads evidence packages produced by ``build_evidence_packages.py`` and
creates one meta-prompt for RQ2 schema/ontology generation.  In ``--dry-run``
mode no API is called: the script writes ``prompt.md``, a template artifact, and
``metadata.json``.  Real execution uses an OpenAI-compatible Chat Completions
endpoint through the Python standard library.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


DEFAULT_EVIDENCE = Path("paper/experiments/evidence.jsonl")
DEFAULT_OUTPUT_DIR = Path("paper/experiments/llm_generated_artifact")
DEFAULT_BASE_URL = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
DEFAULT_MODEL = os.environ.get("LLM_MODEL", "")
ARTIFACTS = ("schema_json", "ontology_ttl")
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
COMPETENCY_QUESTIONS: Tuple[Tuple[str, str], ...] = (
    ("CQ1", "Which physical asset, machine, component, dataset, or industrial system is studied?"),
    ("CQ2", "Which predictive-maintenance task is addressed, such as fault diagnosis, anomaly detection, prognosis, RUL estimation, forecasting, or maintenance decision support?"),
    ("CQ3", "Which variables, sensors, signals, logs, images, or other model inputs are used, and how many input variables are reported?"),
    ("CQ4", "Which modeling approach, model family, and concrete algorithms are used or compared?"),
    ("CQ5", "Which preprocessing, feature-engineering, segmentation, normalization, or data-cleaning steps are described?"),
    ("CQ6", "Which performance indicators and numeric/qualitative performance results are reported?"),
    ("CQ7", "Which exact textual evidence spans support each extracted field or relationship?"),
)


class UserError(Exception):
    """Raised for user-facing CLI errors."""


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def display_path(path: Path) -> str:
    return path.as_posix()


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


def write_text(path: Path, text: str) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    except OSError as exc:
        raise UserError(f"could not write {path}: {exc}") from exc


def write_json(path: Path, obj: Any) -> None:
    write_text(path, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


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


def truncate_text(value: str, max_chars: int) -> str:
    if len(value) <= max_chars:
        return value
    if max_chars <= 80:
        return value[:max_chars]
    return value[: max_chars - 40].rstrip() + "\n...[truncated for prompt budget]..."


def metadata_preview(metadata: Any) -> str:
    if not isinstance(metadata, dict):
        return "{}"
    keep: Dict[str, Any] = {}
    for key in (
        "corpus_id",
        "bibliographic",
        "keywords",
        "screening",
        "sample_manifest_fields",
        "pdf",
        "facts",
        "text",
    ):
        if key in metadata:
            keep[key] = metadata[key]
    if not keep:
        keep = metadata
    return json.dumps(keep, ensure_ascii=False, indent=2, sort_keys=True)


def competency_questions_markdown() -> str:
    return "\n".join(f"- {identifier}: {question}" for identifier, question in COMPETENCY_QUESTIONS)


def competency_questions_json() -> List[Dict[str, str]]:
    return [{"id": identifier, "question": question} for identifier, question in COMPETENCY_QUESTIONS]


def canonical_fields_text() -> str:
    return ", ".join(f"`{field}`" for field in CANONICAL_FIELDS)


def evidence_digest(
    records: Sequence[Tuple[int, Dict[str, Any]]],
    max_chars_per_record: int,
    max_total_chars: int,
) -> Tuple[str, List[str]]:
    lines: List[str] = []
    record_ids: List[str] = []
    used_chars = 0
    truncated = False

    for index, (line_number, record) in enumerate(records, start=1):
        record_id = get_record_id(record, line_number)
        record_ids.append(record_id)
        evidence_text = str(record.get("evidence_text", "")).strip()
        scope = str(record.get("scope", "")).strip() or "unknown"
        metadata = truncate_text(metadata_preview(record.get("metadata")), 2500)
        evidence = truncate_text(evidence_text, max_chars_per_record)
        block = (
            f"### Evidence record {index}: {record_id}\n"
            f"- JSONL line: {line_number}\n"
            f"- Scope: {scope}\n\n"
            "Metadata preview:\n"
            f"```json\n{metadata}\n```\n\n"
            "Evidence text:\n"
            f"```text\n{evidence}\n```\n"
        )
        if used_chars + len(block) > max_total_chars:
            remaining = max_total_chars - used_chars
            if remaining > 200:
                lines.append(truncate_text(block, remaining))
            truncated = True
            break
        lines.append(block)
        used_chars += len(block)

    if truncated:
        lines.append("\n...[evidence digest truncated for prompt budget]...\n")
    return "\n".join(lines).strip(), record_ids


def schema_response_contract() -> str:
    return (
        "Return only one valid JSON object. It should be usable as --schema-context "
        "for downstream extraction and should include at least these top-level keys:\n"
        "- schema_name: concise identifier.\n"
        "- description: scope and assumptions.\n"
        "- competency_questions: array containing CQ1-CQ7.\n"
        "- entity_types: domain entity definitions, including assets, tasks, variables, models, "
        "preprocessing, performance, publications, and textual evidence.\n"
        "- relations: relationships among those entities.\n"
        "- extraction_fields: fields to extract with name, type, description, normalization guidance, "
        "target entity/relation, and whether textual evidence is required.\n"
        "- canonical_field_mapping: mapping to the canonical 19 fields used by the evaluation harness.\n"
        "- provenance_requirements: how to store source record IDs and exact evidence spans.\n"
        "- normalization_rules: recommended controlled vocabularies or normalization steps."
    )


def ontology_response_contract() -> str:
    return (
        "Return only Turtle, with no Markdown fences or explanations. The ontology should be compact but complete "
        "enough to guide downstream extraction. Include:\n"
        "- @prefix declarations, owl:Ontology metadata, rdfs:label, and rdfs:comment annotations.\n"
        "- Classes for Asset, MaintenanceTask, InputVariable, ModelApproach, ModelFamily, Model, "
        "PreprocessingStep, PerformanceIndicator, PerformanceResult, Publication, and TextualEvidence.\n"
        "- Object/datatype properties linking studies to assets, tasks, variables, models, preprocessing, "
        "performance, and textual evidence spans.\n"
        "- Comments or annotations that map ontology terms to the canonical 19 extraction fields.\n"
        "- Domain/range axioms where useful, without overfitting to a single paper."
    )


def build_prompt(
    records: Sequence[Tuple[int, Dict[str, Any]]],
    artifact: str,
    max_chars_per_record: int,
    max_total_chars: int,
) -> Tuple[str, str, List[str]]:
    evidence, record_ids = evidence_digest(
        records=records,
        max_chars_per_record=max_chars_per_record,
        max_total_chars=max_total_chars,
    )
    if artifact == "schema_json":
        response_contract = schema_response_contract()
        artifact_instruction = "Generate a JSON extraction schema."
        return_only = "Return only a JSON object."
    elif artifact == "ontology_ttl":
        response_contract = ontology_response_contract()
        artifact_instruction = "Generate an RDF/OWL ontology in Turtle."
        return_only = "Return only Turtle text."
    else:
        raise UserError(f"unknown artifact: {artifact}")

    system = (
        "You are a careful ontology and information-extraction schema engineer for scientific "
        "predictive-maintenance literature. Design reusable artifacts; do not extract one-off facts. "
        f"{return_only}"
    )
    user = (
        "RQ2 task: use the supplied evidence package examples to design an LLM-generated artifact for "
        "extracting predictive-maintenance knowledge from scientific texts. The artifact will later guide "
        "per-paper extraction, so it must be reusable across papers and should not assert that any example "
        "fact is universally true.\n\n"
        f"Requested artifact: `{artifact}`. {artifact_instruction}\n\n"
        "Competency questions the artifact must support:\n"
        f"{competency_questions_markdown()}\n\n"
        "The downstream evaluator uses these canonical fields; cover them directly or through an explicit mapping:\n"
        f"{canonical_fields_text()}\n\n"
        "Design requirements:\n"
        "- Focus on predictive maintenance, prognostics, diagnostics, anomaly/fault detection, RUL estimation, "
        "condition monitoring, and maintenance decision support in scientific papers.\n"
        "- Represent assets/systems, tasks, variables/inputs, models/algorithms, preprocessing, performance, "
        "publication metadata, and exact textual evidence/provenance.\n"
        "- Prefer normalized labels and aliases, but keep enough flexibility for unseen scientific wording.\n"
        "- Mark unknown or unstated values as missing during downstream extraction; do not encourage inference beyond text.\n"
        "- Require exact evidence spans or source snippets for each extracted value whenever possible.\n\n"
        "Response contract:\n"
        f"{response_contract}\n\n"
        "Evidence package examples:\n"
        f"{evidence}\n"
    )
    return system, user, record_ids


def write_prompt_markdown(path: Path, artifact: str, system: str, user: str) -> None:
    content = (
        f"# LLM-generated {artifact} prompt\n\n"
        "## System\n\n"
        f"{system}\n\n"
        "## User\n\n"
        f"{user}\n"
    )
    write_text(path, content)


def schema_template() -> Dict[str, Any]:
    return {
        "schema_name": "dry_run_template_predictive_maintenance_extraction_schema",
        "artifact_type": "schema_json",
        "description": "Template only; --dry-run made no LLM API call.",
        "competency_questions": competency_questions_json(),
        "entity_types": [],
        "relations": [],
        "extraction_fields": [],
        "canonical_field_mapping": {field: "" for field in CANONICAL_FIELDS},
        "provenance_requirements": {
            "record_id_required": True,
            "textual_evidence_required": True,
            "evidence_span_field": "textual_evidence",
        },
        "normalization_rules": [],
    }


def ontology_template() -> str:
    cq_comments = "\n".join(f"# {identifier}: {question}" for identifier, question in COMPETENCY_QUESTIONS)
    canonical_comments = "\n".join(f"# canonical field: {field}" for field in CANONICAL_FIELDS)
    return f"""@prefix pmllm: <https://w3id.org/predictive-maintenance/llm-generated#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Dry-run template only; --dry-run made no LLM API call.
# Competency questions:
{cq_comments}
# Canonical extraction fields to cover:
{canonical_comments}

pmllm:PredictiveMaintenanceExtractionOntology a owl:Ontology ;
    rdfs:label "Dry-run template for an LLM-generated predictive-maintenance extraction ontology"@en ;
    rdfs:comment "Template artifact for RQ2 schema/ontology generation; replace via real execution before analysis."@en .

pmllm:Study a owl:Class ; rdfs:label "Study"@en .
pmllm:Asset a owl:Class ; rdfs:label "Asset"@en .
pmllm:MaintenanceTask a owl:Class ; rdfs:label "Maintenance task"@en .
pmllm:InputVariable a owl:Class ; rdfs:label "Input variable"@en .
pmllm:Model a owl:Class ; rdfs:label "Model"@en .
pmllm:PreprocessingStep a owl:Class ; rdfs:label "Preprocessing step"@en .
pmllm:PerformanceResult a owl:Class ; rdfs:label "Performance result"@en .
pmllm:TextualEvidence a owl:Class ; rdfs:label "Textual evidence"@en .

pmllm:hasTextualEvidence a owl:ObjectProperty ;
    rdfs:label "has textual evidence"@en ;
    rdfs:comment "Links an extracted value or study to an exact supporting text span."@en .
"""


def artifact_filename(artifact: str) -> str:
    if artifact == "schema_json":
        return "generated_schema.json"
    if artifact == "ontology_ttl":
        return "generated_ontology.ttl"
    raise UserError(f"unknown artifact: {artifact}")


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
    artifact: str,
    system: str,
    user: str,
) -> str:
    payload: Dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
    }
    if artifact == "schema_json":
        payload["response_format"] = {"type": "json_object"}

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
        raise UserError("chat completions response did not contain choices[0].message.content") from exc
    if not isinstance(content, str):
        raise UserError("choices[0].message.content was not a string")
    return content


def strip_markdown_fence(text: str) -> str:
    match = re.fullmatch(r"\s*```(?:[A-Za-z0-9_-]+)?\s*(.*?)\s*```\s*", text, flags=re.DOTALL)
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


def normalize_artifact_response(artifact: str, content: str) -> str:
    if artifact == "schema_json":
        parsed = parse_model_json(content)
        return json.dumps(parsed, ensure_ascii=False, indent=2) + "\n"
    if artifact == "ontology_ttl":
        turtle = strip_markdown_fence(content)
        if not turtle:
            raise UserError("model response for ontology_ttl was empty")
        return turtle.rstrip() + "\n"
    raise UserError(f"unknown artifact: {artifact}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--evidence",
        type=Path,
        default=DEFAULT_EVIDENCE,
        help="Input evidence JSONL path.",
    )
    parser.add_argument(
        "--artifact",
        choices=ARTIFACTS,
        required=True,
        help="Artifact to generate from the evidence prompt.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for prompt.md, generated artifact, and metadata.json.",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        help="Optional maximum number of evidence records to include in the generation prompt.",
    )
    parser.add_argument(
        "--max-chars-per-record",
        type=int,
        default=4000,
        help="Maximum evidence_text characters included per record in prompt.md.",
    )
    parser.add_argument(
        "--max-total-chars",
        type=int,
        default=60000,
        help="Maximum total evidence digest characters included in prompt.md.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not call an API; write prompt.md, a template artifact, and metadata.json.",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="OpenAI-compatible base URL, or full /chat/completions URL.",
    )
    parser.add_argument(
        "--api-key-env",
        default="LLM_API_KEY",
        help="Environment variable containing the API key.",
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
        help="Sampling temperature for real execution.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="API timeout in seconds for real execution.",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    if args.max_records is not None and args.max_records < 0:
        raise UserError("--max-records must be non-negative")
    if args.max_chars_per_record < 1:
        raise UserError("--max-chars-per-record must be positive")
    if args.max_total_chars < 1:
        raise UserError("--max-total-chars must be positive")
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

    output_dir = args.output_dir
    artifact_path = output_dir / artifact_filename(args.artifact)
    prompt_path = output_dir / "prompt.md"
    metadata_path = output_dir / "metadata.json"

    system, user, record_ids = build_prompt(
        records=records,
        artifact=args.artifact,
        max_chars_per_record=args.max_chars_per_record,
        max_total_chars=args.max_total_chars,
    )
    write_prompt_markdown(prompt_path, args.artifact, system, user)

    metadata: Dict[str, Any] = {
        "status": "dry-run" if args.dry_run else "pending",
        "artifact": args.artifact,
        "model": model,
        "temperature": args.temperature,
        "base_url": args.base_url,
        "api_key_env": args.api_key_env,
        "evidence": display_path(args.evidence),
        "record_count": len(records),
        "record_ids": record_ids,
        "max_records": args.max_records,
        "max_chars_per_record": args.max_chars_per_record,
        "max_total_chars": args.max_total_chars,
        "prompt_file": display_path(prompt_path),
        "artifact_file": display_path(artifact_path),
        "created_at": utc_now(),
        "competency_questions": competency_questions_json(),
        "errors": [],
    }

    return_code = 0
    if args.dry_run:
        if args.artifact == "schema_json":
            write_json(artifact_path, schema_template())
        else:
            write_text(artifact_path, ontology_template())
        metadata["elapsed_seconds"] = 0.0
        metadata["finished_at"] = utc_now()
    else:
        started = time.time()
        try:
            api_key = read_api_key(args.api_key_env)
            content = call_chat_completion(
                base_url=args.base_url,
                api_key=api_key,
                model=model,
                temperature=args.temperature,
                timeout=args.timeout,
                artifact=args.artifact,
                system=system,
                user=user,
            )
            artifact_text = normalize_artifact_response(args.artifact, content)
            write_text(artifact_path, artifact_text)
            metadata["status"] = "ok"
            metadata["response_chars"] = len(content)
        except Exception as exc:
            metadata["status"] = "error"
            metadata["errors"] = [str(exc)]
            metadata["artifact_template_written"] = True
            if args.artifact == "schema_json":
                write_json(artifact_path, schema_template())
            else:
                write_text(artifact_path, ontology_template())
            return_code = 2
        finally:
            metadata["elapsed_seconds"] = round(time.time() - started, 3)
            metadata["finished_at"] = utc_now()

    write_json(metadata_path, metadata)

    print("LLM schema/ontology generation complete")
    print(f"  artifact: {args.artifact}")
    print(f"  status: {metadata['status']}")
    print(f"  model: {model}")
    print(f"  records: {len(records)}")
    print(f"  prompt: {prompt_path}")
    print(f"  artifact file: {artifact_path}")
    print(f"  metadata: {metadata_path}")
    return return_code


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
