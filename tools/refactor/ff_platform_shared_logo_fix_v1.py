from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
SHELL = ROOT / "apps/web/app/templates/platform/shells/marketing_base.html"
TOPBAR = ROOT / "apps/web/app/templates/shared/partials/_platform_topbar.html"
CSS = ROOT / "apps/web/app/static/css/platform-pages.css"

for p in (SHELL, TOPBAR, CSS):
    if not p.exists():
        raise SystemExit(f"Missing file: {p}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
for p in (SHELL, TOPBAR, CSS):
    shutil.copy2(p, p.with_name(f"{p.name}.{timestamp}.bak"))

# ------------------------------------------------------------------
# 1) marketing_base.html
# add a shared resolved platform logo variable + include in config
# ------------------------------------------------------------------
shell_src = SHELL.read_text(encoding="utf-8")

anchor = """{% if not _site_name %}
  {% set _site_name = 'FutureFunded' %}
{% endif %}

{% set _public_base_raw = (
"""
insert = """{% if not _site_name %}
  {% set _site_name = 'FutureFunded' %}
{% endif %}

{% set _platform_logo = (
  platform_logo_url
  |default(_cfg.get('FF_PLATFORM_LOGO_URL'), true)
  |default(_cfg.get('FF_LOGO_URL'), true)
  |default('', true)
)|string|trim %}

{% set _public_base_raw = (
"""
if anchor not in shell_src:
    raise SystemExit("Could not find _site_name anchor in marketing_base.html")
shell_src = shell_src.replace(anchor, insert, 1)

config_anchor = """  'brand': _brand,
  'title': _page_title,
"""
config_insert = """  'brand': _brand,
  'logo': _platform_logo,
  'title': _page_title,
"""
if config_anchor not in shell_src:
    raise SystemExit("Could not find _platform_config anchor in marketing_base.html")
shell_src = shell_src.replace(config_anchor, config_insert, 1)

SHELL.write_text(shell_src, encoding="utf-8")

# ------------------------------------------------------------------
# 2) _platform_topbar.html
# replace empty disc with actual logo-or-fallback rendering
# ------------------------------------------------------------------
topbar_src = TOPBAR.read_text(encoding="utf-8")

old = """<div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
  <a
    href="/platform/"
    class="ff-platformBrand ff-nounderline"
    aria-label="FutureFunded platform home"
  >
    <span class="ff-platformBrand__disc" aria-hidden="true"></span>
    <span class="ff-platformBrand__wordmark">
      <strong>FutureFunded</strong>
      <span class="ff-help ff-muted ff-platformBrand__subline">
        {{ 'Operator' if _platform_surface == 'operator' else 'Platform' }}
      </span>
    </span>
  </a>
"""

new = """{% set _platform_logo = (_platform_logo|default('', true))|string|trim %}

<div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
  <a
    href="/platform/"
    class="ff-platformBrand ff-nounderline"
    aria-label="FutureFunded platform home"
  >
    <span class="ff-platformBrand__disc" {% if not _platform_logo %}aria-hidden="true"{% endif %}>
      {% if _platform_logo %}
        <img
          class="ff-platformBrand__logo"
          src="{{ _platform_logo|e }}"
          alt=""
          loading="eager"
          decoding="async"
        />
      {% else %}
        <span class="ff-platformBrand__fallback" aria-hidden="true">FF</span>
      {% endif %}
    </span>
    <span class="ff-platformBrand__wordmark">
      <strong>FutureFunded</strong>
      <span class="ff-help ff-muted ff-platformBrand__subline">
        {{ 'Operator' if _platform_surface == 'operator' else 'Platform' }}
      </span>
    </span>
  </a>
"""
if old not in topbar_src:
    raise SystemExit("Could not find expected brand block in _platform_topbar.html")
topbar_src = topbar_src.replace(old, new, 1)

TOPBAR.write_text(topbar_src, encoding="utf-8")

# ------------------------------------------------------------------
# 3) platform-pages.css
# add fallback mark style if missing
# ------------------------------------------------------------------
css_src = CSS.read_text(encoding="utf-8")

marker = """  body[data-ff-template="platform"] .ff-platformBrand__logo {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: inherit;
  }
"""
addition = """  body[data-ff-template="platform"] .ff-platformBrand__logo {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: inherit;
  }

  body[data-ff-template="platform"] .ff-platformBrand__fallback {
    display: grid;
    place-items: center;
    width: 100%;
    height: 100%;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    color: #fff;
    background:
      radial-gradient(circle at 30% 25%, rgba(255, 255, 255, 0.18), transparent 52%),
      linear-gradient(180deg, rgba(249, 115, 22, 0.94), rgba(234, 88, 12, 0.88));
  }
"""
if marker not in css_src:
    raise SystemExit("Could not find platformBrand__logo marker in platform-pages.css")
css_src = css_src.replace(marker, addition, 1)

CSS.write_text(css_src, encoding="utf-8")

print("== FF PLATFORM SHARED LOGO FIX V1 ==")
print("patched:")
print(" -", SHELL)
print(" -", TOPBAR)
print(" -", CSS)
print("done.")
