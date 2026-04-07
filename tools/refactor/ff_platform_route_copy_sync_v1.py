from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
ROUTES = ROOT / "apps/web/app/routes/platform.py"

if not ROUTES.exists():
    raise SystemExit(f"Missing file: {ROUTES}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
shutil.copy2(ROUTES, ROUTES.with_name(f"{ROUTES.name}.{timestamp}.bak"))

src = ROUTES.read_text(encoding="utf-8")
updated = src
applied: list[str] = []

def replace_once(old: str, new: str, label: str) -> None:
    global updated
    if old in updated:
        updated = updated.replace(old, new, 1)
        applied.append(label)
    else:
        applied.append(f"MISS: {label}")

# ------------------------------------------------------------------
# Home fallback copy sync
# ------------------------------------------------------------------
replace_once(
    '"secondary_cta_label": "View live example",',
    '"secondary_cta_label": "View live fundraiser",',
    "home secondary CTA label",
)

replace_once(
    '"title": "Live fundraiser page",',
    '"title": "Public fundraiser",',
    "home launch card 1 title",
)

replace_once(
    '"title": "Booster memberships",',
    '"title": "Recurring support",',
    "home launch card 3 title",
)

replace_once(
    '"title": "Program hub",',
    '"title": "Operator dashboard",',
    "home launch card 4 title",
)

replace_once(
    '"body": ( "A polished donation surface for Connect ATX Elite with cleaner hierarchy, " "stronger trust, and a fast path to support." ),',
    '"body": ( "A polished public fundraiser for Connect ATX Elite with cleaner hierarchy, " "stronger trust, and a fast path to support." ),',
    "home launch card 1 body",
)

replace_once(
    '"body": ( "Monthly and annual support options that help the program build stability " "beyond one-time campaign pushes." ),',
    '"body": ( "Recurring support options that help the program build stability " "beyond one-time campaign pushes." ),',
    "home launch card 3 body",
)

replace_once(
    '"body": ( "A branded home for the AAU program with colors, campaign story, " "and room to grow into a fuller platform later." ),',
    '"body": ( "An operator dashboard for launch, oversight, and room to grow into a fuller platform later." ),',
    "home launch card 4 body",
)

# ------------------------------------------------------------------
# Onboarding fallback copy sync
# ------------------------------------------------------------------
replace_once(
    '"page_description": ( "Set up your program, campaign, and brand defaults for a premium FutureFunded launch." ),',
    '"page_description": ( "Create your first organization and public fundraiser, then hand off directly into the operator dashboard." ),',
    "onboarding page description",
)

replace_once(
    '"body": ( "Set up the real Connect ATX Elite program and Spring Fundraiser defaults, " "then hand off directly into the operating dashboard." ),',
    '"body": ( "Create the organization, configure the first public fundraiser, " "and hand off directly into the operator dashboard." ),',
    "onboarding body",
)

# ------------------------------------------------------------------
# Dashboard fallback copy sync
# ------------------------------------------------------------------
replace_once(
    '"page_description": ( "Manage campaigns, sponsor tiers, and memberships from the FutureFunded command center." ),',
    '"page_description": ( "Manage the live public fundraiser, sponsor packages, and recurring support from one premium operator workspace." ),',
    "dashboard page description",
)

replace_once(
    '"body": ( "Manage the live Connect ATX Elite fundraiser, sponsor packages, and booster support " "from one premium workspace." ),',
    '"body": ( "Manage the live public fundraiser, sponsor packages, and recurring support " "from one premium operator workspace." ),',
    "dashboard body",
)

# ------------------------------------------------------------------
# Pricing fallback copy sync
# ------------------------------------------------------------------
replace_once(
    '"body": ( "FutureFunded helps youth teams, schools, nonprofits, and clubs launch branded " "fundraising systems with direct giving, sponsor lanes, and recurring support " "from one premium workspace." ),',
    '"body": ( "FutureFunded helps youth teams, schools, nonprofits, and clubs launch public " "fundraisers, sponsor packages, and recurring support from one premium workspace." ),',
    "pricing body",
)

replace_once(
    '{"label": "Open founder demo", "href": "/platform/demo"},',
    '{"label": "View guided demo", "href": "/platform/demo"},',
    "pricing secondary action",
)

replace_once(
    '"title": "Future revenue lanes",',
    '"title": "Sponsor packages + recurring support",',
    "pricing included card title",
)

replace_once(
    '"body": ( "Sponsor packages and support-plan readiness that extend value beyond one campaign." ),',
    '"body": ( "Sponsor packages and recurring support that extend value beyond one campaign." ),',
    "pricing included card body",
)

# ------------------------------------------------------------------
# Demo fallback copy sync
# ------------------------------------------------------------------
replace_once(
    '"body": ( "This guided demo shows the public fundraiser, the onboarding flow, " "the operator dashboard, and the founder-ready pricing model as one connected revenue system." ),',
    '"body": ( "This guided demo shows the public fundraiser, onboarding flow, " "operator dashboard, and founder-ready pricing as one clean sales sequence." ),',
    "demo body",
)

replace_once(
    '"body": ( "Position FutureFunded as a system, not just a page, by showing management and revenue lanes." ),',
    '"body": ( "Position FutureFunded as a system — public fundraiser, operator dashboard, and revenue lanes — not just a page." ),',
    "demo step 3 body",
)

replace_once(
    '{"label": "Launch your program", "href": "/platform/onboarding"},',
    '{"label": "Start guided launch", "href": "/platform/onboarding"},',
    "demo primary action",
)

replace_once(
    '{"label": "View live example", "href": "/c/spring-fundraiser"},',
    '{"label": "View live fundraiser", "href": "/c/spring-fundraiser"},',
    "demo secondary action",
)

ROUTES.write_text(updated, encoding="utf-8")

print("== FF PLATFORM ROUTE COPY SYNC V1 ==")
print("applied:")
for item in applied:
    print(" -", item)
print("done.")
