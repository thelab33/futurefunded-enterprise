from __future__ import annotations

from pathlib import Path
from datetime import datetime

ROOT = Path.home() / "futurefunded-enterprise"
TROOT = ROOT / "apps/web/app/templates"
CAMPAIGN = TROOT / "campaign" / "index.html"

TARGETS = {
    "home": [
        TROOT / "platform" / "home.html",
        TROOT / "platform" / "pages" / "home.html",
    ],
    "onboarding": [
        TROOT / "platform" / "onboarding.html",
        TROOT / "platform" / "pages" / "onboarding.html",
    ],
    "dashboard": [
        TROOT / "platform" / "dashboard.html",
        TROOT / "platform" / "pages" / "dashboard.html",
    ],
    "pricing": [
        TROOT / "platform" / "pricing.html",
        TROOT / "platform" / "pages" / "pricing.html",
    ],
    "demo": [
        TROOT / "platform" / "demo.html",
        TROOT / "platform" / "pages" / "demo.html",
    ],
}

COMMON_TAGLINE_OLD = (
    "Launch sponsor-ready fundraisers, branded program hubs, and recurring support from one premium workspace."
)
COMMON_TAGLINE_NEW = (
    "Launch sponsor-ready fundraisers, branded program hubs, and optional support-plan expansion from one premium workspace."
)

PATCHES = {
    "home": [
        (COMMON_TAGLINE_OLD, COMMON_TAGLINE_NEW),
        (
            "Give youth basketball programs a premium fundraising product with direct giving, sponsor support, booster memberships, and branded organization pages in one place.",
            "Give youth programs a premium fundraising product with direct giving, sponsor support, optional support-plan expansion, and branded organization pages in one place.",
        ),
        (
            "Begin with Connect ATX Elite, then expand into sponsor packages, recurring support, announcement bars, countdowns, and branded organization hubs without rebuilding from scratch.",
            "Begin with Connect ATX Elite, then expand into sponsor packages, optional support plans, announcement bars, countdowns, and branded organization hubs without rebuilding from scratch.",
        ),
    ],
    "onboarding": [
        (COMMON_TAGLINE_OLD, COMMON_TAGLINE_NEW),
        ("Membership expansion", "Support-plan expansion"),
        (
            "The same org can later expand into booster memberships and a fuller platform hub.",
            "The same org can later expand into optional support plans and a fuller platform hub.",
        ),
    ],
    "dashboard": [
        (COMMON_TAGLINE_OLD, COMMON_TAGLINE_NEW),
        (
            "This dashboard is your control layer for live fundraising, sponsor packages, and recurring support lanes.",
            "This dashboard is your control layer for live fundraising, sponsor packages, and configured support-plan lanes.",
        ),
        (
            "Keep momentum going beyond one-time gifts with monthly and annual memberships.",
            "Keep momentum going beyond one-time gifts with configurable monthly and annual support plans.",
        ),
        ("Bronze Sponsor", "Partner Sponsor"),
        ("Gold Sponsor", "VIP Sponsor"),
        ("Membership plans", "Configured support plans"),
        ("Recurring support plans configured", "Support plans configured"),
    ],
    "pricing": [
        (COMMON_TAGLINE_OLD, COMMON_TAGLINE_NEW),
        (
            "FutureFunded helps youth teams, schools, nonprofits, and clubs launch branded fundraising systems with direct giving, sponsor lanes, and recurring support from one premium workspace.",
            "FutureFunded helps youth teams, schools, nonprofits, and clubs launch branded fundraising systems with direct giving, sponsor lanes, and optional support-plan expansion from one premium workspace.",
        ),
        (
            "Start with a lower entry point, get live fast, and grow into sponsor packages and recurring support without rebuilding your system later.",
            "Start with a lower entry point, get live fast, and grow into sponsor packages and optional support plans without rebuilding your system later.",
        ),
        (
            "Public fundraiser, sponsor-ready packages, recurring lanes, and operator dashboard access.",
            "Public fundraiser, sponsor-ready packages, support-plan readiness, and operator dashboard access.",
        ),
        (
            "Sponsor packages and recurring support that extend value beyond one campaign.",
            "Sponsor packages and support-plan readiness that extend value beyond one campaign.",
        ),
        (
            "Start with founder pricing, launch the public fundraiser first, then expand into sponsor packages and recurring support as the program grows.",
            "Start with founder pricing, launch the public fundraiser first, then expand into sponsor packages and optional support plans as the program grows.",
        ),
    ],
    "demo": [
        (COMMON_TAGLINE_OLD, COMMON_TAGLINE_NEW),
    ],
}

def existing_paths(paths: list[Path]) -> list[Path]:
    return [p for p in paths if p.exists()]

def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = path.with_suffix(path.suffix + f".bak.{stamp}")
    bak.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return bak

def patch_file(path: Path, replacements: list[tuple[str, str]]) -> tuple[int, list[str], Path | None]:
    original = path.read_text(encoding="utf-8")
    updated = original
    changed_labels: list[str] = []

    for old, new in replacements:
        if old in updated and new not in updated:
            updated = updated.replace(old, new)
            changed_labels.append(old[:72] + ("…" if len(old) > 72 else ""))

    if updated == original:
        return 0, [], None

    bak = backup(path)
    path.write_text(updated, encoding="utf-8")
    return len(changed_labels), changed_labels, bak

print("== WAVE 1 CONTRACT UNIFY V2 ==")
for name, candidates in TARGETS.items():
    paths = existing_paths(candidates)
    if not paths:
        print(f"⚠ skipped {name}: no matching template path found")
        continue

    for path in paths:
        count, labels, bak = patch_file(path, PATCHES[name])
        if count:
            print(f"✅ patched {name}: {path}")
            print(f"🛟 backup: {bak}")
            for label in labels:
                print(f"   • {label}")
        else:
            print(f"✔ skipped {name}: {path} (already aligned or needles not present)")

if CAMPAIGN.exists():
    print(f"ℹ campaign untouched: {CAMPAIGN}")
else:
    print(f"⚠ missing campaign template: {CAMPAIGN}")

print("\n== TARGET MAP ==")
for name, candidates in TARGETS.items():
    live = existing_paths(candidates)
    if live:
        for path in live:
            print(f"{name:>10}: {path}")
    else:
        print(f"{name:>10}: MISSING")
