from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
FF = ROOT / "apps/web/app/static/css/ff.css"
SHIM = ROOT / "apps/web/app/static/css/ff-above-main-premium.css"
PLATFORM = ROOT / "apps/web/app/static/css/platform-pages.css"

for p in (FF, SHIM, PLATFORM):
    if not p.exists():
        raise SystemExit(f"Missing CSS file: {p}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

for p in (FF, SHIM):
    shutil.copy2(p, p.with_name(f"{p.name}.{timestamp}.bak"))

src = FF.read_text(encoding="utf-8")
updated = src
applied: list[str] = []

def replace_once(old: str, new: str, label: str) -> None:
    global updated
    if old in updated:
        updated = updated.replace(old, new, 1)
        applied.append(label)

def subn_all(pattern: str, repl: str, label: str, flags: int = 0) -> None:
    global updated
    new_text, count = re.subn(pattern, repl, updated, flags=flags)
    if count:
        updated = new_text
        applied.append(f"{label} x{count}")

# ------------------------------------------------------------------
# Exact selector-list repairs (safer than line deletion)
# ------------------------------------------------------------------
replace_once(
    """
.ff-faqEndcap__header, .ff-footerBrand, .ff-footerMeta, .ff-checkoutBody, .ff-onboardModal__body, .ff-onboardSummary {
""",
    """
.ff-faqEndcap__header, .ff-footerBrand, .ff-footerMeta, .ff-checkoutBody {
""",
    "shared grid selector cleanup",
)

replace_once(
    """
.ff-sponsorModal__head, .ff-videoModal__head, .ff-termsModal__head, .ff-privacyModal__head, .ff-onboardModal__head {
""",
    """
.ff-sponsorModal__head, .ff-videoModal__head, .ff-termsModal__head, .ff-privacyModal__head {
""",
    "modal head selector cleanup",
)

replace_once(
    """
.ff-sponsorModal__actions, .ff-onboardModal__actions, .ff-faqEndcap__actions, .ff-faqEndcap__links {
""",
    """
.ff-sponsorModal__actions, .ff-faqEndcap__actions, .ff-faqEndcap__links {
""",
    "shared actions selector cleanup",
)

replace_once(
    """
[data-ff-sponsor-modal], [data-ff-video-modal], [data-ff-terms-modal], [data-ff-privacy-modal], [data-ff-onboard-modal] {
""",
    """
[data-ff-sponsor-modal], [data-ff-video-modal], [data-ff-terms-modal], [data-ff-privacy-modal] {
""",
    "modal isolation selector cleanup",
)

replace_once(
    """
[data-ff-close-video], [data-ff-close-terms], [data-ff-close-privacy], [data-ff-close-sponsor], [data-ff-close-onboard] {
""",
    """
[data-ff-close-video], [data-ff-close-terms], [data-ff-close-privacy], [data-ff-close-sponsor] {
""",
    "close trigger selector cleanup",
)

replace_once(
    """
[data-ff-checkout-error], [data-ff-sponsor-status], [data-ff-sponsor-error], [data-ff-sponsor-success], [data-ff-onboard-status], [data-ff-onboard-result], [data-ff-video-status] {
""",
    """
[data-ff-checkout-error], [data-ff-sponsor-status], [data-ff-sponsor-error], [data-ff-sponsor-success], [data-ff-video-status] {
""",
    "status selector cleanup",
)

replace_once(
    """
#checkout, #press-video, #terms, #privacy, #ff-onboarding { scroll-margin-top: calc(var(--ff-header-offset) + var(--ff-safe-top) + 0.5rem); }
""",
    """
#checkout, #press-video, #terms, #privacy { scroll-margin-top: calc(var(--ff-header-offset) + var(--ff-safe-top) + 0.5rem); }
""",
    "scroll-margin selector cleanup",
)

replace_once(
    """
.ff-checkoutActions, .ff-sponsorModal__actions, .ff-onboardModal__actions {
""",
    """
.ff-checkoutActions, .ff-sponsorModal__actions {
""",
    "mobile actions width selector cleanup",
)

replace_once(
    """
.ff-checkoutActions > *, .ff-sponsorModal__actions > *, .ff-onboardModal__actions > * {
""",
    """
.ff-checkoutActions > *, .ff-sponsorModal__actions > * {
""",
    "mobile actions child selector cleanup",
)

replace_once(
    """
.ff-sponsorModal__footer, .ff-onboardModal__footer {
""",
    """
.ff-sponsorModal__footer {
""",
    "footer selector cleanup",
)

replace_once(
    """
.ff-sponsorModal__footer > *, .ff-onboardModal__footer > * {
""",
    """
.ff-sponsorModal__footer > * {
""",
    "footer child selector cleanup",
)

replace_once(
    """
html.ff-root[data-theme="dark"] .ff-sponsorModal__footer, html.ff-root[data-theme="dark"] .ff-onboardModal__footer {
""",
    """
html.ff-root[data-theme="dark"] .ff-sponsorModal__footer {
""",
    "dark footer selector cleanup",
)

replace_once(
    """
.ff-sponsorModal__footer, .ff-onboardModal__footer {
""",
    """
.ff-sponsorModal__footer {
""",
    "desktop footer selector cleanup",
)

replace_once(
    """
.ff-sponsorModal__footer > *, .ff-onboardModal__footer > * {
""",
    """
.ff-sponsorModal__footer > * {
""",
    "desktop footer child selector cleanup",
)

# ------------------------------------------------------------------
# Remove standalone onboarding-only blocks
# ------------------------------------------------------------------
subn_all(r'\n\s*\.ff-onboardColor\s*\{[^}]*\}\n', '\n', "ff-onboardColor block", flags=re.S)
subn_all(r'\n\s*body\[data-ff-page="fundraiser"\] \.ff-onboardStepper\s*\{[^}]*\}\n', '\n', "onboardStepper block", flags=re.S)
subn_all(r'\n\s*body\[data-ff-page="fundraiser"\] \.ff-onboardStep\s*\{[^}]*\}\n', '\n', "onboardStep block", flags=re.S)
subn_all(
    r'\n\s*body\[data-ff-page="fundraiser"\] \.ff-onboardStep\[aria-selected="true"\],\s*\n\s*body\[data-ff-page="fundraiser"\] \.ff-onboardStep\[aria-current="step"\]\s*\{[^}]*\}\n',
    '\n',
    "onboardStep active block",
    flags=re.S,
)
subn_all(r'\n\s*body\[data-ff-page="fundraiser"\] \.ff-onboardPanel\s*\{[^}]*\}\n', '\n', "onboardPanel block", flags=re.S)
subn_all(r'\n\s*body\[data-ff-page="fundraiser"\] \.ff-onboardSummary\s*\{[^}]*\}\n', '\n', "onboardSummary block", flags=re.S)
subn_all(r'\n\s*html\.ff-root\[data-theme="dark"\] body\[data-ff-page="fundraiser"\] \.ff-onboardSummary\s*\{[^}]*\}\n', '\n', "dark onboardSummary block", flags=re.S)
subn_all(r'\n\s*\.ff-onboardForm,\s*\n\s*\[data-ff-onboard-form\]\s*\{[^}]*\}\n', '\n', "onboard form block", flags=re.S)
subn_all(r'\n\s*\[data-ff-step\],\s*\n\s*\.ff-onboardPanel\s*\{[^}]*\}\n', '\n', "step/onboardPanel block", flags=re.S)
subn_all(r'\n\s*\[data-ff-step-pill\],\s*\n\s*\.ff-onboardStep\s*\{[^}]*\}\n', '\n', "step pill/onboardStep block", flags=re.S)
subn_all(r'\n\s*@media \(min-width: 48rem\) \{\s*\n\s*\.ff-onboardStepper\s*\{[^}]*\}\s*\n', '\n@media (min-width: 48rem) {\n', "media onboardStepper block", flags=re.S)

# ------------------------------------------------------------------
# Remove onboarding-only lines safely inside larger selector groups
# ------------------------------------------------------------------
subn_all(r'^\s*#ff-onboarding,\n', '', "#ff-onboarding line", flags=re.M)
subn_all(r'^\s*\[data-ff-open-onboard\],\n', '', "open onboard selector line", flags=re.M)
subn_all(r'^\s*\[data-ff-onboard-copy\],\n', '', "onboard copy selector line", flags=re.M)
subn_all(r'^\s*\[data-ff-onboard-email\],\n', '', "onboard email selector line", flags=re.M)
subn_all(r'^\s*\[data-ff-onboard-email-target\],\n', '', "onboard email target selector line", flags=re.M)
subn_all(r'^\s*\[data-ff-onboard-endpoint\],\n', '', "onboard endpoint selector line", flags=re.M)
subn_all(r'^\s*\[data-ff-onboard-finish\],\n', '', "onboard finish selector line", flags=re.M)
subn_all(r'^\s*\[data-ff-onboard-next\],\n', '', "onboard next selector line", flags=re.M)
subn_all(r'^\s*\[data-ff-onboard-prev\],\n', '', "onboard prev selector line", flags=re.M)
subn_all(r'^\s*\[data-ff-onboard-summary\],\n', '', "onboard summary selector line", flags=re.M)
subn_all(r'^\s*\.ff-onboardModal__footer,\n', '', "onboard footer selector line", flags=re.M)
subn_all(r'^\s*\.ff-onboardModal__footer > \*,\n', '', "onboard footer child selector line", flags=re.M)

# ------------------------------------------------------------------
# Light cleanup
# ------------------------------------------------------------------
updated = re.sub(r'\n{3,}', '\n\n', updated)
FF.write_text(updated, encoding="utf-8")

# ------------------------------------------------------------------
# Prune shim legacy bridge entirely
# ------------------------------------------------------------------
shim_src = SHIM.read_text(encoding="utf-8")
shim_updated = re.sub(
    r'\n#ff-onboarding,\n#ffOnboardPanel2,\n\[data-ff-open-onboarding\] \{\n --ff-legacy-bridge: 1;\n\}\n?',
    '\n',
    shim_src,
    flags=re.S,
)
shim_updated = re.sub(r'\n{3,}', '\n\n', shim_updated)
SHIM.write_text(shim_updated, encoding="utf-8")

print("== FF CSS PRUNE ONBOARDING RESIDUE V1 ==")
print("applied:")
for item in applied:
    print(f" - {item}")
print("done.")
