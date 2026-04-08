from __future__ import annotations

import os

from flask import jsonify
from app import create_app


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
    return jsonify(
        {
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
        }
    )
