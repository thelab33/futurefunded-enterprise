from pathlib import Path
import json

DATA_PATH = Path(__file__).parent / "campaigns.json"


def _load():
    if not DATA_PATH.exists():
        return {}

    raw = DATA_PATH.read_text(encoding="utf-8").strip()
    if not raw:
        return {}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}

    return data if isinstance(data, dict) else {}


def _save(data):
    DATA_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def create_campaign(slug, payload):
    data = _load()
    data[str(slug)] = payload
    _save(data)


def get_campaign(slug):
    return _load().get(str(slug))


def list_campaigns():
    data = _load()
    rows = []
    for slug, payload in data.items():
        payload = payload or {}
        rows.append(
            {
                "slug": str(slug),
                "org_name": payload.get("org_name", "Untitled Organization"),
                "campaign_name": payload.get("campaign_name", "Untitled Campaign"),
                "headline": payload.get("campaign_headline", ""),
                "goal": payload.get("goal", 0),
                "raised": payload.get("raised", 0),
                "campaign_url": payload.get("campaign_url", f"/c/{slug}"),
                "share_url": payload.get("share_url", f"/c/{slug}"),
                "status": "Live",
            }
        )

    rows.sort(key=lambda x: x["slug"], reverse=True)
    return rows
