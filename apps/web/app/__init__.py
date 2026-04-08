from .routes.payments import bp as payments_bp
from flask import Flask, redirect

from app.config import config_by_env
from app.extensions import compress
from app.routes.platform import bp as platform_bp
from app.routes.campaign import bp as campaign_bp
from packages.shared.settings import settings


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_by_env.get(settings.ENV, config_by_env["development"]))

    compress.init_app(app)
    app.register_blueprint(platform_bp, url_prefix="/platform")
    app.register_blueprint(campaign_bp)
    app.register_blueprint(payments_bp)

    @app.get("/")
    def root():
        return redirect("/platform/", code=302)

    @app.get("/healthz")
    def healthz():
        return {
            "ok": True,
            "service": "futurefunded-web",
            "env": settings.ENV,
        }

    return app
