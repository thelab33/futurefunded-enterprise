from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
TARGET = ROOT / "apps/web/app/routes/platform.py"

if not TARGET.exists():
    raise SystemExit(f"Missing target file: {TARGET}")

text = TARGET.read_text(encoding="utf-8")

if "from copy import deepcopy" not in text:
    import_block = re.compile(r"^(from __future__ import annotations\s*\n)", re.M)
    if import_block.search(text):
        text = import_block.sub(r"\1from copy import deepcopy\n", text, count=1)
    else:
        text = "from copy import deepcopy\n" + text

start_anchor = "def _fallback_pricing() -> dict:"
end_anchor = '@bp.get("/demo")'

start_idx = text.find(start_anchor)
end_idx = text.find(end_anchor)

if start_idx < 0:
    raise SystemExit("Could not find start anchor: def _fallback_pricing() -> dict:")
if end_idx < 0:
    raise SystemExit('Could not find end anchor: @bp.get("/demo")')

demo_return_anchor = 'def demo():\n    return _render_platform_page(page_key="demo")'
demo_return_idx = text.find(demo_return_anchor, end_idx)
if demo_return_idx < 0:
    raise SystemExit('Could not find demo route body anchor')

end_idx = demo_return_idx + len(demo_return_anchor)

replacement = '''def _fallback_pricing() -> dict:
    return {
        "page_title": "FutureFunded Pricing",
        "page_description": (
            "Simple, premium pricing for FutureFunded — launch sponsor-ready fundraisers, "
            "branded program hubs, and recurring support lanes for teams, schools, and youth organizations."
        ),
        "eyebrow": "Pricing",
        "title": "Launch a sponsor-ready fundraiser in minutes.",
        "body": (
            "FutureFunded helps youth teams, schools, nonprofits, and clubs launch public "
            "fundraisers, sponsor packages, and recurring support from one premium workspace."
        ),
        "hero_pills": ["Founder-friendly", "Sponsor-ready", "Launch fast"],
        "plans": [
            {
                "name": "Starter",
                "price": "$49 setup",
                "body": "Best for teams that want a premium public fundraiser fast.",
                "fit": "Perfect for first launches and founder-led setup offers.",
                "cta_label": "Start with Starter",
                "cta_href": "/platform/onboarding",
            },
            {
                "name": "Growth",
                "price": "$79/mo",
                "body": "Best for programs ready to add sponsor packages and recurring support.",
                "fit": "Great for schools, clubs, and growing youth programs.",
                "cta_label": "Start Growth setup",
                "cta_href": "/platform/onboarding",
                "featured": True,
            },
            {
                "name": "White-label",
                "price": "Custom",
                "body": (
                    "Best for schools, nonprofits, and larger organizations that want a fuller "
                    "branded operating system."
                ),
                "fit": "Best when you want the platform to feel like your organization’s own system.",
                "cta_label": "Request white-label path",
                "cta_href": "/platform/demo",
            },
        ],
        "actions": [
            {"label": "Start guided launch", "href": "/platform/onboarding"},
            {"label": "View guided demo", "href": "/platform/demo"},
        ],
        "included_cards": [
            {
                "title": "Public fundraiser",
                "body": (
                    "A polished page for direct giving, cleaner storytelling, and sponsor-ready "
                    "presentation from the start."
                ),
            },
            {
                "title": "Operator dashboard",
                "body": (
                    "A premium workspace for launch, oversight, positioning, and "
                    "program-by-program expansion."
                ),
            },
            {
                "title": "Sponsor packages + recurring support",
                "body": (
                    "Sponsor packages and recurring support that extend value beyond one campaign."
                ),
            },
        ],
    }


def _fallback_demo() -> dict:
    return {
        "page_title": "FutureFunded Demo",
        "page_description": (
            "See how the public fundraiser, onboarding flow, pricing, and operator dashboard work together."
        ),
        "eyebrow": "Demo",
        "title": "See FutureFunded in action.",
        "body": (
            "This guided demo shows the public fundraiser, onboarding flow, "
            "operator dashboard, and founder-ready pricing as one clean sales sequence."
        ),
        "steps": [
            {
                "label": "Step 1",
                "title": "Public fundraiser",
                "body": "Show the polished donation surface, sponsor offers, and public trust signals first.",
                "href": "/c/spring-fundraiser",
            },
            {
                "label": "Step 2",
                "title": "Onboarding flow",
                "body": "Show how quickly a team or organization can move from setup to a launch-ready page.",
                "href": "/platform/onboarding",
            },
            {
                "label": "Step 3",
                "title": "Operator dashboard",
                "body": (
                    "Position FutureFunded as a system — public fundraiser, operator dashboard, "
                    "and revenue lanes — not just a page."
                ),
                "href": "/platform/dashboard",
            },
            {
                "label": "Step 4",
                "title": "Founder pricing",
                "body": "End the demo with a simple pricing story that makes it easy to say yes.",
                "href": "/platform/pricing",
            },
        ],
        "actions": [
            {"label": "Start guided launch", "href": "/platform/onboarding"},
            {"label": "View live fundraiser", "href": "/c/spring-fundraiser"},
        ],
    }


PLATFORM_PAGE_CONFIG: dict[str, dict] = {
    "home": {
        "template_name": "platform/pages/home.html",
        "default_title": "FutureFunded Platform Home",
        "fallback_factory": _fallback_home,
        "api_path": "/api/v1/platform/home",
    },
    "pricing": {
        "template_name": "platform/pages/pricing.html",
        "default_title": "FutureFunded Pricing",
        "fallback_factory": _fallback_pricing,
        "api_path": "/api/v1/platform/pricing",
    },
    "demo": {
        "template_name": "platform/pages/demo.html",
        "default_title": "FutureFunded Demo",
        "fallback_factory": _fallback_demo,
        "api_path": "/api/v1/platform/demo",
    },
    "onboarding": {
        "template_name": "platform/pages/onboarding.html",
        "default_title": "FutureFunded Onboarding",
        "fallback_factory": _fallback_onboarding,
        "api_path": "/api/v1/platform/onboarding",
    },
    "dashboard": {
        "template_name": "platform/pages/dashboard.html",
        "default_title": "FutureFunded Dashboard",
        "fallback_factory": _fallback_dashboard,
        "api_path": "/api/v1/platform/dashboard",
    },
}


def _page_config(page_key: str) -> dict:
    config = PLATFORM_PAGE_CONFIG.get(page_key)
    if not config:
        raise KeyError(f"Unknown platform page_key: {page_key}")
    return config


def _resolve_fallback(config: dict, explicit_fallback: dict | None = None) -> dict:
    if isinstance(explicit_fallback, dict):
        return deepcopy(explicit_fallback)

    fallback_factory = config.get("fallback_factory")
    if callable(fallback_factory):
        produced = fallback_factory()
        if isinstance(produced, dict):
            return deepcopy(produced)

    fallback = config.get("fallback")
    if isinstance(fallback, dict):
        return deepcopy(fallback)

    return {}


def _render_platform_page(
    *,
    page_key: str,
    template_name: str | None = None,
    default_title: str | None = None,
    fallback: dict | None = None,
    api_path: str | None = None,
):
    config = _page_config(page_key)
    template_name = template_name or config.get("template_name")
    default_title = default_title or config.get("default_title", "FutureFunded Platform")
    resolved_fallback = _resolve_fallback(config, fallback)

    if api_path is None:
        api_path = config.get("api_path")

    if not template_name:
        raise KeyError(f"No platform template configured for page_key={page_key!r}")

    api_data = get_json(api_path, {}) if api_path else {}
    data = _deep_merge(resolved_fallback, api_data if isinstance(api_data, dict) else {})

    return render_template(
        template_name,
        page_title=data.get("page_title", default_title),
        page_description=data.get("page_description", ""),
        platform_page=page_key,
        data=data,
    )


@bp.get("/")
def home():
    return _render_platform_page(page_key="home")


@bp.get("/onboarding")
def onboarding():
    return _render_platform_page(page_key="onboarding")


@bp.get("/dashboard")
def dashboard():
    return _render_platform_page(page_key="dashboard")


@bp.get("/pricing")
def pricing():
    return _render_platform_page(page_key="pricing")


@bp.get("/demo")
def demo():
    return _render_platform_page(page_key="demo")
'''

new_text = text[:start_idx] + replacement + text[end_idx:]

ts = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = TARGET.with_name(f"{TARGET.name}.{ts}.bak")
shutil.copy2(TARGET, backup)
TARGET.write_text(new_text, encoding="utf-8")

print(f"changed: {TARGET}")
print(f"backup:  {backup}")
