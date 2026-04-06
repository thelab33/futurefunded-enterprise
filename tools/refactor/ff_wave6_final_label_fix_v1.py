from __future__ import annotations

from pathlib import Path
from datetime import datetime

ROOT = Path.home() / "futurefunded-enterprise"
TROOT = ROOT / "apps/web/app/templates"

TARGETS = [
    TROOT / "platform" / "pricing.html",
    TROOT / "platform" / "pages" / "pricing.html",
]

OLD = "Request white-label path"
NEW = "Request white-label"

def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = path.with_suffix(path.suffix + f".bak.{stamp}")
    bak.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return bak

print("== WAVE 6 FINAL LABEL FIX ==")
for path in TARGETS:
    if not path.exists():
        print(f"⚠ missing: {path}")
        continue

    original = path.read_text(encoding="utf-8")
    updated = original

    if OLD in updated and NEW not in updated:
        updated = updated.replace(OLD, NEW)
        bak = backup(path)
        path.write_text(updated, encoding="utf-8")
        print(f"✅ patched: {path}")
        print(f"🛟 backup: {bak}")
        print(f"   • {OLD!r} -> {NEW!r}")
    else:
        print(f"✔ skipped: {path} (already clean or no match)")
