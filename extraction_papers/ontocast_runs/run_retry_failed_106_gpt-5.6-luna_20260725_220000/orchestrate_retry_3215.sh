#!/usr/bin/env bash
set -uo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
MAIN="$ROOT/run_retry_failed_106_gpt-5.6-luna_20260725_220000"
SINGLE="$ROOT/run_retry_paper3215_gpt-5.6-luna_20260725_220000"
LOG="$MAIN/orchestrator.log"
main_pid=$(cat "$MAIN/run.pid" 2>/dev/null || true)
echo "[$(date -Is)] waiting for retry batch pid=${main_pid}" >> "$LOG"
while [ -n "$main_pid" ] && ps -ef | awk -v pid="$main_pid" '$2==pid {found=1} END{exit !found}'; do sleep 60; done
echo "[$(date -Is)] retry batch stopped; launching isolated paper-3215 retry" >> "$LOG"
: > "$SINGLE/run.log"
ONTOCAST_HEAD_CHUNKS=1 nohup bash "$SINGLE/run_retry_3215.sh" > "$SINGLE/run.log" 2>&1 &
echo $! > "$SINGLE/run.pid"
MONITOR_INTERVAL_SECONDS=60 nohup bash "$SINGLE/monitor_retry_3215.sh" >/dev/null 2>&1 &
echo $! > "$SINGLE/monitor.pid"
echo "[$(date -Is)] isolated retry launched pid=$(cat "$SINGLE/run.pid")" >> "$LOG"
