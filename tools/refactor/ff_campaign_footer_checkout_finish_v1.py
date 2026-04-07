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
applied: list[str] = []

def replace_if_present(old: str, new: str, label: str, replace_all: bool = False) -> None:
    global updated
    if old in updated:
        if replace_all:
            updated = updated.replace(old, new)
        else:
            updated = updated.replace(old, new, 1)
        applied.append(label)

# ------------------------------------------------------------------
# Footer trust closeout
# ------------------------------------------------------------------

replace_if_present(
    "Support helps cover travel, training, tournaments, and season costs.",
    "Support helps cover travel, training, tournaments, and core season costs.",
    "footer brand copy",
    replace_all=True,
)

replace_if_present(
    '<p class="ff-footerNav__title ff-kicker ff-m-0">Explore</p>',
    '<p class="ff-footerNav__title ff-kicker ff-m-0">Quick links</p>',
    "footer nav title",
)

replace_if_present(
    "Secure checkout • Email receipt</p>",
    "Secure checkout • Email receipt • Sponsor-ready</p>",
    "footer trust line",
)

replace_if_present(
    ">Become a sponsor<",
    ">Sponsor the season<",
    "lower sponsor CTA wording",
    replace_all=True,
)

# ------------------------------------------------------------------
# Checkout copy tightening
# ------------------------------------------------------------------

replace_if_present(
    "One clean support flow for families, donors, and sponsors.",
    "One clean support flow for families, donors, and community sponsors.",
    "checkout description",
)

replace_if_present(
    "Enter any whole-dollar amount and review it before payment.",
    "Enter any whole-dollar amount. You’ll review it before payment.",
    "checkout amount help",
)

replace_if_present(
    "Use the best email for confirmation and your receipt.",
    "Use the best email for your receipt and confirmation.",
    "checkout donor details help",
)

# ------------------------------------------------------------------
# Reflow footer -> tabs -> checkout tail cluster
# ------------------------------------------------------------------

footer_start = updated.find('<footer id="footer"')
checkout_start = updated.find('<section id="checkout"')

if footer_start != -1 and checkout_start != -1 and checkout_start > footer_start:
    tail = updated[footer_start:checkout_start]
    original_tail = tail

    tail = re.sub(r'>\s*<', '>\n<', tail)
    tail = re.sub(r'\n{3,}', '\n\n', tail).strip() + '\n\n'

    if tail != original_tail:
        updated = updated[:footer_start] + tail + updated[checkout_start:]
        applied.append("tail footer/tabs reflow")

# ------------------------------------------------------------------
# Reflow early checkout region for maintainability
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
        chunk = updated[checkout_start:checkout_end]
        original_chunk = chunk

        chunk = re.sub(r'>\s*<', '>\n<', chunk)
        chunk = re.sub(r'\n{3,}', '\n\n', chunk).strip() + '\n\n'

        if chunk != original_chunk:
            updated = updated[:checkout_start] + chunk + updated[checkout_end:]
            applied.append("checkout opener reflow")

# Global cleanup
updated = re.sub(r'[ \t]+\n', '\n', updated)
updated = re.sub(r'\n{4,}', '\n\n\n', updated)

if updated == src:
    print("== FF CAMPAIGN FOOTER + CHECKOUT FINISH V1 ==")
    print(f"backup: {backup}")
    print("No changes were needed.")
    raise SystemExit(0)

TEMPLATE.write_text(updated, encoding="utf-8")

print("== FF CAMPAIGN FOOTER + CHECKOUT FINISH V1 ==")
print(f"backup: {backup}")
print("applied:")
for item in applied:
    print(f" - {item}")
print("done.")
