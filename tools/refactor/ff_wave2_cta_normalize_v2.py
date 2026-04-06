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

PATCHES = {
    "home": [
        ("Launch Connect ATX Elite", "Start guided launch"),
        ("Create organization", "Start guided launch"),
        ("Manage platform", "Open dashboard"),
    ],
    "onboarding": [
        ("Create org + campaign", "Create org + launch page"),
    ],
    "dashboard": [
        ("Create another org", "Start guided launch"),
        ("Open live campaign", "Open live fundraiser"),
        ("Open live page", "Open live fundraiser"),
    ],
    "pricing": [
        ("Claim founder setup", "Start guided launch"),
        ("View live demo", "Open founder demo"),
        ("Start with Starter", "Start guided launch"),
        ("Choose Growth", "Start Growth setup"),
        ("Request white-label path", "Request white-label"),
        ("Open guided demo", "Open founder demo"),
    ],
    "demo": [
        ("Launch your program", "Start guided launch"),
        ("Review pricing", "Open pricing"),
        ("View live example", "Open live fundraiser"),
    ],
    "campaign": [
        ("Launch your own", "Start guided launch"),
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

print("== WAVE 2 CTA NORMALIZE V2 ==")
for name, candidates in TARGETS.items():
    paths = existing_paths(candidates)
    if not paths:
        print(f"⚠ skipped {name}: no matching template path found")
        continue

    for path in paths:
        count, changes, bak = patch_file(path, PATCHES[name])
        if count:
            print(f"✅ patched {name}: {path}")
            print(f"🛟 backup: {bak}")
            for item in changes:
                print(f"   • {item}")
        else:
            print(f"✔ skipped {name}: {path} (already aligned or needles not present)")

if CAMPAIGN.exists():
    count, changes, bak = patch_file(CAMPAIGN, PATCHES["campaign"])
    if count:
        print(f"✅ patched campaign: {CAMPAIGN}")
        print(f"🛟 backup: {bak}")
        for item in changes:
            print(f"   • {item}")
    else:
        print(f"✔ skipped campaign: {CAMPAIGN} (already aligned or needles not present)")
else:
    print(f"⚠ missing campaign template: {CAMPAIGN}")
