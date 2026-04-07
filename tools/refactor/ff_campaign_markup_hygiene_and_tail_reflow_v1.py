from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"

if not TEMPLATE.exists():
    raise SystemExit(f"Missing template: {TEMPLATE}")

src = TEMPLATE.read_text(encoding="utf-8")
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = TEMPLATE.with_name(f"{TEMPLATE.name}.{timestamp}.bak")
shutil.copy2(TEMPLATE, backup)

updated = src

# ------------------------------------------------------------------
# Patch 01: remove editorial/developer slice comments from production markup
# ------------------------------------------------------------------
updated = re.sub(
    r"""\n\s*\{#\s*============================================================================\n\s*SLICE A — Chrome / Drawer / Hero / Donate Panel\n\s*Replace from <header class="ff-chrome"\.\.\.> through the closing </section> of #home\n\s*============================================================================\s*#\}\n+""",
    "\n",
    updated,
    flags=re.MULTILINE,
)

# Normalize head/body spacing
updated = updated.replace("</head>  \n  <body", "</head>\n<body")
updated = updated.replace("</head>  \r\n  <body", "</head>\n<body")

# ------------------------------------------------------------------
# Patch 02: reflow footer/tabs/checkout cluster if it got minified
# ------------------------------------------------------------------
footer_start = updated.find('<footer id="footer"')
checkout_start = updated.find('<section id="checkout"')

if footer_start != -1 and checkout_start != -1 and checkout_start > footer_start:
    segment = updated[footer_start:checkout_start]

    # Expand minified tag boundaries into readable block form.
    segment = re.sub(r'>\s*<', '>\n<', segment)

    # Put blank lines before major block roots.
    major_tags = [
        r'<footer\b',
        r'<a\b[^>]*class="ff-backtotop',
        r'<nav\b[^>]*class="ff-tabs',
    ]
    for pat in major_tags:
        segment = re.sub(pat, lambda m: '\n' + m.group(0), segment)

    # Clean excessive blank lines
    segment = re.sub(r'\n{3,}', '\n\n', segment).strip() + '\n\n'
    updated = updated[:footer_start] + segment + updated[checkout_start:]

# Reflow checkout sheet opener region if it is collapsed
checkout_start = updated.find('<section id="checkout"')
if checkout_start != -1:
    # Prefer to stop at terms modal, else privacy, else sponsor-interest, else floating donate.
    tail_markers = [
        '<section id="terms"',
        '<section id="privacy"',
        '<section id="sponsor-interest"',
        '<button\n  type="button"\n  class="ff-floatingDonate',
        '<button type="button" class="ff-floatingDonate',
    ]
    end_candidates = [updated.find(marker, checkout_start + 1) for marker in tail_markers]
    end_candidates = [pos for pos in end_candidates if pos != -1]

    if end_candidates:
        checkout_end = min(end_candidates)
        checkout_segment = updated[checkout_start:checkout_end]
        checkout_segment = re.sub(r'>\s*<', '>\n<', checkout_segment)
        checkout_segment = re.sub(r'\n{3,}', '\n\n', checkout_segment).strip() + '\n\n'
        updated = updated[:checkout_start] + checkout_segment + updated[checkout_end:]

# Final whitespace cleanup
updated = re.sub(r'[ \t]+\n', '\n', updated)
updated = re.sub(r'\n{4,}', '\n\n\n', updated)

if updated == src:
    raise SystemExit("No changes applied; template may already be normalized")

TEMPLATE.write_text(updated, encoding="utf-8")

print("== FF CAMPAIGN MARKUP HYGIENE + TAIL REFLOW V1 ==")
print(f"backup: {backup}")
print("done.")
