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

# NOTE:
# v1 failed because it used a word-boundary after the closing quote in id="ff-onboarding".
# That can fail because the closing quote is not a word character.
OPEN_RE = re.compile(
    r'<section\b[^>]*id=["\']ff-onboarding["\'][^>]*>',
    re.IGNORECASE,
)

SECTION_TAG_RE = re.compile(r'</?section\b[^>]*>', re.IGNORECASE)

def find_balanced_section_bounds(text: str, start_match: re.Match[str]) -> tuple[int, int]:
    start = start_match.start()
    depth = 0
    seen_root = False

    for m in SECTION_TAG_RE.finditer(text, start):
        token = m.group(0).lower()
        if token.startswith("</section"):
            depth -= 1
            if seen_root and depth == 0:
                return start, m.end()
        else:
            depth += 1
            seen_root = True

    raise RuntimeError("Could not find balanced closing </section> for #ff-onboarding")

match = OPEN_RE.search(src)
if not match:
    idx = src.find('id="ff-onboarding"')
    if idx == -1:
        raise SystemExit('Could not find id="ff-onboarding" anywhere in template')
    snippet = src[max(0, idx - 240): idx + 240]
    raise SystemExit(
        "Found id=\"ff-onboarding\" but not a matching <section ...> opener.\n"
        "Nearby source snippet:\n"
        f"{snippet}"
    )

block_start, block_end = find_balanced_section_bounds(src, match)

replacement = """
<!-- FF_CAMPAIGN_ONBOARDING_ROUTE_BRIDGE_V2 -->
<section
  id="ff-onboarding"
  hidden
  aria-hidden="true"
  data-ff-launch-route="/platform/onboarding"
></section>
<!-- /FF_CAMPAIGN_ONBOARDING_ROUTE_BRIDGE_V2 -->
""".strip()

updated = src[:block_start] + replacement + src[block_end:]

# Rewrite only onboarding route triggers on anchors.
ANCHOR_TRIGGER_RE = re.compile(
    r'<a\b[^>]*data-ff-open-onboard=""[^>]*>',
    re.IGNORECASE,
)

def rewrite_anchor(tag: str) -> str:
    tag = re.sub(r'\sdata-ff-open-onboard=""', '', tag, flags=re.IGNORECASE)
    tag = re.sub(r'\shref="#ff-onboarding"', ' href="/platform/onboarding"', tag, flags=re.IGNORECASE)
    tag = re.sub(r'\saria-controls="ff-onboarding"', '', tag, flags=re.IGNORECASE)
    tag = re.sub(r'\saria-haspopup="dialog"', '', tag, flags=re.IGNORECASE)
    if 'href=' not in tag:
        tag = tag[:-1] + ' href="/platform/onboarding">'
    return tag

updated, anchor_count = ANCHOR_TRIGGER_RE.subn(lambda m: rewrite_anchor(m.group(0)), updated)

# Fallback cleanup for any leftover literal references.
updated = re.sub(r'href="#ff-onboarding"', 'href="/platform/onboarding"', updated, flags=re.IGNORECASE)
updated = re.sub(r'\sdata-ff-open-onboard=""', '', updated, flags=re.IGNORECASE)

# Remove dialog attrs only on onboarding route anchors.
updated = re.sub(
    r'(<a\b[^>]*href="/platform/onboarding"[^>]*?)\saria-controls="ff-onboarding"',
    r'\1',
    updated,
    flags=re.IGNORECASE,
)
updated = re.sub(
    r'(<a\b[^>]*href="/platform/onboarding"[^>]*?)\saria-haspopup="dialog"',
    r'\1',
    updated,
    flags=re.IGNORECASE,
)

if updated == src:
    raise SystemExit("No changes applied; template may already be cut over")

TEMPLATE.write_text(updated, encoding="utf-8")

remaining_open_triggers = len(re.findall(r'data-ff-open-onboard=""', updated, flags=re.IGNORECASE))
remaining_hash_links = len(re.findall(r'href="#ff-onboarding"', updated, flags=re.IGNORECASE))
route_links = len(re.findall(r'href="/platform/onboarding"', updated, flags=re.IGNORECASE))
stub_present = 'FF_CAMPAIGN_ONBOARDING_ROUTE_BRIDGE_V2' in updated

print("== FF CAMPAIGN ONBOARDING ROUTE CUTOVER V2 ==")
print(f"backup: {backup}")
print(f"rewritten onboarding CTA anchors: {anchor_count}")
print(f"remaining data-ff-open-onboard triggers: {remaining_open_triggers}")
print(f"remaining #ff-onboarding href links: {remaining_hash_links}")
print(f"/platform/onboarding links now present: {route_links}")
print(f"bridge stub present: {stub_present}")
print("done.")
