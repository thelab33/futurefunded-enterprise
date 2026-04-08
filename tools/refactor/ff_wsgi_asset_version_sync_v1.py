from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

TARGET = Path("apps/web/wsgi.py")
text = TARGET.read_text(encoding="utf-8")
original = text

if "import os" not in text:
    if text.startswith("#!"):
        lines = text.splitlines(True)
        insert_at = 1
        if len(lines) > 1 and "coding" in lines[1]:
            insert_at = 2
        lines.insert(insert_at, "import os\n")
        text = "".join(lines)
    else:
        text = "import os\n" + text

HELPER = r'''
def _ff_sync_asset_version(app):
    """
    Mirror shell/exported build vars into Flask config for template asset versioning.
    This is needed because templates read config-backed values and otherwise fall back to v=1.
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
        app.config["FF_ASSET_V"] = app.config.get("FF_VERSION", app.config.get("FF_BUILD_ID", "1"))

    return app
'''.strip()

if "def _ff_sync_asset_version(app):" not in text:
    marker = "\napp = "
    idx = text.find(marker)
    if idx == -1:
        raise SystemExit("could not find app assignment in apps/web/wsgi.py")
    text = text[:idx] + "\n\n" + HELPER + "\n\n" + text[idx:]

if "app = _ff_sync_asset_version(app)" not in text:
    if "\napp = create_app(" in text:
        text = text.replace("\napp = create_app(", "\napp = _ff_sync_asset_version(create_app(", 1)
    elif "\napp=create_app(" in text:
        text = text.replace("\napp=create_app(", "\napp=_ff_sync_asset_version(create_app(", 1)
    else:
        raise SystemExit("could not find create_app assignment in apps/web/wsgi.py")

if text == original:
    print("skip: no changes needed")
else:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = TARGET.with_name(f"{TARGET.name}.{ts}.bak")
    shutil.copy2(TARGET, backup)
    TARGET.write_text(text, encoding="utf-8")
    print(f"changed: {TARGET}")
    print(f"backup:  {backup}")
