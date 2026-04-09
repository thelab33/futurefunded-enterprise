from __future__ import annotations

from copy import deepcopy

from flask import Blueprint, redirect, render_template, url_for

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
        "page_title": "FutureFunded | Premium fundraising for teams, schools, clubs, and nonprofits",
        "page_description": (
            "Launch premium public fundraising, sponsor-ready support lanes, recurring "
            "memberships, and cleaner operator control from one polished FutureFunded platform."
        ),
        "hero": {
            "eyebrow": "Launch-ready fundraising platform",
            "title": "Launch premium fundraising pages, sponsor lanes, and recurring support from one platform.",
            "body": (
                "FutureFunded turns a youth program into a sponsor-ready, donor-ready "
                "fundraising presence with stronger branding, cleaner readability, and "
                "operator control that feels built — not pieced together."
            ),
            "primary_cta_href": "/platform/dashboard?view=launch",
            "primary_cta_label": "Open launch workspace",
            "secondary_cta_href": "/c/spring-fundraiser",
            "secondary_cta_label": "Open live fundraiser",
        },
        "next_move": {
            "eyebrow": "Next move",
            "title": "Launch with a cleaner fundraising system.",
            "body": (
                "Start with one polished organization, launch a premium public fundraiser, "
                "and grow into sponsor packages and recurring support without rebuilding the experience."
            ),
            "primary_cta_href": "/platform/dashboard?view=launch",
            "primary_cta_label": "Open launch workspace",
            "secondary_cta_href": "/platform/dashboard",
            "secondary_cta_label": "Open operator dashboard",
        },
    }


def _fallback_dashboard() -> dict:
    return {
        "page_title": "FutureFunded Dashboard",
        "page_description": (
            "Launch, manage, and monitor campaigns, sponsor lanes, recurring support, "
            "and organization workflow from one operator-ready workspace."
        ),
        "hero": {
            "eyebrow": "Operator workspace",
            "title": "Run fundraising like a system, not a spreadsheet.",
            "body": (
                "Monitor campaigns, sponsorships, memberships, launch readiness, and "
                "organization workflow from one polished FutureFunded dashboard."
            ),
        },
        "operator_notes": [
            "Open launch workspace fast",
            "Track campaign health clearly",
            "Manage sponsor momentum cleanly",
            "Keep follow-up and operations organized",
        ],
    }


PLATFORM_PAGE_CONFIG: dict[str, dict] = {
    "home": {
        "template_name": "platform/pages/home.html",
        "fallback": _fallback_home,
    },
    "dashboard": {
        "template_name": "platform/pages/dashboard.html",
        "fallback": _fallback_dashboard,
    },
}


def _fetch_platform_payload(page_key: str) -> dict:
    """
    Best-effort API fetch. If the API is unavailable or returns bad data,
    fall back to local page config.
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
        data=page_payload,  # canonical payload key used by templates
        page_title=page_payload.get("page_title"),
        page_description=page_payload.get("page_description"),
    )


@bp.get("/")
def home():
    return _render_platform_page(page_key="home")


@bp.get("/dashboard")
def dashboard():
    return _render_platform_page(page_key="dashboard")


# ---------------------------------------------------------------------------
# Legacy route bridge
# Keep these routes alive while the architecture consolidates.
# Use 302 redirects for now while iterating. Swap to 301 later if desired.
# ---------------------------------------------------------------------------

@bp.get("/onboarding")
def onboarding():
    return redirect(url_for("platform.dashboard", view="launch"), code=302)


@bp.get("/pricing")
def pricing():
    return redirect(url_for("platform.home", _anchor="plans"), code=302)


@bp.get("/demo")
def demo():
    return redirect(url_for("platform.home", _anchor="see-it-live"), code=302)
