from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
SPEC = ROOT / "tests/e2e/fundraiser-smoke.spec.ts"

if not SPEC.exists():
    raise SystemExit(f"Missing spec file: {SPEC}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = SPEC.with_name(f"{SPEC.name}.{timestamp}.bak")
shutil.copy2(SPEC, backup)

src = SPEC.read_text(encoding="utf-8")
updated = src
applied: list[str] = []

def subn_all(pattern: str, repl: str, label: str, flags: int = 0) -> None:
    global updated
    new_text, count = re.subn(pattern, repl, updated, flags=flags)
    if count:
        updated = new_text
        applied.append(f"{label} x{count}")

# Rename outdated test title
updated = updated.replace(
    "sponsor, legal, video, and onboarding modals all open and close",
    "sponsor, legal, and video modals all open and close",
)

# Remove selector-map entries
subn_all(r'^\s*openOnboard:\s*.*\n', '', "SEL.openOnboard entry", flags=re.M)
subn_all(r'^\s*closeOnboard:\s*.*\n', '', "SEL.closeOnboard entry", flags=re.M)
subn_all(r'^\s*onboardModal:\s*.*\n', '', "SEL.onboardModal entry", flags=re.M)

# Remove contract/assertion lines that explicitly expect onboarding
subn_all(r'^\s*.*data-ff-open-onboard.*\n', '', "data-ff-open-onboard lines", flags=re.M)
subn_all(r'^\s*.*data-ff-onboard-modal.*\n', '', "data-ff-onboard-modal lines", flags=re.M)
subn_all(r'^\s*.*SEL\.openOnboard.*\n', '', "SEL.openOnboard lines", flags=re.M)
subn_all(r'^\s*.*SEL\.closeOnboard.*\n', '', "SEL.closeOnboard lines", flags=re.M)
subn_all(r'^\s*.*SEL\.onboardModal.*\n', '', "SEL.onboardModal lines", flags=re.M)

# Remove guarded onboarding modal block(s)
subn_all(
    r'\n\s*if\s*\(\s*await\s+firstVisible\(page,\s*SEL\.openOnboard\)\s*\)\s*\{.*?\n\s*\}\n',
    '\n',
    "firstVisible(openOnboard) block",
    flags=re.S,
)

# Remove direct open/close onboarding modal statements
subn_all(
    r'^\s*await\s+openAndExpectVisible\(.*onboard.*\);\s*\n',
    '',
    "openAndExpectVisible onboarding calls",
    flags=re.M | re.I,
)
subn_all(
    r'^\s*await\s+closeIfPresent\(.*onboard.*\);\s*\n',
    '',
    "closeIfPresent onboarding calls",
    flags=re.M | re.I,
)

# Cleanup punctuation / whitespace drift
updated = re.sub(r',\s*,', ',', updated)
updated = re.sub(r'\[\s*,', '[', updated)
updated = re.sub(r'\{\s*,', '{', updated)
updated = re.sub(r',\s*([\]\}])', r'\1', updated)
updated = re.sub(r'\n{3,}', '\n\n', updated)

SPEC.write_text(updated, encoding="utf-8")

print("== FF PLAYWRIGHT SPEC RESTORE + PRUNE ONBOARDING V2 ==")
print(f"backup: {backup}")
print("applied:")
for item in applied:
    print(f" - {item}")
print("done.")
