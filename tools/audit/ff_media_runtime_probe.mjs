import fs from "node:fs";
import path from "node:path";

let chromium;
try {
  ({ chromium } = await import("playwright"));
} catch (err) {
  console.error("❌ Playwright is not installed.");
  console.error("Run:");
  console.error("  npm i -D playwright");
  console.error("  npx playwright install chromium");
  process.exit(1);
}

const url = process.argv[2] || "http://127.0.0.1:5000/c/connect-atx-elite";
const outDir = path.resolve("tools/audit/runtime-probe-artifacts");
fs.mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 2200 } });

await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
await page.waitForTimeout(1500);

const result = await page.evaluate(async () => {
  const MEDIA_SELECTORS = [
    ".ff-teamCard__img",
    ".ff-storyPoster__img",
    ".ff-videoMount iframe",
    ".ff-videoMount video",
  ];

  const CONTAINER_SELECTORS = [
    ".ff-teamCard__media",
    ".ff-storyPoster",
    ".ff-videoFrame",
    ".ff-videoMount",
  ];

  const nodes = [...document.querySelectorAll(MEDIA_SELECTORS.join(","))];

  const sameOrContains = (a, b) => !!a && !!b && (a === b || a.contains(b) || b.contains(a));

  const short = (v, max = 160) => {
    if (v == null) return "";
    const s = String(v);
    return s.length > max ? s.slice(0, max) + "…" : s;
  };

  const getContainer = (el) => el.closest(CONTAINER_SELECTORS.join(","));

  const centerTopElement = (el) => {
    const r = el.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) return null;
    return document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
  };

  const pick = (el) => {
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const container = getContainer(el);
    const ccs = container ? getComputedStyle(container) : null;
    const cr = container ? container.getBoundingClientRect() : null;
    const topEl = centerTopElement(el);

    return {
      tag: el.tagName,
      className: el.className,
      src: el.currentSrc || el.src || "",
      complete: "complete" in el ? !!el.complete : null,
      naturalWidth: "naturalWidth" in el ? el.naturalWidth : null,
      naturalHeight: "naturalHeight" in el ? el.naturalHeight : null,

      display: cs.display,
      visibility: cs.visibility,
      opacity: cs.opacity,
      position: cs.position,
      zIndex: cs.zIndex,
      pointerEvents: cs.pointerEvents,

      width: Math.round(r.width),
      height: Math.round(r.height),

      containerClass: container?.className || "",
      containerDisplay: ccs?.display || "",
      containerVisibility: ccs?.visibility || "",
      containerOpacity: ccs?.opacity || "",
      containerOverflow: ccs?.overflow || "",
      containerPosition: ccs?.position || "",
      containerWidth: cr ? Math.round(cr.width) : null,
      containerHeight: cr ? Math.round(cr.height) : null,

      topElementTag: topEl?.tagName || "",
      topElementClass: topEl?.className || "",
      topElementSameOrContains: sameOrContains(el, topEl) || sameOrContains(container, topEl),
    };
  };

  const before = nodes.map(pick);

  await new Promise((r) => setTimeout(r, 1800));

  const after = nodes.map(pick);

  const classify = (b, a) => {
    const reasons = [];

    const cssHidden =
      b.display === "none" ||
      b.visibility === "hidden" ||
      Number.parseFloat(b.opacity || "1") === 0 ||
      b.containerDisplay === "none" ||
      b.containerVisibility === "hidden" ||
      Number.parseFloat(b.containerOpacity || "1") === 0;

    if (cssHidden) reasons.push("CSS_HIDING");

    const zeroSize =
      (b.width ?? 0) === 0 ||
      (b.height ?? 0) === 0 ||
      (b.containerWidth ?? 0) === 0 ||
      (b.containerHeight ?? 0) === 0;

    if (zeroSize) reasons.push("ZERO_SIZE_LAYOUT");

    const overlayCollision =
      !b.topElementSameOrContains &&
      !!b.topElementTag &&
      !(String(b.topElementClass || "").includes("ff-storyPoster__overlay"));

    if (overlayCollision) reasons.push("OVERLAY_COLLISION");

    const runtimeMutation =
      b.src !== a.src ||
      b.className !== a.className ||
      b.display !== a.display ||
      b.visibility !== a.visibility ||
      b.opacity !== a.opacity ||
      b.width !== a.width ||
      b.height !== a.height ||
      b.containerWidth !== a.containerWidth ||
      b.containerHeight !== a.containerHeight;

    if (runtimeMutation) reasons.push("RUNTIME_MUTATION");

    const unloadedImage =
      b.tag === "IMG" &&
      ((b.complete === false) || ((b.naturalWidth ?? 0) === 0 && !!b.src));

    if (unloadedImage) reasons.push("IMAGE_NOT_RENDERED");

    if (!reasons.length) reasons.push("HEALTHY");

    return reasons;
  };

  return before.map((b, i) => {
    const a = after[i];
    return {
      index: i,
      node: short(b.className || b.tag),
      src: short(b.src, 120),
      status: classify(b, a).join(" | "),
      before: b,
      after: a,
    };
  });
});

console.log("\n== FF MEDIA RUNTIME PROBE ==\n");
for (const row of result) {
  console.log(`[#${row.index}] ${row.node}`);
  console.log(`status: ${row.status}`);
  console.log(`src   : ${row.src}`);
  console.log(`size  : ${row.before.width}x${row.before.height} | container ${row.before.containerWidth}x${row.before.containerHeight}`);
  console.log(`css   : display=${row.before.display} visibility=${row.before.visibility} opacity=${row.before.opacity}`);
  console.log(`topEl : ${row.before.topElementTag} ${row.before.topElementClass}`);
  console.log("");
}

const screenshotPath = path.join(outDir, "ff_media_runtime_probe.png");
await page.screenshot({ path: screenshotPath, fullPage: true });
console.log("📸 screenshot:", screenshotPath);

const jsonPath = path.join(outDir, "ff_media_runtime_probe.json");
fs.writeFileSync(jsonPath, JSON.stringify(result, null, 2), "utf-8");
console.log("🧾 json:", jsonPath);

await browser.close();
