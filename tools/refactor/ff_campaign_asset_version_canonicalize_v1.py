from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
TARGET = ROOT / "apps/web/app/templates/campaign/index.html"

if not TARGET.exists():
    raise SystemExit(f"Missing target file: {TARGET}")

text = TARGET.read_text(encoding="utf-8")

top_pattern = re.compile(
    r"""
\{#\s*Build / asset version.*?\#\}\s*\n
\{% set FF_BUILD_ID = .*?\n
\{% set FF_VERSION = .*?\n
\{% set _v = .*?\n
(?:\{% if not _v %\}.*?\{% endif %\}\n|\s*\{% set _v = '1' %\}\n)
""",
    re.S | re.X,
)

top_replacement = """{# Build / asset version ---------------------------------------------------- #}
{% set _asset_v = (
  asset_v
  |default(FF_ASSET_V|default(_cfg.get('FF_BUILD_ID'), true), true)
  |default(_cfg.get('FF_VERSION'), true)
)|string|trim %}
{% if not _asset_v %}
  {% set _asset_v = '1' %}
{% endif %}
{% set FF_BUILD_ID = (FF_BUILD_ID|default(_cfg.get('FF_BUILD_ID'), true)|default(_asset_v, true))|string|trim %}
{% set FF_VERSION = (FF_VERSION|default(_cfg.get('FF_VERSION'), true)|default(_asset_v, true))|string|trim %}
{% set _v = _asset_v %}
"""

asset_loader_pattern = re.compile(
    r"""
\{% set _asset_v = \(.*?\)\|string\|trim %\}\s*\n
\{% set _ff_css_authority = url_for\('static', filename='css/ff\.css'\) ~ '\?v=' ~ _asset_v %\}\s*\n
\{% set _ff_css_overrides = url_for\('static', filename='css/ff-above-main-premium\.css'\) ~ '\?v=' ~ _asset_v %\}\s*\n
\{% set _app = url_for\('static', filename='js/ff-app\.js'\) ~ '\?v=' ~ _asset_v %\}\s*\n
\{% set _sponsor_leads_app = url_for\('static', filename='js/ff-sponsor-leads-v1\.js'\) ~ '\?v=' ~ _asset_v %\}
""",
    re.S | re.X,
)

asset_loader_replacement = """{% set _ff_css_authority = url_for('static', filename='css/ff.css') ~ '?v=' ~ _asset_v %}
{% set _ff_css_overrides = url_for('static', filename='css/ff-above-main-premium.css') ~ '?v=' ~ _asset_v %}
{% set _app = url_for('static', filename='js/ff-app.js') ~ '?v=' ~ _asset_v %}
{% set _sponsor_leads_app = url_for('static', filename='js/ff-sponsor-leads-v1.js') ~ '?v=' ~ _asset_v %}"""

new_text, n1 = top_pattern.subn(top_replacement, text, count=1)
if n1 != 1:
    raise SystemExit("Could not replace top build/version block in campaign/index.html")

new_text, n2 = asset_loader_pattern.subn(asset_loader_replacement, new_text, count=1)
if n2 != 1:
    raise SystemExit("Could not replace asset loader block in campaign/index.html")

ts = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_path = TARGET.with_name(f"{TARGET.name}.{ts}.bak")
shutil.copy2(TARGET, backup_path)
TARGET.write_text(new_text, encoding="utf-8")

print(f"changed: {TARGET}")
print(f"backup:  {backup_path}")
