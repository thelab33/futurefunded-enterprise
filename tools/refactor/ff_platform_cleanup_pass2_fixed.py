from __future__ import annotations
from pathlib import Path
import shutil
from datetime import datetime

ROOT = Path(".").resolve()
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")

targets = {
    "dashboard": ROOT / "apps/web/app/templates/platform/dashboard.html",
    "onboarding": ROOT / "apps/web/app/templates/platform/onboarding.html",
    "partial_intro": ROOT / "apps/web/app/templates/platform/_partials/_intro_split.html",
    "partial_promo": ROOT / "apps/web/app/templates/platform/_partials/_promo_bar.html",
}

for key in ["dashboard", "onboarding"]:
    if not targets[key].exists():
        raise SystemExit(f"❌ missing required file: {targets[key]}")

def backup(path: Path) -> Path:
    bak = path.with_name(path.name + f".bak-platform-pass2-fixed-{STAMP}")
    shutil.copy2(path, bak)
    return bak

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"❌ could not find expected block for {label}")
    return text.replace(old, new, 1)

backups = {
    "dashboard": backup(targets["dashboard"]),
    "onboarding": backup(targets["onboarding"]),
}

targets["partial_intro"].write_text(
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
      <h1 class="ff-display ff-mt-2 ff-mb-0 ff-measure-12" id="{{ title_id|default('', true) }}">{{ title }}</h1>
      <p class="ff-lead ff-mt-3 ff-mb-0 ff-measure-42">{{ body }}</p>

      {% if pills %}
        <div class="ff-row ff-wrap ff-gap-2 ff-mt-3" role="list" aria-label="{{ pills_label|default('Page signals', true) }}">
          {% for pill in pills %}
            <span class="ff-pill {% if loop.first or loop.index == 2 %}ff-pill--soft{% else %}ff-pill--ghost{% endif %}" role="listitem">{{ pill }}</span>
          {% endfor %}
        </div>
      {% endif %}
    </div>
  </header>

  <aside class="ff-card ff-glass ff-pad" aria-labelledby="{{ aside_id|default('platformAsideTitle', true) }}">
    <p class="ff-kicker ff-m-0">{{ aside_kicker }}</p>
    <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="{{ aside_id|default('platformAsideTitle', true) }}">{{ aside_title }}</h2>
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

targets["partial_promo"].write_text(
"""{# ---------------------------------------------------------------------------
Platform promo bar
Inputs:
- kicker
- title
- body
- title_id
- actions (optional list of {href, label, variant})
--------------------------------------------------------------------------- #}
<div class="ff-card ff-glass ff-pad ff-mt-3" aria-labelledby="{{ title_id|default('platformPromoTitle', true) }}">
  <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
    <div class="ff-minw-0">
      <p class="ff-kicker ff-m-0">{{ kicker }}</p>
      <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="{{ title_id|default('platformPromoTitle', true) }}">{{ title }}</h2>
      <p class="ff-help ff-muted ff-mt-2 ff-mb-0">{{ body }}</p>
    </div>

    {% if actions %}
      <div class="ff-row ff-wrap ff-gap-2">
        {% for action in actions %}
          <a class="ff-btn ff-btn--{{ action.variant|default('secondary', true) }} ff-btn--pill" href="{{ action.href }}">{{ action.label }}</a>
        {% endfor %}
      </div>
    {% endif %}
  </div>
</div>
""",
    encoding="utf-8",
)

# ---------------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------------
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

dashboard_new = """    {% set intro_pills = ['Live workspace', 'Brand-ready', 'Operator view'] %}
    {% set intro_aside_items = [
      {'title': 'Live campaign', 'body': 'Connect ATX Elite is already launched with a public campaign page and dashboard access.'},
      {'title': 'Sponsor lanes', 'body': 'Manage sponsor packages that feel credible to local businesses and community partners.'},
      {'title': 'Recurring support', 'body': 'Keep momentum going beyond one-time gifts with monthly and annual memberships.'}
    ] %}
    {% with
      eyebrow='Admin dashboard',
      title='FutureFunded command center',
      title_id='platformDashboardTitle',
      body='Manage the live Connect ATX Elite fundraiser, sponsor packages, and recurring booster support from one premium workspace.',
      pills=intro_pills,
      pills_label='Workspace qualities',
      aside_kicker='Workspace brief',
      aside_title='One place to launch, manage, and expand.',
      aside_id='platformWorkspaceBriefTitle',
      aside_body='This dashboard is your control layer for live fundraising, sponsor packages, and recurring support lanes.',
      aside_items=intro_aside_items
    %}
      {% include "platform/_partials/_intro_split.html" %}
    {% endwith %}"""

dashboard = targets["dashboard"].read_text(encoding="utf-8")
if 'platform/_partials/_intro_split.html' not in dashboard:
    dashboard = replace_once(dashboard, dashboard_old, dashboard_new, "dashboard intro")
    targets["dashboard"].write_text(dashboard, encoding="utf-8")

# ---------------------------------------------------------------------
# ONBOARDING
# ---------------------------------------------------------------------
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

onboarding_new = """    {% set intro_pills = ['Real API', 'Brand-ready', 'Launch today'] %}
    {% set intro_aside_items = [
      {'title': 'Brand setup', 'body': 'Name, slug, and color system for the organization shell.'},
      {'title': 'Public route', 'body': 'Creates a live fundraiser at /c/<campaign-slug>.'},
      {'title': 'Operator handoff', 'body': 'Moves directly into the dashboard so you can manage the campaign immediately.'}
    ] %}
    {% with
      eyebrow='Step 1 · Launch your first org',
      title='Onboarding',
      title_id='platformOnboardingTitle',
      body='Create your first organization and campaign against the real API, then hand off directly into your operational dashboard.',
      pills=intro_pills,
      pills_label='Launch qualities',
      aside_kicker='Launch brief',
      aside_title='Start with one org. Publish one live campaign.',
      aside_id='platformLaunchBriefTitle',
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

onboarding = targets["onboarding"].read_text(encoding="utf-8")
if 'platform/_partials/_intro_split.html' not in onboarding:
    onboarding = replace_once(onboarding, onboarding_old, onboarding_new, "onboarding intro")
    targets["onboarding"].write_text(onboarding, encoding="utf-8")

print("✅ platform cleanup pass 2 fixed applied")
for key, bak in backups.items():
    print(f"🛟 backup[{key}]: {bak}")
print(f"✅ partial: {targets['partial_intro']}")
print(f"✅ partial: {targets['partial_promo']}")
