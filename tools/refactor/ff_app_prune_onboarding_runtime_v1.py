from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
JS = ROOT / "apps/web/app/static/js/ff-app.js"

if not JS.exists():
    raise SystemExit(f"Missing JS file: {JS}")

src = JS.read_text(encoding="utf-8")
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = JS.with_name(f"{JS.name}.{timestamp}.bak")
shutil.copy2(JS, backup)

updated = src
applied: list[str] = []

def subn(pattern: str, repl: str, label: str, flags: int = 0) -> None:
    global updated
    new_text, count = re.subn(pattern, repl, updated, count=1, flags=flags)
    if count:
        updated = new_text
        applied.append(label)

def subn_all(pattern: str, repl: str, label: str, flags: int = 0) -> None:
    global updated
    new_text, count = re.subn(pattern, repl, updated, flags=flags)
    if count:
        updated = new_text
        applied.append(f"{label} x{count}")

# ------------------------------------------------------------------
# 1) Remove onboarding hook defaults from defaultHooks
# ------------------------------------------------------------------
subn(
    r''',\s*openOnboard:\s*"\[data-ff-open-onboard\]"\s*,\s*closeOnboard:\s*"\[data-ff-close-onboard\]"\s*,\s*onboardModal:\s*"\[data-ff-onboard-modal\]"\s*,\s*onboardForm:\s*"\[data-ff-onboard-form\]"\s*,\s*onboardNext:\s*"\[data-ff-onboard-next\]"\s*,\s*onboardPrev:\s*"\[data-ff-onboard-prev\]"\s*,\s*onboardFinish:\s*"\[data-ff-onboard-finish\]"\s*,\s*onboardCopy:\s*"\[data-ff-onboard-copy\]"\s*,\s*onboardEmail:\s*"\[data-ff-onboard-email\]"\s*,\s*onboardSummary:\s*"\[data-ff-onboard-summary\]"\s*,\s*onboardStatus:\s*"\[data-ff-onboard-status\]"\s*,\s*onboardResult:\s*"\[data-ff-onboard-result\]"\s*,\s*stepPill:\s*"\[data-ff-step-pill\]"\s*,\s*stepPanel:\s*"\[data-ff-step\]"''',
    "",
    "defaultHooks onboarding keys",
    flags=re.S,
)

# ------------------------------------------------------------------
# 2) Remove onboard overlay registration
# ------------------------------------------------------------------
subn(
    r''',\s*onboard:\s*\{\s*key:\s*"onboard"\s*,\s*container:\s*q\(hooks\.onboardModal\)\s*,\s*panel:\s*q\("\[data-ff-onboard-panel\]"\)\s*\|\|\s*q\("\.ff-modal__panel,\s*\.ff-sheet__panel",\s*q\(hooks\.onboardModal\)\)\s*,\s*openers:\s*hooks\.openOnboard\s*,\s*closers:\s*hooks\.closeOnboard\s*\}''',
    "",
    "overlay onboard registration",
    flags=re.S,
)

# ------------------------------------------------------------------
# 3) Remove onboardEls object
# ------------------------------------------------------------------
subn(
    r'''var onboardEls = \{.*?\}; var uiEls = \{''',
    'var uiEls = {',
    "onboardEls object",
    flags=re.S,
)

# ------------------------------------------------------------------
# 4) Remove onboarding function cluster
# ------------------------------------------------------------------
subn(
    r'''var currentOnboardStep = 1;.*?(?=function initVideoOpen\()''',
    '',
    "onboarding function cluster",
    flags=re.S,
)

# ------------------------------------------------------------------
# 5) Remove ff-onboarding hash opener
# ------------------------------------------------------------------
subn(
    r'''\s*else if \(hash === "ff-onboarding"\) \{ openOverlay\("onboard"\); updateOnboardStep\(1\); \}''',
    '',
    "hash onboard opener",
    flags=re.S,
)

# ------------------------------------------------------------------
# 6) Remove onboarding click handlers
# ------------------------------------------------------------------
subn(
    r'''\s*var openOnboard = target\.closest\(hooks\.openOnboard \|\| ""\); if \(openOnboard\) \{ event\.preventDefault\(\); openOverlay\("onboard", openOnboard\); updateOnboardStep\(1\); return; \}''',
    '',
    "click openOnboard handler",
    flags=re.S,
)

subn(
    r'''\s*var closeOnboard = target\.closest\(hooks\.closeOnboard \|\| ""\); if \(closeOnboard\) \{ event\.preventDefault\(\); closeOverlay\("onboard"\); return; \}''',
    '',
    "click closeOnboard handler",
    flags=re.S,
)

subn(
    r'''\s*var stepPill = target\.closest\(hooks\.stepPill \|\| ""\); if \(stepPill\) \{ event\.preventDefault\(\); updateOnboardStep\(stepPill\.getAttribute\("data-ff-step-pill"\) \|\| "1"\); return; \}''',
    '',
    "click stepPill handler",
    flags=re.S,
)

# ------------------------------------------------------------------
# 7) Remove onboarding init listeners
# ------------------------------------------------------------------
subn(
    r'''\s*if \(onboardEls\.form\) \{.*?\}''',
    '',
    "onboard form listeners",
    flags=re.S,
)

subn(
    r'''\s*if \(onboardEls\.prev\) \{.*?\}''',
    '',
    "onboard prev listener",
    flags=re.S,
)

subn(
    r'''\s*if \(onboardEls\.next\) \{.*?\}''',
    '',
    "onboard next listener",
    flags=re.S,
)

subn(
    r'''\s*if \(onboardEls\.finish\) \{.*?\}''',
    '',
    "onboard finish listener",
    flags=re.S,
)

subn(
    r'''\s*if \(onboardEls\.copy\) \{.*?\}''',
    '',
    "onboard copy listener",
    flags=re.S,
)

subn(
    r'''\s*if \(onboardEls\.email\) \{.*?\}''',
    '',
    "onboard email listener",
    flags=re.S,
)

# ------------------------------------------------------------------
# 8) Remove leftover init calls
# ------------------------------------------------------------------
subn_all(r'''\s*updateOnboardSwatches\(\);''', '', "updateOnboardSwatches init call")
subn_all(r'''\s*updateOnboardStep\(1\);''', '', "updateOnboardStep init call")

# ------------------------------------------------------------------
# 9) Light cleanup
# ------------------------------------------------------------------
updated = re.sub(r'\s{2,}', ' ', updated)
updated = re.sub(r';\s*;', ';', updated)
updated = re.sub(r'\}\s*\}', '}}', updated)

if updated == src:
    raise SystemExit("No changes applied. The runtime may already be cleaned or patterns drifted.")

JS.write_text(updated, encoding="utf-8")

print("== FF APP PRUNE ONBOARDING RUNTIME V1 ==")
print(f"backup: {backup}")
print("applied:")
for item in applied:
    print(f" - {item}")
print("done.")
