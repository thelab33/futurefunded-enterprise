from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path(".").resolve()
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")

TPL = ROOT / "apps/web/app/templates/platform"
PARTIALS = TPL / "_partials"

TARGETS = {
    "home": TPL / "home.html",
    "dashboard": TPL / "dashboard.html",
    "onboarding": TPL / "onboarding.html",
    "pricing": TPL / "pricing.html",
    "demo": TPL / "demo.html",
    "intro_partial": PARTIALS / "_intro_split.html",
    "promo_partial": PARTIALS / "_promo_bar.html",
}

for key in ["home", "dashboard", "onboarding", "pricing", "demo"]:
    if not TARGETS[key].exists():
        raise SystemExit(f"❌ missing required file: {TARGETS[key]}")

PARTIALS.mkdir(parents=True, exist_ok=True)

def backup(path: Path) -> Path:
    bak = path.with_name(path.name + f".bak-platform-repo-surgery-{STAMP}")
    shutil.copy2(path, bak)
    return bak

def write(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")

def replace_if_present(text: str, old: str, new: str, label: str, changes: list[str]) -> str:
    if old in text:
        text = text.replace(old, new, 1)
        changes.append(label)
    return text

def regex_sub(text: str, pattern: str, repl, label: str, changes: list[str], flags: int = 0) -> str:
    updated, count = re.subn(pattern, repl, text, flags=flags)
    if count:
        changes.append(f"{label} x{count}")
    return updated

def generic_platform_cleanup(text: str, changes: list[str]) -> str:
    # normalize align-items inline drift
    text = text.replace(
        '<div class="ff-grid ff-grid--2 ff-gap-3" style="align-items:start;">',
        '<div class="ff-grid ff-grid--2 ff-gap-3 ff-platformGridTop">',
    )
    if 'style="align-items:start;"' not in text:
        changes.append("normalized intro grid alignment")

    # remove max-width inline styles on display titles
    def repl_display_a(m):
        title_id = m.group(1)
        measure = m.group(2)
        return f'class="ff-display ff-mt-2 ff-mb-0 ff-measure-{measure}" id="{title_id}"'

    def repl_display_b(m):
        measure = m.group(1)
        title_id = m.group(2)
        return f'class="ff-display ff-mt-2 ff-mb-0 ff-measure-{measure}" id="{title_id}"'

    text = regex_sub(
        text,
        r'class="ff-display ff-mt-2 ff-mb-0"\s+id="([^"]+)"\s+style="max-width:(\d+)ch;"',
        repl_display_a,
        "display measure cleanup",
        changes,
    )
    text = regex_sub(
        text,
        r'class="ff-display ff-mt-2 ff-mb-0"\s+style="max-width:(\d+)ch;"\s+id="([^"]+)"',
        repl_display_b,
        "display measure cleanup",
        changes,
    )

    # remove max-width inline styles on lead paragraphs
    def repl_lead(m):
        measure = m.group(1)
        return f'class="ff-lead ff-mt-3 ff-mb-0 ff-measure-{measure}"'

    text = regex_sub(
        text,
        r'class="ff-lead ff-mt-3 ff-mb-0"\s+style="max-width:(\d+)ch;"',
        repl_lead,
        "lead measure cleanup",
        changes,
    )

    return text

def write_partials():
    intro = r"""{# ---------------------------------------------------------------------------
Platform intro split
Inputs:
- eyebrow
- title
- title_id (optional)
- body
- pills (optional list)
- pills_label (optional)
- aside_kicker
- aside_title
- aside_id (optional)
- aside_body
- aside_items (optional list of {title, body})
- aside_actions (optional list of {href, label, variant})
--------------------------------------------------------------------------- #}
<div class="ff-grid ff-grid--2 ff-gap-3 ff-platformGridTop">
  <header class="ff-sectionhead ff-sectionhead--flagship ff-sectionhead--compact">
    <div class="ff-sectionhead__text ff-minw-0">
      <p class="ff-kicker ff-m-0">{{ eyebrow }}</p>

      <h1 class="ff-display ff-mt-2 ff-mb-0 ff-measure-12"{% if title_id %} id="{{ title_id }}"{% endif %}>
        {{ title }}
      </h1>

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

  <aside class="ff-card ff-glass ff-pad" {% if aside_id %}aria-labelledby="{{ aside_id }}"{% endif %}>
    <p class="ff-kicker ff-m-0">{{ aside_kicker }}</p>

    <h2 class="ff-h2 ff-mt-2 ff-mb-0"{% if aside_id %} id="{{ aside_id }}"{% endif %}>
      {{ aside_title }}
    </h2>

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

    {% if aside_actions %}
      <div class="ff-row ff-wrap ff-gap-2 ff-mt-3">
        {% for action in aside_actions %}
          <a class="ff-btn ff-btn--{{ action.variant|default('secondary', true) }} ff-btn--pill" href="{{ action.href }}">{{ action.label }}</a>
        {% endfor %}
      </div>
    {% endif %}
  </aside>
</div>
"""
    promo = r"""{# ---------------------------------------------------------------------------
Platform promo bar
Inputs:
- kicker
- title
- title_id (optional)
- body
- actions (optional list of {href, label, variant})
--------------------------------------------------------------------------- #}
<div class="ff-card ff-glass ff-pad ff-mt-3" {% if title_id %}aria-labelledby="{{ title_id }}"{% endif %}>
  <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
    <div class="ff-minw-0">
      <p class="ff-kicker ff-m-0">{{ kicker }}</p>
      <h2 class="ff-h2 ff-mt-2 ff-mb-0"{% if title_id %} id="{{ title_id }}"{% endif %}>{{ title }}</h2>
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
"""
    write(TARGETS["intro_partial"], intro)
    write(TARGETS["promo_partial"], promo)

def patch_dashboard_intro(text: str, changes: list[str]) -> str:
    old = """    <div class="ff-grid ff-grid--2 ff-gap-3 ff-platformGridTop">
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
    new = """    {% set intro_pills = ['Live workspace', 'Brand-ready', 'Operator view'] %}
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
    return replace_if_present(text, old, new, "dashboard intro → _intro_split", changes)

def patch_onboarding_intro(text: str, changes: list[str]) -> str:
    old = """    <div class="ff-grid ff-grid--2 ff-gap-3 ff-platformGridTop">
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
    new = """    {% set intro_pills = ['Real API', 'Brand-ready', 'Launch today'] %}
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
    return replace_if_present(text, old, new, "onboarding intro → _intro_split", changes)

def patch_known_promo_blocks(text: str, page: str, changes: list[str]) -> str:
    promos = {
        "home": [
            (
"""    <div class="ff-card ff-glass ff-pad ff-mt-3" aria-labelledby="platformFounderOfferTitle">
      <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
        <div class="ff-minw-0">
          <p class="ff-kicker ff-m-0">Founder offer</p>
          <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformFounderOfferTitle">First five customers get founder pricing.</h2>
          <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
            Lock in an early rate, launch fast, and grow into sponsor and membership lanes without rebuilding from scratch.
          </p>
        </div>
        <div class="ff-row ff-wrap ff-gap-2">
          <a class="ff-btn ff-btn--primary ff-btn--pill" href="/platform/onboarding">Claim founder setup</a>
          <a class="ff-btn ff-btn--secondary ff-btn--pill" href="/c/spring-fundraiser">View live example</a>
        </div>
      </div>
    </div>""",
"""    {% set promo_actions = [
      {'href': '/platform/onboarding', 'label': 'Claim founder setup', 'variant': 'primary'},
      {'href': '/c/spring-fundraiser', 'label': 'View live example', 'variant': 'secondary'}
    ] %}
    {% with
      kicker='Founder offer',
      title='First five customers get founder pricing.',
      title_id='platformFounderOfferTitle',
      body='Lock in an early rate, launch fast, and grow into sponsor and membership lanes without rebuilding from scratch.',
      actions=promo_actions
    %}
      {% include "platform/_partials/_promo_bar.html" %}
    {% endwith %}""",
                "home founder offer → _promo_bar",
            ),
            (
"""    <div class="ff-card ff-glass ff-pad ff-mt-3" aria-labelledby="platformSellNowTitle">
      <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
        <div class="ff-minw-0">
          <p class="ff-kicker ff-m-0">Sell it now</p>
          <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformSellNowTitle">Use this platform as your live sales demo.</h2>
          <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
            Show the public fundraiser, the onboarding flow, and the dashboard together to position FutureFunded as a full revenue system for youth programs.
          </p>
        </div>
        <div class="ff-row ff-wrap ff-gap-2">
          <a class="ff-btn ff-btn--primary ff-btn--pill" href="/c/spring-fundraiser">Open live fundraiser</a>
          <a class="ff-btn ff-btn--secondary ff-btn--pill" href="/platform/dashboard">Open dashboard</a>
        </div>
      </div>
    </div>""",
"""    {% set promo_actions = [
      {'href': '/c/spring-fundraiser', 'label': 'Open live fundraiser', 'variant': 'primary'},
      {'href': '/platform/dashboard', 'label': 'Open dashboard', 'variant': 'secondary'}
    ] %}
    {% with
      kicker='Sell it now',
      title='Use this platform as your live sales demo.',
      title_id='platformSellNowTitle',
      body='Show the public fundraiser, the onboarding flow, and the dashboard together to position FutureFunded as a full revenue system for youth programs.',
      actions=promo_actions
    %}
      {% include "platform/_partials/_promo_bar.html" %}
    {% endwith %}""",
                "home sell-now → _promo_bar",
            ),
            (
"""    <div class="ff-card ff-glass ff-pad ff-mt-3" aria-labelledby="platformHomeCloseTitle">
      <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
        <div class="ff-minw-0">
          <p class="ff-kicker ff-m-0">Launch your first customer</p>
          <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformHomeCloseTitle">Use FutureFunded as the page you sell from.</h2>
          <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
            Show the live fundraiser, the onboarding flow, and the dashboard together to position FutureFunded as a premium revenue system for youth programs.
          </p>
        </div>
        <div class="ff-row ff-wrap ff-gap-2">
          <a class="ff-btn ff-btn--primary ff-btn--pill" href="/platform/demo">Open guided demo</a>
          <a class="ff-btn ff-btn--secondary ff-btn--pill" href="/platform/pricing">View pricing</a>
        </div>
      </div>
    </div>""",
"""    {% set promo_actions = [
      {'href': '/platform/demo', 'label': 'Open guided demo', 'variant': 'primary'},
      {'href': '/platform/pricing', 'label': 'View pricing', 'variant': 'secondary'}
    ] %}
    {% with
      kicker='Launch your first customer',
      title='Use FutureFunded as the page you sell from.',
      title_id='platformHomeCloseTitle',
      body='Show the live fundraiser, the onboarding flow, and the dashboard together to position FutureFunded as a premium revenue system for youth programs.',
      actions=promo_actions
    %}
      {% include "platform/_partials/_promo_bar.html" %}
    {% endwith %}""",
                "home close → _promo_bar",
            ),
        ],
        "dashboard": [
            (
"""    <div class="ff-card ff-glass ff-pad ff-mt-3" aria-labelledby="platformRevenueFocusTitle">
      <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
        <div class="ff-minw-0">
          <p class="ff-kicker ff-m-0">Revenue focus</p>
          <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformRevenueFocusTitle">The next money move is sponsor conversion.</h2>
          <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
            Direct giving gets the fundraiser live. Sponsor packages and recurring memberships are what turn it into a longer-term revenue system.
          </p>
        </div>
        <div class="ff-row ff-wrap ff-gap-2">
          <a class="ff-btn ff-btn--primary ff-btn--pill" href="/c/spring-fundraiser#sponsors">Open sponsor section</a>
          <a class="ff-btn ff-btn--secondary ff-btn--pill" href="/platform/onboarding">Create another launch</a>
        </div>
      </div>
    </div>""",
"""    {% set promo_actions = [
      {'href': '/c/spring-fundraiser#sponsors', 'label': 'Open sponsor section', 'variant': 'primary'},
      {'href': '/platform/onboarding', 'label': 'Create another launch', 'variant': 'secondary'}
    ] %}
    {% with
      kicker='Revenue focus',
      title='The next money move is sponsor conversion.',
      title_id='platformRevenueFocusTitle',
      body='Direct giving gets the fundraiser live. Sponsor packages and recurring memberships are what turn it into a longer-term revenue system.',
      actions=promo_actions
    %}
      {% include "platform/_partials/_promo_bar.html" %}
    {% endwith %}""",
                "dashboard revenue focus → _promo_bar",
            ),
            (
"""    <div class="ff-card ff-glass ff-pad ff-mt-3" aria-labelledby="platformSalesOpsTitle">
      <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
        <div class="ff-minw-0">
          <p class="ff-kicker ff-m-0">Sales operator note</p>
          <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformSalesOpsTitle">This dashboard is part of the sales pitch.</h2>
          <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
            The strongest demo is showing that one org can launch a public fundraiser, activate sponsor-ready lanes, and manage everything from one branded operator surface.
          </p>
        </div>
        <div class="ff-row ff-wrap ff-gap-2">
          <a class="ff-btn ff-btn--primary ff-btn--pill" href="/platform/">Open platform home</a>
          <a class="ff-btn ff-btn--secondary ff-btn--pill" href="/c/spring-fundraiser">Open live fundraiser</a>
        </div>
      </div>
    </div>""",
"""    {% set promo_actions = [
      {'href': '/platform/', 'label': 'Open platform home', 'variant': 'primary'},
      {'href': '/c/spring-fundraiser', 'label': 'Open live fundraiser', 'variant': 'secondary'}
    ] %}
    {% with
      kicker='Sales operator note',
      title='This dashboard is part of the sales pitch.',
      title_id='platformSalesOpsTitle',
      body='The strongest demo is showing that one org can launch a public fundraiser, activate sponsor-ready lanes, and manage everything from one branded operator surface.',
      actions=promo_actions
    %}
      {% include "platform/_partials/_promo_bar.html" %}
    {% endwith %}""",
                "dashboard sales note → _promo_bar",
            ),
        ],
        "onboarding": [
            (
"""      <div class="ff-card ff-glass ff-pad ff-mt-3" aria-labelledby="platformOnboardingCloseTitle">
        <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
          <div class="ff-minw-0">
            <p class="ff-kicker ff-m-0">Founder setup lane</p>
            <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformOnboardingCloseTitle">Use this form as your guided launch close.</h2>
            <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
              For self-serve users, it gets them live fast. For founder-led customers, it becomes the intake step for a done-with-you setup offer.
            </p>
          </div>
          <div class="ff-row ff-wrap ff-gap-2">
            <a class="ff-btn ff-btn--secondary ff-btn--pill" href="/platform/pricing">View pricing</a>
            <a class="ff-btn ff-btn--secondary ff-btn--pill" href="/platform/demo">View demo</a>
          </div>
        </div>
      </div>""",
"""      {% set promo_actions = [
        {'href': '/platform/pricing', 'label': 'View pricing', 'variant': 'secondary'},
        {'href': '/platform/demo', 'label': 'View demo', 'variant': 'secondary'}
      ] %}
      {% with
        kicker='Founder setup lane',
        title='Use this form as your guided launch close.',
        title_id='platformOnboardingCloseTitle',
        body='For self-serve users, it gets them live fast. For founder-led customers, it becomes the intake step for a done-with-you setup offer.',
        actions=promo_actions
      %}
        {% include "platform/_partials/_promo_bar.html" %}
      {% endwith %}""",
                "onboarding close → _promo_bar",
            ),
        ],
    }

    for old, new, label in promos.get(page, []):
        text = replace_if_present(text, old, new, label, changes)

    return text

def patch_pricing_demo_intro_cleanup(text: str, page: str, changes: list[str]) -> str:
    # leave route structure intact, but remove style drift + align to shared utility classes
    before = text
    text = generic_platform_cleanup(text, changes)

    # make sure pricing/demo intro grids use the platform helper if still on raw grid
    text = text.replace(
        '<div class="ff-grid ff-grid--2 ff-gap-3">',
        '<div class="ff-grid ff-grid--2 ff-gap-3 ff-platformGridTop">',
        1
    )

    if text != before:
        changes.append(f"{page} intro cleaned without route redesign")

    return text

def process_file(name: str, text: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    text = generic_platform_cleanup(text, changes)

    if name == "dashboard":
        text = patch_dashboard_intro(text, changes)
    elif name == "onboarding":
        text = patch_onboarding_intro(text, changes)

    if name in {"home", "dashboard", "onboarding"}:
        text = patch_known_promo_blocks(text, name, changes)

    if name in {"pricing", "demo"}:
        text = patch_pricing_demo_intro_cleanup(text, name, changes)

    # gentle whitespace cleanup
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, changes

def main():
    write_partials()

    backups = {}
    report = {}

    for name in ["home", "dashboard", "onboarding", "pricing", "demo"]:
        path = TARGETS[name]
        backups[name] = backup(path)
        original = path.read_text(encoding="utf-8")
        updated, changes = process_file(name, original)
        write(path, updated)
        report[name] = changes

    print("✅ ff_platform_repo_surgery_v1 applied")
    for name, bak in backups.items():
        print(f"🛟 backup[{name}]: {bak}")

    print(f"✅ partial: {TARGETS['intro_partial']}")
    print(f"✅ partial: {TARGETS['promo_partial']}")

    print("\n== CHANGE REPORT ==")
    for name in ["home", "dashboard", "onboarding", "pricing", "demo"]:
        items = report[name] or ["no-op / already normalized"]
        print(f"\n[{name}]")
        for item in items:
            print(f" - {item}")

    print("\n== INLINE STYLE CHECK ==")
    for name in ["home", "dashboard", "onboarding", "pricing", "demo"]:
        text = TARGETS[name].read_text(encoding="utf-8")
        hits = len(re.findall(r'style="', text))
        print(f"{name}: {hits}")

if __name__ == "__main__":
    main()
