from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.home() / "futurefunded-enterprise"

ROUTES = ROOT / "apps/web/app/routes/platform.py"
ONBOARDING = ROOT / "apps/web/app/templates/platform/pages/onboarding.html"
DASHBOARD = ROOT / "apps/web/app/templates/platform/pages/dashboard.html"

FILES = [ROUTES, ONBOARDING, DASHBOARD]

for path in FILES:
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
for path in FILES:
    shutil.copy2(path, path.with_name(f"{path.name}.{timestamp}.bak"))

def apply_literal(text: str, old: str, new: str, notes: list[str], label: str) -> str:
    if old in text:
        text = text.replace(old, new, 1)
        notes.append(f"changed: {label}")
    else:
        notes.append(f"MISS: {label}")
    return text

def apply_regex(text: str, pattern: str, repl: str, notes: list[str], label: str, flags: int = re.S) -> str:
    updated, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count:
        notes.append(f"changed: {label}")
        return updated
    notes.append(f"MISS: {label}")
    return text

# ---------------------------------------------------------------------
# routes/platform.py
# ---------------------------------------------------------------------
routes_text = ROUTES.read_text(encoding="utf-8")
routes_notes: list[str] = []

routes_text = apply_literal(
    routes_text,
    '"page_description": ( "Set up your program, campaign, and brand defaults for a premium FutureFunded launch." ),',
    '"page_description": ( "Set up your organization, public fundraiser, and brand defaults for a premium FutureFunded launch." ),',
    routes_notes,
    "routes onboarding page_description",
)

routes_text = apply_literal(
    routes_text,
    '"body": ( "Set up the real Connect ATX Elite program and Spring Fundraiser defaults, " "then hand off directly into the operating dashboard." ),',
    '"body": ( "Create the organization, configure the first public fundraiser, " "and hand off directly into the operator dashboard." ),',
    routes_notes,
    "routes onboarding body",
)

routes_text = apply_literal(
    routes_text,
    '"page_description": ( "Manage campaigns, sponsor tiers, and memberships from the FutureFunded command center." ),',
    '"page_description": ( "Manage the live public fundraiser, sponsor packages, and recurring support from one premium operator workspace." ),',
    routes_notes,
    "routes dashboard page_description",
)

routes_text = apply_literal(
    routes_text,
    '"body": ( "Manage the live Connect ATX Elite fundraiser, sponsor packages, and booster support " "from one premium workspace." ),',
    '"body": ( "Manage the live public fundraiser, sponsor packages, and recurring support " "from one premium operator workspace." ),',
    routes_notes,
    "routes dashboard body",
)

ROUTES.write_text(routes_text, encoding="utf-8")

# ---------------------------------------------------------------------
# onboarding.html
# ---------------------------------------------------------------------
onboarding_text = ONBOARDING.read_text(encoding="utf-8")
onboarding_notes: list[str] = []

onboarding_text = apply_regex(
    onboarding_text,
    r'\{% set page_description = .*? %\}',
    '{% set page_description = "Create your first organization and public fundraiser, then hand off directly into the operator dashboard." %}',
    onboarding_notes,
    "onboarding page_description",
)

onboarding_text = apply_regex(
    onboarding_text,
    r'\{% set body = data\.get\("body", .*?%\}',
    '{% set body = data.get("body", "Create your first organization and public fundraiser against the real API, then hand off directly into the operator dashboard.") %}',
    onboarding_notes,
    "onboarding body",
)

onboarding_text = apply_regex(
    onboarding_text,
    r'<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformOnboardingBriefTitle">.*?</h2>',
    '<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformOnboardingBriefTitle">Start with one org. Publish one live fundraiser.</h2>',
    onboarding_notes,
    "onboarding brief title",
)

onboarding_text = apply_regex(
    onboarding_text,
    r'<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformLaunchOutcomeTitle">.*?</h2>',
    '<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformLaunchOutcomeTitle">Create once. Go live fast.</h2>',
    onboarding_notes,
    "onboarding launch outcome title",
)

onboarding_text = apply_regex(
    onboarding_text,
    r'<p class="ff-help ff-muted ff-mt-2 ff-mb-0">The same org can later.*?</p>',
    '<p class="ff-help ff-muted ff-mt-2 ff-mb-0">The same org can later add recurring support and a fuller platform hub.</p>',
    onboarding_notes,
    "onboarding recurring support help",
)

ONBOARDING.write_text(onboarding_text, encoding="utf-8")

# ---------------------------------------------------------------------
# dashboard.html
# ---------------------------------------------------------------------
dashboard_text = DASHBOARD.read_text(encoding="utf-8")
dashboard_notes: list[str] = []

dashboard_text = apply_regex(
    dashboard_text,
    r'\{% set page_description = .*? %\}',
    '{% set page_description = "Manage the live public fundraiser, sponsor packages, and recurring support from one premium operator workspace." %}',
    dashboard_notes,
    "dashboard page_description",
)

dashboard_text = apply_regex(
    dashboard_text,
    r'\{% set body = data\.get\("body", .*?%\}',
    '{% set body = data.get("body", "Manage the live public fundraiser, sponsor packages, and recurring support from one premium operator workspace.") %}',
    dashboard_notes,
    "dashboard body",
)

dashboard_text = apply_literal(
    dashboard_text,
    '{"title": "Membership plans", "body": "Recurring support plans configured", "value": "2"}',
    '{"title": "Recurring support", "body": "Recurring support plans configured", "value": "2"}',
    dashboard_notes,
    "dashboard overview recurring support title",
)

dashboard_text = apply_literal(
    dashboard_text,
    '{"title": "Sponsor tiers", "body": "Active support packages for local partners", "value": "2"}',
    '{"title": "Sponsor packages", "body": "Active support packages for local partners", "value": "2"}',
    dashboard_notes,
    "dashboard overview sponsor packages title",
)

dashboard_text = apply_regex(
    dashboard_text,
    r'actions\[1\]\.get\("label",\s*"[^"]+"\)\s*if actions\|length > 1 else\s*"[^"]+"',
    'actions[1].get("label", "Start another guided launch") if actions|length > 1 else "Start another guided launch"',
    dashboard_notes,
    "dashboard secondary action fallback",
)

dashboard_text = apply_literal(
    dashboard_text,
    '>Open live page</a>',
    '>Open live fundraiser</a>',
    dashboard_notes,
    "dashboard open live fundraiser anchor",
)

dashboard_text = apply_regex(
    dashboard_text,
    r'<p class="ff-help ff-muted ff-mt-2 ff-mb-0">\s*The current workspace is already structured.*?</p>',
    '<p class="ff-help ff-muted ff-mt-2 ff-mb-0">\n          The current workspace is already structured for direct giving, sponsor packages, and recurring support expansion.\n        </p>',
    dashboard_notes,
    "dashboard workspace help copy",
)

dashboard_text = apply_regex(
    dashboard_text,
    r'<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformSponsorTierTitle">.*?</h2>',
    '<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformSponsorTierTitle">Sponsor packages</h2>',
    dashboard_notes,
    "dashboard sponsor packages title",
)

dashboard_text = apply_regex(
    dashboard_text,
    r'<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformMembershipTitle">.*?</h2>',
    '<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformMembershipTitle">Recurring support</h2>',
    dashboard_notes,
    "dashboard recurring support title",
)

DASHBOARD.write_text(dashboard_text, encoding="utf-8")

print("== FF PLATFORM OPERATOR POLISH V2 ==")
for path, notes in [
    (ROUTES, routes_notes),
    (ONBOARDING, onboarding_notes),
    (DASHBOARD, dashboard_notes),
]:
    print(f"patched: {path}")
    for note in notes:
        print(f"  - {note}")

print("done.")
