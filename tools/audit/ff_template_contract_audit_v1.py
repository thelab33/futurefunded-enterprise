from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATES = ROOT / "apps/web/app/templates"
ROUTES = ROOT / "apps/web/app/routes"

if not TEMPLATES.exists():
    raise SystemExit("templates root missing")

active_templates = {
    p.relative_to(TEMPLATES).as_posix()
    for p in TEMPLATES.rglob("*.html")
    if ".bak" not in p.name
}

route_patterns = [
    re.compile(r'render_template\(\s*["\']([^"\']+)["\']'),
    re.compile(r'template_name\s*=\s*["\']([^"\']+)["\']'),
]

jinja_patterns = [
    re.compile(r'{%\s*extends\s+["\']([^"\']+)["\']'),
    re.compile(r'{%\s*include\s+["\']([^"\']+)["\']'),
    re.compile(r'{%\s*import\s+["\']([^"\']+)["\']'),
    re.compile(r'{%\s*from\s+["\']([^"\']+)["\']\s+import'),
]

missing_route_refs = []
missing_jinja_refs = []
legacy_hits = []
backup_hits = []

legacy_patterns = [
    "platform/base.html",
    "platform/dashboard.html",
    "platform/home.html",
    "platform/onboarding.html",
    "platform/pricing.html",
    "platform/demo.html",
    "platform_base_legacy.html",
]

for p in ROOT.rglob("*"):
    if p.is_file() and ".bak" in p.name and "archive/" not in p.as_posix():
        backup_hits.append(p.relative_to(ROOT).as_posix())

for py_file in ROUTES.rglob("*.py"):
    text = py_file.read_text(encoding="utf-8", errors="ignore")
    rel = py_file.relative_to(ROOT).as_posix()

    for pat in route_patterns:
        for match in pat.findall(text):
            if match.endswith(".html") and match not in active_templates:
                missing_route_refs.append((rel, match))

    for old in legacy_patterns:
        if old in text:
            legacy_hits.append((rel, old))

for tpl in TEMPLATES.rglob("*.html"):
    if ".bak" in tpl.name:
        continue
    text = tpl.read_text(encoding="utf-8", errors="ignore")
    rel = tpl.relative_to(ROOT).as_posix()

    for pat in jinja_patterns:
        for match in pat.findall(text):
            if match.endswith(".html") and match not in active_templates:
                missing_jinja_refs.append((rel, match))

    for old in legacy_patterns:
        if old in text:
            legacy_hits.append((rel, old))

print("== TEMPLATE CONTRACT AUDIT ==")
print(f"active_templates={len(active_templates)}")
print(f"missing_route_refs={len(missing_route_refs)}")
print(f"missing_jinja_refs={len(missing_jinja_refs)}")
print(f"legacy_path_hits={len(legacy_hits)}")
print(f"backup_hits_in_live_tree={len(backup_hits)}")

if missing_route_refs:
    print("\n-- MISSING ROUTE TEMPLATE REFS --")
    for rel, ref in missing_route_refs:
        print(f"{rel}: {ref}")

if missing_jinja_refs:
    print("\n-- MISSING JINJA TEMPLATE REFS --")
    for rel, ref in missing_jinja_refs:
        print(f"{rel}: {ref}")

if legacy_hits:
    print("\n-- LEGACY / STALE TEMPLATE PATH HITS --")
    for rel, hit in legacy_hits:
        print(f"{rel}: {hit}")

if backup_hits:
    print("\n-- BACKUPS STILL IN LIVE TREE --")
    for rel in backup_hits[:200]:
        print(rel)
    if len(backup_hits) > 200:
        print(f"... {len(backup_hits) - 200} more omitted")

if missing_route_refs or missing_jinja_refs:
    sys.exit(1)
