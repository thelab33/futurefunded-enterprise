from pathlib import Path
from collections import Counter
import json
import re

ROOT = Path.cwd()
OUT_DIR = ROOT / "scripts" / "audit" / "_out"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "ff_repo_architecture_report.json"

template_roots = [
    ROOT / "apps" / "web" / "app" / "templates",
    ROOT / "apps" / "web" / "templates",
    ROOT / "templates",
]
template_files = []
for base in template_roots:
    if base.exists():
        template_files.extend(sorted(base.rglob("*.html")))

css_files = sorted((ROOT / "apps" / "web" / "app" / "static" / "css").rglob("*.css")) if (ROOT / "apps" / "web" / "app" / "static" / "css").exists() else []
js_files = sorted((ROOT / "apps" / "web" / "app" / "static" / "js").rglob("*.js")) if (ROOT / "apps" / "web" / "app" / "static" / "js").exists() else []

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

templates = []
pages = Counter()
template_types = Counter()

for p in template_files:
    text = p.read_text(encoding="utf-8", errors="ignore")
    page_vals = re.findall(r'data-ff-page="([^"]+)"', text)
    template_vals = re.findall(r'data-ff-template="([^"]+)"', text)
    section_ids = re.findall(r'<section\b[^>]*\bid="([^"]+)"', text, flags=re.I)
    css_refs = re.findall(r'href=["\']([^"\']+\.css[^"\']*)["\']', text, flags=re.I)
    js_refs = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', text, flags=re.I)

    for v in page_vals:
        pages[v] += 1
    for v in template_vals:
        template_types[v] += 1

    templates.append({
        "path": rel(p),
        "data_ff_page": sorted(set(page_vals)),
        "data_ff_template": sorted(set(template_vals)),
        "section_ids": section_ids,
        "css_refs": css_refs,
        "js_refs": js_refs,
        "ff_hook_count": len(re.findall(r'data-ff-[a-z0-9-]+', text)),
        "id_count": len(re.findall(r'\bid="[^"]+"', text)),
        "class_count": len(re.findall(r'\bclass="[^"]+"', text)),
    })

css_summary = []
for p in css_files:
    text = p.read_text(encoding="utf-8", errors="ignore")
    layers = re.findall(r'@layer\s+([^ {;]+)', text)
    markers = re.findall(r'/\*\s*(FF_[A-Z0-9_]+)', text)
    css_summary.append({
        "path": rel(p),
        "size_bytes": p.stat().st_size,
        "layers": sorted(set(layers)),
        "ff_markers": markers,
        "fundraiser_scoped_rules": len(re.findall(r'body\[data-ff-page="fundraiser"\]', text)),
        "platform_scoped_rules": len(re.findall(r'body\[data-ff-template="platform"\]', text)),
    })

js_summary = []
for p in js_files:
    text = p.read_text(encoding="utf-8", errors="ignore")
    js_summary.append({
        "path": rel(p),
        "size_bytes": p.stat().st_size,
        "data_ff_refs": len(re.findall(r'data-ff-[a-z0-9-]+', text)),
        "selector_refs": len(re.findall(r'querySelector(All)?\(', text)),
    })

report = {
    "template_count": len(template_files),
    "css_file_count": len(css_files),
    "js_file_count": len(js_files),
    "data_ff_page_counts": dict(pages),
    "data_ff_template_counts": dict(template_types),
    "templates": templates,
    "css_files": css_summary,
    "js_files": js_summary,
}

OUT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")

print("== REPO ARCHITECTURE AUDIT ==")
print(f"templates: {len(template_files)}")
print(f"css files : {len(css_files)}")
print(f"js files  : {len(js_files)}")
print("\n== data-ff-page counts ==")
for k, v in sorted(pages.items()):
    print(f"{k}: {v}")
print("\n== data-ff-template counts ==")
for k, v in sorted(template_types.items()):
    print(f"{k}: {v}")
print(f"\njson: {OUT_FILE}")
