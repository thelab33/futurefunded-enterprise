from __future__ import annotations

from pathlib import Path
import re
import json

ROOT = Path.home() / "futurefunded-enterprise"

TEMPLATE_FILES = [
    ROOT / "apps/web/app/templates/platform/shells/marketing_base.html",
    ROOT / "apps/web/app/templates/platform/shells/operator_base.html",
    ROOT / "apps/web/app/templates/platform/pages/home.html",
    ROOT / "apps/web/app/templates/platform/pages/pricing.html",
    ROOT / "apps/web/app/templates/platform/pages/demo.html",
    ROOT / "apps/web/app/templates/platform/pages/onboarding.html",
    ROOT / "apps/web/app/templates/platform/pages/dashboard.html",
    ROOT / "apps/web/app/templates/shared/partials/_platform_topbar.html",
    ROOT / "apps/web/app/templates/shared/partials/_platform_status_bar.html",
]

CSS_FILES = {
    "ff.css": ROOT / "apps/web/app/static/css/ff.css",
    "platform-pages.css": ROOT / "apps/web/app/static/css/platform-pages.css",
}

OUT = ROOT / "reports/platform-audit"
OUT.mkdir(parents=True, exist_ok=True)

CLASS_ATTR_RE = re.compile(r'class="([^"]+)"')
CSS_CLASS_RE = re.compile(r'\.([A-Za-z_][A-Za-z0-9_-]*)')
DATA_ATTR_RE = re.compile(r'data-ff-[a-z0-9_-]+')

PLATFORM_FAMILY_RE = re.compile(
    r'^(ff-platform|ff-proofMini|ff-navPill|ff-platformBrand|ff-platformGridTop|ff-platformChrome|ff-platformInlinePill)'
)

def normalize_classes(raw: str) -> list[str]:
    tokens = []
    for token in raw.split():
        token = token.strip()
        if not token:
            continue
        if "{{" in token or "{%" in token:
            continue
        tokens.append(token)
    return tokens

html_classes: set[str] = set()
html_data_attrs: set[str] = set()

for path in TEMPLATE_FILES:
    text = path.read_text(encoding="utf-8")
    for match in CLASS_ATTR_RE.finditer(text):
        html_classes.update(normalize_classes(match.group(1)))
    html_data_attrs.update(DATA_ATTR_RE.findall(text))

css_classes: dict[str, set[str]] = {}
for name, path in CSS_FILES.items():
    text = path.read_text(encoding="utf-8")
    css_classes[name] = set(CSS_CLASS_RE.findall(text))

all_css_classes = set().union(*css_classes.values())

platform_family_classes = sorted(c for c in html_classes if PLATFORM_FAMILY_RE.match(c))
missing_in_all = sorted(c for c in platform_family_classes if c not in all_css_classes)
owned_by_ff = sorted(c for c in platform_family_classes if c in css_classes["ff.css"] and c not in css_classes["platform-pages.css"])
owned_by_platform = sorted(c for c in platform_family_classes if c in css_classes["platform-pages.css"])
shared = sorted(c for c in platform_family_classes if c in css_classes["ff.css"] and c in css_classes["platform-pages.css"])

report = {
    "template_files": [str(p.relative_to(ROOT)) for p in TEMPLATE_FILES],
    "css_files": {k: str(v.relative_to(ROOT)) for k, v in CSS_FILES.items()},
    "platform_family_classes_in_html": platform_family_classes,
    "missing_platform_family_classes_in_all_css": missing_in_all,
    "platform_family_owned_by_ff_css_only": owned_by_ff,
    "platform_family_owned_by_platform_pages_css": owned_by_platform,
    "platform_family_shared_between_ff_and_platform_pages": shared,
    "platform_data_attrs_found": sorted(html_data_attrs),
    "counts": {
        "platform_family_html_classes": len(platform_family_classes),
        "missing_platform_family_classes_in_all_css": len(missing_in_all),
        "platform_family_owned_by_ff_css_only": len(owned_by_ff),
        "platform_family_owned_by_platform_pages_css": len(owned_by_platform),
        "platform_family_shared_between_ff_and_platform_pages": len(shared),
        "platform_data_attrs_found": len(html_data_attrs),
    },
}

json_path = OUT / "platform_css_contract_audit.json"
txt_path = OUT / "platform_css_contract_audit.txt"

json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

lines = []
lines.append("== PLATFORM CSS CONTRACT AUDIT ==")
lines.append("")
lines.append("Template files:")
for p in report["template_files"]:
    lines.append(f" - {p}")

lines.append("")
lines.append("CSS files:")
for k, v in report["css_files"].items():
    lines.append(f" - {k}: {v}")

lines.append("")
lines.append(f"Platform-family HTML classes: {report['counts']['platform_family_html_classes']}")
lines.append(f"Missing in all CSS: {report['counts']['missing_platform_family_classes_in_all_css']}")
lines.append(f"Owned by ff.css only: {report['counts']['platform_family_owned_by_ff_css_only']}")
lines.append(f"Owned by platform-pages.css: {report['counts']['platform_family_owned_by_platform_pages_css']}")
lines.append(f"Shared between both CSS files: {report['counts']['platform_family_shared_between_ff_and_platform_pages']}")
lines.append(f"data-ff-* attrs found: {report['counts']['platform_data_attrs_found']}")

lines.append("")
lines.append("-- Missing platform-family classes in all CSS --")
for item in missing_in_all or ["(none)"]:
    lines.append(f" - {item}")

lines.append("")
lines.append("-- Platform-family classes owned by ff.css only --")
for item in owned_by_ff or ["(none)"]:
    lines.append(f" - {item}")

lines.append("")
lines.append("-- Platform-family classes owned by platform-pages.css --")
for item in owned_by_platform or ["(none)"]:
    lines.append(f" - {item}")

lines.append("")
lines.append("-- Platform-family classes shared between ff.css and platform-pages.css --")
for item in shared or ["(none)"]:
    lines.append(f" - {item}")

lines.append("")
lines.append("-- data-ff-* attrs found in platform runtime --")
for item in sorted(html_data_attrs) or ["(none)"]:
    lines.append(f" - {item}")

txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(lines[0])
print(f"wrote: {json_path}")
print(f"wrote: {txt_path}")
print("")
for line in lines[8:]:
    print(line)
