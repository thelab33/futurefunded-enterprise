from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"

FILES = {
    "home": ROOT / "apps/web/app/templates/platform/pages/home.html",
    "pricing": ROOT / "apps/web/app/templates/platform/pages/pricing.html",
    "demo": ROOT / "apps/web/app/templates/platform/pages/demo.html",
}

for p in FILES.values():
    if not p.exists():
        raise SystemExit(f"Missing file: {p}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
for p in FILES.values():
    shutil.copy2(p, p.with_name(f"{p.name}.{timestamp}.bak"))

replacements = {
    "home": [
        (
            '"title": "Branded fundraiser",',
            '"title": "Public fundraiser",',
        ),
        (
            '"body": "Launch a public fundraising page that looks polished, credible, and ready to share with families and supporters."',
            '"body": "Launch a polished public fundraiser that is ready to share with families, donors, and sponsors."',
        ),
        (
            '"title": "Operator control",',
            '"title": "Operator dashboard",',
        ),
        (
            '"body": "Manage launch messaging, pricing, and team-by-team expansion from one cleaner platform workspace."',
            '"body": "Manage launch messaging, pricing, and expansion from one operator dashboard."',
        ),
        (
            'hero.get("secondary_cta_label", "View live example")',
            'hero.get("secondary_cta_label", "View live fundraiser")',
        ),
        (
            'hero.get("body", "Launch a sponsor-ready fundraising experience for youth boys basketball, starting with Connect ATX Elite — branded giving, booster support, and a cleaner story for families and local sponsors.")',
            'hero.get("body", "Launch a sponsor-ready public fundraiser for youth basketball, starting with Connect ATX Elite — then expand into sponsor packages, recurring support, and cleaner operator control.")',
        ),
        (
            '"body": "FutureFunded helps you sell the system clearly: premium public pages, sponsor-ready packaging, and a cleaner operator story that feels credible in front of real buyers."',
            '"body": "FutureFunded helps you explain the public fundraiser, sponsor packages, recurring support, and operator story as one clean system buyers can understand fast."',
        ),
    ],
    "pricing": [
        (
            '{"label": "Open founder demo", "href": "/platform/demo"}',
            '{"label": "View guided demo", "href": "/platform/demo"}',
        ),
        (
            '"title": "Future revenue lanes",',
            '"title": "Sponsor packages + recurring support",',
        ),
        (
            '"body": "Sponsor packages and support-plan readiness that extend value beyond one campaign."',
            '"body": "Sponsor packages and recurring support that extend value beyond one campaign."',
        ),
        (
            '"body",\n  "FutureFunded helps youth teams, schools, nonprofits, and clubs launch branded fundraising systems with direct giving, sponsor lanes, and optional support-plan expansion from one premium workspace."',
            '"body",\n  "FutureFunded helps youth teams, schools, nonprofits, and clubs launch public fundraisers, sponsor packages, and recurring support from one premium workspace."',
        ),
    ],
    "demo": [
        (
            '"body",\n  "This guided demo shows the public fundraiser, the onboarding flow, the operator dashboard, and the founder-ready pricing model as one connected revenue system."',
            '"body",\n  "This guided demo shows the public fundraiser, onboarding flow, operator dashboard, and founder-ready pricing model as one clean sales sequence."',
        ),
        (
            '{"label": "Launch your program", "href": "/platform/onboarding"}',
            '{"label": "Start guided launch", "href": "/platform/onboarding"}',
        ),
        (
            '{"label": "View live example", "href": "/c/spring-fundraiser"}',
            '{"label": "View live fundraiser", "href": "/c/spring-fundraiser"}',
        ),
        (
            '"body": "Position FutureFunded as a system, not just a page, by showing management and revenue lanes."',
            '"body": "Position FutureFunded as a system — public fundraiser, operator dashboard, and revenue lanes — not just a page."',
        ),
    ],
}

applied: list[str] = []

for key, path in FILES.items():
    src = path.read_text(encoding="utf-8")
    updated = src
    for old, new in replacements[key]:
        if old in updated:
            updated = updated.replace(old, new, 1)
            applied.append(f"{key}: {old[:56]}...")
        else:
            applied.append(f"{key}: MISS -> {old[:56]}...")
    path.write_text(updated, encoding="utf-8")

print("== FF PLATFORM COPY CONSISTENCY V1 ==")
print("applied:")
for item in applied:
    print(" -", item)
print("done.")
