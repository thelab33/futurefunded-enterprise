from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path(".").resolve()
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")

TARGETS = {
    "campaign_html": ROOT / "apps/web/app/templates/campaign/index.html",
    "css": ROOT / "apps/web/app/static/css/ff.css",
    "js": ROOT / "apps/web/app/static/js/ff-app.js",
}

for key, path in TARGETS.items():
    if not path.exists():
        raise SystemExit(f"❌ missing required file: {path}")

def backup(path: Path) -> Path:
    bak = path.with_name(path.name + f".bak-campaign-system-polish-{STAMP}")
    shutil.copy2(path, bak)
    return bak

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")

def upsert_marker_block(text: str, start: str, end: str, block: str) -> str:
    pattern = re.escape(start) + r".*?" + re.escape(end)
    wrapped = block.strip() + "\n"
    if start in text and end in text:
        return re.sub(pattern, wrapped, text, flags=re.S)
    return text.rstrip() + "\n\n" + wrapped

def patch_campaign_html(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    # Ensure body has fundraiser page contract
    def repl_body(m):
        attrs = m.group(1)
        original = attrs
        if 'data-ff-page=' not in attrs:
            attrs += ' data-ff-page="fundraiser"'
        if 'data-ff-template=' not in attrs:
            attrs += ' data-ff-template="index"'
        if attrs != original:
            changes.append("campaign body contract normalized")
        return f"<body{attrs}>"

    text = re.sub(r"<body([^>]*)>", repl_body, text, count=1, flags=re.S)

    # Harden any existing theme toggle button without redesigning markup
    def repl_theme_btn(m):
        attrs = m.group(1)
        original = attrs
        if 'data-ff-theme-toggle' not in attrs:
            attrs += ' data-ff-theme-toggle=""'
        if 'type=' not in attrs:
            attrs += ' type="button"'
        if 'aria-pressed=' not in attrs:
            attrs += ' aria-pressed="false"'
        if 'aria-label=' not in attrs:
            attrs += ' aria-label="Toggle color theme"'
        if attrs != original:
            changes.append("theme toggle button normalized")
        return f"<button{attrs}>"

    text, count = re.subn(
        r"<button([^>]*\bff-themeToggle\b[^>]*)>",
        repl_theme_btn,
        text,
        flags=re.S,
    )

    if count == 0:
        changes.append("no .ff-themeToggle button found in campaign template")

    return text, changes

CSS_START = "/* FF_CAMPAIGN_SYSTEM_POLISH_V1_START */"
CSS_END = "/* FF_CAMPAIGN_SYSTEM_POLISH_V1_END */"

CSS_BLOCK = f"""
{CSS_START}
@layer ff.pages {{
  body[data-ff-page="fundraiser"] {{
    --ff-campaign-bg:
      linear-gradient(180deg, #fcfcfd 0%, #f6f8fc 52%, #f3f5fa 100%);
    --ff-campaign-surface:
      linear-gradient(180deg, rgb(255 255 255 / 0.96), rgb(247 249 253 / 0.94));
    --ff-campaign-surface-strong:
      linear-gradient(180deg, rgb(255 255 255 / 0.98), rgb(243 246 252 / 0.96));
    --ff-campaign-border: rgb(15 23 42 / 0.08);
    --ff-campaign-border-strong: rgb(15 23 42 / 0.12);
    --ff-campaign-shadow:
      0 18px 44px rgb(15 23 42 / 0.07),
      0 4px 12px rgb(15 23 42 / 0.04);
    --ff-campaign-shadow-strong:
      0 28px 70px rgb(2 6 23 / 0.11),
      0 10px 28px rgb(249 115 22 / 0.12);
    --ff-campaign-hero-glow:
      radial-gradient(960px 420px at 10% -10%, rgb(59 130 246 / 0.10), transparent 60%),
      radial-gradient(760px 360px at 100% 0%, rgb(249 115 22 / 0.10), transparent 58%);
    --ff-campaign-text: rgb(15 23 42 / 0.96);
    --ff-campaign-text-soft: rgb(15 23 42 / 0.72);
    --ff-campaign-pill-bg: rgb(15 23 42 / 0.04);
    --ff-campaign-pill-border: rgb(15 23 42 / 0.08);
    --ff-campaign-pill-text: rgb(15 23 42 / 0.70);
    background: var(--ff-campaign-bg);
    color: var(--ff-campaign-text);
  }}

  body[data-ff-page="fundraiser"]::before {{
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background: var(--ff-campaign-hero-glow);
    z-index: 0;
    opacity: 0.95;
  }}

  body[data-ff-page="fundraiser"] main,
  body[data-ff-page="fundraiser"] .ff-site,
  body[data-ff-page="fundraiser"] .ff-page,
  body[data-ff-page="fundraiser"] .ff-container {{
    position: relative;
    z-index: 1;
  }}

  body[data-ff-page="fundraiser"] .ff-display,
  body[data-ff-page="fundraiser"] h1,
  body[data-ff-page="fundraiser"] h2,
  body[data-ff-page="fundraiser"] h3 {{
    letter-spacing: -0.04em;
    text-wrap: balance;
  }}

  body[data-ff-page="fundraiser"] .ff-display {{
    line-height: 0.94;
  }}

  body[data-ff-page="fundraiser"] .ff-help,
  body[data-ff-page="fundraiser"] .ff-muted,
  body[data-ff-page="fundraiser"] .ff-lead,
  body[data-ff-page="fundraiser"] p {{
    color: var(--ff-campaign-text-soft);
  }}

  body[data-ff-page="fundraiser"] .ff-card,
  body[data-ff-page="fundraiser"] .ff-glass,
  body[data-ff-page="fundraiser"] .ff-proofMini,
  body[data-ff-page="fundraiser"] .ff-teamCard,
  body[data-ff-page="fundraiser"] .ff-checkoutShell,
  body[data-ff-page="fundraiser"] .ff-checkoutShell--flagship,
  body[data-ff-page="fundraiser"] .ff-sheet__panel,
  body[data-ff-page="fundraiser"] .ff-sheet__panel--flagship,
  body[data-ff-page="fundraiser"] .ff-modal__panel,
  body[data-ff-page="fundraiser"] .ff-modal__panel--flagship {{
    background: var(--ff-campaign-surface);
    border: 1px solid var(--ff-campaign-border);
    box-shadow: var(--ff-campaign-shadow);
    border-radius: clamp(18px, 2vw, 26px);
    backdrop-filter: saturate(1.06) blur(12px);
  }}

  body[data-ff-page="fundraiser"] #home .ff-card,
  body[data-ff-page="fundraiser"] .ff-checkoutShell--flagship,
  body[data-ff-page="fundraiser"] .ff-modal__panel--flagship {{
    background: var(--ff-campaign-surface-strong);
    border-color: var(--ff-campaign-border-strong);
    box-shadow: var(--ff-campaign-shadow-strong);
  }}

  body[data-ff-page="fundraiser"] .ff-pill,
  body[data-ff-page="fundraiser"] .ff-platformInlinePill,
  body[data-ff-page="fundraiser"] .ff-platformStatPill {{
    background: var(--ff-campaign-pill-bg);
    color: var(--ff-campaign-pill-text);
    border: 1px solid var(--ff-campaign-pill-border);
    box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.55);
  }}

  body[data-ff-page="fundraiser"] .ff-btn {{
    min-height: 2.875rem;
    border-radius: 999px;
    font-weight: 700;
    letter-spacing: -0.01em;
    transition:
      transform 160ms ease,
      box-shadow 160ms ease,
      border-color 160ms ease,
      background 160ms ease;
  }}

  body[data-ff-page="fundraiser"] .ff-btn:hover {{
    transform: translateY(-1px);
  }}

  body[data-ff-page="fundraiser"] .ff-btn--primary {{
    border-color: rgb(234 88 12 / 0.24);
    background:
      linear-gradient(135deg, #fb923c 0%, #f97316 52%, #ea580c 100%);
    color: white;
    box-shadow:
      0 14px 30px rgb(249 115 22 / 0.24),
      inset 0 1px 0 rgb(255 255 255 / 0.18);
  }}

  body[data-ff-page="fundraiser"] .ff-btn--secondary {{
    background: linear-gradient(180deg, rgb(255 255 255 / 0.88), rgb(243 246 251 / 0.86));
    border: 1px solid rgb(15 23 42 / 0.10);
    color: rgb(15 23 42 / 0.86);
    box-shadow:
      0 10px 24px rgb(15 23 42 / 0.06),
      inset 0 1px 0 rgb(255 255 255 / 0.70);
  }}

  body[data-ff-page="fundraiser"] .ff-btn:focus-visible,
  body[data-ff-page="fundraiser"] .ff-input:focus-visible,
  body[data-ff-page="fundraiser"] .ff-themeToggle:focus-visible {{
    outline: none;
    box-shadow:
      0 0 0 3px rgb(255 255 255 / 0.92),
      0 0 0 6px rgb(249 115 22 / 0.28);
  }}

  body[data-ff-page="fundraiser"] .ff-input,
  body[data-ff-page="fundraiser"] input,
  body[data-ff-page="fundraiser"] textarea,
  body[data-ff-page="fundraiser"] select {{
    background: rgb(255 255 255 / 0.82);
    border: 1px solid rgb(15 23 42 / 0.10);
    box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.60);
  }}

  body[data-ff-page="fundraiser"] .ff-themeToggle {{
    border-radius: 999px;
    border: 1px solid rgb(15 23 42 / 0.08);
    background: linear-gradient(180deg, rgb(255 255 255 / 0.90), rgb(244 246 251 / 0.86));
    box-shadow:
      0 12px 24px rgb(15 23 42 / 0.06),
      inset 0 1px 0 rgb(255 255 255 / 0.72);
  }}

  body[data-ff-page="fundraiser"] .ff-themeToggle[aria-pressed="true"] {{
    background:
      linear-gradient(180deg, rgb(15 23 42 / 0.92), rgb(30 41 59 / 0.90));
    border-color: rgb(148 163 184 / 0.24);
    color: rgb(248 250 252 / 0.94);
    box-shadow:
      0 14px 30px rgb(2 6 23 / 0.22),
      inset 0 1px 0 rgb(255 255 255 / 0.08);
  }}

  body[data-ff-page="fundraiser"] .ff-progress__track,
  body[data-ff-page="fundraiser"] .ff-meter,
  body[data-ff-page="fundraiser"] .ff-progressBar,
  body[data-ff-page="fundraiser"] [data-ff-progress-track] {{
    background: rgb(15 23 42 / 0.08);
    border: 1px solid rgb(15 23 42 / 0.05);
    border-radius: 999px;
    overflow: clip;
  }}

  body[data-ff-page="fundraiser"] .ff-progress__fill,
  body[data-ff-page="fundraiser"] .ff-meter__fill,
  body[data-ff-page="fundraiser"] .ff-progressBar__fill,
  body[data-ff-page="fundraiser"] [data-ff-progress-fill] {{
    background:
      linear-gradient(90deg, #fb923c 0%, #f97316 56%, #ea580c 100%);
    box-shadow: 0 8px 18px rgb(249 115 22 / 0.24);
  }}

  body[data-ff-page="fundraiser"] #home,
  body[data-ff-page="fundraiser"] #impact,
  body[data-ff-page="fundraiser"] #teams,
  body[data-ff-page="fundraiser"] #sponsors,
  body[data-ff-page="fundraiser"] #story,
  body[data-ff-page="fundraiser"] #trust-faq {{
    scroll-margin-top: 6rem;
  }}

  body[data-ff-page="fundraiser"] #teams .ff-teamCard,
  body[data-ff-page="fundraiser"] #sponsors .ff-card,
  body[data-ff-page="fundraiser"] #story .ff-card,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card {{
    min-height: 100%;
  }}

  body[data-ff-page="fundraiser"] .ff-sectionhead,
  body[data-ff-page="fundraiser"] .ff-checkoutHead,
  body[data-ff-page="fundraiser"] .ff-sponsorModal__head {{
    border-bottom: 1px solid rgb(15 23 42 / 0.06);
  }}

  body[data-ff-page="fundraiser"] .ff-row.ff-wrap.ff-gap-2[role="list"] {{
    gap: 0.5rem 0.5rem;
  }}

  body[data-ff-page="fundraiser"] .ff-kicker {{
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 800;
    color: rgb(15 23 42 / 0.56);
  }}

  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"],
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] {{
    --ff-campaign-bg:
      linear-gradient(180deg, #020617 0%, #071329 48%, #020617 100%);
    --ff-campaign-surface:
      linear-gradient(180deg, rgb(8 15 30 / 0.92), rgb(7 18 42 / 0.90));
    --ff-campaign-surface-strong:
      linear-gradient(180deg, rgb(9 18 38 / 0.96), rgb(6 16 37 / 0.94));
    --ff-campaign-border: rgb(148 163 184 / 0.14);
    --ff-campaign-border-strong: rgb(148 163 184 / 0.18);
    --ff-campaign-shadow:
      0 24px 60px rgb(2 6 23 / 0.34),
      0 8px 20px rgb(2 6 23 / 0.22);
    --ff-campaign-shadow-strong:
      0 34px 84px rgb(2 6 23 / 0.42),
      0 10px 26px rgb(249 115 22 / 0.14);
    --ff-campaign-hero-glow:
      radial-gradient(980px 430px at 12% -8%, rgb(37 99 235 / 0.15), transparent 60%),
      radial-gradient(760px 340px at 100% 0%, rgb(249 115 22 / 0.13), transparent 58%);
    --ff-campaign-text: rgb(248 250 252 / 0.96);
    --ff-campaign-text-soft: rgb(226 232 240 / 0.72);
    --ff-campaign-pill-bg: rgb(255 255 255 / 0.05);
    --ff-campaign-pill-border: rgb(148 163 184 / 0.14);
    --ff-campaign-pill-text: rgb(226 232 240 / 0.74);
    color: var(--ff-campaign-text);
  }}

  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-btn--secondary,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] .ff-btn--secondary {{
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.08), rgb(255 255 255 / 0.04));
    border-color: rgb(148 163 184 / 0.16);
    color: rgb(248 250 252 / 0.88);
    box-shadow:
      0 12px 24px rgb(2 6 23 / 0.20),
      inset 0 1px 0 rgb(255 255 255 / 0.06);
  }}

  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-input,
  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] input,
  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] textarea,
  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] select,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] .ff-input,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] input,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] textarea,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] select {{
    background: rgb(255 255 255 / 0.05);
    border-color: rgb(148 163 184 / 0.16);
    color: rgb(248 250 252 / 0.92);
    box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.04);
  }}

  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-kicker,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] .ff-kicker {{
    color: rgb(226 232 240 / 0.58);
  }}
}}
{CSS_END}
"""

JS_START = "// FF_THEME_CONTROLLER_V3_START"
JS_END = "// FF_THEME_CONTROLLER_V3_END"

JS_BLOCK = f"""
{JS_START}
(function () {{
  if (window.__FF_THEME_CONTROLLER_V3__) return;
  window.__FF_THEME_CONTROLLER_V3__ = true;

  var root = document.documentElement;
  var KEY = "ff.theme";
  var LEGACY_KEYS = ["ff_theme", "futurefunded.theme"];
  var SELECTOR = "[data-ff-theme-toggle], .ff-themeToggle, #ff-theme-toggle";
  var media = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

  function readStoredTheme() {{
    try {{
      var direct = localStorage.getItem(KEY);
      if (direct === "light" || direct === "dark") return direct;

      for (var i = 0; i < LEGACY_KEYS.length; i += 1) {{
        var legacy = localStorage.getItem(LEGACY_KEYS[i]);
        if (legacy === "light" || legacy === "dark") return legacy;
      }}
    }} catch (err) {{}}
    return null;
  }}

  function writeStoredTheme(theme) {{
    try {{
      localStorage.setItem(KEY, theme);
      for (var i = 0; i < LEGACY_KEYS.length; i += 1) {{
        localStorage.setItem(LEGACY_KEYS[i], theme);
      }}
    }} catch (err) {{}}
  }}

  function getCurrentTheme() {{
    var attr = root.getAttribute("data-theme");
    if (attr === "light" || attr === "dark") return attr;

    var body = document.body;
    if (body) {{
      var bodyAttr = body.getAttribute("data-ff-theme");
      if (bodyAttr === "light" || bodyAttr === "dark") return bodyAttr;
    }}

    var stored = readStoredTheme();
    if (stored) return stored;

    if (media && media.matches) return "dark";
    return "light";
  }}

  function allToggles() {{
    return Array.prototype.slice.call(document.querySelectorAll(SELECTOR));
  }}

  function paintTheme(theme, persist) {{
    var resolved = theme === "dark" ? "dark" : "light";
    root.setAttribute("data-theme", resolved);
    root.style.colorScheme = resolved;

    if (document.body) {{
      document.body.setAttribute("data-ff-theme", resolved);
    }}

    var toggles = allToggles();
    for (var i = 0; i < toggles.length; i += 1) {{
      toggles[i].setAttribute("aria-pressed", resolved === "dark" ? "true" : "false");
      toggles[i].setAttribute(
        "aria-label",
        resolved === "dark" ? "Switch to light theme" : "Switch to dark theme"
      );
    }}

    if (persist) writeStoredTheme(resolved);

    try {{
      document.dispatchEvent(
        new CustomEvent("ff:theme-changed", {{
          detail: {{ theme: resolved }}
        }})
      );
    }} catch (err) {{}}
  }}

  function toggleTheme() {{
    paintTheme(getCurrentTheme() === "dark" ? "light" : "dark", true);
  }}

  document.addEventListener("click", function (event) {{
    var target = event.target;
    if (!target || !target.closest) return;
    var toggle = target.closest(SELECTOR);
    if (!toggle) return;

    event.preventDefault();
    if (event.stopImmediatePropagation) event.stopImmediatePropagation();
    event.stopPropagation();

    toggleTheme();
  }}, true);

  document.addEventListener("keydown", function (event) {{
    var target = event.target;
    if (!target || !target.closest) return;
    var toggle = target.closest(SELECTOR);
    if (!toggle) return;

    if (event.key !== "Enter" && event.key !== " ") return;

    event.preventDefault();
    if (event.stopImmediatePropagation) event.stopImmediatePropagation();
    event.stopPropagation();

    toggleTheme();
  }}, true);

  if (media && media.addEventListener) {{
    media.addEventListener("change", function (event) {{
      var stored = readStoredTheme();
      if (stored === "light" || stored === "dark") return;
      paintTheme(event.matches ? "dark" : "light", false);
    }});
  }}

  var observer = null;
  if (window.MutationObserver) {{
    observer = new MutationObserver(function () {{
      paintTheme(getCurrentTheme(), false);
    }});
    observer.observe(document.documentElement, {{
      childList: true,
      subtree: true
    }});
  }}

  paintTheme(getCurrentTheme(), false);
}})();
{JS_END}
"""

def main():
    backups = {name: backup(path) for name, path in TARGETS.items()}

    campaign_html = read(TARGETS["campaign_html"])
    campaign_html, html_changes = patch_campaign_html(campaign_html)
    write(TARGETS["campaign_html"], campaign_html)

    css = read(TARGETS["css"])
    css = upsert_marker_block(css, CSS_START, CSS_END, CSS_BLOCK)
    write(TARGETS["css"], css)

    js = read(TARGETS["js"])
    js = upsert_marker_block(js, JS_START, JS_END, JS_BLOCK)
    write(TARGETS["js"], js)

    print("✅ ff_campaign_system_polish_v1 applied")
    for name, bak in backups.items():
        print(f"🛟 backup[{name}]: {bak}")

    print("\\n== HTML CHANGES ==")
    for item in html_changes:
        print(f" - {item}")

    print("\\n== MARKER PROOF ==")
    css_text = read(TARGETS["css"])
    js_text = read(TARGETS["js"])
    html_text = read(TARGETS["campaign_html"])

    print("css:", CSS_START in css_text and CSS_END in css_text)
    print("js :", JS_START in js_text and JS_END in js_text)
    print("theme toggle hook present:", ('data-ff-theme-toggle' in html_text) or ('ff-themeToggle' in html_text))
    print("fundraiser body contract:", 'data-ff-page="fundraiser"' in html_text)

if __name__ == "__main__":
    main()
