from __future__ import annotations
from pathlib import Path
import json
import re
import sys
from collections import Counter
from urllib.request import urlopen

ROOT = Path(".").resolve()
DEFAULT_URL = "http://127.0.0.1:5000/c/connect-atx-elite"

CLASS_PAT = re.compile(r'class="([^"]+)"')
CSS_LINK_PAT = re.compile(r'<link[^>]+href="([^"]+\.css[^"]*)"')
JS_LINK_PAT = re.compile(r'<script[^>]+src="([^"]+\.js[^"]*)"')

def fetch(url: str) -> str:
    with urlopen(url) as r:
        return r.read().decode("utf-8", errors="ignore")

def safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def base_class_name(name: str) -> str:
    return name.split("--", 1)[0]

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    html = fetch(url)
    css = safe_read(ROOT / "apps/web/app/static/css/ff.css")

    classes = sorted({c for raw in CLASS_PAT.findall(html) for c in raw.split() if c.strip()})
    css_links = CSS_LINK_PAT.findall(html)
    js_links = JS_LINK_PAT.findall(html)

    dup_css_links = [k for k, v in Counter(css_links).items() if v > 1]

    direct_missing = [c for c in classes if f".{c}" not in css]
    likely_real_missing = []
    for c in direct_missing:
        base = base_class_name(c)
        if f".{base}" not in css:
            likely_real_missing.append(c)

    report = {
        "url": url,
        "css_links": css_links,
        "duplicate_css_links": dup_css_links,
        "js_links": js_links,
        "counts": {
            "classes": len(classes),
            "direct_missing_classes": len(direct_missing),
            "likely_real_missing_classes": len(likely_real_missing),
        },
        "likely_real_missing_classes": likely_real_missing[:250],
    }

    out = ROOT / "tools/.artifacts/ff_campaign_runtime_audit_v2.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("== FF CAMPAIGN RUNTIME AUDIT V2 ==")
    print("url:", url)
    print("\n== CSS LINKS ==")
    for x in css_links:
        print("-", x)
    print("\n== DUPLICATE CSS LINKS ==")
    for x in dup_css_links:
        print("-", x)
    print("\n== JS LINKS ==")
    for x in js_links:
        print("-", x)
    print("\n== COUNTS ==")
    print(json.dumps(report["counts"], indent=2))
    print("\n== LIKELY REAL MISSING CLASSES ==")
    for x in likely_real_missing[:120]:
        print("-", x)
    print(f"\nartifact: {out}")

if __name__ == "__main__":
    main()
