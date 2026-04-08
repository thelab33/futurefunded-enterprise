from __future__ import annotations

import os
from datetime import datetime, timezone

from flask import jsonify
from app import create_app


_BOOTED_AT_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")


def _ff_sync_asset_version(app):
    """
    Mirror shell/exported build vars into Flask config for template asset versioning.
    Templates read config-backed values and otherwise fall back to v=1.
    """
    build_id = (os.getenv("FF_BUILD_ID") or os.getenv("BUILD_ID") or "").strip()
    version = (os.getenv("FF_VERSION") or build_id or "").strip()
    asset_v = (os.getenv("FF_ASSET_V") or version or build_id or "").strip()

    if build_id:
        app.config["FF_BUILD_ID"] = build_id
    elif not str(app.config.get("FF_BUILD_ID", "")).strip():
        app.config["FF_BUILD_ID"] = "1"

    if version:
        app.config["FF_VERSION"] = version
    elif not str(app.config.get("FF_VERSION", "")).strip():
        app.config["FF_VERSION"] = app.config.get("FF_BUILD_ID", "1")

    if asset_v:
        app.config["FF_ASSET_V"] = asset_v
    elif not str(app.config.get("FF_ASSET_V", "")).strip():
        app.config["FF_ASSET_V"] = app.config.get(
            "FF_VERSION",
            app.config.get("FF_BUILD_ID", "1"),
        )

    app.config["FF_BOOTED_AT_UTC"] = _BOOTED_AT_UTC
    return app


app = _ff_sync_asset_version(create_app())


@app.after_request
def _ff_add_build_header(resp):
    try:
        build_id = str(app.config.get("FF_BUILD_ID", "")).strip()
        if build_id:
            resp.headers["X-FutureFunded-Build"] = build_id
    except Exception:
        pass
    return resp


@app.get("/__version")
def _ff_version():
    stripe_pk = (
        os.getenv("STRIPE_PUBLISHABLE_KEY")
        or os.getenv("STRIPE_PUBLIC_KEY")
        or ""
    ).strip()
    paypal_client_id = (os.getenv("PAYPAL_CLIENT_ID") or "").strip()

    stripe_mode = (
        "test" if stripe_pk.startswith("pk_test_")
        else "live" if stripe_pk.startswith("pk_live_")
        else "missing"
    )
    paypal_mode = (
        (os.getenv("PAYPAL_MODE") or "").strip().lower()
        or ("live" if paypal_client_id else "disabled")
    )

    payload = {
        "build_id": str(app.config.get("FF_BUILD_ID", "")).strip(),
        "version": str(app.config.get("FF_VERSION", "")).strip(),
        "asset_version": str(app.config.get("FF_ASSET_V", "")).strip(),
        "env": (
            os.getenv("APP_ENV")
            or os.getenv("ENV")
            or os.getenv("FLASK_ENV")
            or ""
        ).strip(),
        "public_base_url": (
            os.getenv("FF_PUBLIC_BASE_URL")
            or os.getenv("PUBLIC_BASE_URL")
            or ""
        ).strip(),
        "stripe_mode": stripe_mode,
        "paypal_mode": paypal_mode,
        "data_mode": (
            os.getenv("FF_DATA_MODE")
            or os.getenv("DATA_MODE")
            or "runtime"
        ).strip(),
        "booted_at_utc": str(app.config.get("FF_BOOTED_AT_UTC", "")).strip(),
    }
    return jsonify(payload)
