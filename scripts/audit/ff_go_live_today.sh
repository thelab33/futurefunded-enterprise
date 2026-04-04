#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/futurefunded-enterprise}"
cd "$ROOT"

echo "== 1/4 JS runtime gate =="
scripts/audit/ff_launch_runtime_gate.sh

echo
echo "== 2/4 config audit =="
python scripts/audit/ff_launch_config_audit.py

echo
echo "== 3/4 page unification audit =="
python scripts/audit/ff_pages_unification_audit.py
sed -n '1,120p' docs/audits/pages-unification-audit.md

echo
echo "== 4/4 route smoke =="
scripts/audit/ff_route_smoke.sh

echo
echo "✅ go-live today audit pack complete"
