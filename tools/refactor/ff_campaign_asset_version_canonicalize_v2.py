from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
TARGET = ROOT / "apps/web/app/templates/campaign/index.html"

if not TARGET.exists():
    raise SystemExit(f"Missing target file: {TARGET}")

lines = TARGET.read_text(encoding="utf-8").splitlines()


def find_index(predicate, start=0):
    for i in range(start, len(lines)):
        if predicate(lines[i]):
            return i
    return -1


# --- top asset-version block -------------------------------------------------
top_comment_idx = find_index(lambda s: "Build / asset version" in s)
ff_build_idx = find_index(lambda s: "{% set FF_BUILD_ID =" in s, top_comment_idx)
ff_version_idx = find_index(lambda s: "{% set FF_VERSION =" in s, ff_build_idx)
v_idx = find_index(lambda s: "{% set _v =" in s, ff_version_idx)

if min(top_comment_idx, ff_build_idx, ff_version_idx, v_idx) < 0:
    raise SystemExit("Could not locate top build/version anchors in campaign/index.html")

# Old block may have either:
#   {% if not _v %} ... {% endif %}
# or:
#   {% set _v = '1' %}
top_end_idx = find_index(
    lambda s: "{% endif %}" in s or "{% set _v = '1' %}" in s,
    v_idx,
)

if top_end_idx < 0:
    raise SystemExit("Could not locate end of top build/version block")

top_replacement = [
    "{# Build / asset version ---------------------------------------------------- #}",
    "{% set _asset_v = (",
    "  asset_v",
    "  |default(FF_ASSET_V|default(_cfg.get('FF_BUILD_ID'), true), true)",
    "  |default(_cfg.get('FF_VERSION'), true)",
    ")|string|trim %}",
    "{% if not _asset_v %}",
    "  {% set _asset_v = '1' %}",
    "{% endif %}",
    "{% set FF_BUILD_ID = (FF_BUILD_ID|default(_cfg.get('FF_BUILD_ID'), true)|default(_asset_v, true))|string|trim %}",
    "{% set FF_VERSION = (FF_VERSION|default(_cfg.get('FF_VERSION'), true)|default(_asset_v, true))|string|trim %}",
    "{% set _v = _asset_v %}",
]

lines[top_comment_idx : top_end_idx + 1] = top_replacement


# --- later asset-loader block ------------------------------------------------
asset_v_idx = find_index(lambda s: "{% set _asset_v = (" in s, 700)
sponsor_leads_idx = find_index(lambda s: "{% set _sponsor_leads_app =" in s, asset_v_idx)

if asset_v_idx < 0 or sponsor_leads_idx < 0:
    raise SystemExit("Could not locate later asset loader block in campaign/index.html")

asset_loader_replacement = [
    "{% set _ff_css_authority = url_for('static', filename='css/ff.css') ~ '?v=' ~ _asset_v %}",
    "{% set _ff_css_overrides = url_for('static', filename='css/ff-above-main-premium.css') ~ '?v=' ~ _asset_v %}",
    "{% set _app = url_for('static', filename='js/ff-app.js') ~ '?v=' ~ _asset_v %}",
    "{% set _sponsor_leads_app = url_for('static', filename='js/ff-sponsor-leads-v1.js') ~ '?v=' ~ _asset_v %}",
]

lines[asset_v_idx : sponsor_leads_idx + 1] = asset_loader_replacement

new_text = "\n".join(lines) + "\n"

ts = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_path = TARGET.with_name(f"{TARGET.name}.{ts}.bak")
shutil.copy2(TARGET, backup_path)
TARGET.write_text(new_text, encoding="utf-8")

print(f"changed: {TARGET}")
print(f"backup:  {backup_path}")
