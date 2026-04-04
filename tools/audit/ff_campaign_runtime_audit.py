from __future__ import annotations
from pathlib import Path
import json
import re
import sys
from urllib.request import urlopen

ROOT = Path(".").resolve()

DEFAULT_URL = "http://127.0.0.1:5000/c/connect-atx-elite"

CLASS_PAT = re.compile(r'class="([^"]+)"')
ID_PAT = re.compile(r'id="([^"]+)"')
DATAFF_PAT = re.compile(r'(data-ff-[a-z0-9_-]+)')
CSS_LINK_PAT = re.compile(r'<link[^>]+href="([^"]+\.css[^"]*)"')
JS_LINK_PAT = re.compile(r'<script[^>]+src="([^"]+\.js[^"]*)"')
SELECTOR_JSON_PAT = re.compile(r'<script id="ffSelectors"[^>]*>\s*(\{.*?\})\s*</script>', re.S)

def fetch(url: str) -> str:
    with urlopen(url) as r:
        return r.read().decode("utf-8", errors="ignore")

def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def selector_exists(css: str, selector: str) -> bool:
    return selector in css

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    html = fetch(url)

    css_path = ROOT / "apps/web/app/static/css/ff.css"
    js_path = ROOT / "apps/web/app/static/js/ff-app.js"

    css = safe_read(css_path)
    js = safe_read(js_path)

    classes = sorted({c for raw in CLASS_PAT.findall(html) for c in raw.split() if c.strip()})
    ids = sorted(set(ID_PAT.findall(html)))
    dataff = sorted(set(DATAFF_PAT.findall(html)))

    css_links = CSS_LINK_PAT.findall(html)
    js_links = JS_LINK_PAT.findall(html)

    missing_class_selectors = [c for c in classes if f".{c}" not in css]
    missing_id_selectors = [i for i in ids if f"#{i}" not in css]
    missing_dataff_selectors = [d for d in dataff if f"[{d}]" not in css and f"[{d}=" not in css]

    selector_json_match = SELECTOR_JSON_PAT.search(html)
    js_hook_report = {}
    if selector_json_match:
        try:
            selector_map = json.loads(selector_json_match.group(1))
            hooks = selector_map.get("hooks", {})
            for name, selector in hooks.items():
                js_hook_report[name] = {
                    "selector": selector,
                    "present_in_js": selector in js,
                    "present_in_html": (
                        selector.startswith("#") and selector[1:] in ids
                    ) or (
                        selector.startswith("[data-ff-") and selector[1:-1].split("=")[0] in dataff
                    ) or (
                        selector in html
                    )
                }
        except Exception as e:
            js_hook_report = {"error": str(e)}

    report = {
        "url": url,
        "css_links": css_links,
        "js_links": js_links,
        "counts": {
            "classes": len(classes),
            "ids": len(ids),
            "dataff": len(dataff),
            "missing_class_selectors": len(missing_class_selectors),
            "missing_id_selectors": len(missing_id_selectors),
            "missing_dataff_selectors": len(missing_dataff_selectors),
        },
        "missing_class_selectors": missing_class_selectors[:300],
        "missing_id_selectors": missing_id_selectors[:300],
        "missing_dataff_selectors": missing_dataff_selectors[:300],
        "js_hook_report": js_hook_report,
    }

    out = ROOT / "tools/.artifacts/ff_campaign_runtime_audit.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("== FF CAMPAIGN RUNTIME AUDIT ==")
    print("url:", url)
    print("\n== CSS LINKS ==")
    for x in css_links:
        print("-", x)
    print("\n== JS LINKS ==")
    for x in js_links:
        print("-", x)
    print("\n== COUNTS ==")
    print(json.dumps(report["counts"], indent=2))
    print("\n== MISSING CLASS SELECTORS (sample) ==")
    for x in missing_class_selectors[:80]:
        print("-", x)
    print("\n== MISSING ID SELECTORS (sample) ==")
    for x in missing_id_selectors[:40]:
        print("-", x)
    print("\n== MISSING DATA-FF SELECTORS (sample) ==")
    for x in missing_dataff_selectors[:40]:
        print("-", x)
    print(f"\nartifact: {out}")

if __name__ == "__main__":
    main()
