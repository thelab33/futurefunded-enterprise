#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://127.0.0.1:5000/c/connect-atx-elite}"
TMP_HTML="$(mktemp)"
trap 'rm -f "$TMP_HTML"' EXIT

printf '\n== FF LAUNCH SMOKE ==\n'
printf 'URL: %s\n' "$BASE_URL"

printf '\n-- HTML fetch --\n'
curl -fsSL "$BASE_URL" -o "$TMP_HTML"
printf '✅ page fetched\n'

printf '\n-- contract hooks --\n'
checks=(
  'id="heroTitle"'
  'id="checkout"'
  'id="faq"'
  'data-ff-open-checkout'
  'data-ff-checkout-sheet'
  'data-ff-open-sponsor'
  'data-ff-video-modal'
  'data-ff-theme-toggle'
  'data-ff-tabs'
  'id="ffConfig"'
  'id="ffSelectors"'
)
for needle in "${checks[@]}"; do
  if rg -q "$needle" "$TMP_HTML"; then
    printf '✅ %s\n' "$needle"
  else
    printf '❌ %s\n' "$needle"
  fi
done

printf '\n-- css/js references --\n'
CSS_URL="$(python3 - <<'PY' "$TMP_HTML"
from pathlib import Path
import re, sys
t = Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
m = re.search(r'<link[^>]+href="([^"]*ff\.css[^"]*)"', t)
print(m.group(1) if m else "")
PY
)"
JS_URL="$(python3 - <<'PY' "$TMP_HTML"
from pathlib import Path
import re, sys
t = Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
m = re.search(r'<script[^>]+src="([^"]*ff-app\.js[^"]*)"', t)
print(m.group(1) if m else "")
PY
)"

printf 'CSS: %s\n' "${CSS_URL:-MISSING}"
printf 'JS : %s\n' "${JS_URL:-MISSING}"

printf '\n-- static asset reachability --\n'
python3 - <<'PY' "$TMP_HTML" "$BASE_URL"
from pathlib import Path
from urllib.parse import urljoin
import re, sys, subprocess

html = Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
base = sys.argv[2]

srcs = re.findall(r'src="([^"]+)"', html)
imgs = []
for s in srcs:
    if "/static/" in s and any(ext in s.lower() for ext in [".jpg", ".jpeg", ".png", ".webp", ".svg"]):
        imgs.append(urljoin(base, s))

seen = []
for u in imgs:
    if u not in seen:
        seen.append(u)

if not seen:
    print("⚠️ no static image URLs found in rendered HTML")
    raise SystemExit(0)

for u in seen[:20]:
    code = subprocess.run(
        ["bash", "-lc", f"curl -I -L -s -o /dev/null -w '%{{http_code}}' '{u}'"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    ok = code.startswith("2") or code.startswith("3")
    print(("✅" if ok else "❌"), code, u)
PY

printf '\n-- local file syntax checks --\n'
python3 - <<'PY'
from pathlib import Path
p = Path("apps/web/app/static/css/ff.css")
t = p.read_text(encoding="utf-8")
print("CSS braces balanced:", t.count("{") == t.count("}"))
print("CSS opens :", t.count("{"))
print("CSS closes:", t.count("}"))
PY

node --check apps/web/app/static/js/ff-app.js
printf '✅ JS syntax OK\n'

printf '\n== DONE ==\n'
