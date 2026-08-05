#!/usr/bin/env bash
set -uo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
FIRST="$ROOT/run_remaining_500_gpt-5.6-luna_20260723_010000"
SECOND="$ROOT/run_remaining_222_gpt-5.6-luna_20260723_010000"
LOG="$FIRST/orchestrator.log"
first_pid=$(cat "$FIRST/run.pid" 2>/dev/null || true)
echo "[$(date -Is)] waiting for first batch pid=${first_pid}" >> "$LOG"
while [ -n "$first_pid" ] && ps -ef | awk -v pid="$first_pid" '$2==pid {found=1} END{exit !found}'; do
  sleep 60
done
echo "[$(date -Is)] first batch stopped; launching remaining 222-paper batch" >> "$LOG"
: > "$SECOND/run.log"
ONTOCAST_HEAD_CHUNKS=3 nohup bash "$SECOND/run_ontocast_222.sh" > "$SECOND/run.log" 2>&1 &
echo $! > "$SECOND/run.pid"
MONITOR_INTERVAL_SECONDS=60 nohup bash "$SECOND/monitor_ontocast_222.sh" >/dev/null 2>&1 &
echo $! > "$SECOND/monitor.pid"
echo "[$(date -Is)] second batch launched pid=$(cat "$SECOND/run.pid")" >> "$LOG"
