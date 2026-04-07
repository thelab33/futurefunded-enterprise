from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
SPEC = ROOT / "tests/e2e/fundraiser-smoke.spec.ts"

if not SPEC.exists():
    raise SystemExit(f"Missing spec file: {SPEC}")

# Restore from latest backup first
backups = sorted(SPEC.parent.glob("fundraiser-smoke.spec.ts.*.bak"), key=lambda p: p.stat().st_mtime, reverse=True)
if not backups:
    raise SystemExit("No fundraiser-smoke.spec.ts backup files found.")

restore_src = backups[0]
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
pre_restore = SPEC.with_name(f"{SPEC.name}.pre-restore.{timestamp}.bak")
shutil.copy2(SPEC, pre_restore)
shutil.copy2(restore_src, SPEC)

src = SPEC.read_text(encoding="utf-8")
updated = src
applied: list[str] = []

def subn_all(pattern: str, repl: str, label: str, flags: int = 0) -> None:
    global updated
    new_text, count = re.subn(pattern, repl, updated, flags=flags)
    if count:
        updated = new_text
        applied.append(f"{label} x{count}")

# ------------------------------------------------------------------
# 1) Rename outdated test title
# ------------------------------------------------------------------
updated = updated.replace(
    "sponsor, legal, video, and onboarding modals all open and close",
    "sponsor, legal, and video modals all open and close",
)

# ------------------------------------------------------------------
# 2) Remove onboarding selectors from SEL map
# ------------------------------------------------------------------
subn_all(r'^\s*openOnboard:\s*.*\n', '', "SEL.openOnboard removal", flags=re.M)
subn_all(r'^\s*closeOnboard:\s*.*\n', '', "SEL.closeOnboard removal", flags=re.M)
subn_all(r'^\s*onboardModal:\s*.*\n', '', "SEL.onboardModal removal", flags=re.M)

# ------------------------------------------------------------------
# 3) Remove full onboarding-specific conditional blocks safely
# ------------------------------------------------------------------
subn_all(
    r'\n\s*if\s*\(\s*await\s+firstVisible\(page,\s*SEL\.openOnboard\)\s*\)\s*\{.*?\n\s*\}\n',
    '\n',
    "firstVisible(openOnboard) block",
    flags=re.S,
)

# ------------------------------------------------------------------
# 4) Remove standalone onboarding modal statements
# ------------------------------------------------------------------
subn_all(r'^\s*.*openAndExpectVisible\(.*SEL\.openOnboard.*SEL\.onboardModal.*\);\s*\n', '', "open onboarding modal statement", flags=re.M)
subn_all(r'^\s*.*closeIfPresent\(.*SEL\.closeOnboard.*SEL\.onboardModal.*\);\s*\n', '', "close onboarding modal statement", flags=re.M)
subn_all(r'^\s*.*SEL\.onboardModal.*\n', '', "remaining SEL.onboardModal lines", flags=re.M)
subn_all(r'^\s*.*SEL\.openOnboard.*\n', '', "remaining SEL.openOnboard lines", flags=re.M)
subn_all(r'^\s*.*SEL\.closeOnboard.*\n', '', "remaining SEL.closeOnboard lines", flags=re.M)

# ------------------------------------------------------------------
# 5) Cleanup common punctuation / whitespace drift
# ------------------------------------------------------------------
updated = re.sub(r',\s*,', ',', updated)
updated = re.sub(r'\[\s*,', '[', updated)
updated = re.sub(r'\{\s*,', '{', updated)
updated = re.sub(r',\s*([\]\}])', r'\1', updated)
updated = re.sub(r'\n{3,}', '\n\n', updated)

SPEC.write_text(updated, encoding="utf-8")

print("== FF PLAYWRIGHT SPEC ONBOARDING REPAIR V1 ==")
print(f"restored from: {restore_src}")
print(f"pre-restore backup: {pre_restore}")
print("applied:")
for item in applied:
    print(f" - {item}")
print("done.")
