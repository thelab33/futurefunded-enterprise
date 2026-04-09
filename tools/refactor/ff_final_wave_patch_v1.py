from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"
CSS = ROOT / "apps/web/app/static/css/ff.css"


def backup(path: Path) -> None:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(path, path.with_name(f"{path.name}.{ts}.bak"))


# ---------------------------------------------------------------------
# 1) campaign/index.html — null-safe asset version fallback
# ---------------------------------------------------------------------
template_text = TEMPLATE.read_text(encoding="utf-8")

old = "{% if not _asset_v %}"
new = "{% if (not _asset_v) or (_asset_v|lower in ['none', 'null', 'dev']) %}"

if old not in template_text:
    raise SystemExit("Could not find asset fallback condition in campaign/index.html")

backup(TEMPLATE)
template_text = template_text.replace(old, new, 1)
TEMPLATE.write_text(template_text, encoding="utf-8")
print("changed: campaign/index.html asset fallback made null-safe")


# ---------------------------------------------------------------------
# 2) ff.css — compress teams proof mini slab
# ---------------------------------------------------------------------
BLOCK = r'''
/* ==========================================================================
   FF_CAMPAIGN_TEAMS_PROOFMINI_COMPRESSION_V1
   - compress oversized teams proof mini slab
   - reduce dead air above team cards
   ========================================================================== */

body[data-ff-page="fundraiser"] .ff-proofMini--teams {
  min-height: clamp(8.5rem, 16vw, 11.5rem);
  padding: clamp(0.9rem, 1.4vw, 1.1rem);
  gap: 0.65rem;
  border-radius: 1.15rem;
  align-content: start;
}

body[data-ff-page="fundraiser"] .ff-proofMini--teams .ff-proofMini__body,
body[data-ff-page="fundraiser"] .ff-proofMini--teams p {
  max-width: 66ch;
}

body[data-ff-page="fundraiser"] .ff-proofMini--teams .ff-proofMini__meta,
body[data-ff-page="fundraiser"] .ff-proofMini--teams .ff-proofMini__stats {
  margin-top: 0.25rem;
}

@media (max-width: 768px) {
  body[data-ff-page="fundraiser"] .ff-proofMini--teams {
    min-height: 6.5rem;
    padding: 0.85rem;
    gap: 0.45rem;
    border-radius: 1rem;
  }
}
'''

css_text = CSS.read_text(encoding="utf-8")

if "FF_CAMPAIGN_TEAMS_PROOFMINI_COMPRESSION_V1" not in css_text:
    backup(CSS)
    if css_text and not css_text.endswith("\n"):
        css_text += "\n"
    css_text += "\n" + BLOCK.strip() + "\n"
    CSS.write_text(css_text, encoding="utf-8")
    print("changed: ff.css teams proof mini compression block appended")
else:
    print("skip: teams proof mini compression block already present")
