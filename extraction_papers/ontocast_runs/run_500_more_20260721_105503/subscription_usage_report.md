# Subscription usage estimate for run_500_more_20260721_105503

Scope: local Pi Codex/OpenAI-compatible proxy logs for the 500-paper OntoCast extraction run.

## What can be measured

- Successful Codex completion requests: 2,052
- Failed requests caused by unsupported temporary model setting: 18
- Total proxy requests observed: 2,070
- Extracted papers: 500
- Successful completion requests per extracted paper: 4.10
- Total requests per extracted paper including failed unsupported-model attempts: 4.14
- First successful proxy completion: 2026-07-21T17:10:03.096Z
- Last successful proxy completion: 2026-07-22T22:38:24.345Z
- Elapsed wall-clock span between first/last completion: 29h 28m 21s
- Sum of per-request completion latencies: 10h 27m 45s
- Average completion latency: 18.36s/request

## Important limitation

The proxy logs did not persist token counts or a provider-side subscription quota counter. Therefore this report measures subscription activity as request counts and latency, not exact tokens, dollars, or percent of monthly subscription quota consumed.

The ChatGPT/Codex subscription is a flat subscription rather than direct API billing in this workflow, so there is no per-token dollar cost available from these logs.
