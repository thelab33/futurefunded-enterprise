from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import sys

ROOT = Path.home() / "futurefunded-enterprise"

MARKETING = ROOT / "apps/web/app/templates/platform/shells/marketing_base.html"
OPERATOR = ROOT / "apps/web/app/templates/platform/shells/operator_base.html"
TOPBAR = ROOT / "apps/web/app/templates/shared/partials/_platform_topbar.html"
STATUS = ROOT / "apps/web/app/templates/shared/partials/_platform_status_bar.html"

FILES = [MARKETING, OPERATOR, TOPBAR, STATUS]


def backup(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = path.with_name(f"{path.name}.bak.{ts}")
    shutil.copy2(path, bak)
    return bak


def ensure_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"missing file: {path}")


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def patch_shell(path: Path, surface: str) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    original = text
    notes: list[str] = []

    page_marker = "{% if not _platform_page %}{% set _platform_page = 'home' %}{% endif %}"
    surface_block = f"\n\n{{% set _platform_surface = '{surface}' %}}"

    if "{% set _platform_surface =" not in text:
        if page_marker not in text:
            raise RuntimeError(f"{path}: could not find _platform_page marker")
        text = text.replace(page_marker, page_marker + surface_block, 1)
        notes.append(f"added _platform_surface={surface}")

    old_routes = """'routes': {
    'home': '/platform/',
    'onboarding': '/platform/onboarding',
    'dashboard': '/platform/dashboard'
  }"""
    new_routes = """'routes': {
    'home': '/platform/',
    'pricing': '/platform/pricing',
    'demo': '/platform/demo',
    'onboarding': '/platform/onboarding',
    'dashboard': '/platform/dashboard'
  }"""

    if old_routes in text:
        text = text.replace(old_routes, new_routes, 1)
        notes.append("expanded ffPlatformConfig.routes")
    elif new_routes in text:
        notes.append("routes already expanded")
    else:
        raise RuntimeError(f"{path}: could not find routes block")

    surface_anchor = """'brand': _brand,
  'canonical': canonical,"""
    surface_replacement = """'brand': _brand,
  'surface': _platform_surface,
  'canonical': canonical,"""

    if "'surface': _platform_surface," not in text:
        if surface_anchor not in text:
            raise RuntimeError(f"{path}: could not find platform config surface anchor")
        text = text.replace(surface_anchor, surface_replacement, 1)
        notes.append("added surface to ffPlatformConfig")
    else:
        notes.append("surface already present in ffPlatformConfig")

    literal_attr = f'data-ff-platform-surface="{surface}"'
    dynamic_attr = 'data-ff-platform-surface="{{ _platform_surface|e }}"'
    if literal_attr in text:
        text = text.replace(literal_attr, dynamic_attr, 1)
        notes.append("made body surface attribute dynamic")
    elif dynamic_attr in text:
        notes.append("body surface attribute already dynamic")
    else:
        raise RuntimeError(f"{path}: could not find body surface attribute")

    changed = text != original
    if changed:
        write_text(path, text)
    return changed, notes


TOPBAR_TEXT = """<div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
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

  <nav
    class="ff-navPill ff-glass ff-surface ff-nav ff-nav--pill"
    aria-label="Platform navigation"
  >
    {% if _platform_surface == 'operator' %}
      <a
        class="ff-nav__link"
        href="/platform/dashboard"
        {% if _platform_page == 'dashboard' %}aria-current="page"{% endif %}
      >Dashboard</a>
      <a
        class="ff-nav__link"
        href="/platform/onboarding"
        {% if _platform_page == 'onboarding' %}aria-current="page"{% endif %}
      >Onboarding</a>
    {% else %}
      <a
        class="ff-nav__link"
        href="/platform/"
        {% if _platform_page in ['home', 'platform', 'index'] %}aria-current="page"{% endif %}
      >Home</a>
      <a
        class="ff-nav__link"
        href="/platform/pricing"
        {% if _platform_page == 'pricing' %}aria-current="page"{% endif %}
      >Pricing</a>
      <a
        class="ff-nav__link"
        href="/platform/demo"
        {% if _platform_page == 'demo' %}aria-current="page"{% endif %}
      >Demo</a>
    {% endif %}
  </nav>

  <div class="ff-row ff-wrap ff-gap-2">
    {% if _platform_surface == 'operator' %}
      <a class="ff-btn ff-btn--secondary ff-btn--pill" href="/c/spring-fundraiser">
        Open live page
      </a>
    {% else %}
      <a class="ff-btn ff-btn--secondary ff-btn--pill" href="/c/spring-fundraiser">
        Live example
      </a>
      <a class="ff-btn ff-btn--primary ff-btn--pill" href="/platform/onboarding">
        Start launch
      </a>
    {% endif %}
  </div>
</div>
"""

STATUS_TEXT = """{% set _status_is_operator = (_platform_surface == 'operator') %}

<section
  class="ff-glass ff-surface ff-pad ff-mt-3"
  aria-label="{{ 'Operator status strip' if _status_is_operator else 'Platform trust strip' }}"
  data-ff-platform-trust=""
>
  <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
    <div class="ff-minw-0">
      {% if _status_is_operator %}
        <p class="ff-kicker ff-m-0">Operator workspace</p>
        <p class="ff-help ff-muted ff-mt-1 ff-mb-0">
          Manage live campaigns, sponsor tiers, and support lanes from one clean operating surface.
        </p>
      {% else %}
        <p class="ff-kicker ff-m-0">Revenue operating system</p>
        <p class="ff-help ff-muted ff-mt-1 ff-mb-0">
          Launch sponsor-ready fundraisers, branded program hubs, and recurring support from one premium workspace.
        </p>
      {% endif %}
    </div>

    <div class="ff-row ff-wrap ff-gap-2" role="list" aria-label="Platform trust signals">
      {% if _status_is_operator %}
        <span class="ff-pill ff-pill--soft" role="listitem">Live workspace</span>
        <span class="ff-pill ff-pill--soft" role="listitem">Campaign-ready</span>
        <span class="ff-pill ff-pill--ghost" role="listitem">Operator view</span>
      {% else %}
        <span class="ff-pill ff-pill--soft" role="listitem">Sponsor-ready</span>
        <span class="ff-pill ff-pill--soft" role="listitem">Brand-ready</span>
        <span class="ff-pill ff-pill--ghost" role="listitem">Launch fast</span>
      {% endif %}
    </div>
  </div>
</section>
"""


def main() -> int:
    print("== FF PLATFORM ARCHITECTURE PASS V1 ==")

    for path in FILES:
        ensure_exists(path)

    backups = []
    for path in FILES:
        bak = backup(path)
        backups.append((path, bak))

    changed_any = False

    changed, notes = patch_shell(MARKETING, "marketing")
    changed_any = changed_any or changed
    print(f"patched: {MARKETING}")
    for note in notes:
        print(f"  - {note}")

    changed, notes = patch_shell(OPERATOR, "operator")
    changed_any = changed_any or changed
    print(f"patched: {OPERATOR}")
    for note in notes:
        print(f"  - {note}")

    old_topbar = TOPBAR.read_text(encoding="utf-8")
    if old_topbar != TOPBAR_TEXT.rstrip() + "\n":
        write_text(TOPBAR, TOPBAR_TEXT)
        changed_any = True
        print(f"rewrote: {TOPBAR}")
    else:
        print(f"unchanged: {TOPBAR}")

    old_status = STATUS.read_text(encoding="utf-8")
    if old_status != STATUS_TEXT.rstrip() + "\n":
        write_text(STATUS, STATUS_TEXT)
        changed_any = True
        print(f"rewrote: {STATUS}")
    else:
        print(f"unchanged: {STATUS}")

    print("\\nbackups:")
    for path, bak in backups:
        print(f"  - {path.name} -> {bak.name}")

    print("\\nresult:")
    print("  - changed" if changed_any else "  - no-op (already aligned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
