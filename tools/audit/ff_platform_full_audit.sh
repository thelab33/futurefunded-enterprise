#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/futurefunded-enterprise}"
BASE_URL="${BASE_URL:-http://127.0.0.1:5000}"

cd "$ROOT"

STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="reports/platform-audit/${STAMP}"
RENDERED_DIR="${OUT}/rendered"

mkdir -p "$OUT" "$RENDERED_DIR"

echo "== FutureFunded platform full audit =="
echo "root: $ROOT"
echo "base_url: $BASE_URL"
echo "out: $OUT"

# -------------------------------------------------------------------
# 00) Platform file tree
# -------------------------------------------------------------------
find apps/web/app/templates/platform -maxdepth 3 -type f | sort > "$OUT/00_platform_tree.txt"

# -------------------------------------------------------------------
# 01) Route/render map
# -------------------------------------------------------------------
rg -n \
  '@bp\.get\(|def (home|onboarding|dashboard|pricing|demo)\(|template_name="platform/pages/|page_key=' \
  apps/web/app/routes/platform.py \
  > "$OUT/01_route_render_map.txt" || true

# -------------------------------------------------------------------
# 02) Template extends / includes / imports
# -------------------------------------------------------------------
rg -n \
  '{% extends |{% include |{% from |{% import ' \
  apps/web/app/templates/platform \
  > "$OUT/02_template_extends_includes.txt" || true

# -------------------------------------------------------------------
# 03) Platform <-> campaign links and route references
# -------------------------------------------------------------------
rg -n \
  'href="/platform/|href="/platform|href="/c/|href="/c|submit_href|primary_cta_href|secondary_cta_href|primary_action|secondary_action|campaign_url' \
  apps/web/app/routes/platform.py \
  apps/web/app/templates/platform \
  > "$OUT/03_platform_campaign_links.txt" || true

# -------------------------------------------------------------------
# 04) Forms / submit actions / buttons
# -------------------------------------------------------------------
rg -n \
  '<form|action=|type="submit"|submit_label|submit_href|primary_action|secondary_action|ff-btn|button' \
  apps/web/app/routes/platform.py \
  apps/web/app/templates/platform \
  > "$OUT/04_forms_and_actions.txt" || true

# -------------------------------------------------------------------
# 05) HTML hook inventory (ids, data attrs, ff classes)
# -------------------------------------------------------------------
rg -n \
  'id="|data-ff-|class="' \
  apps/web/app/templates/platform \
  > "$OUT/05_platform_html_hooks.txt" || true

# Extract ff-class usage in platform HTML
rg -o 'ff-[A-Za-z0-9_-]+' apps/web/app/templates/platform -g '*.html' \
  | sort -u > "$OUT/05a_platform_html_ff_classes.txt" || true

# -------------------------------------------------------------------
# 06) CSS ownership map
# -------------------------------------------------------------------
rg -n \
  '\.ff-|body\[data-ff-platform|html\.ff-root|data-ff-platform' \
  apps/web/app/static/css/platform-pages.css \
  apps/web/app/static/css/ff.css \
  > "$OUT/06_css_ownership_map.txt" || true

# Extract ff-class selectors from CSS
rg -o '\.ff-[A-Za-z0-9_-]+' \
  apps/web/app/static/css/platform-pages.css \
  apps/web/app/static/css/ff.css \
  | sed 's/^\.//' | sort -u > "$OUT/06a_css_ff_classes.txt" || true

# Platform HTML classes missing from CSS
comm -23 \
  "$OUT/05a_platform_html_ff_classes.txt" \
  "$OUT/06a_css_ff_classes.txt" \
  > "$OUT/06b_platform_classes_missing_in_css.txt" || true

# -------------------------------------------------------------------
# 07) JS/platform touchpoints
# -------------------------------------------------------------------
if [ -d apps/web/app/static/js ]; then
  rg -n \
    'platform|/platform/|/c/|data-ff-|ff[A-Z]|ff-' \
    apps/web/app/static/js \
    apps/web/app/routes/platform.py \
    apps/web/app/templates/platform \
    > "$OUT/07_js_platform_touchpoints.txt" || true
else
  : > "$OUT/07_js_platform_touchpoints.txt"
fi

# -------------------------------------------------------------------
# 08) Campaign surface touchpoints from platform side
# -------------------------------------------------------------------
rg -n \
  '/c/spring-fundraiser|campaign_url|Open live fundraiser|View live fundraiser|View live example|Launch your program|Start guided launch' \
  apps/web/app/routes/platform.py \
  apps/web/app/templates/platform \
  > "$OUT/08_campaign_touchpoints.txt" || true

# -------------------------------------------------------------------
# 09) Render smoke for key routes
# -------------------------------------------------------------------
: > "$OUT/09_render_smoke.txt"

render_route() {
  local route="$1"
  local safe_name
  safe_name="$(echo "$route" | sed 's#^/##; s#[^a-zA-Z0-9._-]#_#g; s#/$##')"
  if [ -z "$safe_name" ]; then
    safe_name="root"
  fi

  local html_file="${RENDERED_DIR}/${safe_name}.html"
  local head_file="${RENDERED_DIR}/${safe_name}.headers.txt"

  local status
  status="$(curl -sS -L -D "$head_file" -o "$html_file" -w '%{http_code}' "${BASE_URL}${route}" || echo "000")"

  printf '%s %s\n' "$status" "$route" >> "$OUT/09_render_smoke.txt"
}

render_route "/platform/"
render_route "/platform/onboarding"
render_route "/platform/dashboard"
render_route "/platform/pricing"
render_route "/platform/demo"
render_route "/c/spring-fundraiser"

# -------------------------------------------------------------------
# 10) Rendered title / headings / key links summary
# -------------------------------------------------------------------
export FF_AUDIT_OUT="$OUT"
export FF_AUDIT_BASE_URL="$BASE_URL"

python3 - <<'PY'
from __future__ import annotations
from pathlib import Path
import os
import re
from html import unescape

OUT = Path(os.environ["FF_AUDIT_OUT"])
RENDERED = OUT / "rendered"

title_re = re.compile(r"<title>(.*?)</title>", re.I | re.S)
h1_re = re.compile(r"<h1[^>]*>(.*?)</h1>", re.I | re.S)
h2_re = re.compile(r"<h2[^>]*>(.*?)</h2>", re.I | re.S)
href_re = re.compile(r'href="([^"]+)"', re.I)
tag_re = re.compile(r"<[^>]+>")

def clean(s: str) -> str:
    s = tag_re.sub("", s)
    s = unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

rows = []
link_lines = []

for html_path in sorted(RENDERED.glob("*.html")):
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    title = clean(title_re.search(html).group(1)) if title_re.search(html) else ""
    h1 = clean(h1_re.search(html).group(1)) if h1_re.search(html) else ""
    h2s = [clean(m.group(1)) for m in h2_re.finditer(html)]
    filtered_h2s = [x for x in h2s if x][:5]
    hrefs = []
    for href in href_re.findall(html):
        if href.startswith("/platform") or href.startswith("/c/"):
            hrefs.append(href)
    hrefs = list(dict.fromkeys(hrefs))
    rows.append((html_path.name, title, h1, filtered_h2s, hrefs))
    link_lines.append(f"## {html_path.name}")
    link_lines.append(f"- title: {title or '(missing)'}")
    link_lines.append(f"- h1: {h1 or '(missing)'}")
    if filtered_h2s:
        link_lines.append("- h2 sample:")
        for item in filtered_h2s:
            link_lines.append(f"  - {item}")
    else:
        link_lines.append("- h2 sample: (none found)")
    if hrefs:
        link_lines.append("- platform/campaign links:")
        for href in hrefs:
            link_lines.append(f"  - {href}")
    else:
        link_lines.append("- platform/campaign links: (none found)")
    link_lines.append("")

(OUT / "10_rendered_titles_and_links.md").write_text("\n".join(link_lines) + "\n", encoding="utf-8")
PY

# -------------------------------------------------------------------
# 11) High-level summary
# -------------------------------------------------------------------
python3 - <<'PY'
from __future__ import annotations
from pathlib import Path
import os

OUT = Path(os.environ["FF_AUDIT_OUT"])

def read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.rstrip("\n") for line in path.read_text(encoding="utf-8", errors="ignore").splitlines()]

tree = read_lines(OUT / "00_platform_tree.txt")
routes = read_lines(OUT / "01_route_render_map.txt")
links = read_lines(OUT / "03_platform_campaign_links.txt")
forms = read_lines(OUT / "04_forms_and_actions.txt")
missing_css = read_lines(OUT / "06b_platform_classes_missing_in_css.txt")
smoke = read_lines(OUT / "09_render_smoke.txt")

status_lines = []
bad_routes = []
for line in smoke:
    parts = line.split(" ", 1)
    if len(parts) == 2:
        status, route = parts
        status_lines.append(f"- {route}: {status}")
        if status != "200":
            bad_routes.append((route, status))

summary = []
summary.append("# FutureFunded platform audit summary")
summary.append("")
summary.append("## Snapshot")
summary.append(f"- platform template files: {len(tree)}")
summary.append(f"- route/render map hits: {len(routes)}")
summary.append(f"- platform/campaign link refs: {len(links)}")
summary.append(f"- form/action refs: {len(forms)}")
summary.append(f"- platform ff-classes missing in CSS: {len(missing_css)}")
summary.append("")
summary.append("## Render smoke")
summary.extend(status_lines or ["- no render smoke output"])
summary.append("")
if bad_routes:
    summary.append("## Render issues")
    for route, status in bad_routes:
        summary.append(f"- {route} returned {status}")
    summary.append("")
summary.append("## Files to inspect next")
summary.append(f"- {OUT / '01_route_render_map.txt'}")
summary.append(f"- {OUT / '02_template_extends_includes.txt'}")
summary.append(f"- {OUT / '03_platform_campaign_links.txt'}")
summary.append(f"- {OUT / '06b_platform_classes_missing_in_css.txt'}")
summary.append(f"- {OUT / '10_rendered_titles_and_links.md'}")
summary.append("")
summary.append("## Founder next use")
summary.append("- Use this summary to confirm the actual page graph before wiring Playwright demo-flow coverage.")
summary.append("- If render smoke is all 200 and link flow looks coherent, move into the scripted founder demo flow next.")
summary.append("")

(OUT / "11_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
PY

echo
echo "Audit complete:"
echo "  $OUT"
echo
echo "Key files:"
echo "  $OUT/11_summary.md"
echo "  $OUT/09_render_smoke.txt"
echo "  $OUT/10_rendered_titles_and_links.md"
echo "  $OUT/06b_platform_classes_missing_in_css.txt"
