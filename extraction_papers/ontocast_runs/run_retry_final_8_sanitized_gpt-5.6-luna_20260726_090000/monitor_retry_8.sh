#!/usr/bin/env bash
set -uo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUN_DIR="extraction_papers/ontocast_runs/$(basename "${SCRIPT_DIR}")"
PID=$(cat "$RUN_DIR/run.pid" 2>/dev/null || echo "")
LOG="$RUN_DIR/monitor.log"
interval=${MONITOR_INTERVAL_SECONDS:-60}
echo "[$(date -Is)] monitor started pid=$PID interval=${interval}s" >> "$LOG"
while true; do
  if [ -n "$PID" ] && ps -ef | awk -v pid="$PID" '$2==pid {found=1} END{exit !found}'; then status=running; else status=not_running; fi
  facts=$(find "$RUN_DIR/output" -maxdepth 1 -type f -name 'facts_*.ttl' | wc -l | tr -d ' ')
  files=$(find "$RUN_DIR/output" -maxdepth 1 -type f | wc -l | tr -d ' ')
  last=$(find "$RUN_DIR/output" -maxdepth 1 -type f -printf '%T@ %f\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)
  echo "[$(date -Is)] status=$status facts=$facts output_files=$files last_output=${last:-none}" >> "$LOG"
  if [ "$status" != running ]; then echo "[$(date -Is)] monitor finished" >> "$LOG"; break; fi
  sleep "$interval"
done
