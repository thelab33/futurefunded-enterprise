from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff-above-main-premium.css"
JS = ROOT / "apps/web/app/static/js/ff-app.js"

for path in (CSS, JS):
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
for path in (CSS, JS):
    shutil.copy2(path, path.with_name(f"{path.name}.{timestamp}.bak"))

css_block = """
/* ==========================================================================
   FF_MOBILE_CONVERSION_RAIL_V1
   Mobile-first sticky conversion rail for fundraiser surface
   ========================================================================== */

@media (max-width: 820px) {
  body[data-ff-page="fundraiser"] {
    padding-bottom: calc(5.75rem + env(safe-area-inset-bottom));
  }

  body[data-ff-page="fundraiser"] .ff-mobileActionRail {
    position: fixed;
    inset-inline: 0;
    bottom: 0;
    z-index: 120;
    display: grid;
    grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.9fr);
    gap: 0.75rem;
    align-items: center;
    padding:
      0.75rem
      clamp(0.875rem, 4vw, 1rem)
      calc(0.85rem + env(safe-area-inset-bottom));
    background:
      linear-gradient(180deg, rgb(10 14 24 / 0.02), rgb(10 14 24 / 0.86)),
      linear-gradient(135deg, rgb(255 255 255 / 0.92), rgb(248 250 252 / 0.94));
    border-top: 1px solid rgb(148 163 184 / 0.18);
    box-shadow:
      0 -12px 40px rgb(2 6 23 / 0.18),
      inset 0 1px 0 rgb(255 255 255 / 0.52);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
  }

  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-mobileActionRail {
    background:
      linear-gradient(180deg, rgb(2 6 23 / 0.08), rgb(2 6 23 / 0.92)),
      linear-gradient(135deg, rgb(15 23 42 / 0.96), rgb(15 23 42 / 0.92));
    border-top-color: rgb(148 163 184 / 0.14);
    box-shadow:
      0 -12px 36px rgb(2 6 23 / 0.44),
      inset 0 1px 0 rgb(255 255 255 / 0.04);
  }

  body[data-ff-page="fundraiser"] .ff-mobileActionRail__button {
    min-height: 3.25rem;
    border: 1px solid rgb(148 163 184 / 0.16);
    border-radius: 999px;
    padding: 0.9rem 1rem;
    font: inherit;
    font-weight: 800;
    letter-spacing: 0.01em;
    text-align: center;
    cursor: pointer;
    transition:
      transform 160ms ease,
      box-shadow 160ms ease,
      border-color 160ms ease,
      background-color 160ms ease;
  }

  body[data-ff-page="fundraiser"] .ff-mobileActionRail__button:hover,
  body[data-ff-page="fundraiser"] .ff-mobileActionRail__button:focus-visible {
    transform: translateY(-1px);
  }

  body[data-ff-page="fundraiser"] .ff-mobileActionRail__button--primary {
    color: rgb(255 255 255 / 0.98);
    background: linear-gradient(135deg, rgb(249 115 22), rgb(234 88 12));
    box-shadow: 0 12px 24px rgb(249 115 22 / 0.28);
  }

  body[data-ff-page="fundraiser"] .ff-mobileActionRail__button--secondary {
    color: rgb(15 23 42 / 0.94);
    background: rgb(255 255 255 / 0.82);
    box-shadow: 0 10px 22px rgb(15 23 42 / 0.08);
  }

  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-mobileActionRail__button--secondary {
    color: rgb(226 232 240 / 0.96);
    background: rgb(15 23 42 / 0.82);
    box-shadow: 0 10px 22px rgb(2 6 23 / 0.24);
  }
}

@media (min-width: 821px) {
  body[data-ff-page="fundraiser"] .ff-mobileActionRail {
    display: none !important;
  }
}
""".strip() + "\n"

js_block = r"""
/* ==========================================================================
   FF_MOBILE_CONVERSION_RAIL_V1
   Mobile fundraiser sticky action rail
   ========================================================================== */
(function () {
  function isVisibleElement(el) {
    if (!(el instanceof HTMLElement)) return false;
    if (el.hasAttribute("hidden")) return false;
    const style = window.getComputedStyle(el);
    if (style.display === "none" || style.visibility === "hidden" || style.opacity === "0") return false;
    return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
  }

  function findByText(matchers) {
    const candidates = Array.from(document.querySelectorAll("a, button, [role='button']"));
    return candidates.find((el) => {
      if (!isVisibleElement(el)) return false;
      const text = (el.textContent || "").replace(/\s+/g, " ").trim().toLowerCase();
      if (!text) return false;
      return matchers.some((m) => text.includes(m));
    }) || null;
  }

  function initMobileActionRail() {
    const body = document.body;
    if (!body) return;
    if (body.getAttribute("data-ff-page") !== "fundraiser") return;
    if (window.matchMedia("(min-width: 821px)").matches) return;
    if (document.querySelector("[data-ff-mobile-rail]")) return;

    const donateSource =
      document.querySelector("[data-ff-open-checkout]") ||
      document.querySelector("[data-ff-donate]") ||
      findByText(["donate", "give now", "support now"]);

    const sponsorSource =
      document.querySelector("[data-ff-open-sponsor]") ||
      document.querySelector("[data-ff-sponsor-interest]") ||
      findByText(["sponsor", "become a sponsor"]);

    if (!donateSource && !sponsorSource) return;

    const rail = document.createElement("div");
    rail.className = "ff-mobileActionRail";
    rail.setAttribute("data-ff-mobile-rail", "");

    if (donateSource) {
      const donateBtn = document.createElement("button");
      donateBtn.type = "button";
      donateBtn.className = "ff-mobileActionRail__button ff-mobileActionRail__button--primary";
      donateBtn.textContent = "Donate";
      donateBtn.addEventListener("click", function () {
        donateSource.dispatchEvent(new MouseEvent("click", {
          bubbles: true,
          cancelable: true,
          view: window
        }));
      });
      rail.appendChild(donateBtn);
    }

    if (sponsorSource) {
      const sponsorBtn = document.createElement("button");
      sponsorBtn.type = "button";
      sponsorBtn.className = "ff-mobileActionRail__button ff-mobileActionRail__button--secondary";
      sponsorBtn.textContent = "Sponsor";
      sponsorBtn.addEventListener("click", function () {
        sponsorSource.dispatchEvent(new MouseEvent("click", {
          bubbles: true,
          cancelable: true,
          view: window
        }));
      });
      rail.appendChild(sponsorBtn);
    }

    if (!rail.children.length) return;
    body.appendChild(rail);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initMobileActionRail, { once: true });
  } else {
    initMobileActionRail();
  }
})();
""".strip() + "\n"

css_text = CSS.read_text(encoding="utf-8")
js_text = JS.read_text(encoding="utf-8")

if "FF_MOBILE_CONVERSION_RAIL_V1" not in css_text:
    CSS.write_text(css_text.rstrip() + "\n\n" + css_block, encoding="utf-8")

if "FF_MOBILE_CONVERSION_RAIL_V1" not in js_text:
    JS.write_text(js_text.rstrip() + "\n\n" + js_block, encoding="utf-8")

print("patched mobile conversion rail.")
