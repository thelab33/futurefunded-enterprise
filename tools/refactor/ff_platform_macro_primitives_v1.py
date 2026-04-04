from __future__ import annotations

from pathlib import Path

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATES = ROOT / "apps/web/app/templates"

TARGETS = {
    TEMPLATES / "shared/macros/ui.html": """{# FutureFunded shared UI macros #}

{% macro ff_button(label, href='#', variant='primary', size='md', pill=True, attrs='') -%}
  {% set _classes = ['ff-btn'] %}
  {% if variant == 'secondary' %}
    {% set _classes = _classes + ['ff-btn--secondary'] %}
  {% elif variant == 'ghost' %}
    {% set _classes = _classes + ['ff-btn--ghost'] %}
  {% else %}
    {% set _classes = _classes + ['ff-btn--primary'] %}
  {% endif %}

  {% if size == 'sm' %}
    {% set _classes = _classes + ['ff-btn--sm'] %}
  {% elif size == 'lg' %}
    {% set _classes = _classes + ['ff-btn--lg'] %}
  {% endif %}

  {% if pill %}
    {% set _classes = _classes + ['ff-btn--pill'] %}
  {% endif %}

  <a class="{{ _classes|join(' ') }}" href="{{ href|e }}"{% if attrs %} {{ attrs|safe }}{% endif %}>{{ label }}</a>
{%- endmacro %}


{% macro ff_section_header(eyebrow='', title='', body='', section_id='', compact=True) -%}
  <header class="ff-sectionhead ff-sectionhead--flagship{% if compact %} ff-sectionhead--compact{% endif %}">
    <div class="ff-sectionhead__text ff-minw-0">
      {% if eyebrow %}<p class="ff-kicker ff-m-0">{{ eyebrow }}</p>{% endif %}
      {% if title %}<h2 class="ff-h2 ff-m-0"{% if section_id %} id="{{ section_id|e }}"{% endif %}>{{ title }}</h2>{% endif %}
      {% if body %}<p class="ff-lead ff-mt-2 ff-mb-0">{{ body }}</p>{% endif %}
    </div>
  </header>
{%- endmacro %}


{% macro ff_cta_pair(primary_label='', primary_href='#', secondary_label='', secondary_href='#') -%}
  <div class="ff-row ff-wrap ff-gap-2">
    {% if primary_label %}
      {{ ff_button(primary_label, primary_href, 'primary', 'md', True) }}
    {% endif %}
    {% if secondary_label %}
      {{ ff_button(secondary_label, secondary_href, 'secondary', 'md', True) }}
    {% endif %}
  </div>
{%- endmacro %}
""",

    TEMPLATES / "shared/macros/cards.html": """{# FutureFunded shared card macros #}

{% from "shared/macros/pills.html" import ff_pill_list %}

{% macro metric_card(title='', body='', value='') -%}
  <article class="ff-card ff-glass ff-pad">
    {% if title %}<p class="ff-kicker ff-m-0">{{ title }}</p>{% endif %}
    {% if value %}<h3 class="ff-h2 ff-mt-1 ff-mb-0">{{ value }}</h3>{% endif %}
    {% if body %}<p class="ff-help ff-muted ff-mt-2 ff-mb-0">{{ body }}</p>{% endif %}
  </article>
{%- endmacro %}


{% macro feature_card(title='', body='', pills=None) -%}
  <article class="ff-card ff-glass ff-pad">
    {% if title %}<h3 class="ff-h3 ff-m-0">{{ title }}</h3>{% endif %}
    {% if body %}<p class="ff-help ff-muted ff-mt-2 ff-mb-0">{{ body }}</p>{% endif %}
    {% if pills %}
      <div class="ff-mt-3">
        {{ ff_pill_list(pills, 'soft') }}
      </div>
    {% endif %}
  </article>
{%- endmacro %}


{% macro plan_card(name='', price='', body='', fit='', featured=False, cta_label='', cta_href='#') -%}
  <article class="ff-card ff-glass ff-pad{% if featured %} ff-card--lift{% endif %}">
    <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
      <div class="ff-minw-0">
        {% if name %}<p class="ff-kicker ff-m-0">{{ name }}</p>{% endif %}
        {% if price %}<h3 class="ff-h2 ff-mt-1 ff-mb-0">{{ price }}</h3>{% endif %}
      </div>
      {% if featured %}
        <span class="ff-pill ff-pill--accent">Featured</span>
      {% endif %}
    </div>
    {% if body %}<p class="ff-help ff-muted ff-mt-2 ff-mb-0">{{ body }}</p>{% endif %}
    {% if fit %}<p class="ff-help ff-mt-3 ff-mb-0"><strong>Best for:</strong> {{ fit }}</p>{% endif %}
    {% if cta_label %}
      <div class="ff-mt-3">
        <a class="ff-btn ff-btn--primary ff-btn--pill" href="{{ cta_href|e }}">{{ cta_label }}</a>
      </div>
    {% endif %}
  </article>
{%- endmacro %}
""",

    TEMPLATES / "shared/macros/pills.html": """{# FutureFunded shared pill / badge macros #}

{% macro ff_pill(label, variant='soft') -%}
  {% set _class = 'ff-pill ff-pill--soft' %}
  {% if variant == 'ghost' %}
    {% set _class = 'ff-pill ff-pill--ghost' %}
  {% elif variant == 'accent' %}
    {% set _class = 'ff-pill ff-pill--accent' %}
  {% endif %}
  <span class="{{ _class }}">{{ label }}</span>
{%- endmacro %}


{% macro ff_pill_list(items, variant='soft') -%}
  <div class="ff-row ff-wrap ff-gap-2" role="list">
    {% for item in (items or []) %}
      <span role="listitem">{{ ff_pill(item, variant) }}</span>
    {% endfor %}
  </div>
{%- endmacro %}
""",

    TEMPLATES / "shared/partials/_section_header.html": """{# expects: eyebrow, title, body, section_id, compact #}
<header class="ff-sectionhead ff-sectionhead--flagship{% if compact|default(true) %} ff-sectionhead--compact{% endif %}">
  <div class="ff-sectionhead__text ff-minw-0">
    {% if eyebrow %}<p class="ff-kicker ff-m-0">{{ eyebrow }}</p>{% endif %}
    {% if title %}<h2 class="ff-h2 ff-m-0"{% if section_id %} id="{{ section_id|e }}"{% endif %}>{{ title }}</h2>{% endif %}
    {% if body %}<p class="ff-lead ff-mt-2 ff-mb-0">{{ body }}</p>{% endif %}
  </div>
</header>
""",

    TEMPLATES / "shared/partials/_cta_band.html": """{# expects: kicker, title, body, primary_label, primary_href, secondary_label, secondary_href #}
<section class="ff-card ff-glass ff-pad" aria-label="Call to action">
  {% if kicker %}<p class="ff-kicker ff-m-0">{{ kicker }}</p>{% endif %}
  {% if title %}<h2 class="ff-h2 ff-mt-2 ff-mb-0">{{ title }}</h2>{% endif %}
  {% if body %}<p class="ff-help ff-muted ff-mt-2 ff-mb-0">{{ body }}</p>{% endif %}
  <div class="ff-row ff-wrap ff-gap-2 ff-mt-3">
    {% if primary_label %}<a class="ff-btn ff-btn--primary ff-btn--pill" href="{{ primary_href|default('#')|e }}">{{ primary_label }}</a>{% endif %}
    {% if secondary_label %}<a class="ff-btn ff-btn--secondary ff-btn--pill" href="{{ secondary_href|default('#')|e }}">{{ secondary_label }}</a>{% endif %}
  </div>
</section>
""",

    TEMPLATES / "shared/partials/_footer_minimal.html": """<footer class="ff-footer ff-footer--minimal" data-ff-footer="">
  <div class="ff-container">
    <div class="ff-footerShell ff-glass ff-surface ff-footerShell--minimal">
      <div class="ff-footerGrid ff-footerGrid--minimal">
        <section class="ff-footerBrand ff-minw-0" aria-label="FutureFunded footer brand">
          <div class="ff-brand">
            <div class="ff-brand__title">FutureFunded</div>
            <p class="ff-brand__sub ff-m-0">Launch sponsor-ready fundraising systems faster.</p>
          </div>
        </section>
        <nav class="ff-footerNav ff-footerNav--minimal" aria-label="Footer navigation">
          <ul class="ff-footerLinkList" role="list">
            <li><a class="ff-footer__link" href="/platform/">Platform</a></li>
            <li><a class="ff-footer__link" href="/platform/onboarding">Onboarding</a></li>
            <li><a class="ff-footer__link" href="/platform/dashboard">Dashboard</a></li>
            <li><a class="ff-footer__link" href="/platform/pricing">Pricing</a></li>
            <li><a class="ff-footer__link" href="/platform/demo">Demo</a></li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</footer>
""",
}

def main() -> None:
    for path, content in TARGETS.items():
        path.parent.mkdir(parents=True, exist_ok=True)

        backup = path.with_name(path.name + ".bak-macro-primitives-v1")
        if path.exists() and not backup.exists():
            backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

        path.write_text(content, encoding="utf-8")
        print(f"✅ wrote {path}")

if __name__ == "__main__":
    main()

