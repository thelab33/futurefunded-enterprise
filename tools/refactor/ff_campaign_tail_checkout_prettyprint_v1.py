from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"

if not TEMPLATE.exists():
    raise SystemExit(f"Missing template: {TEMPLATE}")

src = TEMPLATE.read_text(encoding="utf-8")
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = TEMPLATE.with_name(f"{TEMPLATE.name}.{timestamp}.bak")
shutil.copy2(TEMPLATE, backup)

updated = src
applied = []

def pretty_segment(segment: str) -> str:
    s = segment

    # Split collapsed HTML tags
    s = re.sub(r'>\s*<', '>\n<', s)

    # Split HTML and Jinja boundaries
    s = re.sub(r'>\s*({%|{{)', r'>\n\1', s)
    s = re.sub(r'(%}|}})\s*<', r'\1\n<', s)

    # Split consecutive Jinja blocks a bit more readably
    s = re.sub(r'(%})\s*({%)', r'\1\n\2', s)
    s = re.sub(r'(}})\s*({%)', r'\1\n\2', s)

    # Reduce excessive blank lines
    s = re.sub(r'\n{3,}', '\n\n', s).strip() + '\n'
    return s

# ------------------------------------------------------------------
# Pretty-print footer -> tabs tail cluster
# ------------------------------------------------------------------
footer_start = updated.find('<footer id="footer"')
checkout_start = updated.find('<section id="checkout"')

if footer_start != -1 and checkout_start != -1 and checkout_start > footer_start:
    tail = updated[footer_start:checkout_start]
    pretty_tail = pretty_segment(tail)
    if pretty_tail != tail:
        updated = updated[:footer_start] + pretty_tail + '\n' + updated[checkout_start:]
        applied.append("footer/tabs tail pretty-print")

# ------------------------------------------------------------------
# Pretty-print checkout cluster
# ------------------------------------------------------------------
checkout_start = updated.find('<section id="checkout"')
if checkout_start != -1:
    end_markers = [
        '<section id="terms"',
        '<section id="privacy"',
        '<section id="sponsor-interest"',
        '<section id="video"',
        '<button type="button" class="ff-floatingDonate',
        '<button\n  type="button"\n  class="ff-floatingDonate',
    ]
    end_positions = [updated.find(marker, checkout_start + 1) for marker in end_markers]
    end_positions = [p for p in end_positions if p != -1]

    if end_positions:
        checkout_end = min(end_positions)
        checkout = updated[checkout_start:checkout_end]
        pretty_checkout = pretty_segment(checkout)
        if pretty_checkout != checkout:
            updated = updated[:checkout_start] + pretty_checkout + '\n' + updated[checkout_end:]
            applied.append("checkout pretty-print")

# ------------------------------------------------------------------
# Minor top-shell readability touch
# ------------------------------------------------------------------
updated = updated.replace(
    '<div class="ff-shell" data-ff-shell="">\n    <div class="ff-shellBg" aria-hidden="true"></div>\n<header class="ff-chrome" data-ff-chrome="">',
    '<div class="ff-shell" data-ff-shell="">\n    <div class="ff-shellBg" aria-hidden="true"></div>\n\n<header class="ff-chrome" data-ff-chrome="">'
)
if updated != src and "top shell spacing" not in applied:
    if '<div class="ff-shell" data-ff-shell="">\n    <div class="ff-shellBg" aria-hidden="true"></div>\n\n<header class="ff-chrome" data-ff-chrome="">' in updated:
        applied.append("top shell spacing")

# Final whitespace cleanup
updated = re.sub(r'[ \t]+\n', '\n', updated)
updated = re.sub(r'\n{4,}', '\n\n\n', updated)

if updated == src:
    print("== FF CAMPAIGN TAIL + CHECKOUT PRETTYPRINT V1 ==")
    print(f"backup: {backup}")
    print("No formatting changes were needed.")
    raise SystemExit(0)

TEMPLATE.write_text(updated, encoding="utf-8")

print("== FF CAMPAIGN TAIL + CHECKOUT PRETTYPRINT V1 ==")
print(f"backup: {backup}")
print("applied:")
for item in applied:
    print(f" - {item}")
print("done.")
