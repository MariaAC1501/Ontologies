#!/usr/bin/env bash
set -uo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUN_DIR="extraction_papers/ontocast_runs/$(basename "${SCRIPT_DIR}")"
PID=$(cat "$RUN_DIR/run.pid" 2>/dev/null || echo "")
if [ -n "$PID" ] && ps -ef | awk -v pid="$PID" '$2==pid {found=1} END{exit !found}'; then
  proc_status="running"
else
  proc_status="not_running"
fi
facts=$(find "$RUN_DIR/output" -maxdepth 1 -type f -name 'facts_*.ttl' | wc -l | tr -d ' ')
files=$(find "$RUN_DIR/output" -maxdepth 1 -type f | wc -l | tr -d ' ')
last=$(find "$RUN_DIR/output" -maxdepth 1 -type f -printf '%T@ %f
' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)
echo "run_dir=$RUN_DIR"
echo "pid=${PID:-none}"
echo "status=$proc_status"
echo "facts=$facts"
echo "output_files=$files"
echo "last_output=${last:-none}"
echo "run_log=$RUN_DIR/run.log"
echo "monitor_log=$RUN_DIR/monitor.log"
