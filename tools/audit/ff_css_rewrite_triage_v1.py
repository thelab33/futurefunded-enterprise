from __future__ import annotations

from pathlib import Path
from collections import defaultdict, Counter
import json
import re

ROOT = Path.home() / "futurefunded-enterprise"
AUDIT = ROOT / "tools/audit/ff_css_contract_audit_v1.json"
SECTION_MAP = ROOT / "tools/audit/ff_css_section_class_map.json"
OUT_MD = ROOT / "tools/audit/ff_css_rewrite_triage.md"
OUT_JSON = ROOT / "tools/audit/ff_css_rewrite_triage.json"

audit = json.loads(AUDIT.read_text(encoding="utf-8"))
section_map = json.loads(SECTION_MAP.read_text(encoding="utf-8"))

missing_classes = set(audit["missing_in_css"]["classes"])
dead_classes = audit["dead_in_css"]["classes"]
dead_ids = audit["dead_in_css"]["ids"]

def family_of(name: str) -> str:
    if name.startswith("ff-"):
        parts = name.split("-")
        return "-".join(parts[:2]) if len(parts) >= 2 else name
    if name.startswith("ff"):
        m = re.match(r"(ff[A-Z][a-zA-Z0-9]*)", name)
        if m:
            return m.group(1)
        return "ff-misc"
    return "misc"

# -----------------------------
# missing classes by section
# -----------------------------
section_missing = []
for sec_id, meta in section_map.items():
    hits = sorted(set(meta.get("missing_classes_in_this_section", [])))
    section_missing.append({
        "section_id": sec_id,
        "missing_count": len(hits),
        "missing_classes": hits,
        "class_count": meta.get("class_count", 0),
        "id_count": meta.get("id_count", 0),
    })

section_missing.sort(key=lambda x: (-x["missing_count"], x["section_id"]))

# -----------------------------
# dead selector families
# -----------------------------
dead_class_families = Counter(family_of(c) for c in dead_classes)
dead_id_families = Counter(family_of(i) for i in dead_ids)

# -----------------------------
# rewrite order heuristic
# -----------------------------
priority_order = []
for item in section_missing:
    sid = item["section_id"]
    sid_lower = sid.lower()
    if any(k in sid_lower for k in ["hero", "top", "chrome", "header"]):
        bucket = 1
    elif any(k in sid_lower for k in ["story", "mission", "team", "roster", "players", "sponsor"]):
        bucket = 2
    elif any(k in sid_lower for k in ["checkout", "drawer", "modal", "faq", "footer"]):
        bucket = 3
    else:
        bucket = 2
    priority_order.append((bucket, -item["missing_count"], sid))

priority_order = [sid for _, _, sid in sorted(priority_order)]

report = {
    "summary": {
        "missing_css_classes": len(missing_classes),
        "dead_css_classes": len(dead_classes),
        "dead_css_ids": len(dead_ids),
        "sections": len(section_map),
    },
    "sections_by_missing_class_count": section_missing,
    "dead_class_families": dict(dead_class_families.most_common()),
    "dead_id_families": dict(dead_id_families.most_common()),
    "recommended_rewrite_order": priority_order,
}

OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

lines = []
lines.append("# FF CSS Rewrite Triage\n")
lines.append("## Summary")
lines.append(f"- Missing CSS classes: {len(missing_classes)}")
lines.append(f"- Dead CSS classes: {len(dead_classes)}")
lines.append(f"- Dead CSS ids: {len(dead_ids)}")
lines.append(f"- Sections mapped: {len(section_map)}")
lines.append("")

lines.append("## Recommended rewrite order")
for i, sid in enumerate(priority_order, 1):
    lines.append(f"{i}. `{sid}`")
lines.append("")

lines.append("## Sections by missing class count")
for item in section_missing:
    lines.append(
        f"- `{item['section_id']}` — {item['missing_count']} missing classes "
        f"({item['class_count']} classes / {item['id_count']} ids)"
    )
    for cls in item["missing_classes"]:
        lines.append(f"  - `{cls}`")
lines.append("")

lines.append("## Dead class families")
for fam, count in dead_class_families.most_common():
    lines.append(f"- `{fam}` — {count}")
lines.append("")

lines.append("## Dead id families")
for fam, count in dead_id_families.most_common():
    lines.append(f"- `{fam}` — {count}")

OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("== FF CSS REWRITE TRIAGE V1 ==")
print("audit      :", AUDIT)
print("section map:", SECTION_MAP)
print()
print("wrote:")
print(" -", OUT_MD)
print(" -", OUT_JSON)
print()
print("summary:")
print(" - missing css classes:", len(missing_classes))
print(" - dead css classes   :", len(dead_classes))
print(" - dead css ids       :", len(dead_ids))
print(" - sections           :", len(section_map))
print()
print("top rewrite order:")
for i, sid in enumerate(priority_order[:8], 1):
    print(f" {i}. {sid}")
