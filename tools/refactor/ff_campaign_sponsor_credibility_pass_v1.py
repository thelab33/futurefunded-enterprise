from __future__ import annotations

from pathlib import Path
from datetime import datetime
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
applied = []

def replace_if_present(old: str, new: str, label: str) -> None:
    global updated
    if old in updated:
        updated = updated.replace(old, new, 1)
        applied.append(label)

# ------------------------------------------------------------------
# Sponsor section copy tightening
# ------------------------------------------------------------------

replace_if_present(
    """        <h2 class="ff-h2 ff-m-0" id="sponsorsTitle">Become a featured sponsor</h2>""",
    """        <h2 class="ff-h2 ff-m-0" id="sponsorsTitle">Become a season sponsor</h2>""",
    "sponsor section title"
)

replace_if_present(
    """          Support the program with structured recognition designed for local businesses and community partners.""",
    """          Support the season with structured recognition designed for local businesses and community partners.""",
    "sponsor section lead"
)

replace_if_present(
    """          Limited sponsor spots available this season • name or logo placement • sponsor-safe visibility""",
    """          Limited sponsor spots • name or logo placement • clean community visibility""",
    "sponsor section hint"
)

replace_if_present(
    """            <h3 class="ff-h3 ff-mt-1 ff-mb-0" id="sponsorWallTitle">
              Featured recognition preview
            </h3>""",
    """            <h3 class="ff-h3 ff-mt-1 ff-mb-0" id="sponsorWallTitle">
              Featured sponsor visibility
            </h3>""",
    "sponsor wall title"
)

replace_if_present(
    """              Approved partners can appear here with structured placement and a clean first impression.""",
    """              Approved sponsors can appear here with structured placement and a polished first impression.""",
    "sponsor wall description"
)

replace_if_present(
    """          <span class="ff-pill ff-pill--ghost">Add yours</span>""",
    """          <span class="ff-pill ff-pill--ghost">Open spot</span>""",
    "sponsor wall pill"
)

replace_if_present(
    """            Sponsor recognition opens here after approval.""",
    """            Approved sponsors appear here after confirmation.""",
    "sponsor empty state title"
)

replace_if_present(
    """            Featured placement preview • logo or business name • VIP spotlight rotation.""",
    """            Logo or business name • featured placement • VIP spotlight rotation.""",
    "sponsor empty state detail"
)

replace_if_present(
    """              Simple sponsor options with a clear fit and next step.""",
    """              Clear sponsor options with a practical fit and next step.""",
    "sponsor tier intro"
)

replace_if_present(
    """          <strong>Have a custom idea or in-kind support?</strong>""",
    """          <strong>Need a custom package or in-kind support?</strong>""",
    "sponsor callout title"
)

replace_if_present(
    """          Become a sponsor""",
    """          Sponsor the season""",
    "sponsor CTA label"
)

replace_if_present(
    """          Send to a business""",
    """          Share with a business""",
    "sponsor share CTA"
)

# ------------------------------------------------------------------
# Sponsor tier subtitle polish
# ------------------------------------------------------------------

replace_if_present(
    """'sub': 'Supporter tier'""",
    """'sub': 'Entry sponsor tier'""",
    "community tier subtitle"
)

replace_if_present(
    """'sub': 'Local business tier'""",
    """'sub': 'Recommended sponsor tier'""",
    "partner tier subtitle"
)

replace_if_present(
    """'sub': 'Featured support tier'""",
    """'sub': 'Growth sponsor tier'""",
    "champion tier subtitle"
)

replace_if_present(
    """'sub': 'Featured recognition'""",
    """'sub': 'Top visibility tier'""",
    "vip tier subtitle"
)

if updated == src:
    print("== FF CAMPAIGN SPONSOR CREDIBILITY PASS V1 ==")
    print(f"backup: {backup}")
    print("No sponsor copy changes were needed.")
    raise SystemExit(0)

TEMPLATE.write_text(updated, encoding="utf-8")

print("== FF CAMPAIGN SPONSOR CREDIBILITY PASS V1 ==")
print(f"backup: {backup}")
print("applied:")
for item in applied:
    print(f" - {item}")
print("done.")
