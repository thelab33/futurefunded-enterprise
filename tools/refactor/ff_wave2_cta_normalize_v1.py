from __future__ import annotations

from pathlib import Path
from datetime import datetime

ROOT = Path.home() / "futurefunded-enterprise"
TROOT = ROOT / "apps/web/app/templates"
CAMPAIGN = TROOT / "campaign" / "index.html"

DISCOVERY = {
    "home": "Give Connect ATX Elite a premium fundraising home.",
    "onboarding": "Step 1 · Launch Connect ATX Elite",
    "dashboard": "FutureFunded command center",
    "pricing": "Launch a sponsor-ready fundraiser in minutes.",
    "demo": "See FutureFunded in action.",
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

def find_template(needle: str) -> Path:
    for path in TROOT.rglob("*.html"):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        if needle in text:
            return path
    raise SystemExit(f"❌ Could not find template containing: {needle!r}")

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

targets = {name: find_template(needle) for name, needle in DISCOVERY.items()}
targets["campaign"] = CAMPAIGN

print("== WAVE 2 CTA NORMALIZE ==")
for name, path in targets.items():
    count, changes, bak = patch_file(path, PATCHES[name])
    if count:
        print(f"✅ patched {name}: {path}")
        print(f"🛟 backup: {bak}")
        for item in changes:
            print(f"   • {item}")
    else:
        print(f"✔ skipped {name}: {path} (already aligned or needles not present)")
