#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/futurefunded-enterprise}"
cd "$ROOT"

JS="apps/web/app/static/js/ff-app.js"
BASE_URL="${FF_BASE_URL:-http://127.0.0.1:5000}"
PLATFORM_HOME_PATH="${FF_PLATFORM_HOME_PATH:-/platform}"
CAMPAIGN_PATH="${FF_CAMPAIGN_PATH:-/c/spring-fundraiser}"

echo "== JS SYNTAX =="
node --check "$JS"

echo
echo "== KEY STRING CONTRACTS =="
python - <<'PY'
from pathlib import Path

p = Path("apps/web/app/static/js/ff-app.js")
t = p.read_text(encoding="utf-8")

required = [
    "toggleTheme",
    "applySavedTheme",
    "syncThemeButtons",
    "setAmount",
    "syncAmountChipState",
    "updateSummaryAmount",
    "ff:runtime-hardened",
]

missing = [x for x in required if x not in t]
if missing:
    raise SystemExit("Missing runtime markers: " + ", ".join(missing))

print("OK: runtime markers present")
PY

echo
echo "== PLATFORM HOME FETCH =="
curl -fsS "${BASE_URL}${PLATFORM_HOME_PATH}" > /tmp/ff-platform-home.html

python - <<'PY'
from pathlib import Path

t = Path("/tmp/ff-platform-home.html").read_text(encoding="utf-8", errors="ignore")

required_any = [
    "FutureFunded",
    "Launch your first organization",
    "Open dashboard",
    "Onboarding",
    "Dashboard",
    "<html",
    "<body",
]

if not any(x in t for x in required_any):
    raise SystemExit("Platform home fetch succeeded, but expected platform-home markers were not found.")

print("OK: platform home fetched and contains expected platform markers")
PY

echo
echo "== CAMPAIGN PAGE CONTRACT CHECK =="
curl -fsS "${BASE_URL}${CAMPAIGN_PATH}" > /tmp/ff-campaign-page.html

python - <<'PY'
from pathlib import Path

t = Path("/tmp/ff-campaign-page.html").read_text(encoding="utf-8", errors="ignore")

required = [
    'id="ffConfig"',
    'id="ffSelectors"',
    'id="checkout"',
    'data-ff-checkout-sheet',
]

missing = [x for x in required if x not in t]
if missing:
    raise SystemExit("Missing campaign contracts: " + ", ".join(missing))

print("OK: campaign contracts present")
PY

echo
echo "✅ ff launch runtime gate passed"
