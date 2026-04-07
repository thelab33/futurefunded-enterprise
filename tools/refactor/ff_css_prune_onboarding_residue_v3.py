from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
FF = ROOT / "apps/web/app/static/css/ff.css"

if not FF.exists():
    raise SystemExit(f"Missing CSS file: {FF}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
shutil.copy2(FF, FF.with_name(f"{FF.name}.{timestamp}.bak"))

src = FF.read_text(encoding="utf-8")
updated = src
applied: list[str] = []

def subn(pattern: str, repl: str, label: str, flags: int = 0) -> None:
    global updated
    new_text, count = re.subn(pattern, repl, updated, flags=flags)
    if count:
        updated = new_text
        applied.append(f"{label} x{count}")

# ------------------------------------------------------------------
# Remove remaining grouped-selector residue
# ------------------------------------------------------------------
subn(r',\s*\[data-ff-onboard-status\]', '', "remove [data-ff-onboard-status] from selector groups")
subn(r',\s*\[data-ff-onboard-result\]', '', "remove [data-ff-onboard-result] from selector groups")
subn(r',\s*#ffOnboardPanel2\b', '', "remove #ffOnboardPanel2 from selector groups")
subn(r',\s*html\.ff-root\[data-theme="dark"\]\s*\.ff-onboardModal__footer', '', "remove dark onboard footer from selector groups")

# ------------------------------------------------------------------
# Remove standalone leftover blocks
# ------------------------------------------------------------------
subn(
    r'\n\s*\.ff-onboardStepper\s*\{[^{}]*\}\n',
    '\n',
    "remove standalone .ff-onboardStepper block",
    flags=re.S,
)

subn(
    r'\n\s*html\.ff-root\[data-theme="dark"\]\s*\.ff-onboardModal__footer\s*\{[^{}]*\}\n',
    '\n',
    "remove standalone dark .ff-onboardModal__footer block",
    flags=re.S,
)

# ------------------------------------------------------------------
# Remove any lingering selector lines inside multiline groups
# ------------------------------------------------------------------
subn(r'^\s*\[data-ff-onboard-status\],\n', '', "remove [data-ff-onboard-status] line", flags=re.M)
subn(r'^\s*\[data-ff-onboard-result\],\n', '', "remove [data-ff-onboard-result] line", flags=re.M)
subn(r'^\s*#ffOnboardPanel2,\n', '', "remove #ffOnboardPanel2 line", flags=re.M)

# ------------------------------------------------------------------
# Stylelint friendliness: ensure blank line before block comments
# ------------------------------------------------------------------
updated = re.sub(r'([^\n])\n(/\*)', r'\1\n\n\2', updated)

# Light cleanup
updated = re.sub(r'\n{3,}', '\n\n', updated)

FF.write_text(updated, encoding="utf-8")

print("== FF CSS PRUNE ONBOARDING RESIDUE V3 ==")
print("applied:")
if applied:
    for item in applied:
        print(f" - {item}")
else:
    print(" - no changes matched")
print("done.")
