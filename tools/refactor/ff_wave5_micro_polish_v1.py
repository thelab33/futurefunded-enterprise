from __future__ import annotations

from pathlib import Path
from datetime import datetime

ROOT = Path.home() / "futurefunded-enterprise"
TROOT = ROOT / "apps/web/app/templates"

LIVE_FILES = [
    TROOT / "platform" / "home.html",
    TROOT / "platform" / "dashboard.html",
    TROOT / "platform" / "onboarding.html",
    TROOT / "platform" / "pricing.html",
    TROOT / "platform" / "pages" / "home.html",
    TROOT / "platform" / "pages" / "dashboard.html",
    TROOT / "platform" / "pages" / "onboarding.html",
    TROOT / "platform" / "pages" / "pricing.html",
]

REPLACEMENTS = [
    # dashboard / home wording cleanup
    ("optional support-plan expansion expansion.", "optional support-plan expansion."),
    ("optional support-plan expansion expansion", "optional support-plan expansion"),
    ("optional support-plan expansion lanes", "optional support-plan lanes"),

    # onboarding sponsor seed cleanup
    ("VIP Sponsor — $250", "Partner Sponsor — $250"),

    # pricing CTA wording cleanup
    ("Request white-label path", "Request white-label"),

    # pricing CTA target cleanup
    ('href="/c/spring-fundraiser">Open founder demo</a>', 'href="/platform/demo">Open founder demo</a>'),
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

print("== WAVE 5 MICRO POLISH ==")
for path in LIVE_FILES:
    if not path.exists():
        print(f"⚠ missing: {path}")
        continue

    count, changes, bak = patch_file(path, REPLACEMENTS)
    if count:
        print(f"✅ patched: {path}")
        print(f"🛟 backup: {bak}")
        for item in changes:
            print(f"   • {item}")
    else:
        print(f"✔ skipped: {path} (already clean or no matching strings)")
