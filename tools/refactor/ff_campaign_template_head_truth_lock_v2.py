from __future__ import annotations
from pathlib import Path
import re

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"

START_ANCHOR = "{% set _public_base_raw = ("
END_ANCHOR = "{% set _safe_email ="

REPLACEMENT = """{% set _ff_public_base = ff_public_base_url|default('', true)|trim %}
{% set _canonical_from_ctx = canonical_url|default('', true)|trim %}
{% set _stripe_return_from_ctx = stripe_return_url|default('', true)|trim %}
{% set _share_from_ctx = share_url|default('', true)|trim %}
{% set _campaign_from_ctx = campaign_url|default('', true)|trim %}

{% set _public_base_raw = (
  _ff_public_base
  or _cfg.get('FF_PUBLIC_BASE_URL')
  or _cfg.get('PUBLIC_BASE_URL')
  or _cfg.get('CANONICAL_BASE_URL')
  or 'https://getfuturefunded.com'
)|string|trim %}

{% if _public_base_raw.endswith('/') %}
  {% set _public_base_raw = _public_base_raw[:-1] %}
{% endif %}

{% set _public_base_lower = _public_base_raw|lower %}
{% if 'localhost' in _public_base_lower or '127.0.0.1' in _public_base_lower or '[::1]' in _public_base_lower %}
  {% set _public_base_raw = 'https://getfuturefunded.com' %}
{% endif %}

{% if not _public_base_raw %}
  {% set _public_base_raw = 'https://getfuturefunded.com' %}
{% endif %}

{% set _public_base = _public_base_raw %}
{% set _locked_campaign_url = _canonical_from_ctx or _campaign_from_ctx or (_public_base ~ _path) %}

{% set canonical = _locked_campaign_url|string|trim %}
{% set canonical_url = canonical %}
{% set _stripe_return = (_stripe_return_from_ctx or canonical)|string|trim %}
{% set stripe_return_url = _stripe_return %}
{% set _share_url_resolved = (_share_from_ctx or canonical)|string|trim %}
{% set share_url = _share_url_resolved %}
"""

def main() -> None:
    if not TEMPLATE.exists():
        raise SystemExit(f"Missing template: {TEMPLATE}")

    text = TEMPLATE.read_text(encoding="utf-8")

    start = text.find(START_ANCHOR)
    if start == -1:
        raise SystemExit("Could not find _public_base_raw start anchor.")

    end = text.find(END_ANCHOR, start)
    if end == -1:
        raise SystemExit("Could not find _safe_email anchor after URL block.")

    backup = TEMPLATE.with_name(TEMPLATE.name + ".bak-head-truth-lock-v2")
    if not backup.exists():
        backup.write_text(text, encoding="utf-8")

    updated = text[:start] + REPLACEMENT + "\n\n" + text[end:]
    TEMPLATE.write_text(updated, encoding="utf-8")

    print(f"✅ patched {TEMPLATE}")
    print(f"🛟 backup: {backup}")

if __name__ == "__main__":
    main()
