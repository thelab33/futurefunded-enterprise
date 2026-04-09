from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
ARCHIVE_ROOT = ROOT / "archive" / "template-backups" / datetime.now().strftime("%Y%m%d-%H%M%S")

SCAN_ROOTS = [
    ROOT / "apps/web/app/templates",
    ROOT / "apps/web/app/routes",
    ROOT / "apps/web/app/static",
    ROOT / "apps/web/app",
]

moved = []

for scan_root in SCAN_ROOTS:
    if not scan_root.exists():
        continue
    for path in scan_root.rglob("*"):
        if not path.is_file():
            continue
        name = path.name
        if ".bak" not in name:
            continue
        rel = path.relative_to(ROOT)
        dest = ARCHIVE_ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(dest))
        moved.append((str(rel), str(dest.relative_to(ROOT))))

print(f"archive_root: {ARCHIVE_ROOT}")
print(f"moved_count: {len(moved)}")
for src, dst in moved[:200]:
    print(f"MOVED {src} -> {dst}")
if len(moved) > 200:
    print(f"... {len(moved) - 200} more omitted")
