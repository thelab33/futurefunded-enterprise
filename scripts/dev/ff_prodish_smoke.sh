#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG="/tmp/ff_prodish_smoke.log"

cleanup() {
  if [[ -n "${FF_PID:-}" ]]; then
    kill "$FF_PID" 2>/dev/null || true
    wait "$FF_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

cd "$ROOT" || exit 1
fuser -k 5000/tcp 2>/dev/null || true

echo "== START PRODISH SERVER =="
nohup "$ROOT/scripts/dev/ff_run_local_prodish.sh" >"$LOG" 2>&1 &
FF_PID=$!

# wait for server
for _ in $(seq 1 20); do
  if curl -fsS http://127.0.0.1:5000/c/spring-fundraiser >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

echo
echo "== SERVER LOG (tail) =="
tail -n 40 "$LOG" || true

echo
echo "== PRODISH AUDIT =="
FF_FORCE_PRODISH=1 "$ROOT/scripts/audit/ff_campaign_truth_audit.sh" http://127.0.0.1:5000/c/spring-fundraiser
