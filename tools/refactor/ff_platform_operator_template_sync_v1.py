from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"

ONBOARDING = ROOT / "apps/web/app/templates/platform/pages/onboarding.html"
DASHBOARD = ROOT / "apps/web/app/templates/platform/pages/dashboard.html"

TARGETS = [ONBOARDING, DASHBOARD]

for path in TARGETS:
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
for path in TARGETS:
    shutil.copy2(path, path.with_name(f"{path.name}.{timestamp}.bak"))

def patch_once(text: str, old: str, new: str, notes: list[str], label: str) -> str:
    if old in text:
        text = text.replace(old, new, 1)
        notes.append(f"changed: {label}")
    else:
        notes.append(f"MISS: {label}")
    return text

# ------------------------------------------------------------------
# onboarding
# ------------------------------------------------------------------
onboarding_text = ONBOARDING.read_text(encoding="utf-8")
onboarding_notes: list[str] = []

onboarding_text = patch_once(
    onboarding_text,
    '{% set title = data.get("title", "Onboarding") %}',
    '{% set title = data.get("title", "Set up your first live fundraiser.") %}',
    onboarding_notes,
    "onboarding title default",
)

onboarding_text = patch_once(
    onboarding_text,
    'One branded organization. One live campaign. One clean handoff.',
    'One branded organization. One live fundraiser. One clean handoff.',
    onboarding_notes,
    "onboarding promise title",
)

onboarding_text = patch_once(
    onboarding_text,
    '{{ campaign.get("title", "Campaign") }}',
    '{{ campaign.get("title", "Public fundraiser") }}',
    onboarding_notes,
    "onboarding campaign title fallback",
)

onboarding_text = patch_once(
    onboarding_text,
    '{% set body = data.get("body", "Create your first organization and campaign against the real API, then hand off directly into your operational dashboard.") %}',
    '{% set body = data.get("body", "Create your first organization and public fundraiser against the real API, then hand off directly into the operator dashboard.") %}',
    onboarding_notes,
    "onboarding body default",
)

onboarding_text = patch_once(
    onboarding_text,
    'Set the live campaign headline, URL slug, and launch goal.',
    'Set the live public fundraiser headline, URL slug, and launch goal.',
    onboarding_notes,
    "onboarding campaign helper copy",
)

ONBOARDING.write_text(onboarding_text, encoding="utf-8")

# ------------------------------------------------------------------
# dashboard
# ------------------------------------------------------------------
dashboard_text = DASHBOARD.read_text(encoding="utf-8")
dashboard_notes: list[str] = []

dashboard_text = patch_once(
    dashboard_text,
    '{% set title = data.get("title", "FutureFunded command center") %}',
    '{% set title = data.get("title", "Operator command center") %}',
    dashboard_notes,
    "dashboard title default",
)

dashboard_text = patch_once(
    dashboard_text,
    '{"title": "Campaigns", "body": "Live fundraising campaigns you can manage", "value": "1"},',
    '{"title": "Live fundraisers", "body": "Public fundraisers you can manage", "value": "1"},',
    dashboard_notes,
    "dashboard overview campaigns card",
)

dashboard_text = patch_once(
    dashboard_text,
    '{"label": "Create another org", "href": "/platform/onboarding", "variant": "secondary"}',
    '{"label": "Start another guided launch", "href": "/platform/onboarding", "variant": "secondary"}',
    dashboard_notes,
    "dashboard secondary action object",
)

dashboard_text = patch_once(
    dashboard_text,
    '{% set secondary_action = actions[1] if actions|length > 1 else {"label": "Create another org", "href": "/platform/onboarding"} %}',
    '{% set secondary_action = actions[1] if actions|length > 1 else {"label": "Start another guided launch", "href": "/platform/onboarding"} %}',
    dashboard_notes,
    "dashboard secondary action fallback",
)

dashboard_text = patch_once(
    dashboard_text,
    '>Create another org</a>',
    '>Start another guided launch</a>',
    dashboard_notes,
    "dashboard create another org anchor",
)

dashboard_text = patch_once(
    dashboard_text,
    '>Launch another org</a>',
    '>Start another guided launch</a>',
    dashboard_notes,
    "dashboard launch another org anchor",
)

dashboard_text = patch_once(
    dashboard_text,
    'Live fundraising campaigns you can manage',
    'Public fundraisers you can manage',
    dashboard_notes,
    "dashboard campaign copy",
)

DASHBOARD.write_text(dashboard_text, encoding="utf-8")

print("== FF PLATFORM OPERATOR TEMPLATE SYNC V1 ==")
for path, notes in [
    (ONBOARDING, onboarding_notes),
    (DASHBOARD, dashboard_notes),
]:
    print(f"patched: {path}")
    for note in notes:
        print(f"  - {note}")

print("done.")
