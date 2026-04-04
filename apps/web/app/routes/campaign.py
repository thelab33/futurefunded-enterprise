from flask import Blueprint, current_app, render_template
from urllib.parse import urlparse

from app.data.campaign_store import get_campaign

bp = Blueprint("campaign", __name__)


def _public_base_url() -> str:
    configured = (
        current_app.config.get("FF_PUBLIC_BASE_URL")
        or current_app.config.get("PUBLIC_BASE_URL")
        or current_app.config.get("CANONICAL_BASE_URL")
    )

    configured = str(configured or "").rstrip("/")
    app_env = str(
        current_app.config.get("APP_ENV")
        or current_app.config.get("FLASK_ENV")
        or current_app.config.get("ENV")
        or ""
    ).lower()
    is_prod = app_env == "production"

    if is_prod:
        if not configured or _is_localish_url(configured):
            raise RuntimeError(
                "Production PUBLIC_BASE_URL/CANONICAL_BASE_URL is missing or points to localhost."
            )
        return configured

    return configured or "https://getfuturefunded.com"

def _is_localish_url(value: str | None) -> bool:
    if not value:
        return True
    host = (urlparse(str(value)).hostname or "").lower()
    return host in {"127.0.0.1", "localhost", "::1"}


def _normalize_campaign_context(data: dict, slug: str) -> dict:
    ctx = dict(data or {})
    base = _public_base_url().rstrip("/")
    is_prodish = not _is_localish_url(base)
    campaign_url = f"{base}/c/{slug}"

    ctx["canonical"] = campaign_url
    ctx["share_url"] = campaign_url
    ctx["campaign_url"] = campaign_url
    # Public-surface source of truth for the Jinja contract.
    # The campaign template reads these early for canonical/meta/schema/return wiring.
    ctx["ff_public_base_url"] = base
    ctx["canonical_url"] = campaign_url
    ctx["stripe_return_url"] = campaign_url
    ctx["_share_url_resolved"] = campaign_url
    ctx["_stripe_return"] = campaign_url

    if is_prodish:
        ctx["ff_data_mode"] = "live"
        ctx["_totals_verified"] = True
        ctx["ff_allow_test_payments_demo"] = False

    return ctx

def _demo_campaign_context(slug: str) -> dict:
    base = _public_base_url()
    return {
        "config": current_app.config,
        "org_name": "Connect ATX Elite",
        "campaign_name": "Spring Fundraiser",
        "campaign_location": "Austin, TX",
        "campaign_headline": "Fuel the season. Fund the future.",
        "campaign_subhead": "Back the athletes of",
        "campaign_tagline": "Support travel, training, tournament fees, and shared team costs with one secure gift.",
        "fundraiser_goal": 10000,
        "amount_raised": 175,
        "goal": 10000,
        "raised": 175,
        "announcement_text": "Season support is live now.",
        "proof_blurb": "This program helps athletes train, compete, travel, and grow together.",
        "policy_blurb": "Questions, corrections, or receipts: email the organizer address listed on this page.",
        "terms_url": "https://getfuturefunded.com/terms",
        "privacy_url": "https://getfuturefunded.com/privacy",
        "teams_list": [
            {
                "id": "6g",
                "name": "6th Grade Gold",
                "tier": "Gold",
                "meta": "First AAU reps — fundamentals + communication.",
                "featured": True,
                "needs": False,
            },
            {
                "id": "7g",
                "name": "7th Grade Gold",
                "tier": "Gold",
                "meta": "Speed + spacing — film + pressure reps.",
                "featured": True,
                "needs": False,
            },
            {
                "id": "7b",
                "name": "7th Grade Black",
                "tier": "Black",
                "meta": "Defense travels — stops into transition.",
                "featured": False,
                "needs": True,
            },
            {
                "id": "8g",
                "name": "8th Grade Gold",
                "tier": "Gold",
                "meta": "Finish strong — intensity + leadership.",
                "featured": False,
                "needs": False,
            },
        ],
        "share_url": f"{base}/c/{slug}",
        "campaign_url": f"{base}/c/{slug}",
    }


@bp.get("/c/<slug>")
@bp.get("/campaign/<slug>")
def campaign(slug: str):
    data = get_campaign(slug)
    if not data:
        data = _demo_campaign_context(slug)
        data = _normalize_campaign_context(data, slug)
    return render_template("campaign/index.html", **data)
