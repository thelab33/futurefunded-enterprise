from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

TARGET = Path("apps/web/app/__init__.py")
text = TARGET.read_text(encoding="utf-8")

original = text

# 1) ensure os import exists
if "import os" not in text:
    if re.search(r"^from __future__ import annotations\n", text, flags=re.M):
        text = re.sub(
            r"^(from __future__ import annotations\n)",
            r"\1import os\n",
            text,
            count=1,
            flags=re.M,
        )
    else:
        text = "import os\n" + text

helper = '''
def _sync_build_env_into_config(app) -> None:
    """
    Mirror build/version env vars into Flask config so Jinja templates can
    resolve stable asset cache-busting values in production-like runs.
    """
    env_build = (os.getenv("FF_BUILD_ID") or os.getenv("BUILD_ID") or "").strip()
    env_version = (os.getenv("FF_VERSION") or env_build or "").strip()
    env_asset_v = (os.getenv("FF_ASSET_V") or env_version or env_build or "").strip()

    if env_build:
        app.config["FF_BUILD_ID"] = env_build
    elif not str(app.config.get("FF_BUILD_ID", "")).strip():
        app.config["FF_BUILD_ID"] = "dev"

    if env_version:
        app.config["FF_VERSION"] = env_version
    elif not str(app.config.get("FF_VERSION", "")).strip():
        app.config["FF_VERSION"] = app.config.get("FF_BUILD_ID", "dev")

    if env_asset_v:
        app.config["FF_ASSET_V"] = env_asset_v
    elif not str(app.config.get("FF_ASSET_V", "")).strip():
        app.config["FF_ASSET_V"] = app.config.get("FF_VERSION", app.config.get("FF_BUILD_ID", "1"))
'''.strip()

if "_sync_build_env_into_config(app)" not in text and "def _sync_build_env_into_config(app) -> None:" not in text:
    # insert helper before create_app if possible
    m = re.search(r"\ndef create_app\(", text)
    if not m:
        raise SystemExit("could not find create_app() in apps/web/app/__init__.py")
    text = text[:m.start()] + "\n\n" + helper + "\n\n" + text[m.start():]

# 2) call helper inside create_app, after app is created
create_app_match = re.search(
    r"(def create_app\([^)]*\):\n(?:    .*\n)+?)",
    text
)
if not create_app_match:
    raise SystemExit("could not safely parse create_app() body")

block = create_app_match.group(1)

if "_sync_build_env_into_config(app)" not in block:
    # best target: immediately after first app = Flask(...)
    new_block, n = re.subn(
        r"(\n\s*app\s*=\s*Flask\([^\n]*\)\n)",
        r"\1    _sync_build_env_into_config(app)\n",
        block,
        count=1,
    )
    if n == 0:
        # fallback: insert near start of function after first indented line
        new_block, n = re.subn(
            r"(def create_app\([^)]*\):\n\s*[^\n]*\n)",
            r"\1    _sync_build_env_into_config(app)\n",
            block,
            count=1,
        )
    if n == 0:
        raise SystemExit("could not insert _sync_build_env_into_config(app) into create_app()")
    text = text.replace(block, new_block, 1)

if text == original:
    print("skip: no changes needed")
else:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = TARGET.with_name(f"{TARGET.name}.{ts}.bak")
    shutil.copy2(TARGET, backup)
    TARGET.write_text(text, encoding="utf-8")
    print(f"changed: {TARGET}")
    print(f"backup:  {backup}")
