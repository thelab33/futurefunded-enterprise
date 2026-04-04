from __future__ import annotations
from pathlib import Path
import re
import shutil
from datetime import datetime

ROOT = Path(".").resolve()
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")

targets = {
    "base": ROOT / "apps/web/app/templates/platform/base.html",
    "home": ROOT / "apps/web/app/templates/platform/home.html",
    "dashboard": ROOT / "apps/web/app/templates/platform/dashboard.html",
    "onboarding": ROOT / "apps/web/app/templates/platform/onboarding.html",
    "platform_css": ROOT / "apps/web/app/static/css/platform-pages.css",
    "ownership_doc": ROOT / "docs/architecture/frontend-ownership.md",
}

for key, path in targets.items():
    if key == "ownership_doc":
        continue
    if not path.exists():
        raise SystemExit(f"❌ Missing required file: {path}")

def backup(path: Path) -> Path:
    bak = path.with_name(path.name + f".bak-platform-cleanup-{STAMP}")
    shutil.copy2(path, bak)
    return bak

backups = {}
for key, path in targets.items():
    if key == "ownership_doc":
        continue
    backups[key] = backup(path)

# -------------------------------------------------------------------
# platform/base.html
# -------------------------------------------------------------------
base = targets["base"].read_text(encoding="utf-8")

old_styles = """  <link rel="stylesheet" href="{{ url_for('static', filename='css/ff.css') }}?v={{ _asset_v|e }}" />
  <link rel="stylesheet" href="{{ url_for('static', filename='css/ff-above-main-premium.css') }}?v={{ _asset_v|e }}" />
  <link rel="stylesheet" href="{{ url_for('static', filename='css/platform-pages.css') }}?v={{ _asset_v|e }}" />

  <script
"""

new_styles = """  <link rel="stylesheet" href="{{ url_for('static', filename='css/ff.css') }}?v={{ _asset_v|e }}" />
  <link rel="stylesheet" href="{{ url_for('static', filename='css/platform-pages.css') }}?v={{ _asset_v|e }}" />
  {% set _platform_use_premium_bridge = (
    platform_use_premium_bridge|default(false, true)
  ) %}
  {% if _platform_use_premium_bridge %}
    <link rel="stylesheet" href="{{ url_for('static', filename='css/ff-above-main-premium.css') }}?v={{ _asset_v|e }}" />
  {% endif %}

  <script
"""

if old_styles in base:
    base = base.replace(old_styles, new_styles, 1)

base = base.replace(
    '<div class="ff-container" style="padding-top:1.25rem;">',
    '<div class="ff-container ff-platformChrome__inner">',
)

base = base.replace(
    '''              <span
                class="ff-help ff-muted"
                style="display:block; letter-spacing:.08em; text-transform:uppercase;"
              >''',
    '''              <span class="ff-help ff-muted ff-platformBrand__subline">'''
)

targets["base"].write_text(base, encoding="utf-8")

# -------------------------------------------------------------------
# shared inline-style cleanup helper
# -------------------------------------------------------------------
def replace_style_class(text: str, old: str, new: str) -> str:
    return text.replace(old, new)

# -------------------------------------------------------------------
# platform/home.html
# -------------------------------------------------------------------
home = targets["home"].read_text(encoding="utf-8")
home = replace_style_class(home, '<div class="ff-grid ff-grid--2 ff-gap-3" style="align-items:start;">', '<div class="ff-grid ff-grid--2 ff-gap-3 ff-platformGridTop">')
home = home.replace('class="ff-display ff-mt-2 ff-mb-0"\n          style="max-width:11ch;"', 'class="ff-display ff-mt-2 ff-mb-0 ff-measure-11"')
home = home.replace('class="ff-lead ff-mt-3 ff-mb-0" style="max-width:38ch;"', 'class="ff-lead ff-mt-3 ff-mb-0 ff-measure-38"')
home = home.replace('class="ff-display ff-mt-2 ff-mb-0"\n          style="max-width:10ch;"', 'class="ff-display ff-mt-2 ff-mb-0 ff-measure-10"')
home = home.replace('class="ff-lead ff-mt-3 ff-mb-0" style="max-width:36ch;"', 'class="ff-lead ff-mt-3 ff-mb-0 ff-measure-36"')
targets["home"].write_text(home, encoding="utf-8")

# -------------------------------------------------------------------
# platform/dashboard.html
# -------------------------------------------------------------------
dashboard = targets["dashboard"].read_text(encoding="utf-8")
dashboard = replace_style_class(dashboard, '<div class="ff-grid ff-grid--2 ff-gap-3" style="align-items:start;">', '<div class="ff-grid ff-grid--2 ff-gap-3 ff-platformGridTop">')
dashboard = dashboard.replace('class="ff-display ff-mt-2 ff-mb-0"\n            id="platformDashboardTitle"\n            style="max-width:12ch;"', 'class="ff-display ff-mt-2 ff-mb-0 ff-measure-12"\n            id="platformDashboardTitle"')
dashboard = dashboard.replace('class="ff-lead ff-mt-3 ff-mb-0" style="max-width:42ch;"', 'class="ff-lead ff-mt-3 ff-mb-0 ff-measure-42"')
targets["dashboard"].write_text(dashboard, encoding="utf-8")

# -------------------------------------------------------------------
# platform/onboarding.html
# -------------------------------------------------------------------
onboarding = targets["onboarding"].read_text(encoding="utf-8")
onboarding = replace_style_class(onboarding, '<div class="ff-grid ff-grid--2 ff-gap-3" style="align-items:start;">', '<div class="ff-grid ff-grid--2 ff-gap-3 ff-platformGridTop">')
onboarding = onboarding.replace('class="ff-display ff-mt-2 ff-mb-0"\n            id="platformOnboardingTitle"\n            style="max-width:10ch;"', 'class="ff-display ff-mt-2 ff-mb-0 ff-measure-10"\n            id="platformOnboardingTitle"')
onboarding = onboarding.replace('class="ff-lead ff-mt-3 ff-mb-0" style="max-width:42ch;"', 'class="ff-lead ff-mt-3 ff-mb-0 ff-measure-42"')
targets["onboarding"].write_text(onboarding, encoding="utf-8")

# -------------------------------------------------------------------
# platform-pages.css
# -------------------------------------------------------------------
platform_css = targets["platform_css"].read_text(encoding="utf-8")

css_start = "/* FF_PLATFORM_CLEANUP_PASS1_START */"
css_end = "/* FF_PLATFORM_CLEANUP_PASS1_END */"

css_block = """
/* FF_PLATFORM_CLEANUP_PASS1_START */
body[data-ff-platform="true"] .ff-platformChrome__inner {
  padding-top: 1.25rem;
}

body[data-ff-platform="true"] .ff-platformBrand__subline {
  display: block;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

body[data-ff-platform="true"] .ff-platformGridTop {
  align-items: start;
}

body[data-ff-platform="true"] .ff-measure-10 {
  max-width: 10ch;
}

body[data-ff-platform="true"] .ff-measure-11 {
  max-width: 11ch;
}

body[data-ff-platform="true"] .ff-measure-12 {
  max-width: 12ch;
}

body[data-ff-platform="true"] .ff-measure-36 {
  max-width: 36ch;
}

body[data-ff-platform="true"] .ff-measure-38 {
  max-width: 38ch;
}

body[data-ff-platform="true"] .ff-measure-42 {
  max-width: 42ch;
}
/* FF_PLATFORM_CLEANUP_PASS1_END */
""".strip() + "\n"

if css_start in platform_css and css_end in platform_css:
    platform_css = re.sub(
        re.escape(css_start) + r".*?" + re.escape(css_end),
        css_block.strip(),
        platform_css,
        flags=re.S,
    )
else:
    platform_css = platform_css.rstrip() + "\n\n" + css_block

targets["platform_css"].write_text(platform_css, encoding="utf-8")

# -------------------------------------------------------------------
# ownership doc
# -------------------------------------------------------------------
doc = """# FutureFunded Frontend Ownership

## CSS ownership
- `apps/web/app/static/css/ff.css`
  - shared cross-app foundation
  - campaign core primitives
  - safe shared utilities used by both campaign and platform

- `apps/web/app/static/css/platform-pages.css`
  - platform-only layout and presentation
  - onboarding, dashboard, pricing, demo, and platform home
  - should own platform-specific overrides and layout helpers

- `apps/web/app/static/css/ff-above-main-premium.css`
  - campaign premium bridge / residual campaign-only layer
  - do **not** load by default on platform pages
  - opt in only when a specific platform page explicitly needs it

## Template ownership
- `apps/web/app/templates/campaign/index.html`
  - public campaign surface only

- `apps/web/app/templates/platform/base.html`
  - shared platform shell only
  - shared nav, trust strip, canonical/meta, platform config payload

- `apps/web/app/templates/platform/*.html`
  - page-specific platform content only
  - avoid inline styles
  - avoid redefining global shell behavior here

## Cleanup rule
When changing platform UI:
1. Prefer `platform-pages.css`
2. Use `ff.css` only for shared primitives
3. Avoid touching campaign template/CSS unless the campaign itself changed
"""
targets["ownership_doc"].write_text(doc, encoding="utf-8")

print("✅ platform cleanup pass 1 applied")
for key, bak in backups.items():
    print(f"🛟 backup[{key}]: {bak}")
print(f"📝 doc: {targets['ownership_doc']}")
