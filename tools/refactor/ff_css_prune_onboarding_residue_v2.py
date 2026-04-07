from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
FF = ROOT / "apps/web/app/static/css/ff.css"
SHIM = ROOT / "apps/web/app/static/css/ff-above-main-premium.css"

for p in (FF, SHIM):
    if not p.exists():
        raise SystemExit(f"Missing CSS file: {p}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
for p in (FF, SHIM):
    shutil.copy2(p, p.with_name(f"{p.name}.{timestamp}.bak"))

ff = FF.read_text(encoding="utf-8")
shim = SHIM.read_text(encoding="utf-8")
applied: list[str] = []

def cleanup_selector_groups(text: str) -> str:
    rules = [
        (r',\s*\.ff-onboardModal__body\b', '', "remove .ff-onboardModal__body from selector groups"),
        (r',\s*\.ff-onboardSummary\b', '', "remove .ff-onboardSummary from selector groups"),
        (r',\s*\.ff-onboardModal__head\b', '', "remove .ff-onboardModal__head from selector groups"),
        (r',\s*\.ff-onboardModal__actions\b', '', "remove .ff-onboardModal__actions from selector groups"),
        (r',\s*\[data-ff-onboard-modal\]\b', '', "remove [data-ff-onboard-modal] from selector groups"),
        (r',\s*\[data-ff-close-onboard\]\b', '', "remove [data-ff-close-onboard] from selector groups"),
        (r',\s*\[data-ff-onboard-status\]\b', '', "remove [data-ff-onboard-status] from selector groups"),
        (r',\s*\[data-ff-onboard-result\]\b', '', "remove [data-ff-onboard-result] from selector groups"),
        (r',\s*\.ff-onboardModal__footer\b', '', "remove .ff-onboardModal__footer from selector groups"),
        (r',\s*\.ff-onboardModal__footer\s*>\s*\*', '', "remove .ff-onboardModal__footer > * from selector groups"),
        (r'#ff-onboarding\s*,\s*', '', "remove leading #ff-onboarding from selector groups"),
        (r',\s*#ff-onboarding\b', '', "remove #ff-onboarding from selector groups"),
    ]
    out = text
    for pattern, repl, label in rules:
        new_out, count = re.subn(pattern, repl, out)
        if count:
            applied.append(f"{label} x{count}")
            out = new_out
    return out

# 1) clean grouped selector lists safely
ff = cleanup_selector_groups(ff)

# 2) remove any remaining standalone onboarding-only blocks in ff.css
standalone_patterns = [
    (r'\n[ \t]*\.ff-onboardModal__body\s*\{[^{}]*\}\n', '\n', "standalone .ff-onboardModal__body block"),
    (r'\n[ \t]*\.ff-onboardSummary\s*\{[^{}]*\}\n', '\n', "standalone .ff-onboardSummary block"),
    (r'\n[ \t]*\.ff-onboardModal__head\s*\{[^{}]*\}\n', '\n', "standalone .ff-onboardModal__head block"),
    (r'\n[ \t]*\.ff-onboardModal__actions\s*\{[^{}]*\}\n', '\n', "standalone .ff-onboardModal__actions block"),
    (r'\n[ \t]*\[data-ff-onboard-modal\]\s*\{[^{}]*\}\n', '\n', "standalone [data-ff-onboard-modal] block"),
    (r'\n[ \t]*\[data-ff-close-onboard\]\s*\{[^{}]*\}\n', '\n', "standalone [data-ff-close-onboard] block"),
    (r'\n[ \t]*\[data-ff-onboard-status\]\s*\{[^{}]*\}\n', '\n', "standalone [data-ff-onboard-status] block"),
    (r'\n[ \t]*\[data-ff-onboard-result\]\s*\{[^{}]*\}\n', '\n', "standalone [data-ff-onboard-result] block"),
    (r'\n[ \t]*\.ff-onboardModal__footer\s*\{[^{}]*\}\n', '\n', "standalone .ff-onboardModal__footer block"),
    (r'\n[ \t]*\.ff-onboardModal__footer\s*>\s*\*\s*\{[^{}]*\}\n', '\n', "standalone .ff-onboardModal__footer > * block"),
]

for pattern, repl, label in standalone_patterns:
    ff_new, count = re.subn(pattern, repl, ff, flags=re.S)
    if count:
        ff = ff_new
        applied.append(f"{label} x{count}")

# 3) remove exact leftover shim bridge block regardless of spacing
shim_new, count = re.subn(
    r'\n?[ \t]*#ff-onboarding,\s*\n[ \t]*#ffOnboardPanel2,\s*\n[ \t]*\[data-ff-open-onboarding\]\s*\{\s*\n[ \t]*--ff-legacy-bridge:\s*1;\s*\n[ \t]*\}\s*\n?',
    '\n',
    shim,
    flags=re.S,
)
if count:
    shim = shim_new
    applied.append(f"remove shim legacy bridge block x{count}")

# 4) normalize blank lines
ff = re.sub(r'\n{3,}', '\n\n', ff)
shim = re.sub(r'\n{3,}', '\n\n', shim)

# 5) lint-friendly empty line before comments
ff = re.sub(r'([^\n])\n(/\*[-=]{2,})', r'\1\n\n\2', ff)

FF.write_text(ff, encoding="utf-8")
SHIM.write_text(shim, encoding="utf-8")

print("== FF CSS PRUNE ONBOARDING RESIDUE V2 ==")
print("applied:")
if applied:
    for item in applied:
        print(f" - {item}")
else:
    print(" - no changes matched")
print("done.")
