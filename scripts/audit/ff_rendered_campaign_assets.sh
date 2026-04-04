#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://127.0.0.1:5000/c/spring-fundraiser}"
OUT_DIR="scripts/audit/_out/rendered_campaign"
mkdir -p "$OUT_DIR"

HTML_FILE="$OUT_DIR/page.html"
CSS_URLS="$OUT_DIR/css_urls.txt"
JS_URLS="$OUT_DIR/js_urls.txt"
SUMMARY="$OUT_DIR/summary.txt"

echo "== FETCH PAGE =="
echo "URL: $URL"

curl -fsSL "$URL" -o "$HTML_FILE"

python3 - "$HTML_FILE" "$URL" "$CSS_URLS" "$JS_URLS" <<'PY'
from pathlib import Path
from urllib.parse import urljoin
import re
import sys

html_path = Path(sys.argv[1])
base_url = sys.argv[2]
css_out = Path(sys.argv[3])
js_out = Path(sys.argv[4])

html = html_path.read_text(encoding="utf-8", errors="ignore")

body_tag = re.search(r'<body\b([^>]*)>', html, flags=re.I | re.S)
print("\n== BODY TAG ==")
if body_tag:
    print(body_tag.group(0))
else:
    print("No body tag found")

styles = re.findall(r'<link[^>]+rel=["\'][^"\']*stylesheet[^"\']*["\'][^>]+href=["\']([^"\']+)["\']', html, flags=re.I)
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html, flags=re.I)
inline_styles = len(re.findall(r'<style\b', html, flags=re.I))

css_urls = [urljoin(base_url, s) for s in styles]
js_urls = [urljoin(base_url, s) for s in scripts]

css_out.write_text("\n".join(css_urls) + ("\n" if css_urls else ""), encoding="utf-8")
js_out.write_text("\n".join(js_urls) + ("\n" if js_urls else ""), encoding="utf-8")

print("\n== CSS URLS ==")
for u in css_urls:
    print(u)

print("\n== JS URLS ==")
for u in js_urls:
    print(u)

print(f"\n== INLINE STYLE TAG COUNT ==\n{inline_styles}")
PY

echo
echo "== DOWNLOAD CSS ASSETS =="
: > "$SUMMARY"

i=0
while IFS= read -r css; do
  [ -n "$css" ] || continue
  i=$((i+1))
  out="$OUT_DIR/css_$i.css"
  echo "[$i] $css"
  curl -fsSL "$css" -o "$out"
  size="$(wc -c < "$out" | tr -d ' ')"
  {
    echo "[$i] $css"
    echo "file: $out"
    echo "bytes: $size"
    echo "markers:"
    rg -n 'FF_[A-Z0-9_]+' "$out" || true
    echo
  } >> "$SUMMARY"
done < "$CSS_URLS"

echo
echo "== DOWNLOAD JS ASSETS =="
j=0
while IFS= read -r js; do
  [ -n "$js" ] || continue
  j=$((j+1))
  out="$OUT_DIR/js_$j.js"
  echo "[$j] $js"
  curl -fsSL "$js" -o "$out"
done < "$JS_URLS"

echo
echo "== SUMMARY FILE =="
echo "$SUMMARY"
sed -n '1,220p' "$SUMMARY"
