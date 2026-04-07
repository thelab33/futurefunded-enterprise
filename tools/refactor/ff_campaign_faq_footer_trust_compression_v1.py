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
# FAQ trust compression
# ------------------------------------------------------------------

replace_if_present(
    """          <p class="ff-kicker ff-m-0">Support help</p>""",
    """          <p class="ff-kicker ff-m-0">Support questions</p>""",
    "faq kicker"
)

replace_if_present(
    """            Three quick answers before someone donates or reaches out about sponsorship.""",
    """            Three quick answers before someone donates or asks about sponsorship.""",
    "faq lead"
)

replace_if_present(
    """              Yes. Team-specific actions can preload checkout for the selected team while still supporting the shared season fund.""",
    """              Yes. Team-specific actions can preload checkout while still supporting the shared season fund.""",
    "faq answer team-specific"
)

replace_if_present(
    """              Yes. A confirmation receipt is sent to the email entered during checkout after payment succeeds.""",
    """              Yes. A receipt is sent to the email used at checkout after payment succeeds.""",
    "faq answer receipt"
)

replace_if_present(
    """              Sponsors can inquire through the sponsor path for tiered, custom, or in-kind support. Follow-up covers fit, visibility, and next steps.""",
    """              Sponsors can inquire for tiered, custom, or in-kind support. Follow-up covers fit, visibility, and next steps.""",
    "faq answer sponsorships"
)

replace_if_present(
    """          Secure checkout • Email receipt • Sponsor-friendly follow-up.""",
    """          Secure checkout • Email receipt • Clear sponsor follow-up.""",
    "faq trust cue"
)

# ------------------------------------------------------------------
# Footer trust compression
# ------------------------------------------------------------------

replace_if_present(
    """            Support helps cover travel, training, tournaments, and season costs.""",
    """            Support helps cover travel, training, tournaments, and core season costs.""",
    "footer brand copy"
)

replace_if_present(
    """          <p class="ff-footerNav__title ff-kicker ff-m-0">Explore</p>""",
    """          <p class="ff-footerNav__title ff-kicker ff-m-0">Quick links</p>""",
    "footer nav title"
)

replace_if_present(
    """        <p class="ff-help ff-muted ff-m-0">Secure checkout • Email receipt</p>""",
    """        <p class="ff-help ff-muted ff-m-0">Secure checkout • Email receipt • Sponsor-ready</p>""",
    "footer trust line"
)

if updated == src:
    print("== FF CAMPAIGN FAQ + FOOTER TRUST COMPRESSION V1 ==")
    print(f"backup: {backup}")
    print("No FAQ/footer trust changes were needed.")
    raise SystemExit(0)

TEMPLATE.write_text(updated, encoding="utf-8")

print("== FF CAMPAIGN FAQ + FOOTER TRUST COMPRESSION V1 ==")
print(f"backup: {backup}")
print("applied:")
for item in applied:
    print(f" - {item}")
print("done.")
