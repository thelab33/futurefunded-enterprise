#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/futurefunded-enterprise}"
BASE_URL="${BASE_URL:-http://127.0.0.1:5000}"

cd "$ROOT"

STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="reports/platform-audit/${STAMP}"
RENDERED_DIR="${OUT}/rendered"
LATEST_PTR="reports/platform-audit/LATEST.txt"

mkdir -p "$OUT" "$RENDERED_DIR"

printf '%s\n' "$OUT" > "$LATEST_PTR"

echo "== FutureFunded platform full audit v2 =="
echo "root: $ROOT"
echo "base_url: $BASE_URL"
echo "out: $OUT"

# -------------------------------------------------------------------
# 00) Repo shape / platform + testing footprint
# -------------------------------------------------------------------
{
  echo "# repo shape"
  echo
  find . -maxdepth 2 \
    \( -path './apps' -o -path './apps/*' -o -path './tests' -o -path './tests/*' -o -path './e2e' -o -path './e2e/*' -o -path './tools' -o -path './tools/*' -o -name 'playwright.config.js' -o -name 'playwright.config.ts' -o -name 'package.json' \) \
    | sort
} > "$OUT/00_repo_shape.txt"

# -------------------------------------------------------------------
# 01) Platform file tree
# -------------------------------------------------------------------
find apps/web/app/templates/platform -maxdepth 3 -type f | sort > "$OUT/01_platform_tree.txt"

# -------------------------------------------------------------------
# 02) Route/render map
# -------------------------------------------------------------------
rg -n \
  -e '@bp\.get\(' \
  -e 'def home\(' \
  -e 'def onboarding\(' \
  -e 'def dashboard\(' \
  -e 'def pricing\(' \
  -e 'def demo\(' \
  -e 'template_name="platform/pages/' \
  -e 'page_key=' \
  apps/web/app/routes/platform.py \
  > "$OUT/02_route_render_map.txt" || true

# -------------------------------------------------------------------
# 03) Template extends / includes / imports (literal mode)
# -------------------------------------------------------------------
rg -F -n \
  -e '{% extends ' \
  -e '{% include ' \
  -e '{% from ' \
  -e '{% import ' \
  apps/web/app/templates/platform \
  > "$OUT/03_template_extends_includes.txt" || true

# -------------------------------------------------------------------
# 04) Platform <-> campaign links and route refs
# -------------------------------------------------------------------
rg -n \
  -e 'href="/platform/' \
  -e 'href="/c/' \
  -e 'submit_href' \
  -e 'primary_cta_href' \
  -e 'secondary_cta_href' \
  -e 'primary_action' \
  -e 'secondary_action' \
  -e 'campaign_url' \
  apps/web/app/routes/platform.py \
  apps/web/app/templates/platform \
  > "$OUT/04_platform_campaign_links.txt" || true

# -------------------------------------------------------------------
# 05) Forms / actions / buttons
# -------------------------------------------------------------------
rg -n \
  -e '<form' \
  -e 'action=' \
  -e 'type="submit"' \
  -e 'submit_label' \
  -e 'submit_href' \
  -e 'primary_action' \
  -e 'secondary_action' \
  -e 'ff-btn' \
  -e '<button' \
  apps/web/app/routes/platform.py \
  apps/web/app/templates/platform \
  > "$OUT/05_forms_and_actions.txt" || true

# -------------------------------------------------------------------
# 06) HTML hooks inventory
# -------------------------------------------------------------------
rg -n \
  -e 'id="' \
  -e 'data-ff-' \
  -e 'class="' \
  apps/web/app/templates/platform \
  > "$OUT/06_platform_html_hooks.txt" || true

rg -o 'ff-[A-Za-z0-9_-]+' apps/web/app/templates/platform -g '*.html' \
  | sort -u > "$OUT/06a_platform_html_ff_classes.txt" || true

# -------------------------------------------------------------------
# 07) CSS ownership
# -------------------------------------------------------------------
rg -n \
  -e '\.ff-' \
  -e 'data-ff-platform' \
  -e 'body\[data-ff-platform' \
  -e 'html\.ff-root' \
  apps/web/app/static/css/platform-pages.css \
  apps/web/app/static/css/ff.css \
  > "$OUT/07_css_ownership_map.txt" || true

rg -o '\.ff-[A-Za-z0-9_-]+' \
  apps/web/app/static/css/platform-pages.css \
  apps/web/app/static/css/ff.css \
  | sed 's/^\.//' | sort -u > "$OUT/07a_css_ff_classes.txt" || true

comm -23 \
  "$OUT/06a_platform_html_ff_classes.txt" \
  "$OUT/07a_css_ff_classes.txt" \
  > "$OUT/07b_platform_classes_missing_in_css.txt" || true

# -------------------------------------------------------------------
# 08) JS / runtime touchpoints
# -------------------------------------------------------------------
if [ -d apps/web/app/static/js ]; then
  rg -n \
    -e 'platform' \
    -e '/platform/' \
    -e '/c/' \
    -e 'data-ff-' \
    -e 'ff-' \
    apps/web/app/static/js \
    apps/web/app/routes/platform.py \
    apps/web/app/templates/platform \
    > "$OUT/08_js_platform_touchpoints.txt" || true
else
  : > "$OUT/08_js_platform_touchpoints.txt"
fi

# -------------------------------------------------------------------
# 09) Playwright footprint
# -------------------------------------------------------------------
{
  echo "# playwright configs"
  find . -maxdepth 1 \( -name 'playwright.config.js' -o -name 'playwright.config.ts' \) | sort
  echo
  echo "# e2e dirs"
  find . -maxdepth 2 \( -path './e2e' -o -path './e2e/*' -o -path './tests/e2e' -o -path './tests/e2e/*' -o -path './tests/prod' -o -path './tests/prod/*' \) | sort
} > "$OUT/09_playwright_footprint.txt"

# -------------------------------------------------------------------
# 10) Render smoke
# -------------------------------------------------------------------
: > "$OUT/10_render_smoke.txt"

render_route() {
  local route="$1"
  local safe_name
  safe_name="$(echo "$route" | sed 's#^/##; s#/$##; s#[^a-zA-Z0-9._-]#_#g')"
  if [ -z "$safe_name" ]; then
    safe_name="root"
  fi

  local html_file="${RENDERED_DIR}/${safe_name}.html"
  local head_file="${RENDERED_DIR}/${safe_name}.headers.txt"

  local status
  status="$(curl -sS -L -D "$head_file" -o "$html_file" -w '%{http_code}' "${BASE_URL}${route}" || echo "000")"

  printf '%s %s\n' "$status" "$route" >> "$OUT/10_render_smoke.txt"
}

render_route "/platform/"
render_route "/platform/onboarding"
render_route "/platform/dashboard"
render_route "/platform/pricing"
render_route "/platform/demo"
render_route "/c/spring-fundraiser"

# -------------------------------------------------------------------
# 11) Rendered titles / headings / route links
# -------------------------------------------------------------------
export FF_AUDIT_OUT="$OUT"

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

out_lines: list[str] = []

for html_path in sorted(RENDERED.glob("*.html")):
    html = html_path.read_text(encoding="utf-8", errors="ignore")

    m_title = title_re.search(html)
    m_h1 = h1_re.search(html)
    h2s = [clean(m.group(1)) for m in h2_re.finditer(html)]

    title = clean(m_title.group(1)) if m_title else ""
    h1 = clean(m_h1.group(1)) if m_h1 else ""
    h2s = [x for x in h2s if x][:6]

    hrefs = []
    for href in href_re.findall(html):
        if href.startswith("/platform") or href.startswith("/c/"):
            hrefs.append(href)
    hrefs = list(dict.fromkeys(hrefs))

    out_lines.append(f"## {html_path.name}")
    out_lines.append(f"- title: {title or '(missing)'}")
    out_lines.append(f"- h1: {h1 or '(missing)'}")
    if h2s:
        out_lines.append("- h2 sample:")
        for item in h2s:
            out_lines.append(f"  - {item}")
    else:
        out_lines.append("- h2 sample: (none found)")
    if hrefs:
        out_lines.append("- platform/campaign links:")
        for href in hrefs:
            out_lines.append(f"  - {href}")
    else:
        out_lines.append("- platform/campaign links: (none found)")
    out_lines.append("")

(OUT / "11_rendered_titles_and_links.md").write_text("\n".join(out_lines) + "\n", encoding="utf-8")
PY

# -------------------------------------------------------------------
# 12) High-level summary
# -------------------------------------------------------------------
python3 - <<'PY'
from __future__ import annotations
from pathlib import Path
import os

OUT = Path(os.environ["FF_AUDIT_OUT"])

def lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8", errors="ignore").splitlines()

repo_shape = lines(OUT / "00_repo_shape.txt")
platform_tree = lines(OUT / "01_platform_tree.txt")
route_map = lines(OUT / "02_route_render_map.txt")
template_graph = lines(OUT / "03_template_extends_includes.txt")
link_refs = lines(OUT / "04_platform_campaign_links.txt")
forms = lines(OUT / "05_forms_and_actions.txt")
missing_css = lines(OUT / "07b_platform_classes_missing_in_css.txt")
render_smoke = lines(OUT / "10_render_smoke.txt")
playwright = lines(OUT / "09_playwright_footprint.txt")

bad_routes: list[str] = []
status_lines: list[str] = []

for line in render_smoke:
    parts = line.split(" ", 1)
    if len(parts) != 2:
        continue
    status, route = parts
    status_lines.append(f"- {route}: {status}")
    if status != "200":
        bad_routes.append(f"- {route}: {status}")

summary: list[str] = []
summary.append("# FutureFunded platform audit summary")
summary.append("")
summary.append("## Snapshot")
summary.append(f"- repo shape lines: {len(repo_shape)}")
summary.append(f"- platform template files: {len(platform_tree)}")
summary.append(f"- route/render hits: {len(route_map)}")
summary.append(f"- template graph hits: {len(template_graph)}")
summary.append(f"- platform/campaign link refs: {len(link_refs)}")
summary.append(f"- form/action refs: {len(forms)}")
summary.append(f"- platform ff-classes missing in CSS: {len(missing_css)}")
summary.append(f"- playwright footprint lines: {len(playwright)}")
summary.append("")
summary.append("## Render smoke")
summary.extend(status_lines or ["- no render smoke output"])
summary.append("")
if bad_routes:
    summary.append("## Render issues")
    summary.extend(bad_routes)
    summary.append("")
summary.append("## Files to inspect next")
summary.append(f"- {OUT / '02_route_render_map.txt'}")
summary.append(f"- {OUT / '03_template_extends_includes.txt'}")
summary.append(f"- {OUT / '04_platform_campaign_links.txt'}")
summary.append(f"- {OUT / '09_playwright_footprint.txt'}")
summary.append(f"- {OUT / '11_rendered_titles_and_links.md'}")
summary.append("")
summary.append("## Founder next use")
summary.append("- Confirm the real page graph and handoff points before wiring founder-demo Playwright coverage.")
summary.append("- Decide which Playwright config and test lane is canonical before adding more demo-flow tests.")
summary.append("")

(OUT / "12_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
PY

echo
echo "Audit complete:"
echo "  $OUT"
echo
echo "Key files:"
echo "  $OUT/12_summary.md"
echo "  $OUT/10_render_smoke.txt"
echo "  $OUT/11_rendered_titles_and_links.md"
echo "  $OUT/09_playwright_footprint.txt"
echo "  $OUT/07b_platform_classes_missing_in_css.txt"
echo
echo "LATEST pointer:"
echo "  $LATEST_PTR"
