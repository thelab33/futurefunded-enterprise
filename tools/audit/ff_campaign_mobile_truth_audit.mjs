import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";

const URL = process.env.FF_AUDIT_URL || "http://127.0.0.1:5000/c/spring-fundraiser";
const OUT = path.resolve("artifacts/reports/ff_campaign_mobile_truth_audit.json");

const buttonSelectors = [
  ".ff-donate-btn",
  ".ff-btn",
  "[data-ff-donate]",
  "[data-ff-open-sponsor]",
  ".ff-mobileCtaBar__btn",
  ".ff-mobileActionRail__button--primary",
  ".ff-mobileActionRail__button--secondary",
  ".ff-footer__link--button",
];

const stageSelectors = [
  ".ff-teamsEmpty",
  "#teams .ff-teamsShell",
  "#teams .ff-teamGrid",
  ".ff-storyMedia",
  ".ff-storyMediaCard",
];

function uniqBy(arr, keyFn) {
  const seen = new Set();
  const out = [];
  for (const item of arr) {
    const key = keyFn(item);
    if (!seen.has(key)) {
      seen.add(key);
      out.push(item);
    }
  }
  return out;
}

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({
  viewport: { width: 390, height: 844 },
  deviceScaleFactor: 2,
  isMobile: true,
  hasTouch: true,
});

await page.goto(URL, { waitUntil: "networkidle" });

const cssLinks = await page.evaluate(async () => {
  const links = [...document.querySelectorAll('link[rel="stylesheet"]')].map((el) => el.href);
  return links;
});

const buttons = await page.evaluate((selectors) => {
  const els = selectors.flatMap((sel) => [...document.querySelectorAll(sel)]);
  const visible = els.filter((el) => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== "hidden" && cs.display !== "none";
  });

  return visible.slice(0, 18).map((el) => {
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    return {
      text: (el.textContent || "").replace(/\s+/g, " ").trim(),
      tag: el.tagName,
      id: el.id || null,
      className: el.className || null,
      dataset: { ...el.dataset },
      width: Math.round(r.width),
      height: Math.round(r.height),
      backgroundColor: cs.backgroundColor,
      backgroundImage: cs.backgroundImage,
      color: cs.color,
      borderColor: cs.borderColor,
      borderRadius: cs.borderRadius,
      boxShadow: cs.boxShadow,
      minHeight: cs.minHeight,
    };
  });
}, buttonSelectors);

const stages = await page.evaluate((selectors) => {
  const out = [];
  for (const sel of selectors) {
    for (const el of document.querySelectorAll(sel)) {
      const cs = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      if (r.width <= 0 || r.height <= 0) continue;
      out.push({
        selector: sel,
        tag: el.tagName,
        id: el.id || null,
        className: el.className || null,
        text: (el.textContent || "").replace(/\s+/g, " ").trim().slice(0, 180),
        width: Math.round(r.width),
        height: Math.round(r.height),
        minHeight: cs.minHeight,
        maxHeight: cs.maxHeight,
        display: cs.display,
        backgroundColor: cs.backgroundColor,
        backgroundImage: cs.backgroundImage,
        borderRadius: cs.borderRadius,
        overflow: cs.overflow,
      });
    }
  }
  return out;
}, stageSelectors);

const teamsSection = await page.evaluate(() => {
  const el = document.querySelector("#teams");
  if (!el) return null;
  const r = el.getBoundingClientRect();
  const cs = getComputedStyle(el);
  return {
    width: Math.round(r.width),
    height: Math.round(r.height),
    paddingTop: cs.paddingTop,
    paddingBottom: cs.paddingBottom,
    marginTop: cs.marginTop,
    marginBottom: cs.marginBottom,
  };
});

const report = {
  url: URL,
  cssLinks,
  buttons: uniqBy(buttons, (x) => `${x.tag}|${x.text}|${x.className}|${x.id}`),
  stages,
  teamsSection,
};

fs.writeFileSync(OUT, JSON.stringify(report, null, 2), "utf8");
console.log(JSON.stringify(report, null, 2));

await browser.close();
