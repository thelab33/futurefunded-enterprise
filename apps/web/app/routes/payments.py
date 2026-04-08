from __future__ import annotations

import os
from typing import Any

import stripe
from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("payments", __name__, url_prefix="/payments")

_TRUTHY = {"1", "true", "yes", "on"}


def _cfg(name: str, default: str = "") -> str:
    return str(
        current_app.config.get(name)
        or os.getenv(name)
        or default
    ).strip()


def _bool(name: str, default: bool = False) -> bool:
    raw = _cfg(name, "1" if default else "")
    return raw.lower() in _TRUTHY


def _stripe_pk() -> str:
    return (
        _cfg("STRIPE_PUBLISHABLE_KEY")
        or _cfg("STRIPE_PUBLIC_KEY")
        or _cfg("FF_STRIPE_PUBLISHABLE_KEY")
    )


def _paypal_client_id() -> str:
    return _cfg("PAYPAL_CLIENT_ID") or _cfg("FF_PAYPAL_CLIENT_ID")


def _paypal_enabled() -> bool:
    mode = (_cfg("PAYPAL_MODE") or "disabled").lower()
    client_id = _paypal_client_id()
    return bool(client_id and mode not in {"disabled", "off", "false", "0", ""})


@bp.get("/config")
def payments_config():
    return jsonify(
        {
            "stripe": {
                "enabled": bool(_stripe_pk()),
                "publishableKey": _stripe_pk(),
                "intentEndpoint": "/payments/stripe/intent",
            },
            "paypal": {
                "enabled": _paypal_enabled(),
                "clientId": _paypal_client_id(),
                "createEndpoint": "/payments/paypal/order",
                "captureEndpoint": "/payments/paypal/capture",
            },
        }
    )


@bp.get("/health")
def payments_health():
    stripe_secret = _cfg("STRIPE_SECRET_KEY")
    return jsonify(
        {
            "ok": bool(_stripe_pk() and stripe_secret),
            "stripe": {
                "publishableKeyLoaded": bool(_stripe_pk()),
                "secretKeyLoaded": bool(stripe_secret),
                "mode": _cfg("STRIPE_MODE", "unknown"),
            },
            "paypal": {
                "clientIdLoaded": bool(_paypal_client_id()),
                "mode": _cfg("PAYPAL_MODE", "disabled"),
                "enabled": _paypal_enabled(),
            },
        }
    )


@bp.post("/stripe/intent")
def create_stripe_intent():
    secret = _cfg("STRIPE_SECRET_KEY")
    if not secret:
        return jsonify({"error": "Stripe secret key is missing."}), 503

    payload: dict[str, Any] = request.get_json(silent=True) or {}
    amount_raw = payload.get("amount", 0)
    currency = str(payload.get("currency") or "usd").lower().strip()

    try:
        amount_cents = int(round(float(amount_raw) * 100))
    except Exception:
        return jsonify({"error": "Invalid amount."}), 400

    if amount_cents < 50:
        return jsonify({"error": "Minimum amount is $0.50."}), 400

    stripe.api_key = secret

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency,
            automatic_payment_methods={"enabled": True},
            metadata={
                "campaign_name": str(payload.get("campaign_name") or ""),
                "organization_name": str(payload.get("organization_name") or ""),
                "team_id": str(payload.get("team_id") or "default"),
                "player_id": str(payload.get("player_id") or ""),
                "supporting_label": str(payload.get("supporting_label") or ""),
                "page_url": str(payload.get("page_url") or ""),
            },
        )
    except Exception as exc:
        return jsonify({"error": f"Stripe intent creation failed: {exc}"}), 500

    return jsonify(
        {
            "clientSecret": intent.client_secret,
            "id": intent.id,
        }
    )


@bp.post("/paypal/order")
def paypal_order():
    return jsonify({"error": "PayPal is disabled for this local environment."}), 503


@bp.post("/paypal/capture")
def paypal_capture():
    return jsonify({"error": "PayPal is disabled for this local environment."}), 503


@bp.post("/stripe/webhook")
def stripe_webhook():
    secret = _cfg("STRIPE_WEBHOOK_SECRET")
    payload = request.get_data()
    sig_header = request.headers.get("Stripe-Signature", "")

    if secret:
        try:
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=sig_header,
                secret=secret,
            )
        except Exception as exc:
            current_app.logger.warning("Invalid Stripe webhook: %s", exc)
            return jsonify({"error": f"Invalid webhook: {exc}"}), 400
    else:
        event = request.get_json(silent=True) or {"type": "unknown"}

    try:
        event_type = str(event["type"])
    except Exception:
        event_type = str(getattr(event, "type", "unknown") or "unknown")
    current_app.logger.info("Stripe webhook received: %s", event_type)

    # Minimal local ack path.
    # Add fulfillment / receipts / donation state updates here later.
    return jsonify({"received": True, "type": event_type})
