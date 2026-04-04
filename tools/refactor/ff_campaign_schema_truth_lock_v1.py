from __future__ import annotations

from pathlib import Path
import re

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"

SCHEMA_PATTERN = re.compile(
    r"\{% set _schema_graph = \{.*?\n  \} %\}",
    re.S,
)

SCHEMA_REPLACEMENT = """{% set _schema_public_base = _public_base %}
{% set _schema_canonical = canonical %}
{% set _schema_og_jpg = og_jpg %}

{% set _schema_public_base_lower = _schema_public_base|lower %}
{% if _is_prod and _schema_public_base_lower.startswith('http://') %}
  {% set _schema_public_base = _schema_public_base|replace('http://', 'https://', 1) %}
{% endif %}
{% if _is_prod and ('localhost' in _schema_public_base_lower or '127.0.0.1' in _schema_public_base_lower or '[::1]' in _schema_public_base_lower) %}
  {% set _schema_public_base = 'https://getfuturefunded.com' %}
{% endif %}

{% set _schema_canonical_lower = _schema_canonical|lower %}
{% if _is_prod and _schema_canonical_lower.startswith('http://') %}
  {% set _schema_canonical = _schema_canonical|replace('http://', 'https://', 1) %}
  {% set _schema_canonical_lower = _schema_canonical|lower %}
{% endif %}
{% if _is_prod and ('localhost' in _schema_canonical_lower or '127.0.0.1' in _schema_canonical_lower or '[::1]' in _schema_canonical_lower) %}
  {% set _schema_canonical = _schema_public_base ~ _path %}
{% endif %}

{% set _schema_og_jpg_lower = _schema_og_jpg|lower %}
{% if _is_prod and _schema_og_jpg_lower.startswith('http://') %}
  {% set _schema_og_jpg = _schema_og_jpg|replace('http://', 'https://', 1) %}
  {% set _schema_og_jpg_lower = _schema_og_jpg|lower %}
{% endif %}
{% if _is_prod and ('localhost' in _schema_og_jpg_lower or '127.0.0.1' in _schema_og_jpg_lower or '[::1]' in _schema_og_jpg_lower) %}
  {% set _schema_og_jpg = _schema_public_base ~ url_for('static', filename='images/og.jpg') ~ '?v=' ~ _v %}
{% endif %}

{% set _schema_graph = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': ['Organization', 'SportsOrganization'],
        '@id': _schema_canonical ~ '#org',
        'name': _org_name,
        'url': _schema_canonical,
        'email': _email,
        'logo': _schema_public_base ~ url_for('static', filename='images/logo.webp') ~ '?v=' ~ _v
      },
      {
        '@type': 'WebSite',
        '@id': _schema_public_base ~ '#website',
        'name': 'FutureFunded',
        'url': _schema_public_base
      },
      {
        '@type': 'WebPage',
        '@id': _schema_canonical ~ '#webpage',
        'url': _schema_canonical,
        'name': page_title_final,
        'description': page_desc_final,
        'isPartOf': {'@id': _schema_public_base ~ '#website'},
        'about': {'@id': _schema_canonical ~ '#org'},
        'primaryImageOfPage': {
          '@type': 'ImageObject',
          'url': _schema_og_jpg
        }
      }
    ]
  } %}"""

def main() -> None:
    if not TEMPLATE.exists():
        raise SystemExit(f"Missing template: {TEMPLATE}")

    text = TEMPLATE.read_text(encoding="utf-8")
    if "_schema_public_base" in text:
        raise SystemExit("Schema truth lock appears to be already applied.")

    match = SCHEMA_PATTERN.search(text)
    if not match:
        raise SystemExit("Could not find _schema_graph block to replace.")

    backup = TEMPLATE.with_name(TEMPLATE.name + ".bak-schema-truth-lock-v1")
    if not backup.exists():
        backup.write_text(text, encoding="utf-8")

    updated = text[:match.start()] + SCHEMA_REPLACEMENT + text[match.end():]
    TEMPLATE.write_text(updated, encoding="utf-8")

    print(f"✅ patched {TEMPLATE}")
    print(f"🛟 backup: {backup}")

if __name__ == "__main__":
    main()
