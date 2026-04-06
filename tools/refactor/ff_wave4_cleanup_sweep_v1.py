from __future__ import annotations

from pathlib import Path
from datetime import datetime

ROOT = Path.home() / "futurefunded-enterprise"
TROOT = ROOT / "apps/web/app/templates"

LIVE_FILES = [
    TROOT / "platform" / "home.html",
    TROOT / "platform" / "onboarding.html",
    TROOT / "platform" / "dashboard.html",
    TROOT / "platform" / "pricing.html",
    TROOT / "platform" / "demo.html",
    TROOT / "platform" / "pages" / "home.html",
    TROOT / "platform" / "pages" / "onboarding.html",
    TROOT / "platform" / "pages" / "dashboard.html",
    TROOT / "platform" / "pages" / "pricing.html",
    TROOT / "platform" / "pages" / "demo.html",
]

SWEEP_REPLACEMENTS = [
    ("recurring support", "optional support-plan expansion"),
    ("booster memberships", "optional support plans"),
    ("recurring lanes", "support-plan readiness"),
    ("Membership expansion", "Support-plan expansion"),
    ("Membership plans", "Configured support plans"),
    ("Bronze Sponsor", "Partner Sponsor"),
    ("Gold Sponsor", "VIP Sponsor"),
    ("Request white-label path", "Request white-label"),
]

HOME_FORCE_REPLACEMENTS = [
    (
        "Launch sponsor-ready fundraisers, branded program hubs, and recurring support from one premium workspace.",
        "Launch sponsor-ready fundraisers, branded program hubs, and optional support-plan expansion from one premium workspace.",
    ),
    (
        "Give youth basketball programs a premium fundraising product with direct giving, sponsor support, booster memberships, and branded organization pages in one place.",
        "Give youth programs a premium fundraising product with direct giving, sponsor support, optional support-plan expansion, and branded organization pages in one place.",
    ),
    (
        "Begin with Connect ATX Elite, then expand into sponsor packages, recurring support, announcement bars, countdowns, and branded organization hubs without rebuilding from scratch.",
        "Begin with Connect ATX Elite, then expand into sponsor packages, optional support plans, announcement bars, countdowns, and branded organization hubs without rebuilding from scratch.",
    ),
]

def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = path.with_suffix(path.suffix + f".bak.{stamp}")
    bak.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return bak

def patch_file(path: Path, replacements: list[tuple[str, str]]) -> tuple[int, list[str], Path | None]:
    original = path.read_text(encoding="utf-8")
    updated = original
    changed: list[str] = []

    for old, new in replacements:
        if old in updated and new not in updated:
            updated = updated.replace(old, new)
            changed.append(f"{old!r} -> {new!r}")

    if updated == original:
        return 0, [], None

    bak = backup(path)
    path.write_text(updated, encoding="utf-8")
    return len(changed), changed, bak

print("== WAVE 4 CLEANUP SWEEP ==")
for path in LIVE_FILES:
    if not path.exists():
        print(f"⚠ missing: {path}")
        continue

    replacements = list(SWEEP_REPLACEMENTS)
    if path.name == "home.html":
        replacements.extend(HOME_FORCE_REPLACEMENTS)

    count, changes, bak = patch_file(path, replacements)
    if count:
        print(f"✅ patched: {path}")
        print(f"🛟 backup: {bak}")
        for item in changes:
            print(f"   • {item}")
    else:
        print(f"✔ skipped: {path} (already aligned or no lingering strings)")
