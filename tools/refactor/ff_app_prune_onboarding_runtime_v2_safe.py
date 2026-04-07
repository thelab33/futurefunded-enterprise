from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
JS = ROOT / "apps/web/app/static/js/ff-app.js"

if not JS.exists():
    raise SystemExit(f"Missing JS file: {JS}")

# ------------------------------------------------------------------
# Restore from latest backup first
# ------------------------------------------------------------------
backups = sorted(JS.parent.glob("ff-app.js.*.bak"), key=lambda p: p.stat().st_mtime, reverse=True)
if not backups:
    raise SystemExit("No ff-app.js backup files found. Aborting safe restore.")
restore_src = backups[0]

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
pre_restore_copy = JS.with_name(f"{JS.name}.pre-restore.{timestamp}.bak")
shutil.copy2(JS, pre_restore_copy)
shutil.copy2(restore_src, JS)

src = JS.read_text(encoding="utf-8")
updated = src
applied: list[str] = []

def replace_once_literal(old: str, new: str, label: str) -> None:
    global updated
    if old in updated:
        updated = updated.replace(old, new, 1)
        applied.append(label)

def replace_once_regex(pattern: str, repl: str, label: str, flags: int = 0) -> None:
    global updated
    new_text, count = re.subn(pattern, repl, updated, count=1, flags=flags)
    if count:
        updated = new_text
        applied.append(label)

# ------------------------------------------------------------------
# 1) Strip onboarding keys from defaultHooks
# ------------------------------------------------------------------
replace_once_regex(
    r''',\s*openOnboard:\s*"\[data-ff-open-onboard\]"\s*,\s*closeOnboard:\s*"\[data-ff-close-onboard\]"\s*,\s*onboardModal:\s*"\[data-ff-onboard-modal\]"\s*,\s*onboardForm:\s*"\[data-ff-onboard-form\]"\s*,\s*onboardNext:\s*"\[data-ff-onboard-next\]"\s*,\s*onboardPrev:\s*"\[data-ff-onboard-prev\]"\s*,\s*onboardFinish:\s*"\[data-ff-onboard-finish\]"\s*,\s*onboardCopy:\s*"\[data-ff-onboard-copy\]"\s*,\s*onboardEmail:\s*"\[data-ff-onboard-email\]"\s*,\s*onboardSummary:\s*"\[data-ff-onboard-summary\]"\s*,\s*onboardStatus:\s*"\[data-ff-onboard-status\]"\s*,\s*onboardResult:\s*"\[data-ff-onboard-result\]"\s*,\s*stepPill:\s*"\[data-ff-step-pill\]"\s*,\s*stepPanel:\s*"\[data-ff-step\]"''',
    "",
    "defaultHooks onboarding keys",
    flags=re.S,
)

# ------------------------------------------------------------------
# 2) Strip onboard overlay registration
# ------------------------------------------------------------------
replace_once_regex(
    r''',\s*onboard:\s*\{\s*key:\s*"onboard"\s*,\s*container:\s*q\(hooks\.onboardModal\)\s*,\s*panel:\s*q\("\[data-ff-onboard-panel\]"\)\s*\|\|\s*q\("\.ff-modal__panel,\s*\.ff-sheet__panel",\s*q\(hooks\.onboardModal\)\)\s*,\s*openers:\s*hooks\.openOnboard\s*,\s*closers:\s*hooks\.closeOnboard\s*\}''',
    "",
    "overlay onboard registration",
    flags=re.S,
)

# ------------------------------------------------------------------
# 3) Remove onboardEls object
# ------------------------------------------------------------------
replace_once_regex(
    r'''var onboardEls = \{.*?\}; var uiEls = \{''',
    'var uiEls = {',
    "onboardEls object",
    flags=re.S,
)

# ------------------------------------------------------------------
# 4) Remove onboarding function cluster
# Safe anchor: from currentOnboardStep to initVideoOpen
# ------------------------------------------------------------------
replace_once_regex(
    r'''var currentOnboardStep = 1;.*?(?=function initVideoOpen\()''',
    '',
    "onboarding function cluster",
    flags=re.S,
)

# ------------------------------------------------------------------
# 5) Remove hash-based ff-onboarding opener
# ------------------------------------------------------------------
replace_once_literal(
    ' else if (hash === "ff-onboarding") { openOverlay("onboard"); updateOnboardStep(1); }',
    '',
    "hash onboard opener",
)

# ------------------------------------------------------------------
# 6) Remove onboarding click handlers
# ------------------------------------------------------------------
replace_once_literal(
    ' var openOnboard = target.closest(hooks.openOnboard || ""); if (openOnboard) { event.preventDefault(); openOverlay("onboard", openOnboard); updateOnboardStep(1); return; }',
    '',
    "click openOnboard handler",
)

replace_once_literal(
    ' var closeOnboard = target.closest(hooks.closeOnboard || ""); if (closeOnboard) { event.preventDefault(); closeOverlay("onboard"); return; }',
    '',
    "click closeOnboard handler",
)

replace_once_literal(
    ' var stepPill = target.closest(hooks.stepPill || ""); if (stepPill) { event.preventDefault(); updateOnboardStep(stepPill.getAttribute("data-ff-step-pill") || "1"); return; }',
    '',
    "click stepPill handler",
)

# ------------------------------------------------------------------
# 7) Remove contiguous onboarding init listener block
# Safe anchor: from if (onboardEls.form) ... through if (onboardEls.email) ...
# and rejoin directly into if (uiEls.backToTop)
# ------------------------------------------------------------------
replace_once_regex(
    r'''\s*if \(onboardEls\.form\) \{.*?\}\s*if \(uiEls\.backToTop\) \{''',
    ' if (uiEls.backToTop) {',
    "onboarding init listener block",
    flags=re.S,
)

# ------------------------------------------------------------------
# 8) Remove final init calls
# ------------------------------------------------------------------
replace_once_literal(
    ' populateSponsorWall(); updateOnboardSwatches(); updateOnboardStep(1); hydrateSuccessFromUrl();',
    ' populateSponsorWall(); hydrateSuccessFromUrl();',
    "final onboarding init calls",
)

# ------------------------------------------------------------------
# 9) Small cleanup only (do NOT aggressively minify or rebalance)
# ------------------------------------------------------------------
updated = re.sub(r';\s*;', ';', updated)
updated = re.sub(r'\s+\)', ')', updated)
updated = re.sub(r'\(\s+', '(', updated)

if updated == src:
    raise SystemExit("No changes applied after restore; onboarding prune patterns may have drifted.")

JS.write_text(updated, encoding="utf-8")

print("== FF APP PRUNE ONBOARDING RUNTIME V2 SAFE ==")
print(f"restored from: {restore_src}")
print(f"pre-restore backup: {pre_restore_copy}")
print("applied:")
for item in applied:
    print(f" - {item}")
print("done.")
