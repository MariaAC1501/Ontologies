# Extraction run manifests

`pipeline.run_manifest` is a standard-library CLI for recording an extraction run without changing any extraction behavior. Integration into a wrapper is intentionally left to the wrapper owner.

## Create

Run this after outputs exist when output checksums are required (omit `--output` for a pre-run manifest):

```bash
python3 -m pipeline.run_manifest create \
  --manifest run/manifest.json \
  --base-dir . \
  --input 'corpus/**/*.pdf' \
  --config pipeline/parser-config.json \
  --prompt pipeline/prompts/extract.txt \
  --ontology pipeline/seed_ontology/opmad_seed.ttl \
  --output 'run/output/**/*' \
  --provider openai \
  --model gpt-example \
  --setting temperature=0 \
  --setting max_tokens=4096 \
  --parser-version facts-parser-v2 \
  --normalization-version opmad-normalization-v1 \
  --started-at 2026-08-24T12:00:00Z \
  --finished-at 2026-08-24T12:30:00Z
```

The JSON records:

- SHA-256 and byte size for each input, config, prompt, ontology, and existing output file;
- requested provider, model, settings, parser version, and normalization version;
- containing Git repository revision and dirty state;
- each recursively listed submodule's expected revision and, when initialized, its checked-out revision and dirty state;
- Python implementation/version and OS system/release/machine; and
- UTC creation time plus optional run start/finish times.

Use `--created-at` when an externally assigned timestamp is needed. Serialization is UTF-8 JSON with sorted keys, a trailing newline, and stable path ordering. Paths are POSIX-style and relative to `--base-dir`; absolute workstation paths are not stored.

## Check before resume

Re-hash all compatibility artifacts at their recorded paths and supply the settings for the proposed resumed request:

```bash
python3 -m pipeline.run_manifest validate run/manifest.json \
  --base-dir . \
  --provider openai \
  --model gpt-example \
  --setting temperature=0 \
  --setting max_tokens=4096 \
  --parser-version facts-parser-v2 \
  --normalization-version opmad-normalization-v1
```

If any `--setting` is supplied to `validate`, those arguments are treated as the complete current settings map. `--check-outputs` also verifies output files; outputs are not resume-compatibility fields by default because a resumed run can extend or replace them.

To compare two captured manifests:

```bash
python3 -m pipeline.run_manifest compare old-manifest.json proposed-manifest.json
```

Both commands print each actionable mismatch and return 0 when compatible, 1 for drift, or 2 for malformed input/usage. Comparisons use only `compatibility`: inputs, config, prompts, ontologies, model request, parser version, and normalization version. Outputs, Git state, runtime details, and timestamps are provenance and do not make two runs incompatible.

## File and security behavior

- A spec may be a regular file, directory, or recursive glob. Directories are recursively expanded. Duplicate and overlapping matches are deduplicated.
- Literal missing paths, unmatched globs, empty directories, symlinks, non-files, and paths outside `--base-dir` are errors rather than silently omitted.
- Obvious credential paths (`.env`, `.env.*`, `.aws`, `.ssh`, `.git`, credential/secret-named files, common private-key names, and private-key file extensions) are refused. Do not include secrets in any other hashed config file; keep secret injection separate from reproducibility config.
- Settings with secret-bearing names (API keys, access/auth/bearer/refresh tokens, passwords, credentials, authorization, private keys, or secrets) are stored as `[REDACTED]`. The process never loads dotenv files or reads secret values from the environment. Do not put a real secret on the command line; credential changes are intentionally not compatibility checks.
- A file changing while it is hashed is an error.
- No Git repository is represented explicitly with `present: false`. Dirty repositories are accepted and recorded, not cleaned or rejected.
- An uninitialized submodule has `initialized: false`, its index (`expected_revision`) recorded, and `revision`/`dirty` set to null. Initialized submodules record both expected and actual revisions.

## Tests

```bash
python3 -m unittest pipeline.tests.test_run_manifest
```
