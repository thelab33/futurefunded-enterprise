from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
TARGET = ROOT / "apps/web/app/routes/campaign.py"

text = TARGET.read_text(encoding="utf-8")

pattern = re.compile(
    r'(?P<indent>\s*)return render_template\("campaign/index\.html", \*\*data\)',
    re.M,
)

replacement = r'''
\g<indent>data = dict(data or {})
\g<indent>for key in ("asset_v", "FF_ASSET_V", "FF_BUILD_ID", "FF_VERSION"):
\g<indent>    value = str(data.get(key, "") or "").strip().lower()
\g<indent>    if value == "dev":
\g<indent>        data.pop(key, None)
\g<indent>
\g<indent>cfg = data.get("_cfg")
\g<indent>if isinstance(cfg, dict):
\g<indent>    cfg = dict(cfg)
\g<indent>    for key in ("asset_v", "FF_ASSET_V", "FF_BUILD_ID", "FF_VERSION"):
\g<indent>        value = str(cfg.get(key, "") or "").strip().lower()
\g<indent>        if value == "dev":
\g<indent>            cfg.pop(key, None)
\g<indent>    data["_cfg"] = cfg
\g<indent>
\g<indent>return render_template("campaign/index.html", **data)
'''.lstrip("\n")

new_text, n = pattern.subn(replacement, text, count=1)
if n != 1:
    raise SystemExit("Could not find campaign render_template(...) line to patch")

ts = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_path = TARGET.with_name(f"{TARGET.name}.{ts}.bak")
shutil.copy2(TARGET, backup_path)
TARGET.write_text(new_text, encoding="utf-8")

print(f"changed: {TARGET}")
print(f"backup:  {backup_path}")
