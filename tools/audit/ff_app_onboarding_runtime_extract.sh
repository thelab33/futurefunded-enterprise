#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/futurefunded-enterprise}"
cd "$ROOT"

OUT="reports/js-audit"
mkdir -p "$OUT"

JS="apps/web/app/static/js/ff-app.js"

printf '== FILE CHECK ==\n' | tee "$OUT/00_file_check.txt"
ls -l "$JS" | tee -a "$OUT/00_file_check.txt"

printf '\n== ONBOARD / RUNTIME GREP ==\n' | tee "$OUT/01_onboard_runtime_grep.txt"
rg -n \
  'onboard|openOnboard|closeOnboard|ff-onboarding|data-ff-open-onboard|data-ff-close-onboard|onboardModal|onboardNext|onboardPrev|onboardFinish|themeToggle|openDrawer|openSponsor|openCheckout|ffSelectors|selectors' \
  "$JS" | tee -a "$OUT/01_onboard_runtime_grep.txt" || true

printf '\n== FIRST 260 LINES ==\n' | tee "$OUT/02_head.txt"
sed -n '1,260p' "$JS" | tee -a "$OUT/02_head.txt"

printf '\n== AROUND ONBOARD MATCHES ==\n' | tee "$OUT/03_onboard_context.txt"
python3 - <<'PY' | tee -a "$OUT/03_onboard_context.txt"
from pathlib import Path
import re

p = Path("apps/web/app/static/js/ff-app.js")
text = p.read_text(encoding="utf-8")
lines = text.splitlines()

patterns = [
    r'onboard',
    r'openOnboard',
    r'closeOnboard',
    r'ff-onboarding',
    r'data-ff-open-onboard',
    r'onboardModal',
    r'onboardNext',
    r'onboardPrev',
    r'onboardFinish',
]

hits = []
for i, line in enumerate(lines, start=1):
    for pat in patterns:
        if re.search(pat, line):
            hits.append(i)
            break

seen = set()
for line_no in hits:
    start = max(1, line_no - 10)
    end = min(len(lines), line_no + 18)
    key = (start, end)
    if key in seen:
        continue
    seen.add(key)
    print(f"\n--- CONTEXT {start}:{end} ---")
    for n in range(start, end + 1):
        print(f"{n:04d}: {lines[n-1]}")
PY

printf '\n== JS SYNTAX CHECK ==\n' | tee "$OUT/04_node_check.txt"
node --check "$JS" | tee -a "$OUT/04_node_check.txt"

printf '\n== DONE ==\n'
