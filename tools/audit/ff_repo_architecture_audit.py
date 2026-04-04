from __future__ import annotations
from pathlib import Path
import json
import re

ROOT = Path(".").resolve()

ROUTE_PATTERNS = [
    re.compile(r"@.*?route\((.*?)\)", re.S),
]
RENDER_PAT = re.compile(r"render_template\(\s*['\"]([^'\"]+)['\"]")
URLFOR_STATIC_PAT = re.compile(r"url_for\(\s*['\"]static['\"]\s*,\s*filename\s*=\s*['\"]([^'\"]+)['\"]")

KEY_FILES = [
    "apps/web/app/templates/campaign/index.html",
    "apps/web/app/static/css/ff.css",
    "apps/web/app/static/css/ff-above-main-premium.css",
    "apps/web/app/static/js/ff-app.js",
]

def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def find_files(exts: tuple[str, ...]):
    out = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts:
            out.append(p)
    return sorted(out)

def main():
    py_files = find_files((".py",))
    html_files = find_files((".html", ".jinja", ".j2"))
    css_files = find_files((".css",))
    js_files = find_files((".js", ".mjs"))

    routes = []
    render_calls = []
    static_refs = []

    for p in py_files + html_files:
        txt = safe_read(p)
        if not txt:
            continue

        if p.suffix == ".py":
            for m in ROUTE_PATTERNS[0].finditer(txt):
                routes.append({
                    "file": str(p.relative_to(ROOT)),
                    "route_decorator_args": m.group(1).strip()[:240]
                })
            for m in RENDER_PAT.finditer(txt):
                render_calls.append({
                    "file": str(p.relative_to(ROOT)),
                    "template": m.group(1)
                })

        for m in URLFOR_STATIC_PAT.finditer(txt):
            static_refs.append({
                "file": str(p.relative_to(ROOT)),
                "static_file": m.group(1)
            })

    report = {
        "root": str(ROOT),
        "counts": {
            "python_files": len(py_files),
            "html_files": len(html_files),
            "css_files": len(css_files),
            "js_files": len(js_files),
        },
        "key_files_present": {
            k: (ROOT / k).exists() for k in KEY_FILES
        },
        "routes": routes[:300],
        "render_calls": render_calls[:300],
        "static_refs": static_refs[:500],
        "templates": [str(p.relative_to(ROOT)) for p in html_files[:500]],
        "css_files": [str(p.relative_to(ROOT)) for p in css_files[:500]],
        "js_files": [str(p.relative_to(ROOT)) for p in js_files[:500]],
    }

    out = ROOT / "tools/.artifacts/ff_repo_architecture_audit.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("== FF REPO ARCHITECTURE AUDIT ==")
    print(json.dumps(report["counts"], indent=2))
    print("\n== KEY FILES ==")
    for k, v in report["key_files_present"].items():
        print(("✅" if v else "❌"), k)
    print("\n== ROUTES (sample) ==")
    for item in report["routes"][:40]:
        print(f"- {item['file']}: {item['route_decorator_args']}")
    print("\n== RENDER CALLS (sample) ==")
    for item in report["render_calls"][:40]:
        print(f"- {item['file']}: {item['template']}")
    print(f"\nartifact: {out}")

if __name__ == "__main__":
    main()
