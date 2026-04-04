from __future__ import annotations
from pathlib import Path
import re
import sys

ROOT = Path(".").resolve()
CSS_PATH = ROOT / "apps/web/app/static/css/ff.css"

def main():
    if len(sys.argv) < 2:
        print("usage: python3 tools/audit/ff_css_origin_audit.py <selector1> [selector2] ...")
        raise SystemExit(1)

    css = CSS_PATH.read_text(encoding="utf-8", errors="ignore")
    lines = css.splitlines()

    print("== FF CSS ORIGIN AUDIT ==")
    print("css:", CSS_PATH)
    for needle in sys.argv[1:]:
        print(f"\n-- {needle}")
        hits = 0
        for i, line in enumerate(lines, start=1):
            if needle in line:
                hits += 1
                print(f"{i}: {line.rstrip()}")
        if hits == 0:
            print("NOT FOUND")
        else:
            print(f"hits: {hits}")

if __name__ == "__main__":
    main()
