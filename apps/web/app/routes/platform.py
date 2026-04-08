from __future__ import annotations

from copy import deepcopy

from flask import Blueprint, render_template

from app.services.api_client import get_json

bp = Blueprint("platform", __name__)


def _deep_merge(base: dict | None, override: dict | None) -> dict:
    """
    Merge override data onto base data without losing nested fallback structure.
    Lists are replaced wholesale. Dicts are merged recursively.
    """
    merged = deepcopy(base if isinstance(base, dict) else {})
    if not isinstance(override, dict):
        return merged

    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged.get(key, {}), value)
        else:
            merged[key] = deepcopy(value)

    return merged


def _fallback_home() -> dict:
    return {
        "page_title": "FutureFunded Platform Home",
        "page_description": (
            "Launch and manage premium fundraising pages, sponsor-ready packages, "
            "and recurring memberships from one branded FutureFunded workspace."
        ),
        "hero": {
            "eyebrow": "AAU launch-ready fundraising",
            "title": "Launch premium fundraising pages without the setup drag.",
            "body": (
                "FutureFunded helps youth teams, nonprofits, schools, and clubs go live "
                "with branded donation pages, sponsor lanes, memberships, and operator tools."
            ),
            "primary_cta": {
                "label": "Start guided launch",
                "href": "/platform/onboarding",
            },
            "secondary_cta": {
                "label": "View live fundraiser",
                "href": "/c/spring-fundraiser",
            },
        },
        "proof_points": [
            "Branded campaign pages",
            "Sponsor + donor revenue lanes",
            "Mobile-first checkout",
            "Operator dashboard workflow",
        ],
        "next_move": {
            "title": "Launch in one guided flow",
            "body": (
                "Upload a logo, set colors, connect payments, and go live with a "
                "credible sponsor-ready fundraising surface."
            ),
        },
    }


def _fallback_onboarding() -> dict:
    return {
        "page_title": "FutureFunded Onboarding",
        "page_description": (
            "Guided onboarding for teams, schools, nonprofits, and clubs launching "
            "a branded FutureFunded page."
        ),
        "hero": {
            "eyebrow": "Guided setup",
            "title": "Get your organization launch-ready fast.",
            "body": (
                "Create a premium fundraiser with your logo, colors, fundraising goal, "
                "story, sponsor packages, and payment setup."
            ),
        },
        "steps": [
            "Add organization details",
            "Upload logo and brand colors",
            "Set fundraising goal and story",
            "Enable donations and sponsor offers",
            "Preview and publish",
        ],
    }


def _fallback_dashboard() -> dict:
    return {
        "page_title": "FutureFunded Dashboard",
        "page_description": (
            "Track revenue lanes, campaign health, donor momentum, and sponsor performance "
            "from one operator-friendly workspace."
        ),
        "hero": {
            "eyebrow": "Operator workspace",
            "title": "Run fundraising like a system, not a spreadsheet.",
            "body": (
                "Monitor donations, sponsorships, memberships, campaign progress, "
                "and launch readiness from one polished dashboard."
            ),
        },
        "operator_notes": [
            "Track raised vs goal",
            "See sponsor interest clearly",
            "Spot conversion friction early",
            "Keep launch and follow-up organized",
        ],
    }


def _fallback_pricing() -> dict:
    return {
        "page_title": "FutureFunded Pricing",
        "page_description": (
            "Founder-friendly pricing for premium fundraising pages, sponsor-ready upgrades, "
            "and organization onboarding."
        ),
        "hero": {
            "eyebrow": "Simple pricing",
            "title": "Price the platform like a real revenue tool.",
            "body": (
                "Use FutureFunded as a launch-ready fundraising system with branded pages, "
                "sponsor visibility, memberships, and premium conversion UX."
            ),
        },
        "plans": [
            {
                "name": "Starter",
                "headline": "Get live fast",
                "price": "$0 setup + platform fee",
            },
            {
                "name": "Growth",
                "headline": "More sponsor leverage",
                "price": "$99/mo",
            },
            {
                "name": "Pro",
                "headline": "White-glove launch",
                "price": "Custom",
            },
        ],
    }


def _fallback_demo() -> dict:
    return {
        "page_title": "FutureFunded Demo",
        "page_description": (
            "Walk through the public fundraiser, onboarding flow, dashboard, and pricing "
            "as one clean founder-ready sales sequence."
        ),
        "hero": {
            "eyebrow": "Guided founder demo",
            "title": "Show the whole product story in one pass.",
            "body": (
                "Use the live fundraiser, guided onboarding, operator dashboard, and pricing "
                "surface together to sell FutureFunded as a complete system."
            ),
            "primary_cta": {
                "label": "Open live fundraiser",
                "href": "/c/spring-fundraiser",
            },
            "secondary_cta": {
                "label": "Start guided launch",
                "href": "/platform/onboarding",
            },
        },
    }


PLATFORM_PAGE_CONFIG: dict[str, dict] = {
    "home": {
        "template_name": "platform/pages/home.html",
        "fallback": _fallback_home,
    },
    "onboarding": {
        "template_name": "platform/pages/onboarding.html",
        "fallback": _fallback_onboarding,
    },
    "dashboard": {
        "template_name": "platform/pages/dashboard.html",
        "fallback": _fallback_dashboard,
    },
    "pricing": {
        "template_name": "platform/pages/pricing.html",
        "fallback": _fallback_pricing,
    },
    "demo": {
        "template_name": "platform/pages/demo.html",
        "fallback": _fallback_demo,
    },
}


def _fetch_platform_payload(page_key: str) -> dict:
    """
    Best-effort API fetch. If the API is unavailable or returns bad data,
    we fall back to the local config for that page.
    """
    try:
        payload = get_json(f"/api/platform/{page_key}")
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def _render_platform_page(page_key: str):
    config = PLATFORM_PAGE_CONFIG.get(page_key)
    if not config:
        raise KeyError(f"Unknown platform page: {page_key}")

    fallback_factory = config["fallback"]
    template_name = config["template_name"]

    fallback_payload = fallback_factory() if callable(fallback_factory) else {}
    remote_payload = _fetch_platform_payload(page_key)

    page_payload = _deep_merge(fallback_payload, remote_payload)

    return render_template(
        template_name,
        page_key=page_key,
        page_data=page_payload,
        page_title=page_payload.get("page_title"),
        page_description=page_payload.get("page_description"),
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
