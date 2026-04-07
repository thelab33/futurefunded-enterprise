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

SECTION_START_RE = re.compile(r'<section\b[^>]*\bid="ff-onboarding"\b[^>]*>', re.IGNORECASE)
SECTION_TAG_RE = re.compile(r'</?section\b[^>]*>', re.IGNORECASE)

def find_balanced_section_bounds(text: str, start_match: re.Match[str]) -> tuple[int, int]:
    start = start_match.start()
    depth = 0
    found_first = False

    for m in SECTION_TAG_RE.finditer(text, start):
        token = m.group(0).lower()

        if token.startswith("</section"):
            depth -= 1
            if found_first and depth == 0:
                return start, m.end()
        else:
            depth += 1
            found_first = True

    raise RuntimeError('Could not find balanced closing </section> for #ff-onboarding block')

section_match = SECTION_START_RE.search(src)
if not section_match:
    raise SystemExit('Could not find <section id="ff-onboarding"...> block')

block_start, block_end = find_balanced_section_bounds(src, section_match)

replacement = """
<!-- FF_CAMPAIGN_ONBOARDING_ROUTE_BRIDGE_V1 -->
<section
  id="ff-onboarding"
  hidden
  aria-hidden="true"
  data-ff-launch-route="/platform/onboarding"
></section>
<!-- /FF_CAMPAIGN_ONBOARDING_ROUTE_BRIDGE_V1 -->
""".strip()

updated = src[:block_start] + replacement + src[block_end:]

anchor_re = re.compile(r'<a\b[^>]*data-ff-open-onboard=""[^>]*>', re.IGNORECASE)

def rewrite_onboard_anchor(match: re.Match[str]) -> str:
    tag = match.group(0)

    tag = re.sub(r'\sdata-ff-open-onboard=""', '', tag, flags=re.IGNORECASE)
    tag = re.sub(r'\shref="#ff-onboarding"', ' href="/platform/onboarding"', tag, flags=re.IGNORECASE)
    tag = re.sub(r'\saria-controls="ff-onboarding"', '', tag, flags=re.IGNORECASE)
    tag = re.sub(r'\saria-haspopup="dialog"', '', tag, flags=re.IGNORECASE)

    if 'href=' not in tag:
        tag = tag[:-1] + ' href="/platform/onboarding">'

    return tag

updated, rewritten_anchor_count = anchor_re.subn(rewrite_onboard_anchor, updated)

# Fallback cleanup for any leftover literal references.
updated = re.sub(r'href="#ff-onboarding"', 'href="/platform/onboarding"', updated, flags=re.IGNORECASE)
updated = re.sub(r'\sdata-ff-open-onboard=""', '', updated, flags=re.IGNORECASE)

# Remove dialog semantics only when directly tied to onboarding anchors still pointing to the route.
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

remaining_modal_hooks = len(re.findall(r'data-ff-onboard-(modal|form|step|next|prev|finish|copy|email|close)', updated, flags=re.IGNORECASE))
remaining_open_triggers = len(re.findall(r'data-ff-open-onboard=""', updated, flags=re.IGNORECASE))
remaining_hash_links = len(re.findall(r'href="#ff-onboarding"', updated, flags=re.IGNORECASE))
route_links = len(re.findall(r'href="/platform/onboarding"', updated, flags=re.IGNORECASE))

print("== FF CAMPAIGN ONBOARDING ROUTE CUTOVER V1 ==")
print(f"backup: {backup}")
print(f"rewritten onboarding CTA anchors: {rewritten_anchor_count}")
print(f"remaining onboard modal hooks in template: {remaining_modal_hooks}")
print(f"remaining data-ff-open-onboard triggers: {remaining_open_triggers}")
print(f"remaining #ff-onboarding href links: {remaining_hash_links}")
print(f"/platform/onboarding links now present: {route_links}")
print("done.")
