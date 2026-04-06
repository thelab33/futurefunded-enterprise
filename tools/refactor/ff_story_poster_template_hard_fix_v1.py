from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"

text = TEMPLATE.read_text(encoding="utf-8")

old = (
    '<a class="ff-storyPoster" href="{{ _press_watch_url|e }}" target="_blank" rel="noopener noreferrer" '
    'aria-label="Watch program video" data-ff-open-video="" data-ff-story-poster="" '
    'data-ff-video-src="{{ _press_embed_url|e }}" data-ff-video-title="{{ _press_video_title|e }}">'
    '<picture class="ff-storyPoster__picture"><source srcset="{{ _press_poster_webp|e }}" type="image/webp" />'
    '<img class="ff-storyPoster__img" src="{{ _press_poster_fallback|e }}" width="1200" height="675" '
    'loading="lazy" decoding="async" alt="{{ _safe_org_name|e }} program photo" /></picture>'
    '<span class="ff-storyPoster__overlay" aria-hidden="true"><span class="ff-storyPoster__play">▶</span>'
    '<span class="ff-storyPoster__label">Watch</span></span>'
    '</a>'
)

new = (
    '<a class="ff-storyPoster" href="{{ _press_watch_url|e }}" target="_blank" rel="noopener noreferrer" '
    'aria-label="Watch program video" data-ff-open-video="" data-ff-story-poster="" '
    'data-ff-video-src="{{ _press_embed_url|e }}" data-ff-video-title="{{ _press_video_title|e }}">'
    '<img class="ff-storyPoster__img" src="{{ _press_poster_fallback|e }}" width="1200" height="675" '
    'loading="eager" fetchpriority="high" decoding="sync" alt="{{ _safe_org_name|e }} program photo" />'
    '<span class="ff-storyPoster__overlay" aria-hidden="true"><span class="ff-storyPoster__play">▶</span>'
    '<span class="ff-storyPoster__label">Watch</span></span>'
    '</a>'
)

if old not in text:
    pattern = re.compile(
        r'<a class="ff-storyPoster".*?</a>',
        re.S
    )
    match = pattern.search(text)
    if not match:
        raise SystemExit("❌ Could not find ff-storyPoster block in template.")
    text = text[:match.start()] + new + text[match.end():]
else:
    text = text.replace(old, new, 1)

backup = TEMPLATE.with_suffix(TEMPLATE.suffix + f".bak.{datetime.now().strftime('%Y%m%d-%H%M%S')}")
backup.write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")
TEMPLATE.write_text(text, encoding="utf-8")

print("✅ patched", TEMPLATE)
print("🗂 backup ", backup)
print("✅ applied FF_STORY_POSTER_TEMPLATE_HARD_FIX_V1")
