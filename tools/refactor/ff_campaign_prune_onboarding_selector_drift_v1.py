from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"

if not TEMPLATE.exists():
    raise SystemExit(f"Missing template: {TEMPLATE}")

src = TEMPLATE.read_text(encoding="utf-8")
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = TEMPLATE.with_name(f"{TEMPLATE.name}.{timestamp}.bak")
shutil.copy2(TEMPLATE, backup)

updated = src

# Remove onboarding hook entries from the Jinja selector object block.
jinja_patterns = [
    r"""\n\s*'openOnboard':\s*'\[data-ff-open-onboard\]',""",
    r"""\n\s*'closeOnboard':\s*'\[data-ff-close-onboard\]',""",
    r"""\n\s*'onboardModal':\s*'\[data-ff-onboard-modal\]',""",
    r"""\n\s*'onboardForm':\s*'\[data-ff-onboard-form\]',""",
    r"""\n\s*'onboardNext':\s*'\[data-ff-onboard-next\]',""",
    r"""\n\s*'onboardPrev':\s*'\[data-ff-onboard-prev\]',""",
    r"""\n\s*'onboardFinish':\s*'\[data-ff-onboard-finish\]',""",
    r"""\n\s*'onboardCopy':\s*'\[data-ff-onboard-copy\]',""",
    r"""\n\s*'onboardEmail':\s*'\[data-ff-onboard-email\]',""",
    r"""\n\s*'onboardSummary':\s*'\[data-ff-onboard-summary\]',""",
    r"""\n\s*'onboardStatus':\s*'\[data-ff-onboard-status\]',""",
    r"""\n\s*'onboardResult':\s*'\[data-ff-onboard-result\]',""",
    r"""\n\s*'stepPill':\s*'\[data-ff-step-pill\]',""",
    r"""\n\s*'stepPanel':\s*'\[data-ff-step\]',""",
]

for pat in jinja_patterns:
    updated = re.sub(pat, "", updated)

# Remove onboarding entries from the JSON ffSelectors script block.
json_patterns = [
    r'''\n\s*"openOnboard":\s*"\[data-ff-open-onboard\]",''',
    r'''\n\s*"closeOnboard":\s*"\[data-ff-close-onboard\]",''',
    r'''\n\s*"onboardModal":\s*"\[data-ff-onboard-modal\]",''',
    r'''\n\s*"onboardNext":\s*"\[data-ff-onboard-next\]",''',
    r'''\n\s*"onboardPrev":\s*"\[data-ff-onboard-prev\]",''',
    r'''\n\s*"onboardFinish":\s*"\[data-ff-onboard-finish\]",''',
]

for pat in json_patterns:
    updated = re.sub(pat, "", updated)

# Optional: remove the temporary bridge stub now that the route cutover is done.
updated = re.sub(
    r'''\n<!-- FF_CAMPAIGN_ONBOARDING_ROUTE_BRIDGE_V2 -->\n<section\s+id="ff-onboarding"\s+hidden\s+aria-hidden="true"\s+data-ff-launch-route="/platform/onboarding"\s*></section>\n<!-- /FF_CAMPAIGN_ONBOARDING_ROUTE_BRIDGE_V2 -->\n''',
    "\n",
    updated,
    flags=re.MULTILINE,
)

if updated == src:
    raise SystemExit("No changes applied; file may already be clean")

TEMPLATE.write_text(updated, encoding="utf-8")

print("== FF CAMPAIGN PRUNE ONBOARDING SELECTOR DRIFT V1 ==")
print(f"backup: {backup}")
print("done.")
