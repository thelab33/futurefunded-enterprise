from __future__ import annotations
from pathlib import Path
import shutil
from datetime import datetime

ROOT = Path(".").resolve()
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")

files = {
    "home": ROOT / "apps/web/app/templates/platform/home.html",
    "dashboard": ROOT / "apps/web/app/templates/platform/dashboard.html",
    "onboarding": ROOT / "apps/web/app/templates/platform/onboarding.html",
    "partial_intro": ROOT / "apps/web/app/templates/platform/_partials/_intro_split.html",
    "partial_promo": ROOT / "apps/web/app/templates/platform/_partials/_promo_bar.html",
}

for key in ["home", "dashboard", "onboarding"]:
    p = files[key]
    if not p.exists():
        raise SystemExit(f"❌ missing required file: {p}")

def backup(path: Path) -> Path:
    bak = path.with_name(path.name + f".bak-platform-pass2-{STAMP}")
    shutil.copy2(path, bak)
    return bak

backups = {k: backup(files[k]) for k in ["home", "dashboard", "onboarding"]}

files["partial_intro"].write_text(
"""{# ---------------------------------------------------------------------------
Platform intro split
Inputs:
- eyebrow
- title
- body
- pills (optional list)
- aside_kicker
- aside_title
- aside_body
- aside_items (optional list of {title, body})
--------------------------------------------------------------------------- #}
<div class="ff-grid ff-grid--2 ff-gap-3 ff-platformGridTop">
  <header class="ff-sectionhead ff-sectionhead--flagship ff-sectionhead--compact">
    <div class="ff-sectionhead__text ff-minw-0">
      <p class="ff-kicker ff-m-0">{{ eyebrow }}</p>
      <h1 class="ff-display ff-mt-2 ff-mb-0 ff-measure-12">{{ title }}</h1>
      <p class="ff-lead ff-mt-3 ff-mb-0 ff-measure-42">{{ body }}</p>

      {% if pills %}
        <div class="ff-row ff-wrap ff-gap-2 ff-mt-3" role="list" aria-label="Page signals">
          {% for pill in pills %}
            <span class="ff-pill {% if loop.first or loop.index == 2 %}ff-pill--soft{% else %}ff-pill--ghost{% endif %}" role="listitem">{{ pill }}</span>
          {% endfor %}
        </div>
      {% endif %}
    </div>
  </header>

  <aside class="ff-card ff-glass ff-pad" aria-labelledby="platformAsideTitle">
    <p class="ff-kicker ff-m-0">{{ aside_kicker }}</p>
    <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformAsideTitle">{{ aside_title }}</h2>
    <p class="ff-help ff-muted ff-mt-2 ff-mb-0">{{ aside_body }}</p>

    {% if aside_items %}
      <div class="ff-platformMiniList ff-mt-3">
        {% for item in aside_items %}
          <article class="ff-proofMini">
            <p class="ff-kicker ff-m-0">{{ item.title }}</p>
            <p class="ff-help ff-muted ff-mt-2 ff-mb-0">{{ item.body }}</p>
          </article>
        {% endfor %}
      </div>
    {% endif %}
  </aside>
</div>
""",
    encoding="utf-8",
)

files["partial_promo"].write_text(
"""{# ---------------------------------------------------------------------------
Platform promo bar
Inputs:
- kicker
- title
- body
- actions (optional list of {href, label, variant})
--------------------------------------------------------------------------- #}
<div class="ff-card ff-glass ff-pad ff-mt-3" aria-labelledby="platformPromoTitle">
  <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
    <div class="ff-minw-0">
      <p class="ff-kicker ff-m-0">{{ kicker }}</p>
      <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformPromoTitle">{{ title }}</h2>
      <p class="ff-help ff-muted ff-mt-2 ff-mb-0">{{ body }}</p>
    </div>
    {% if actions %}
      <div class="ff-row ff-wrap ff-gap-2">
        {% for action in actions %}
          <a class="ff-btn ff-btn--{{ action.variant|default('secondary') }} ff-btn--pill" href="{{ action.href }}">{{ action.label }}</a>
        {% endfor %}
      </div>
    {% endif %}
  </div>
</div>
""",
    encoding="utf-8",
)

home = files["home"].read_text(encoding="utf-8")
home_old = """    <div class="ff-grid ff-grid--2 ff-gap-3 ff-platformGridTop">

      <article class="ff-card ff-glass ff-pad">
        <p class="ff-kicker ff-m-0">{{ data.hero.eyebrow }}</p>

        <h1
          id="platformHeroTitle"
          class="ff-display ff-mt-2 ff-mb-0 ff-measure-11"
        >
          {{ data.hero.title }}
        </h1>

        <p class="ff-lead ff-mt-3 ff-mb-0 ff-measure-38">
          {{ data.hero.body }}
        </p>

        <div class="ff-row ff-wrap ff-gap-2 ff-mt-4">
          <a
            class="ff-btn ff-btn--primary ff-btn--pill"
            href="{{ data.hero.primary_cta_href }}"
          >
            {{ data.hero.primary_cta_label }}
          </a>

          <a
            class="ff-btn ff-btn--secondary ff-btn--pill"
            href="{{ data.hero.secondary_cta_href }}"
          >
            {{ data.hero.secondary_cta_label }}
          </a>
        </div>

        <div class="ff-proofMini ff-mt-3" aria-label="Launch trust note">
          <p class="ff-kicker ff-m-0">What you’re launching</p>
          <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
            A public fundraiser, sponsor packages, and a clean operator dashboard that makes the program look credible fast.
          </p>
        </div>

        <div class="ff-row ff-wrap ff-gap-2 ff-mt-3" role="list" aria-label="Hero signals">
          {% for pill in data.hero.pills %}
            <span class="ff-pill ff-pill--soft" role="listitem">{{ pill }}</span>
          {% endfor %}
        </div>
      </article>

      <div class="ff-stack ff-gap-3">

        <article class="ff-card ff-glass ff-pad" aria-labelledby="platformLaunchTitle">
          <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
            <h2 class="ff-h2 ff-m-0" id="platformLaunchTitle">What you can launch</h2>
            <span class="ff-platformInlinePill">Launch-ready</span>
          </div>

          <div class="ff-grid ff-grid--2 ff-gap-2 ff-mt-3">
            {% for card in data.launch_cards %}
              <div class="ff-proofMini">
                <p class="ff-kicker ff-m-0">{{ card.title }}</p>
                <p class="ff-help ff-muted ff-mt-2 ff-mb-0">{{ card.body }}</p>
              </div>
            {% endfor %}
          </div>
        </article>

        <article class="ff-card ff-glass ff-pad" aria-labelledby="platformStatusTitle">
          <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
            <h2 class="ff-h2 ff-m-0" id="platformStatusTitle">Launch status</h2>
            <span class="ff-platformInlinePill">Operator readout</span>
          </div>

          <div class="ff-grid ff-grid--3 ff-gap-2 ff-mt-3">
            {% for card in data.status_cards %}
              <div class="ff-proofMini">
                <p class="ff-kicker ff-m-0">{{ card.label }}</p>
                <p class="ff-h2 ff-mt-2 ff-mb-0">{{ card.value }}</p>
              </div>
            {% endfor %}
          </div>

          <div class="ff-row ff-wrap ff-gap-2 ff-mt-3" role="list" aria-label="Launch status tags">
            {% for pill in data.status_pills %}
              <span class="ff-pill ff-pill--ghost" role="listitem">{{ pill }}</span>
            {% endfor %}
          </div>
        </article>


        <article class="ff-card ff-glass ff-pad ff-mt-3" aria-labelledby="platformRevenueOsTitle">
          <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
            <h2 class="ff-h2 ff-m-0" id="platformRevenueOsTitle">Why teams buy this</h2>
            <span class="ff-platformInlinePill">Sellable system</span>
          </div>

          <div class="ff-grid ff-grid--3 ff-gap-2 ff-mt-3">
            <div class="ff-proofMini">
              <p class="ff-kicker ff-m-0">Direct giving</p>
              <p class="ff-help ff-muted ff-mt-2 ff-mb-0">A clean donation path that looks credible to families and supporters.</p>
            </div>
            <div class="ff-proofMini">
              <p class="ff-kicker ff-m-0">Sponsor lanes</p>
              <p class="ff-help ff-muted ff-mt-2 ff-mb-0">Business-ready packages that add revenue beyond one-time gifts.</p>
            </div>
            <div class="ff-proofMini">
              <p class="ff-kicker ff-m-0">Recurring support</p>
              <p class="ff-help ff-muted ff-mt-2 ff-mb-0">Memberships and booster plans that keep momentum going after launch.</p>
            </div>
          </div>
        </article>

      </div>
    </div>"""
home_new = """    {% include "platform/_partials/_promo_bar.html" with context %}

    <div class="ff-grid ff-grid--2 ff-gap-3 ff-platformGridTop">

      <article class="ff-card ff-glass ff-pad">
        <p class="ff-kicker ff-m-0">{{ data.hero.eyebrow }}</p>

        <h1
          id="platformHeroTitle"
          class="ff-display ff-mt-2 ff-mb-0 ff-measure-11"
        >
          {{ data.hero.title }}
        </h1>

        <p class="ff-lead ff-mt-3 ff-mb-0 ff-measure-38">
          {{ data.hero.body }}
        </p>

        <div class="ff-row ff-wrap ff-gap-2 ff-mt-4">
          <a
            class="ff-btn ff-btn--primary ff-btn--pill"
            href="{{ data.hero.primary_cta_href }}"
          >
            {{ data.hero.primary_cta_label }}
          </a>

          <a
            class="ff-btn ff-btn--secondary ff-btn--pill"
            href="{{ data.hero.secondary_cta_href }}"
          >
            {{ data.hero.secondary_cta_label }}
          </a>
        </div>

        <div class="ff-proofMini ff-mt-3" aria-label="Launch trust note">
          <p class="ff-kicker ff-m-0">What you’re launching</p>
          <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
            A public fundraiser, sponsor packages, and a clean operator dashboard that makes the program look credible fast.
          </p>
        </div>

        <div class="ff-row ff-wrap ff-gap-2 ff-mt-3" role="list" aria-label="Hero signals">
          {% for pill in data.hero.pills %}
            <span class="ff-pill ff-pill--soft" role="listitem">{{ pill }}</span>
          {% endfor %}
        </div>
      </article>

      <div class="ff-stack ff-gap-3">

        <article class="ff-card ff-glass ff-pad" aria-labelledby="platformLaunchTitle">
          <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
            <h2 class="ff-h2 ff-m-0" id="platformLaunchTitle">What you can launch</h2>
            <span class="ff-platformInlinePill">Launch-ready</span>
          </div>

          <div class="ff-grid ff-grid--2 ff-gap-2 ff-mt-3">
            {% for card in data.launch_cards %}
              <div class="ff-proofMini">
                <p class="ff-kicker ff-m-0">{{ card.title }}</p>
                <p class="ff-help ff-muted ff-mt-2 ff-mb-0">{{ card.body }}</p>
              </div>
            {% endfor %}
          </div>
        </article>

        <article class="ff-card ff-glass ff-pad" aria-labelledby="platformStatusTitle">
          <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
            <h2 class="ff-h2 ff-m-0" id="platformStatusTitle">Launch status</h2>
            <span class="ff-platformInlinePill">Operator readout</span>
          </div>

          <div class="ff-grid ff-grid--3 ff-gap-2 ff-mt-3">
            {% for card in data.status_cards %}
              <div class="ff-proofMini">
                <p class="ff-kicker ff-m-0">{{ card.label }}</p>
                <p class="ff-h2 ff-mt-2 ff-mb-0">{{ card.value }}</p>
              </div>
            {% endfor %}
          </div>

          <div class="ff-row ff-wrap ff-gap-2 ff-mt-3" role="list" aria-label="Launch status tags">
            {% for pill in data.status_pills %}
              <span class="ff-pill ff-pill--ghost" role="listitem">{{ pill }}</span>
            {% endfor %}
          </div>
        </article>

        <article class="ff-card ff-glass ff-pad ff-mt-3" aria-labelledby="platformRevenueOsTitle">
          <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
            <h2 class="ff-h2 ff-m-0" id="platformRevenueOsTitle">Why teams buy this</h2>
            <span class="ff-platformInlinePill">Sellable system</span>
          </div>

          <div class="ff-grid ff-grid--3 ff-gap-2 ff-mt-3">
            <div class="ff-proofMini">
              <p class="ff-kicker ff-m-0">Direct giving</p>
              <p class="ff-help ff-muted ff-mt-2 ff-mb-0">A clean donation path that looks credible to families and supporters.</p>
            </div>
            <div class="ff-proofMini">
              <p class="ff-kicker ff-m-0">Sponsor lanes</p>
              <p class="ff-help ff-muted ff-mt-2 ff-mb-0">Business-ready packages that add revenue beyond one-time gifts.</p>
            </div>
            <div class="ff-proofMini">
              <p class="ff-kicker ff-m-0">Recurring support</p>
              <p class="ff-help ff-muted ff-mt-2 ff-mb-0">Memberships and booster plans that keep momentum going after launch.</p>
            </div>
          </div>
        </article>

      </div>
    </div>"""
# no replacement for home to avoid risky broad edits

dashboard = files["dashboard"].read_text(encoding="utf-8")
dashboard_insert_after = '{% block platform_content %}\n<section class="ff-section" aria-labelledby="platformDashboardTitle">\n  <div class="ff-container">\n'
dashboard_inject = """{% set intro_pills = ['Live workspace', 'Brand-ready', 'Operator view'] %}
{% set intro_aside_items = [
  {'title': 'Live campaign', 'body': 'Connect ATX Elite is already launched with a public campaign page and dashboard access.'},
  {'title': 'Sponsor lanes', 'body': 'Manage sponsor packages that feel credible to local businesses and community partners.'},
  {'title': 'Recurring support', 'body': 'Keep momentum going beyond one-time gifts with monthly and annual memberships.'}
] %}
"""
if dashboard_insert_after in dashboard and intro_inject not in dashboard:
    pass
intro_inject = dashboard_inject
dashboard = dashboard.replace('{% block platform_content %}\n', '{% block platform_content %}\n' + intro_inject, 1)

dashboard_old = """    <div class="ff-grid ff-grid--2 ff-gap-3 ff-platformGridTop">
      <header class="ff-sectionhead ff-sectionhead--flagship ff-sectionhead--compact">
        <div class="ff-sectionhead__text ff-minw-0">
          <p class="ff-kicker ff-m-0">Admin dashboard</p>

          <h1
            class="ff-display ff-mt-2 ff-mb-0 ff-measure-12"
            id="platformDashboardTitle"
          >
            FutureFunded command center
          </h1>

          <p class="ff-lead ff-mt-3 ff-mb-0 ff-measure-42">
            Manage the live Connect ATX Elite fundraiser, sponsor packages, and recurring booster support from one premium workspace.
          </p>

          <div class="ff-row ff-wrap ff-gap-2 ff-mt-3" role="list" aria-label="Workspace qualities">
            <span class="ff-pill ff-pill--soft" role="listitem">Live workspace</span>
            <span class="ff-pill ff-pill--soft" role="listitem">Brand-ready</span>
            <span class="ff-pill ff-pill--ghost" role="listitem">Operator view</span>
          </div>
        </div>
      </header>

      <aside class="ff-card ff-glass ff-pad" aria-labelledby="platformWorkspaceBriefTitle">
        <p class="ff-kicker ff-m-0">Workspace brief</p>
        <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformWorkspaceBriefTitle">One place to launch, manage, and expand.</h2>
        <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
          This dashboard is your control layer for live fundraising, sponsor packages, and recurring support lanes.
        </p>

        <div class="ff-platformMiniList ff-mt-3">
          <article class="ff-proofMini">
            <p class="ff-kicker ff-m-0">Live campaign</p>
            <p class="ff-help ff-muted ff-mt-2 ff-mb-0">Connect ATX Elite is already launched with a public campaign page and dashboard access.</p>
          </article>

          <article class="ff-proofMini">
            <p class="ff-kicker ff-m-0">Sponsor lanes</p>
            <p class="ff-help ff-muted ff-mt-2 ff-mb-0">Manage sponsor packages that feel credible to local businesses and community partners.</p>
          </article>

          <article class="ff-proofMini">
            <p class="ff-kicker ff-m-0">Recurring support</p>
            <p class="ff-help ff-muted ff-mt-2 ff-mb-0">Keep momentum going beyond one-time gifts with monthly and annual memberships.</p>
          </article>
        </div>
      </aside>
    </div>"""
dashboard_new = """    {% with
      eyebrow='Admin dashboard',
      title='FutureFunded command center',
      body='Manage the live Connect ATX Elite fundraiser, sponsor packages, and recurring booster support from one premium workspace.',
      pills=intro_pills,
      aside_kicker='Workspace brief',
      aside_title='One place to launch, manage, and expand.',
      aside_body='This dashboard is your control layer for live fundraising, sponsor packages, and recurring support lanes.',
      aside_items=intro_aside_items
    %}
      {% include "platform/_partials/_intro_split.html" %}
    {% endwith %}"""
dashboard = dashboard.replace(dashboard_old, dashboard_new, 1)
files["dashboard"].write_text(dashboard, encoding="utf-8")

onboarding = files["onboarding"].read_text(encoding="utf-8")
onboarding = onboarding.replace('{% block platform_content %}\n', '''{% block platform_content %}
{% set intro_pills = ['Real API', 'Brand-ready', 'Launch today'] %}
{% set intro_aside_items = [
  {'title': 'Brand setup', 'body': 'Name, slug, and color system for the organization shell.'},
  {'title': 'Public route', 'body': 'Creates a live fundraiser at /c/<campaign-slug>.'},
  {'title': 'Operator handoff', 'body': 'Moves directly into the dashboard so you can manage the campaign immediately.'}
] %}
''', 1)

onboarding_old = """    <div class="ff-grid ff-grid--2 ff-gap-3 ff-platformGridTop">
      <header class="ff-sectionhead ff-sectionhead--flagship ff-sectionhead--compact">
        <div class="ff-sectionhead__text ff-minw-0">
          <p class="ff-kicker ff-m-0">Step 1 · Launch your first org</p>

          <h1
            class="ff-display ff-mt-2 ff-mb-0 ff-measure-10"
            id="platformOnboardingTitle"
          >
            Onboarding
          </h1>

          <p class="ff-lead ff-mt-3 ff-mb-0 ff-measure-42">
            Create your first organization and campaign against the real API, then hand off directly into your operational dashboard.
          </p>

          <div class="ff-row ff-wrap ff-gap-2 ff-mt-3" role="list" aria-label="Launch qualities">
            <span class="ff-pill ff-pill--soft" role="listitem">Real API</span>
            <span class="ff-pill ff-pill--soft" role="listitem">Brand-ready</span>
            <span class="ff-pill ff-pill--ghost" role="listitem">Launch today</span>
          </div>

          <section class="ff-card ff-glass ff-pad ff-mt-3" aria-label="Launch steps">
            <div class="ff-row ff-wrap ff-gap-2" role="list" aria-label="Onboarding steps">
              <span class="ff-platformInlinePill" role="listitem">1. Program</span>
              <span class="ff-platformInlinePill" role="listitem">2. Branding</span>
              <span class="ff-platformInlinePill" role="listitem">3. Launch</span>
            </div>
            <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
              We’ll generate the public fundraiser route, operator dashboard handoff, and a sponsor-ready starting point from one simple setup.
            </p>
          </section>
        </div>
      </header>

      <aside class="ff-card ff-glass ff-pad" aria-labelledby="platformLaunchBriefTitle">
        <p class="ff-kicker ff-m-0">Launch brief</p>
        <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformLaunchBriefTitle">Start with one org. Publish one live campaign.</h2>
        <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
          This setup gives you the minimum premium launch surface: a branded organization, a live fundraiser route, and a direct dashboard handoff.
        </p>

        <div class="ff-platformMiniList ff-mt-3">
          <article class="ff-proofMini">
            <p class="ff-kicker ff-m-0">Brand setup</p>
            <p class="ff-help ff-muted ff-mt-2 ff-mb-0">Name, slug, and color system for the organization shell.</p>
          </article>

          <article class="ff-proofMini">
            <p class="ff-kicker ff-m-0">Public route</p>
            <p class="ff-help ff-muted ff-mt-2 ff-mb-0">Creates a live fundraiser at <code>/c/&lt;campaign-slug&gt;</code>.</p>
          </article>

          <article class="ff-proofMini">
            <p class="ff-kicker ff-m-0">Operator handoff</p>
            <p class="ff-help ff-muted ff-mt-2 ff-mb-0">Moves directly into the dashboard so you can manage the campaign immediately.</p>
          </article>
        </div>
      </aside>
    </div>"""
onboarding_new = """    {% with
      eyebrow='Step 1 · Launch your first org',
      title='Onboarding',
      body='Create your first organization and campaign against the real API, then hand off directly into your operational dashboard.',
      pills=intro_pills,
      aside_kicker='Launch brief',
      aside_title='Start with one org. Publish one live campaign.',
      aside_body='This setup gives you the minimum premium launch surface: a branded organization, a live fundraiser route, and a direct dashboard handoff.',
      aside_items=intro_aside_items
    %}
      {% include "platform/_partials/_intro_split.html" %}
    {% endwith %}

    <section class="ff-card ff-glass ff-pad ff-mt-3" aria-label="Launch steps">
      <div class="ff-row ff-wrap ff-gap-2" role="list" aria-label="Onboarding steps">
        <span class="ff-platformInlinePill" role="listitem">1. Program</span>
        <span class="ff-platformInlinePill" role="listitem">2. Branding</span>
        <span class="ff-platformInlinePill" role="listitem">3. Launch</span>
      </div>
      <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
        We’ll generate the public fundraiser route, operator dashboard handoff, and a sponsor-ready starting point from one simple setup.
      </p>
    </section>"""
onboarding = onboarding.replace(onboarding_old, onboarding_new, 1)
files["onboarding"].write_text(onboarding, encoding="utf-8")

print("✅ platform cleanup pass 2 applied")
for key, bak in backups.items():
    print(f"🛟 backup[{key}]: {bak}")
print(f"✅ partial: {files['partial_intro']}")
print(f"✅ partial: {files['partial_promo']}")
