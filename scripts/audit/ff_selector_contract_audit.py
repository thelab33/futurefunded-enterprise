from __future__ import annotations

from pathlib import Path
import json
import re
from collections import Counter, defaultdict

ROOT = Path(".")
INDEX = ROOT / "apps/web/app/templates/campaign/index.html"
CSS_MAIN = ROOT / "apps/web/app/static/css/ff.css"
CSS_SHIM = ROOT / "apps/web/app/static/css/ff-above-main-premium.css"

if not INDEX.exists():
    raise SystemExit(f"❌ Missing index template: {INDEX}")

text = INDEX.read_text(encoding="utf-8", errors="replace")

id_re = re.compile(r'\bid="([^"]+)"')
class_re = re.compile(r'\bclass="([^"]+)"')
data_ff_re = re.compile(r'\b(data-ff-[a-zA-Z0-9_-]+)\b')
aria_controls_re = re.compile(r'\baria-controls="([^"]+)"')
href_hash_re = re.compile(r'\bhref="#([^"]+)"')

ids = id_re.findall(text)
classes = []
for raw in class_re.findall(text):
    classes.extend([c for c in raw.split() if c.strip()])

data_ff = data_ff_re.findall(text)
aria_controls = aria_controls_re.findall(text)
href_hashes = href_hash_re.findall(text)

selector_json_match = re.search(
    r'<script id="ffSelectors"[^>]*>\s*(\{.*?\})\s*</script>',
    text,
    re.S
)
selector_hooks = {}
selector_hook_values = []

if selector_json_match:
    raw_json = selector_json_match.group(1)
    try:
        parsed = json.loads(raw_json)
        selector_hooks = parsed.get("hooks", {})
        selector_hook_values = list(selector_hooks.values())
    except Exception as e:
        print(f"❌ Could not parse ffSelectors JSON: {e}")

all_ids = Counter(ids)
dupe_ids = [k for k, v in all_ids.items() if v > 1]

declared_targets = set(ids)
missing_aria_targets = sorted(set(aria_controls) - declared_targets)
missing_href_targets = sorted(set(href_hashes) - declared_targets)

css_texts = {}
for p in [CSS_MAIN, CSS_SHIM]:
    if p.exists():
        css_texts[str(p)] = p.read_text(encoding="utf-8", errors="replace")

selector_presence = defaultdict(dict)
for sel in selector_hook_values:
    for path, css in css_texts.items():
        selector_presence[sel][path] = sel in css or any(
            token in css for token in re.findall(r'[#.\[][^\s>+~:,]+', sel)
        )

print("== FF SELECTOR CONTRACT AUDIT ==")
print(f"Template: {INDEX}")
print(f"IDs: {len(ids)}")
print(f"Classes: {len(classes)}")
print(f"Unique classes: {len(set(classes))}")
print(f"data-ff hooks: {len(data_ff)}")
print(f"Unique data-ff hooks: {len(set(data_ff))}")
print(f"aria-controls refs: {len(aria_controls)}")
print(f"href hash refs: {len(href_hashes)}")
print(f"ffSelectors hooks: {len(selector_hooks)}")
print()

print("== DUPLICATE IDS ==")
if dupe_ids:
    for i in dupe_ids:
        print("❌", i)
else:
    print("✅ none")
print()

print("== MISSING aria-controls TARGETS ==")
if missing_aria_targets:
    for t in missing_aria_targets:
        print("❌", t)
else:
    print("✅ none")
print()

print("== MISSING href=\"#...\" TARGETS ==")
if missing_href_targets:
    for t in missing_href_targets:
        print("❌", t)
else:
    print("✅ none")
print()

print("== ffSelectors HOOKS ==")
for k, v in selector_hooks.items():
    print(f"- {k}: {v}")
print()

print("== ffSelectors PRESENCE IN CSS ==")
for sel, status in selector_presence.items():
    row = " | ".join(
        f"{Path(path).name}: {'✅' if ok else '⚠️'}"
        for path, ok in status.items()
    )
    print(f"{sel} -> {row}")

print()
print("== TOP data-ff HOOKS ==")
for k, v in Counter(data_ff).most_common(40):
    print(f"{k}: {v}")

print()
print("== TOP CLASSES ==")
for k, v in Counter(classes).most_common(50):
    print(f"{k}: {v}")
