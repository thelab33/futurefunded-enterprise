from __future__ import annotations
from pathlib import Path
import json
import re

ROOT = Path(".").resolve()

IGNORE_PARTS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".mypy_cache",
    ".pytest_cache", ".ruff_cache", "dist", "build", ".next", ".svelte-kit",
    "coverage", "htmlcov", ".cache"
}

ROUTE_PAT = re.compile(r"@\w+(?:\.\w+)?\.route\((.*?)\)", re.S)
RENDER_PAT = re.compile(r"render_template\(\s*['\"]([^'\"]+)['\"]")
URLFOR_STATIC_PAT = re.compile(r"url_for\(\s*['\"]static['\"]\s*,\s*filename\s*=\s*['\"]([^'\"]+)['\"]")

KEY_FILES = [
    "apps/web/app/routes/campaign.py",
    "apps/web/app/routes/platform.py",
    "apps/web/app/templates/campaign/index.html",
    "apps/web/app/static/css/ff.css",
    "apps/web/app/static/css/ff-above-main-premium.css",
    "apps/web/app/static/js/ff-app.js",
]

def allowed(path: Path) -> bool:
    return not any(part in IGNORE_PARTS for part in path.parts)

def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def find_files(exts: tuple[str, ...]):
    out = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts and allowed(p.relative_to(ROOT)):
            out.append(p)
    return sorted(out)

def main():
    py_files = find_files((".py",))
    html_files = find_files((".html", ".jinja", ".j2"))
    css_files = find_files((".css",))
    js_files = find_files((".js", ".mjs"))

    routes, render_calls, static_refs = [], [], []

    for p in py_files + html_files:
        txt = safe_read(p)
        if not txt:
            continue

        if p.suffix == ".py":
            for m in ROUTE_PAT.finditer(txt):
                routes.append({
                    "file": str(p.relative_to(ROOT)),
                    "route": m.group(1).strip()[:240]
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
        "counts": {
            "python_files": len(py_files),
            "html_files": len(html_files),
            "css_files": len(css_files),
            "js_files": len(js_files),
        },
        "key_files_present": {k: (ROOT / k).exists() for k in KEY_FILES},
        "routes": routes,
        "render_calls": render_calls,
        "static_refs": static_refs,
    }

    out = ROOT / "tools/.artifacts/ff_repo_architecture_audit_v2.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("== FF REPO ARCHITECTURE AUDIT V2 ==")
    print(json.dumps(report["counts"], indent=2))
    print("\n== KEY FILES ==")
    for k, v in report["key_files_present"].items():
        print(("✅" if v else "❌"), k)
    print("\n== APP ROUTES ==")
    for item in report["routes"][:80]:
        print(f"- {item['file']}: {item['route']}")
    print("\n== RENDER CALLS ==")
    for item in report["render_calls"][:80]:
        print(f"- {item['file']}: {item['template']}")
    print(f"\nartifact: {out}")

if __name__ == "__main__":
    main()
