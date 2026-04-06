from __future__ import annotations

from pathlib import Path
import json
import re
from collections import defaultdict

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"
CSS = ROOT / "apps/web/app/static/css/ff.css"
AUDIT = ROOT / "tools/audit/ff_css_contract_audit_v1.json"

OUT_DIR = ROOT / "tools/audit"
MANIFEST = OUT_DIR / "ff_css_rewrite_manifest.md"
SKELETON = OUT_DIR / "ff_css_authority_skeleton.css"
MISSING_CLASSES = OUT_DIR / "ff_css_missing_classes.txt"
DEAD_CLASSES = OUT_DIR / "ff_css_dead_classes.txt"
DEAD_IDS = OUT_DIR / "ff_css_dead_ids.txt"
SECTION_MAP = OUT_DIR / "ff_css_section_class_map.json"

html = TEMPLATE.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")
audit = json.loads(AUDIT.read_text(encoding="utf-8"))

def uniq(seq):
    return sorted(set(seq))

def section_chunks(src: str):
    pattern = re.compile(
        r'(<section\b[^>]*\bid="([^"]+)"[^>]*>)(.*?)(</section>)',
        flags=re.S | re.I
    )
    return [(m.group(2), m.group(0)) for m in pattern.finditer(src)]

def extract_classes(fragment: str):
    attrs = re.findall(r'class="([^"]+)"', fragment, flags=re.S)
    out = []
    for attr in attrs:
        for token in attr.split():
            token = token.strip()
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", token):
                out.append(token)
    return uniq(out)

def extract_ids(fragment: str):
    return uniq([
        x for x in re.findall(r'id="([^"]+)"', fragment)
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", x)
    ])

def first_present(items, prefixes):
    ranked = []
    for item in items:
        score = 999
        for idx, prefix in enumerate(prefixes):
            if item.startswith(prefix):
                score = idx
                break
        ranked.append((score, item))
    ranked.sort(key=lambda x: (x[0], x[1]))
    return [x[1] for x in ranked]

missing_classes = audit["missing_in_css"]["classes"]
dead_classes = audit["dead_in_css"]["classes"]
dead_ids = audit["dead_in_css"]["ids"]

sections = section_chunks(html)
section_map = {}

for sec_id, frag in sections:
    sec_classes = extract_classes(frag)
    sec_ids = extract_ids(frag)
    ff_classes = [c for c in sec_classes if c.startswith("ff-") or c.startswith("ff")]
    section_map[sec_id] = {
        "class_count": len(sec_classes),
        "id_count": len(sec_ids),
        "classes": ff_classes,
        "ids": sec_ids,
        "missing_classes_in_this_section": sorted([c for c in ff_classes if c in missing_classes]),
    }

# global families for scaffolding
all_html_classes = audit["all_html_contract"]["classes"]
ff_classes = [c for c in all_html_classes if c.startswith("ff-") or c.startswith("ff")]
family_prefixes = [
    "ff-topbar", "ff-progress", "ff-hero", "ff-story", "ff-team", "ff-player",
    "ff-sponsor", "ff-checkout", "ff-drawer", "ff-sheet", "ff-modal",
    "ff-faq", "ff-footer", "ff-button", "ff-pill", "ff-card", "ff-stat",
    "ff-trust", "ff-tabs", "ff-gallery", "ff-video"
]
ranked_classes = first_present(ff_classes, family_prefixes)

MISSING_CLASSES.write_text("\n".join(missing_classes) + ("\n" if missing_classes else ""), encoding="utf-8")
DEAD_CLASSES.write_text("\n".join(dead_classes) + ("\n" if dead_classes else ""), encoding="utf-8")
DEAD_IDS.write_text("\n".join(dead_ids) + ("\n" if dead_ids else ""), encoding="utf-8")
SECTION_MAP.write_text(json.dumps(section_map, indent=2), encoding="utf-8")

manifest = f"""# FF CSS Rewrite Manifest

## Inputs
- Template: `{TEMPLATE}`
- CSS: `{CSS}`
- Audit: `{AUDIT}`

## Audit summary
- HTML classes: {audit["counts"]["html_classes"]}
- HTML ids: {audit["counts"]["html_ids"]}
- HTML hooks: {audit["counts"]["html_hooks"]}
- CSS class candidates: {audit["counts"]["css_class_candidates"]}
- CSS id candidates: {audit["counts"]["css_id_candidates"]}
- CSS hook candidates: {audit["counts"]["css_hook_candidates"]}

## Delta summary
- Missing CSS classes: {len(missing_classes)}
- Missing CSS ids: {len(audit["missing_in_css"]["ids"])}
- Missing CSS hooks: {len(audit["missing_in_css"]["hooks"])}
- Dead CSS classes: {len(dead_classes)}
- Dead CSS ids: {len(dead_ids)}
- Missing JS hooks: {len(audit["missing_in_js"]["hooks"])}

## Interpretation
This is a good candidate for a full authority rewrite.
The contract is mostly intact.
Main tasks:
1. Style the remaining missing classes
2. Remove dead selector drift
3. Reorganize CSS by section
4. Preserve existing hook contract and modal/drawer/checkout semantics
5. Re-run audit after rewrite

## Missing CSS classes
{chr(10).join(f"- `{c}`" for c in missing_classes) if missing_classes else "- None"}

## Dead CSS classes
{chr(10).join(f"- `{c}`" for c in dead_classes) if dead_classes else "- None"}

## Dead CSS ids
{chr(10).join(f"- `{i}`" for i in dead_ids) if dead_ids else "- None"}

## Sections discovered
{chr(10).join(f"- `{sid}` — {section_map[sid]['class_count']} classes / {section_map[sid]['id_count']} ids / {len(section_map[sid]['missing_classes_in_this_section'])} missing classes"
              for sid in section_map)}
"""
MANIFEST.write_text(manifest, encoding="utf-8")

skeleton_parts = []
skeleton_parts.append("""/*!
 * FutureFunded — ff.css
 * Authority skeleton generated from current campaign contract
 * Fill this file during the rewrite and keep selectors aligned to index.html
 */

/* =========================================
   01. TOKENS
========================================= */

/* =========================================
   02. RESET / BASE
========================================= */

/* =========================================
   03. APP SHELL
========================================= */

html.ff-root {}
body[data-ff-page="fundraiser"] {}

/* =========================================
   04. TOPBAR / CHROME
========================================= */

/* =========================================
   05. HERO / ABOVE THE FOLD
========================================= */

/* =========================================
   06. STORY / MISSION
========================================= */

/* =========================================
   07. TEAM / PLAYERS / ROSTER
========================================= */

/* =========================================
   08. SPONSORS / PARTNERS
========================================= */

/* =========================================
   09. DONATION / CHECKOUT / AMOUNT UI
========================================= */

/* =========================================
   10. DRAWERS / MODALS / SHEETS
========================================= */

/* =========================================
   11. FAQ / TRUST / END CAP
========================================= */

/* =========================================
   12. FOOTER
========================================= */

/* =========================================
   13. UTILITIES / STATES
========================================= */

/* =========================================
   14. DARK MODE
========================================= */

/* =========================================
   15. RESPONSIVE
========================================= */
""")

for sec_id, meta in section_map.items():
    section_header = f"\n/* ===== SECTION: {sec_id} ===== */\n"
    skeleton_parts.append(section_header)
    for cls in meta["classes"]:
        skeleton_parts.append(f".{cls} {{}}\n")
    for _id in meta["ids"]:
        skeleton_parts.append(f"#{_id} {{}}\n")

SKELETON.write_text("".join(skeleton_parts), encoding="utf-8")

print("== FF CSS REWRITE PREP V1 ==")
print("template :", TEMPLATE)
print("css      :", CSS)
print("audit    :", AUDIT)
print()
print("wrote:")
for p in [MANIFEST, SKELETON, MISSING_CLASSES, DEAD_CLASSES, DEAD_IDS, SECTION_MAP]:
    print(" -", p)
print()
print("summary:")
print(" - missing css classes:", len(missing_classes))
print(" - dead css classes   :", len(dead_classes))
print(" - dead css ids       :", len(dead_ids))
print(" - sections mapped    :", len(section_map))
