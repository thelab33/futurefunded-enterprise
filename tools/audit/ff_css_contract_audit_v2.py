from __future__ import annotations

from pathlib import Path
from collections import Counter
import json
import re

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"
CSS = ROOT / "apps/web/app/static/css/ff.css"
JS = ROOT / "apps/web/app/static/js/ff-app.js"
OUT = ROOT / "tools/audit/ff_css_contract_audit_v2.json"

html = TEMPLATE.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")
js = JS.read_text(encoding="utf-8") if JS.exists() else ""

IGNORE_CLASS_TOKENS = {
    "if", "else", "endif", "elif",
    "base", "components", "css", "layout", "overlays",
    "sections", "tokens", "utilities",
    "true", "false", "none",
    "is_feature",
}

IGNORE_ID_TOKENS = {
    "fff", "ffffff",
    "b6c4d8", "b91c1c", "ca8a04", "dc2626",
    "dfe9f7", "ea580c", "edf3f8", "edf4ff",
    "f7fafd", "f97316",
}

def uniq_sorted(items):
    return sorted(set(items))

def clean_token(token: str) -> str:
    return token.strip()

def valid_class_token(token: str) -> bool:
    if token in IGNORE_CLASS_TOKENS:
        return False
    if token.startswith("_"):
        return False
    if token.startswith("{{") or token.endswith("}}"):
        return False
    if token.startswith("{%") or token.endswith("%}"):
        return False
    return bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", token))

def valid_id_token(token: str) -> bool:
    if token in IGNORE_ID_TOKENS:
        return False
    if re.fullmatch(r"[0-9a-fA-F]{3,8}", token):
        return False
    return bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", token))

# ---------------------------------
# strip obvious jinja blocks for extraction stability
# ---------------------------------
html_for_scan = re.sub(r"\{\#.*?\#\}", " ", html, flags=re.S)
html_for_scan = re.sub(r"\{\%.*?\%\}", " ", html_for_scan, flags=re.S)
html_for_scan = re.sub(r"\{\{.*?\}\}", " ", html_for_scan, flags=re.S)

# ---------------------------------
# extract class names
# ---------------------------------
class_attrs = re.findall(r'class="([^"]+)"', html_for_scan, flags=re.S)
html_classes = []
for attr in class_attrs:
    for token in attr.split():
        token = clean_token(token)
        if valid_class_token(token):
            html_classes.append(token)

html_classes = uniq_sorted(html_classes)

# ---------------------------------
# extract ids
# ---------------------------------
html_ids = uniq_sorted([
    x for x in re.findall(r'id="([^"]+)"', html_for_scan)
    if valid_id_token(x)
])

# ---------------------------------
# extract hooks
# ---------------------------------
html_hooks = uniq_sorted(re.findall(r'(data-ff-[a-z0-9_-]+)', html))

# ---------------------------------
# css presence checks
# ---------------------------------
missing_classes_in_css = [c for c in html_classes if f".{c}" not in css]
missing_ids_in_css = [i for i in html_ids if f"#{i}" not in css]
missing_hooks_in_css = [h for h in html_hooks if h not in css]

# ---------------------------------
# js hook presence checks
# ---------------------------------
missing_hooks_in_js = [h for h in html_hooks if h not in js]

# ---------------------------------
# dead css selectors
# ---------------------------------
css_class_candidates_raw = uniq_sorted(re.findall(r'\.([A-Za-z_][A-Za-z0-9_-]*)', css))
css_id_candidates_raw = uniq_sorted(re.findall(r'#([A-Za-z_][A-Za-z0-9_-]*)', css))
css_hook_candidates = uniq_sorted(re.findall(r'(data-ff-[a-z0-9_-]+)', css))

css_class_candidates = [c for c in css_class_candidates_raw if valid_class_token(c)]
css_id_candidates = [i for i in css_id_candidates_raw if valid_id_token(i)]

dead_css_classes = [c for c in css_class_candidates if c not in html_classes]
dead_css_ids = [i for i in css_id_candidates if i not in html_ids]
dead_css_hooks = [h for h in css_hook_candidates if h not in html_hooks]

# ---------------------------------
# duplication / frequency checks
# ---------------------------------
class_counts = Counter(html_classes)
id_counts = Counter(html_ids)
hook_counts = Counter(html_hooks)

# ---------------------------------
# section markers
# ---------------------------------
section_ids = uniq_sorted([
    x for x in re.findall(r'<section[^>]*id="([^"]+)"', html_for_scan)
    if valid_id_token(x)
])

report = {
    "template": str(TEMPLATE),
    "css": str(CSS),
    "js": str(JS),
    "counts": {
        "html_classes": len(html_classes),
        "html_ids": len(html_ids),
        "html_hooks": len(html_hooks),
        "css_class_candidates": len(css_class_candidates),
        "css_id_candidates": len(css_id_candidates),
        "css_hook_candidates": len(css_hook_candidates),
        "section_ids": len(section_ids),
    },
    "section_ids": section_ids,
    "missing_in_css": {
        "classes": missing_classes_in_css,
        "ids": missing_ids_in_css,
        "hooks": missing_hooks_in_css,
    },
    "missing_in_js": {
        "hooks": missing_hooks_in_js,
    },
    "dead_in_css": {
        "classes": dead_css_classes,
        "ids": dead_css_ids,
        "hooks": dead_css_hooks,
    },
    "all_html_contract": {
        "classes": html_classes,
        "ids": html_ids,
        "hooks": html_hooks,
    }
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print("== FF CSS CONTRACT AUDIT V2 ==")
print("template:", TEMPLATE)
print("css     :", CSS)
print("js      :", JS)
print()
print("-- counts --")
print(json.dumps(report["counts"], indent=2))
print()
print("-- missing in css --")
print("classes:", len(missing_classes_in_css))
print("ids    :", len(missing_ids_in_css))
print("hooks  :", len(missing_hooks_in_css))
print()
print("-- missing in js --")
print("hooks  :", len(missing_hooks_in_js))
print()
print("-- dead in css --")
print("classes:", len(dead_css_classes))
print("ids    :", len(dead_css_ids))
print("hooks  :", len(dead_css_hooks))
print()
print("report:", OUT)
