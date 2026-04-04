from __future__ import annotations

import httpx

from packages.shared.settings import settings


def get_json(path: str, fallback: dict) -> dict:
    url = f"{settings.API_BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, dict) else fallback
    except Exception:
        return fallback
