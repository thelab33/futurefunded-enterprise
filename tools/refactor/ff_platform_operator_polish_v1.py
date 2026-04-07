from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"

ROUTES = ROOT / "apps/web/app/routes/platform.py"
ONBOARDING = ROOT / "apps/web/app/templates/platform/pages/onboarding.html"
DASHBOARD = ROOT / "apps/web/app/templates/platform/pages/dashboard.html"

TARGETS = [ROUTES, ONBOARDING, DASHBOARD]

for p in TARGETS:
    if not p.exists():
        raise SystemExit(f"Missing file: {p}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
for p in TARGETS:
    shutil.copy2(p, p.with_name(f"{p.name}.{timestamp}.bak"))

def patch_file(path: Path, replacements: list[tuple[str, str]]) -> list[str]:
    src = path.read_text(encoding="utf-8")
    updated = src
    notes: list[str] = []
    for old, new in replacements:
        if old in updated:
            updated = updated.replace(old, new, 1)
            notes.append(f"changed: {old[:64]}...")
        else:
            notes.append(f"MISS: {old[:64]}...")
    path.write_text(updated, encoding="utf-8")
    return notes

route_replacements = [
    ('"eyebrow": "Step 1 · Launch Connect ATX Elite",', '"eyebrow": "Guided launch",'),
    ('"title": "Onboarding",', '"title": "Set up your first live fundraiser.",'),
    (
        '"body": "Set up the real Connect ATX Elite program and Spring Fundraiser defaults, then hand off directly into the operating dashboard.",',
        '"body": "Create the organization, configure the first public fundraiser, and hand off directly into the operator dashboard.",',
    ),
    ('"title": "Campaign",', '"title": "Public fundraiser",'),
    ('"submit_label": "Create org + campaign",', '"submit_label": "Create org + live page",'),
    ('"eyebrow": "Admin dashboard",', '"eyebrow": "Operator dashboard",'),
    ('"title": "FutureFunded command center",', '"title": "Operator command center",'),
    (
        '"body": "Manage the live Connect ATX Elite fundraiser, sponsor packages, and booster support from one premium workspace.",',
        '"body": "Manage the live public fundraiser, sponsor packages, and recurring support from one premium operator workspace.",',
    ),
    (
        '{"title": "Campaigns", "body": "Live fundraising campaigns you can manage", "value": "1"},',
        '{"title": "Live fundraisers", "body": "Public fundraisers you can manage", "value": "1"},',
    ),
    (
        '{"title": "Sponsor tiers", "body": "Active support packages for local partners", "value": "2"},',
        '{"title": "Sponsor packages", "body": "Active support packages for local partners", "value": "2"},',
    ),
    (
        '{"title": "Membership plans", "body": "Recurring support plans configured", "value": "2"},',
        '{"title": "Recurring support", "body": "Recurring support plans configured", "value": "2"},',
    ),
    (
        '{"label": "Open live campaign", "href": "/c/spring-fundraiser", "variant": "primary"},',
        '{"label": "Open live fundraiser", "href": "/c/spring-fundraiser", "variant": "primary"},',
    ),
    (
        '{"label": "Create another org", "href": "/platform/onboarding", "variant": "secondary"},',
        '{"label": "Start another guided launch", "href": "/platform/onboarding", "variant": "secondary"},',
    ),
]

onboarding_replacements = [
    (
        '{% set page_description = "Create your first organization and campaign, then hand off directly into the operating dashboard." %}',
        '{% set page_description = "Create your first organization and public fundraiser, then hand off directly into the operator dashboard." %}',
    ),
    (
        '{% set eyebrow = data.get("eyebrow", "Step 1 · Launch your first org") %}',
        '{% set eyebrow = data.get("eyebrow", "Guided launch") %}',
    ),
    (
        '{% set title = data.get("title", "Onboarding") %}',
        '{% set title = data.get("title", "Set up your first live fundraiser.") %}',
    ),
    (
        '{% set body = data.get("body", "Create your first organization and campaign against the real API, then hand off directly into your operational dashboard.") %}',
        '{% set body = data.get("body", "Create your first organization and public fundraiser against the real API, then hand off directly into the operator dashboard.") %}',
    ),
    (
        '{% set submit_label = data.get("submit_label", "Create org + launch page") %}',
        '{% set submit_label = data.get("submit_label", "Create org + live page") %}',
    ),
    (
        '<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformOnboardingBriefTitle">Start with one org. Publish one live campaign.</h2>',
        '<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformOnboardingBriefTitle">Start with one org. Publish one live fundraiser.</h2>',
    ),
    (
        '<p class="ff-help ff-muted ff-mt-2 ff-mb-0">\n          This setup gives you the minimum premium launch surface: a branded organization, a live fundraiser route, and a direct dashboard handoff.\n        </p>',
        '<p class="ff-help ff-muted ff-mt-2 ff-mb-0">\n          This setup gives you the minimum premium launch surface: a branded organization, a live fundraiser route, and a direct operator-dashboard handoff.\n        </p>',
    ),
    (
        '<p class="ff-help ff-muted ff-mt-2 ff-mb-0">\n          Set the live campaign headline, URL slug, and launch goal.\n        </p>',
        '<p class="ff-help ff-muted ff-mt-2 ff-mb-0">\n          Set the live public fundraiser headline, URL slug, and launch goal.\n        </p>',
    ),
    (
        '<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformLaunchOutcomeTitle">Create once. Go live instantly.</h2>',
        '<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformLaunchOutcomeTitle">Create once. Go live fast.</h2>',
    ),
    (
        '<p class="ff-kicker ff-m-0">Support-plan expansion</p>',
        '<p class="ff-kicker ff-m-0">Recurring support</p>',
    ),
    (
        '<p class="ff-help ff-muted ff-mt-2 ff-mb-0">The same org can later expand into optional support plans and a fuller platform hub.</p>',
        '<p class="ff-help ff-muted ff-mt-2 ff-mb-0">The same org can later add recurring support and a fuller platform hub.</p>',
    ),
]

dashboard_replacements = [
    (
        '{% set page_description = "Manage the live fundraiser, sponsor tiers, and optional support-plan lanes from one premium FutureFunded workspace." %}',
        '{% set page_description = "Manage the live public fundraiser, sponsor packages, and recurring support from one premium operator workspace." %}',
    ),
    (
        '{% set eyebrow = data.get("eyebrow", "Admin dashboard") %}',
        '{% set eyebrow = data.get("eyebrow", "Operator dashboard") %}',
    ),
    (
        '{% set title = data.get("title", "FutureFunded command center") %}',
        '{% set title = data.get("title", "Operator command center") %}',
    ),
    (
        '{% set body = data.get("body", "Manage the live Connect ATX Elite fundraiser, sponsor packages, and booster support from one premium workspace.") %}',
        '{% set body = data.get("body", "Manage the live public fundraiser, sponsor packages, and recurring support from one premium operator workspace.") %}',
    ),
    (
        '{{ ff_pill("Live workspace", "soft") }}',
        '{{ ff_pill("Live fundraiser", "soft") }}',
    ),
    (
        '<p class="ff-help ff-muted ff-mt-2 ff-mb-0">\n          This dashboard is your control layer for live fundraising, sponsor packages, and configured support-plan lanes.\n        </p>',
        '<p class="ff-help ff-muted ff-mt-2 ff-mb-0">\n          This dashboard is your control layer for the live public fundraiser, sponsor packages, and recurring support.\n        </p>',
    ),
    (
        '<p class="ff-kicker ff-m-0">Live campaign</p>',
        '<p class="ff-kicker ff-m-0">Live fundraiser</p>',
    ),
    (
        '<p class="ff-kicker ff-m-0">Sponsor lanes</p>',
        '<p class="ff-kicker ff-m-0">Sponsor packages</p>',
    ),
    (
        'actions[1].get("label", "Create another org") if actions|length > 1 else "Create another org",',
        'actions[1].get("label", "Start another guided launch") if actions|length > 1 else "Start another guided launch",',
    ),
    (
        '<p class="ff-kicker ff-m-0">Latest live organization</p>',
        '<p class="ff-kicker ff-m-0">Latest live fundraiser</p>',
    ),
    (
        '>Open live page</a>',
        '>Open live fundraiser</a>',
    ),
    (
        '<p class="ff-help ff-muted ff-mt-2 ff-mb-0">\n          The current workspace is already structured for direct giving, sponsor upsells, and optional support-plan expansion.\n        </p>',
        '<p class="ff-help ff-muted ff-mt-2 ff-mb-0">\n          The current workspace is already structured for direct giving, sponsor packages, and recurring support expansion.\n        </p>',
    ),
    (
        '<p class="ff-kicker ff-m-0">Sponsor tiers</p>',
        '<p class="ff-kicker ff-m-0">Sponsor packages</p>',
    ),
    (
        '<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformSponsorTierTitle">Revenue lane</h2>',
        '<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformSponsorTierTitle">Sponsor packages</h2>',
    ),
    (
        '<p class="ff-kicker ff-m-0">Configured support plans</p>',
        '<p class="ff-kicker ff-m-0">Recurring support</p>',
    ),
    (
        '<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformMembershipTitle">Recurring lane</h2>',
        '<h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformMembershipTitle">Recurring support</h2>',
    ),
]

print("== FF PLATFORM OPERATOR POLISH V1 ==")
for path, reps in [
    (ROUTES, route_replacements),
    (ONBOARDING, onboarding_replacements),
    (DASHBOARD, dashboard_replacements),
]:
    notes = patch_file(path, reps)
    print(f"patched: {path}")
    for note in notes:
        print(f"  - {note}")

print("done.")
