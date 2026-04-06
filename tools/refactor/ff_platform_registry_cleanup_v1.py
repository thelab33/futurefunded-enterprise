from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
ROUTES = ROOT / "apps/web/app/routes/platform.py"


def backup(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = path.with_name(f"{path.name}.bak.{ts}")
    shutil.copy2(path, bak)
    return bak


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str, *, label: str) -> tuple[str, bool]:
    if old in text:
        return text.replace(old, new, 1), True
    if new in text:
        return text, False
    raise RuntimeError(f"could not find expected block for: {label}")


OLD_RENDER_BLOCK = """def _render_platform_page(
    *,
    template_name: str,
    page_key: str,
    default_title: str,
    fallback: dict | None = None,
    api_path: str | None = None,
):
    data = get_json(api_path, fallback or {}) if api_path else (fallback or {})
    return render_template(
        template_name,
        page_title=data.get("page_title", default_title),
        platform_page=page_key,
        data=data,
    )"""

NEW_RENDER_BLOCK = """PLATFORM_PAGE_CONFIG: dict[str, dict] = {
    "home": {
        "template_name": "platform/pages/home.html",
        "default_title": "FutureFunded Platform Home",
        "fallback": _fallback_home(),
        "api_path": "/platform/home",
    },
    "pricing": {
        "template_name": "platform/pages/pricing.html",
        "default_title": "FutureFunded Pricing",
        "fallback": _fallback_pricing(),
        "api_path": "/platform/pricing",
    },
    "demo": {
        "template_name": "platform/pages/demo.html",
        "default_title": "FutureFunded Demo",
        "fallback": _fallback_demo(),
        "api_path": "/platform/demo",
    },
    "onboarding": {
        "template_name": "platform/pages/onboarding.html",
        "default_title": "FutureFunded Onboarding",
        "fallback": _fallback_onboarding(),
        "api_path": "/platform/onboarding",
    },
    "dashboard": {
        "template_name": "platform/pages/dashboard.html",
        "default_title": "FutureFunded Dashboard",
        "fallback": _fallback_dashboard(),
        "api_path": "/platform/dashboard",
    },
}


def _page_config(page_key: str) -> dict:
    config = PLATFORM_PAGE_CONFIG.get(page_key)
    if not config:
        raise KeyError(f"Unknown platform page_key: {page_key}")
    return config


def _render_platform_page(
    *,
    page_key: str,
    template_name: str | None = None,
    default_title: str | None = None,
    fallback: dict | None = None,
    api_path: str | None = None,
):
    config = PLATFORM_PAGE_CONFIG.get(page_key, {})

    template_name = template_name or config.get("template_name")
    default_title = default_title or config.get("default_title", "FutureFunded Platform")
    if fallback is None:
        fallback = config.get("fallback")
    if api_path is None:
        api_path = config.get("api_path")

    if not template_name:
        raise KeyError(f"No platform template configured for page_key={page_key!r}")

    data = get_json(api_path, fallback or {}) if api_path else (fallback or {})
    return render_template(
        template_name,
        page_title=data.get("page_title", default_title),
        platform_page=page_key,
        data=data,
    )"""


def main() -> int:
    print("== FF PLATFORM REGISTRY CLEANUP V1 ==")

    if not ROUTES.exists():
        raise FileNotFoundError(ROUTES)

    bak = backup(ROUTES)
    text = ROUTES.read_text(encoding="utf-8")
    original = text

    text, changed = replace_once(
        text,
        OLD_RENDER_BLOCK,
        NEW_RENDER_BLOCK,
        label="_render_platform_page block",
    )

    if changed:
        write_text(ROUTES, text)

    print(f"patched: {ROUTES}")
    print(f"backup:  {bak}")
    print("result:  changed" if text != original else "result:  no-op (already aligned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
