#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(".").resolve()

TEMPLATE_DIRS = [
    ROOT / "apps/web/app/templates",
]

CSS_GLOBS = [
    "apps/web/app/static/css/**/*.css",
]

JS_GLOBS = [
    "apps/web/app/static/js/**/*.js",
]

REPORT_PATH = ROOT / "artifacts/_out/ff_repo_style_ownership_report.json"
MD_PATH = ROOT / "artifacts/_out/ff_repo_style_ownership_report.md"

CLASS_RE = re.compile(r'class\s*=\s*"([^"]+)"')
ID_RE = re.compile(r'id\s*=\s*"([^"]+)"')
ASSET_CSS_RE = re.compile(r'href\s*=\s*"([^"]+\.css(?:\?[^"]*)?)"')
ASSET_JS_RE = re.compile(r'src\s*=\s*"([^"]+\.js(?:\?[^"]*)?)"')
DATA_HOOK_RE = re.compile(r'\b(data-ff-[a-zA-Z0-9_-]+)\b')

# keep selectors conservative; we want useful signal, not parser fantasy
CSS_CLASS_DEF_RE = re.compile(r'(?<![A-Za-z0-9_-])\.([A-Za-z_][A-Za-z0-9_-]*)')
CSS_ID_DEF_RE = re.compile(r'(?<![A-Za-z0-9_-])#([A-Za-z_][A-Za-z0-9_-]*)')

IGNORE_DIR_NAMES = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "playwright-report",
    "test-results",
}

PATCHY_NAME_HINTS = (
    "patch",
    "hotfix",
    "rescue",
    "override",
    "bak",
    "backup",
    "legacy",
    "old",
    "tmp",
)

PRIORITY_TEMPLATES = [
    "campaign/index.html",
    "index.html",
]

def is_ignored(path: Path) -> bool:
    return any(part in IGNORE_DIR_NAMES for part in path.parts)

def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except Exception:
        return str(path)

def find_files(globs: list[str]) -> list[Path]:
    out: list[Path] = []
    for pattern in globs:
        for p in ROOT.glob(pattern):
            if p.is_file() and not is_ignored(p):
                out.append(p)
    return sorted(set(out))

def find_templates() -> list[Path]:
    found: list[Path] = []
    for base in TEMPLATE_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*.html"):
            if p.is_file() and not is_ignored(p):
                found.append(p)
    return sorted(set(found))

def normalize_class_tokens(raw: str) -> list[str]:
    tokens = []
    for token in raw.split():
        token = token.strip()
        if not token:
            continue
        if "{{" in token or "{%" in token or "}}" in token or "%}" in token:
            continue
        if token.startswith(("'", '"')) or token.endswith(("'", '"')):
            token = token.strip("'\"")
        if token:
            tokens.append(token)
    return tokens

def scan_template(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    classes = set()
    ids = set()
    data_hooks = set()
    css_assets = []
    js_assets = []

    for m in CLASS_RE.finditer(text):
        classes.update(normalize_class_tokens(m.group(1)))

    for m in ID_RE.finditer(text):
        val = m.group(1).strip()
        if val and "{{" not in val and "{%" not in val:
            ids.add(val)

    for m in DATA_HOOK_RE.finditer(text):
        data_hooks.add(m.group(1))

    for m in ASSET_CSS_RE.finditer(text):
        css_assets.append(m.group(1))

    for m in ASSET_JS_RE.finditer(text):
        js_assets.append(m.group(1))

    return {
        "path": rel(path),
        "classes": sorted(classes),
        "ids": sorted(ids),
        "data_hooks": sorted(data_hooks),
        "css_assets": css_assets,
        "js_assets": js_assets,
    }

def scan_css(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    class_defs = sorted(set(CSS_CLASS_DEF_RE.findall(text)))
    id_defs = sorted(set(CSS_ID_DEF_RE.findall(text)))
    lines = text.splitlines()

    patch_markers = []
    for i, line in enumerate(lines, start=1):
        line_l = line.lower()
        if any(h in line_l for h in PATCHY_NAME_HINTS):
            patch_markers.append({"line": i, "text": line.strip()[:160]})

    return {
        "path": rel(path),
        "class_defs": class_defs,
        "id_defs": id_defs,
        "patch_markers": patch_markers[:40],
        "size_bytes": path.stat().st_size,
    }

def scan_js(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    hooks = sorted(set(DATA_HOOK_RE.findall(text)))
    return {
        "path": rel(path),
        "data_hooks": hooks,
        "size_bytes": path.stat().st_size,
    }

templates = [scan_template(p) for p in find_templates()]
css_files = [scan_css(p) for p in find_files(CSS_GLOBS)]
js_files = [scan_js(p) for p in find_files(JS_GLOBS)]

class_owner_map: dict[str, list[str]] = defaultdict(list)
id_owner_map: dict[str, list[str]] = defaultdict(list)
hook_owner_map: dict[str, list[str]] = defaultdict(list)

for css in css_files:
    for cls in css["class_defs"]:
        class_owner_map[cls].append(css["path"])
    for ident in css["id_defs"]:
        id_owner_map[ident].append(css["path"])

for js in js_files:
    for hook in js["data_hooks"]:
        hook_owner_map[hook].append(js["path"])

template_reports = []

for tpl in templates:
    used_classes = tpl["classes"]
    used_ids = tpl["ids"]
    used_hooks = tpl["data_hooks"]

    missing_classes = []
    multi_owner_classes = []
    owned_classes = []

    for cls in used_classes:
        owners = class_owner_map.get(cls, [])
        if not owners:
            missing_classes.append(cls)
        else:
            owned_classes.append({"selector": f".{cls}", "owners": owners})
            if len(owners) > 1:
                multi_owner_classes.append({"selector": f".{cls}", "owners": owners})

    missing_ids = []
    multi_owner_ids = []

    for ident in used_ids:
        owners = id_owner_map.get(ident, [])
        if not owners:
            missing_ids.append(ident)
        elif len(owners) > 1:
            multi_owner_ids.append({"selector": f"#{ident}", "owners": owners})

    js_hook_presence = []
    missing_hooks_in_js = []

    for hook in used_hooks:
        owners = hook_owner_map.get(hook, [])
        js_hook_presence.append({"hook": hook, "owners": owners})
        if not owners:
            missing_hooks_in_js.append(hook)

    template_reports.append({
        "path": tpl["path"],
        "css_assets": tpl["css_assets"],
        "js_assets": tpl["js_assets"],
        "counts": {
            "classes": len(used_classes),
            "ids": len(used_ids),
            "data_hooks": len(used_hooks),
            "missing_classes": len(missing_classes),
            "missing_ids": len(missing_ids),
            "missing_hooks_in_js": len(missing_hooks_in_js),
            "multi_owner_classes": len(multi_owner_classes),
            "multi_owner_ids": len(multi_owner_ids),
        },
        "missing_classes": missing_classes[:200],
        "missing_ids": missing_ids[:200],
        "missing_hooks_in_js": missing_hooks_in_js[:200],
        "multi_owner_classes": multi_owner_classes[:200],
        "multi_owner_ids": multi_owner_ids[:200],
        "js_hook_presence": js_hook_presence[:400],
    })

patchy_files = []
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or is_ignored(p):
        continue
    name_l = p.name.lower()
    if any(h in name_l for h in PATCHY_NAME_HINTS):
        patchy_files.append(rel(p))

asset_index = []
for tpl in template_reports:
    asset_index.append({
        "template": tpl["path"],
        "css_assets": tpl["css_assets"],
        "js_assets": tpl["js_assets"],
    })

campaign_templates = [
    t for t in template_reports
    if "campaign/" in t["path"] or t["path"].endswith("index.html")
]

priority_template_report = None
for want in PRIORITY_TEMPLATES:
    for t in template_reports:
        if t["path"].endswith(want):
            priority_template_report = t
            break
    if priority_template_report:
        break

report = {
    "root": rel(ROOT),
    "templates_scanned": len(template_reports),
    "css_files_scanned": len(css_files),
    "js_files_scanned": len(js_files),
    "asset_index": asset_index,
    "priority_template_report": priority_template_report,
    "campaign_templates": campaign_templates,
    "patchy_files": patchy_files[:500],
    "css_files": css_files,
    "js_files": js_files,
}

REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")

def md_list(items, bullet="- "):
    if not items:
        return f"{bullet}(none)"
    return "\n".join(f"{bullet}{item}" for item in items)

lines = []
lines.append("# FF Repo Style Ownership Audit")
lines.append("")
lines.append(f"- Templates scanned: **{report['templates_scanned']}**")
lines.append(f"- CSS files scanned: **{report['css_files_scanned']}**")
lines.append(f"- JS files scanned: **{report['js_files_scanned']}**")
lines.append("")

if priority_template_report:
    p = priority_template_report
    lines.append("## Priority template")
    lines.append(f"- Template: `{p['path']}`")
    lines.append(f"- CSS assets: `{', '.join(p['css_assets']) or '(none)'}`")
    lines.append(f"- JS assets: `{', '.join(p['js_assets']) or '(none)'}`")
    lines.append(f"- Missing classes: **{p['counts']['missing_classes']}**")
    lines.append(f"- Missing ids: **{p['counts']['missing_ids']}**")
    lines.append(f"- Missing JS hooks: **{p['counts']['missing_hooks_in_js']}**")
    lines.append(f"- Multi-owner classes: **{p['counts']['multi_owner_classes']}**")
    lines.append("")
    lines.append("### First missing classes")
    lines.append(md_list([f"`.{x}`" for x in p["missing_classes"][:60]]))
    lines.append("")
    lines.append("### First multi-owner classes")
    if p["multi_owner_classes"]:
        for item in p["multi_owner_classes"][:40]:
            lines.append(f"- `{item['selector']}` -> {', '.join(f'`{o}`' for o in item['owners'])}")
    else:
        lines.append("- (none)")
    lines.append("")

lines.append("## Templates → assets")
for item in asset_index:
    lines.append(f"### `{item['template']}`")
    lines.append(f"- CSS: `{', '.join(item['css_assets']) or '(none)'}`")
    lines.append(f"- JS: `{', '.join(item['js_assets']) or '(none)'}`")
    lines.append("")

lines.append("## Patch-era / risky files")
lines.append(md_list([f"`{x}`" for x in patchy_files[:200]]))
lines.append("")

lines.append("## Recommended cleanup heuristic")
lines.append("- Keep exactly one canonical campaign stylesheet owner.")
lines.append("- Move patch-era CSS fragments into one reviewed authority file or archive them.")
lines.append("- Treat missing selectors in the priority template as either:")
lines.append("  - real regressions to restore, or")
lines.append("  - dead template classes to delete from markup after proof.")
lines.append("- Treat multi-owner selectors as cascade-risk candidates.")
lines.append("")

MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("== FF REPO STYLE OWNERSHIP AUDIT ==")
print(f"json: {REPORT_PATH}")
print(f"md  : {MD_PATH}")
print()
print("== SUMMARY ==")
print(f"templates_scanned={report['templates_scanned']}")
print(f"css_files_scanned={report['css_files_scanned']}")
print(f"js_files_scanned={report['js_files_scanned']}")
if priority_template_report:
    c = priority_template_report["counts"]
    print()
    print("== PRIORITY TEMPLATE ==")
    print(priority_template_report["path"])
    print(f"css_assets={priority_template_report['css_assets']}")
    print(f"js_assets={priority_template_report['js_assets']}")
    print(f"missing_classes={c['missing_classes']}")
    print(f"missing_ids={c['missing_ids']}")
    print(f"missing_hooks_in_js={c['missing_hooks_in_js']}")
    print(f"multi_owner_classes={c['multi_owner_classes']}")
    if priority_template_report["missing_classes"]:
        print()
        print("first_missing_classes=")
        for item in priority_template_report["missing_classes"][:40]:
            print(f"  .{item}")
print()
print("== PATCHY FILES (first 80) ==")
for item in patchy_files[:80]:
    print(item)
