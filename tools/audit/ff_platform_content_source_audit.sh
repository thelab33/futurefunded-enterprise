#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/futurefunded-enterprise}"
BASE_URL="${BASE_URL:-http://127.0.0.1:5000}"

cd "$ROOT"

STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="reports/platform-content-audit/${STAMP}"
LATEST_PTR="reports/platform-content-audit/LATEST.txt"

mkdir -p "$OUT"
printf '%s\n' "$OUT" > "$LATEST_PTR"

echo "== FutureFunded platform content-source audit =="
echo "root: $ROOT"
echo "base_url: $BASE_URL"
echo "out: $OUT"

# -------------------------------------------------------------------
# 00) Find platform API route implementations / references
# -------------------------------------------------------------------
rg -n \
  -e '/api/v1/platform/home' \
  -e '/api/v1/platform/onboarding' \
  -e '/api/v1/platform/dashboard' \
  -e '/api/v1/platform/pricing' \
  -e '/api/v1/platform/demo' \
  -e 'platform/home' \
  -e 'platform/onboarding' \
  -e 'platform/dashboard' \
  -e 'platform/pricing' \
  -e 'platform/demo' \
  apps packages \
  > "$OUT/00_api_route_refs.txt" || true

# -------------------------------------------------------------------
# 01) Search for old/new copy across app code
# -------------------------------------------------------------------
rg -n \
  -e 'FutureFunded command center' \
  -e 'Operator command center' \
  -e 'Admin dashboard' \
  -e 'Operator dashboard' \
  -e 'Onboarding' \
  -e 'Guided launch' \
  -e 'One branded organization\. One live campaign\. One clean handoff\.' \
  -e 'Start with one org\. Publish one live fundraiser\.' \
  -e '>Campaign<' \
  -e 'Public fundraiser' \
  -e 'Support-plan' \
  -e 'Recurring support' \
  apps packages \
  > "$OUT/01_copy_hits_repo.txt" || true

# -------------------------------------------------------------------
# 02) Focused hits for active templates + routes
# -------------------------------------------------------------------
rg -n \
  -e 'FutureFunded command center' \
  -e 'Operator command center' \
  -e 'Admin dashboard' \
  -e 'Operator dashboard' \
  -e 'Onboarding' \
  -e 'Guided launch' \
  -e 'One branded organization\. One live campaign\. One clean handoff\.' \
  -e 'Start with one org\. Publish one live fundraiser\.' \
  -e 'Campaign' \
  -e 'Public fundraiser' \
  apps/web/app/routes/platform.py \
  apps/web/app/templates/platform/pages/onboarding.html \
  apps/web/app/templates/platform/pages/dashboard.html \
  > "$OUT/02_active_surface_copy_hits.txt" || true

# -------------------------------------------------------------------
# 03) Fetch live API payloads
# -------------------------------------------------------------------
fetch_json() {
  local key="$1"
  local url="${BASE_URL}/api/v1/platform/${key}"
  local raw="${OUT}/api_${key}.json"

  curl -sS "$url" -o "$raw" || true
}

fetch_json home
fetch_json onboarding
fetch_json dashboard
fetch_json pricing
fetch_json demo

# -------------------------------------------------------------------
# 04) Search live API payloads for old/new strings
# -------------------------------------------------------------------
rg -n \
  -e 'FutureFunded command center' \
  -e 'Operator command center' \
  -e 'Admin dashboard' \
  -e 'Operator dashboard' \
  -e 'Onboarding' \
  -e 'Guided launch' \
  -e 'One branded organization\. One live campaign\. One clean handoff\.' \
  -e 'Start with one org\. Publish one live fundraiser\.' \
  -e 'Campaign' \
  -e 'Public fundraiser' \
  -e 'Recurring support' \
  "$OUT"/api_*.json \
  > "$OUT/04_api_copy_hits.txt" || true

# -------------------------------------------------------------------
# 05) Quick rendered page check for onboarding/dashboard headings
# -------------------------------------------------------------------
curl -sS "${BASE_URL}/platform/onboarding" -o "$OUT/render_onboarding.html" || true
curl -sS "${BASE_URL}/platform/dashboard" -o "$OUT/render_dashboard.html" || true

rg -n \
  -e '<h1' \
  -e 'One branded organization\. One live campaign\. One clean handoff\.' \
  -e 'Start with one org\. Publish one live fundraiser\.' \
  -e '>Campaign<' \
  -e 'Public fundraiser' \
  "$OUT/render_onboarding.html" \
  "$OUT/render_dashboard.html" \
  > "$OUT/05_rendered_copy_hits.txt" || true

# -------------------------------------------------------------------
# 06) Summary
# -------------------------------------------------------------------
export FF_CONTENT_AUDIT_OUT="$OUT"

python3 - <<'PY'
from __future__ import annotations
from pathlib import Path
import os

OUT = Path(os.environ["FF_CONTENT_AUDIT_OUT"])

def lines(name: str) -> list[str]:
    path = OUT / name
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8", errors="ignore").splitlines()

api_refs = lines("00_api_route_refs.txt")
repo_hits = lines("01_copy_hits_repo.txt")
active_hits = lines("02_active_surface_copy_hits.txt")
api_hits = lines("04_api_copy_hits.txt")
render_hits = lines("05_rendered_copy_hits.txt")

summary: list[str] = []
summary.append("# FutureFunded platform content-source audit summary")
summary.append("")
summary.append("## Snapshot")
summary.append(f"- platform API route refs: {len(api_refs)}")
summary.append(f"- repo copy hits: {len(repo_hits)}")
summary.append(f"- active surface copy hits: {len(active_hits)}")
summary.append(f"- live API copy hits: {len(api_hits)}")
summary.append(f"- rendered onboarding/dashboard hits: {len(render_hits)}")
summary.append("")
summary.append("## Files to inspect next")
summary.append(f"- {OUT / '00_api_route_refs.txt'}")
summary.append(f"- {OUT / '02_active_surface_copy_hits.txt'}")
summary.append(f"- {OUT / '04_api_copy_hits.txt'}")
summary.append(f"- {OUT / '05_rendered_copy_hits.txt'}")
summary.append("")
summary.append("## Founder question this answers")
summary.append("- Is live operator copy coming from route fallback, template defaults, or API payloads?")
summary.append("- Are onboarding/dashboard still being overridden by older API data?")
summary.append("")

(OUT / "06_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
PY

echo
echo "Audit complete:"
echo "  $OUT"
echo
echo "Key files:"
echo "  $OUT/06_summary.md"
echo "  $OUT/00_api_route_refs.txt"
echo "  $OUT/02_active_surface_copy_hits.txt"
echo "  $OUT/04_api_copy_hits.txt"
echo "  $OUT/05_rendered_copy_hits.txt"
echo
echo "LATEST pointer:"
echo "  $LATEST_PTR"
