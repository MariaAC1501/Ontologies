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
- containing Git repository revision and dirty state (also a resume-compatibility field);
- each recursively listed submodule's expected revision and, when initialized, its checked-out revision and dirty state (also resume-compatibility fields);
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

Resume compatibility is checked only when `--provider`, `--model`, the complete settings map, `--parser-version`, and `--normalization-version` are all supplied. Repeat `--setting` for the complete map, or use `--no-settings` for an empty map. A partial proposed request is an error. With none of those options, `validate` explicitly reports **file-integrity-only mode** and does not print `compatible`. `--check-outputs` also verifies output files; outputs are not resume-compatibility fields by default because a resumed run can extend or replace them.

To compare two captured manifests:

```bash
python3 -m pipeline.run_manifest compare old-manifest.json proposed-manifest.json
```

Both commands print each actionable mismatch and return 0 when compatible (or when an explicitly reported file-integrity-only check passes), 1 for drift, or 2 for malformed input/usage. Comparisons use only `compatibility`: inputs, config, prompts, ontologies, model request, parser/normalization versions, and code provenance (root revision/dirty state plus initialized submodule revisions/dirty state). Outputs, runtime details, and timestamps are excluded. Complete-request `validate` refreshes Git state by default before comparison.

Resume comparison fails closed whenever either manifest has a dirty root repository or dirty initialized submodule, even when both dirty booleans and revisions match. Schema v2 does not store a dirty-content fingerprint, so equality of those fields cannot establish that two worktrees contain the same code. Commit or otherwise clean the code tree before capturing a resume-compatible manifest.

## File and security behavior

- A spec may be a regular file, directory, or recursive glob. Directories are recursively expanded. Duplicate and overlapping matches are deduplicated.
- Literal missing paths, unmatched globs, empty directories, symlinks (including directory ancestors), non-files, and paths outside `--base-dir` are errors rather than silently omitted. The manifest destination must not be selected by any artifact file, directory, or glob specification; destination checks account for filesystem identity, parent aliases, and case-insensitive filesystems.
- Obvious credential paths (`.env`, `.env.*`, `.aws`, `.ssh`, `.git`, credential/secret-named files, common private-key names, and private-key file extensions) are refused. Do not include secrets in any other hashed config file; keep secret injection separate from reproducibility config.
- Settings with secret-bearing names (including PATs; API, SSH, signing, and other keys; access/auth/bearer/refresh tokens; passwords/passphrases; credentials; authorization; and secrets) are stored as `[REDACTED]`. Separator-delimited, camel-case, and common unseparated credential spellings are recognized conservatively. The process never loads dotenv files or reads secret values from the environment. Do not put a real secret on the command line; credential changes are intentionally not compatibility checks.
- Hashing opens each path component without following links where the platform supports it, requires a regular-file descriptor, and checks device/inode/type/size/mtime/ctime snapshots before and after reading. File or ancestor replacement is an error; swapped links, FIFOs, and outside targets are never read.
- No Git repository is represented explicitly with `present: false`. Dirty repositories are accepted and recorded for provenance, but are never resume-compatible. Git discovery, status, revision, and submodule failures are fatal rather than treated as absence.
- An uninitialized submodule has `initialized: false`, its index (`expected_revision`) recorded, and `revision`/`dirty` set to null. Initialized submodules record both expected and actual revisions.
- Loaded schema-version-2 manifests are fully type/shape checked, including canonical safe relative paths, checksums, sizes, timestamps, settings redaction, known artifact groups, and duplicate paths.

## Tests

```bash
python3 -m unittest pipeline.tests.test_run_manifest
```
