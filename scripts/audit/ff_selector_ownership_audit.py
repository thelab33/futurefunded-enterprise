from pathlib import Path
from collections import defaultdict
import json
import re

ROOT = Path.cwd()
OUT_DIR = ROOT / "scripts" / "audit" / "_out"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "ff_selector_ownership_report.json"

template_path = ROOT / "apps" / "web" / "app" / "templates" / "campaign" / "index.html"
css_root = ROOT / "apps" / "web" / "app" / "static" / "css"

if not template_path.exists():
    raise SystemExit(f"❌ Missing template: {template_path}")
if not css_root.exists():
    raise SystemExit(f"❌ Missing css root: {css_root}")

html = template_path.read_text(encoding="utf-8", errors="ignore")
css_files = sorted(css_root.rglob("*.css"))

ids = sorted(set(re.findall(r'\bid="([^"]+)"', html)))
classes = []
for m in re.findall(r'\bclass="([^"]+)"', html):
    classes.extend([c for c in m.split() if c.startswith("ff-")])
classes = sorted(set(classes))
hooks = sorted(set(re.findall(r'data-(ff-[a-z0-9-]+)', html)))

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

ownership = {
    "ids": defaultdict(list),
    "classes": defaultdict(list),
    "hooks": defaultdict(list),
}

for css in css_files:
    text = css.read_text(encoding="utf-8", errors="ignore")
    r = rel(css)

    for selector_id in ids:
        if re.search(r'#' + re.escape(selector_id) + r'\b', text):
            ownership["ids"][selector_id].append(r)

    for cls in classes:
        if re.search(r'\.' + re.escape(cls) + r'\b', text):
            ownership["classes"][cls].append(r)

    for hook in hooks:
        if re.search(r'\[data-' + re.escape(hook) + r'(?:[=\]]|\])', text):
            ownership["hooks"][hook].append(r)

missing = {
    "ids": [k for k in ids if not ownership["ids"][k]],
    "classes": [k for k in classes if not ownership["classes"][k]],
    "hooks": [k for k in hooks if not ownership["hooks"][k]],
}

report = {
    "template": rel(template_path),
    "counts": {
        "ids": len(ids),
        "classes": len(classes),
        "hooks": len(hooks),
    },
    "missing": missing,
    "ownership": {
        "ids": dict(ownership["ids"]),
        "classes": dict(ownership["classes"]),
        "hooks": dict(ownership["hooks"]),
    }
}

OUT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")

print("== SELECTOR OWNERSHIP AUDIT ==")
print(f"template: {rel(template_path)}")
print(f"ids    : {len(ids)}")
print(f"classes: {len(classes)}")
print(f"hooks  : {len(hooks)}")
print("\n== MISSING IDs ==")
print("\n".join(missing["ids"][:60]) or "none")
print("\n== MISSING CLASSES ==")
print("\n".join(missing["classes"][:60]) or "none")
print("\n== MISSING HOOKS ==")
print("\n".join(missing["hooks"][:60]) or "none")
print(f"\njson: {OUT_FILE}")
