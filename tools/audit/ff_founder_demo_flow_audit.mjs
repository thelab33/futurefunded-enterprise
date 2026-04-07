import { chromium, devices } from "@playwright/test";
import fs from "node:fs/promises";
import path from "node:path";

const BASE_URL = process.env.BASE_URL || "http://127.0.0.1:5000";
const NOW = new Date().toISOString().replaceAll(":", "-").replaceAll(".", "-");
const OUT = path.join(process.cwd(), "reports", "founder-demo-flow", NOW);
const LATEST = path.join(process.cwd(), "reports", "founder-demo-flow", "LATEST.txt");

const desktopProject = {
  name: "desktop",
  viewport: { width: 1440, height: 1100 },
  isMobile: false,
  hasTouch: false,
};

const mobileProject = {
  name: "mobile",
  ...devices["iPhone 14"],
};

const routes = [
  {
    key: "platform-home",
    route: "/platform/",
    titleIncludes: "FutureFunded",
    checks: [
      { label: "home hero", locator: "main h1, [data-ff-platform-hero] h1", type: "visible" },
      { label: "launch CTA", locator: 'a[href="/platform/onboarding"]', type: "visible" },
      { label: "live fundraiser CTA", locator: 'a[href="/c/spring-fundraiser"]', type: "visible" },
      { label: "pricing link", locator: 'a[href="/platform/pricing"]', type: "visible" },
      { label: "demo link", locator: 'a[href="/platform/demo"]', type: "visible" },
    ],
  },
  {
    key: "platform-onboarding",
    route: "/platform/onboarding",
    titleIncludes: "Onboarding",
    checks: [
      { label: "onboarding title", locator: "main h1", type: "visible" },
      { label: "live fundraiser promise", text: /live fundraiser|go live/i, type: "text" },
      { label: "public fundraiser copy", text: /public fundraiser|campaign/i, type: "text" },
      { label: "dashboard handoff", locator: 'a[href="/platform/dashboard"]', type: "visible" },
    ],
  },
  {
    key: "platform-dashboard",
    route: "/platform/dashboard",
    titleIncludes: "Dashboard",
    checks: [
      { label: "dashboard heading", locator: "main h1", type: "visible" },
      { label: "live fundraisers card", text: /live fundraiser|active campaign|fundraisers/i, type: "text" },
      { label: "guided launch action", locator: 'a[href="/platform/onboarding"]', type: "visible" },
      { label: "fundraiser link", locator: 'a[href="/c/spring-fundraiser"]', type: "visible" },
      { label: "pricing link", locator: 'a[href="/platform/pricing"]', type: "visible" },
    ],
  },
  {
    key: "platform-pricing",
    route: "/platform/pricing",
    titleIncludes: "Pricing",
    checks: [
      { label: "pricing heading", locator: "main h1", type: "visible" },
      { label: "starter plan", text: /starter/i, type: "text" },
      { label: "growth plan", text: /growth/i, type: "text" },
      { label: "white-label option", text: /white.label|white label|premium/i, type: "text" },
      { label: "guided launch link", locator: 'a[href="/platform/onboarding"]', type: "visible" },
      { label: "demo link", locator: 'a[href="/platform/demo"]', type: "visible" },
    ],
  },
  {
    key: "platform-demo",
    route: "/platform/demo",
    titleIncludes: "Demo",
    checks: [
      { label: "demo heading", locator: "main h1", type: "visible" },
      { label: "fundraiser link", locator: 'a[href="/c/spring-fundraiser"]', type: "visible" },
      { label: "pricing link", locator: 'a[href="/platform/pricing"]', type: "visible" },
    ],
  },
  {
    key: "campaign",
    route: "/c/spring-fundraiser",
    titleIncludes: "Fundraiser",
    checks: [
      { label: "campaign heading", locator: "main h1, #heroTitle", type: "visible" },
      { label: "donate control", locator: '[data-ff-open-checkout]', type: "tapTarget" },
      { label: "sponsor cue", locator: '[data-ff-sponsor-a-player], [data-ff-sponsor-modal], [data-ff-sponsor-submit]', type: "existsAny" },
      { label: "platform return link", locator: 'a[href="/platform/"]', type: "visibleOptional" },
    ],
  },
];

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true });
}

async function locatorExists(locator) {
  return (await locator.count()) > 0;
}

async function isActuallyVisible(locator) {
  if (!(await locatorExists(locator))) return false;
  return await locator.first().isVisible();
}

async function hasGoodTapTarget(locator) {
  const count = await locator.count();
  if (!count) return false;

  for (let i = 0; i < count; i += 1) {
    const el = locator.nth(i);

    try {
      if (!(await el.isVisible())) continue;
      const box = await el.boundingBox();
      if (!box) continue;
      if (box.width >= 44 && box.height >= 32) return true;
    } catch {
      continue;
    }
  }

  return false;
}

async function textMatch(page, regex) {
  const body = await page.locator("body").innerText();
  return regex.test(body);
}

async function runRoute(context, page, project, item) {
  const result = {
    key: item.key,
    route: item.route,
    status: null,
    title: "",
    screenshot: "",
    checks: [],
    consoleErrors: [],
    badResponses: [],
    pageErrors: [],
    pass: true,
  };

  page.on("console", (msg) => {
    if (msg.type() === "error") result.consoleErrors.push(msg.text());
  });

  page.on("pageerror", (err) => {
    result.pageErrors.push(String(err));
  });

  page.on("response", (resp) => {
    if (resp.status() >= 400) {
      result.badResponses.push(`${resp.status()} ${resp.url()}`);
    }
  });

  const url = BASE_URL + item.route;
  const resp = await page.goto(url, { waitUntil: "networkidle" });
  result.status = resp ? resp.status() : null;
  result.title = await page.title();

  await page.screenshot({
    path: path.join(OUT, project.name, `${item.key}.png`),
    fullPage: true,
  });

  result.screenshot = path.join("reports", "founder-demo-flow", NOW, project.name, `${item.key}.png`);

  if (result.status !== 200) result.pass = false;
  if (!result.title.includes(item.titleIncludes)) result.pass = false;

  for (const check of item.checks) {
    let ok = false;

    if (check.type === "visible") {
      ok = await isActuallyVisible(page.locator(check.locator));
    } else if (check.type === "visibleOptional") {
      ok = true;
    } else if (check.type === "tapTarget") {
      ok = await hasGoodTapTarget(page.locator(check.locator));
    } else if (check.type === "text") {
      ok = await textMatch(page, check.text);
    } else if (check.type === "existsAny") {
      ok = await locatorExists(page.locator(check.locator));
    }

    result.checks.push({ label: check.label, ok });

    if (!ok && check.type !== "visibleOptional") {
      result.pass = false;
    }
  }

  return result;
}

function renderSummary(allRuns) {
  let overallPass = true;
  const lines = [];

  lines.push("# FutureFunded founder demo flow audit");
  lines.push("");
  lines.push(`- base_url: ${BASE_URL}`);
  lines.push(`- out: ${OUT}`);
  lines.push("");

  for (const run of allRuns) {
    lines.push(`## ${run.project}`);
    lines.push("");

    for (const page of run.results) {
      lines.push(`### ${page.pass ? "PASS" : "FAIL"} ${page.key}`);
      lines.push(`- route: ${page.route}`);
      lines.push(`- status: ${page.status}`);
      lines.push(`- title: ${page.title}`);
      lines.push(`- screenshot: ${page.screenshot}`);
      lines.push("- checks:");
      for (const check of page.checks) {
        lines.push(`  - ${check.ok ? "PASS" : "FAIL"} ${check.label}`);
      }
      lines.push("");

      if (!page.pass) overallPass = false;
      if (page.consoleErrors.length) overallPass = false;
      if (page.pageErrors.length) overallPass = false;
      if (page.badResponses.length) overallPass = false;
    }

    const consoleErrors = [...new Set(run.results.flatMap((r) => r.consoleErrors))];
    const pageErrors = [...new Set(run.results.flatMap((r) => r.pageErrors))];
    const badResponses = [...new Set(run.results.flatMap((r) => r.badResponses))];

    lines.push("- page errors:");
    lines.push(pageErrors.length ? pageErrors.map((x) => `  - ${x}`).join("\n") : "  - none");
    lines.push("- console errors:");
    lines.push(consoleErrors.length ? consoleErrors.map((x) => `  - ${x}`).join("\n") : "  - none");
    lines.push("- bad responses:");
    lines.push(badResponses.length ? badResponses.map((x) => `  - ${x}`).join("\n") : "  - none");
    lines.push("");
  }

  lines.push("## Overall verdict");
  lines.push(`- ${overallPass ? "PASS" : "FAIL"}`);
  lines.push("");

  return lines.join("\n");
}

async function main() {
  await ensureDir(path.join(OUT, "desktop"));
  await ensureDir(path.join(OUT, "mobile"));
  await fs.writeFile(LATEST, OUT + "\n", "utf8");

  const browser = await chromium.launch({ headless: true });
  const projects = [desktopProject, mobileProject];
  const allRuns = [];

  for (const project of projects) {
    const context = await browser.newContext(project);
    const page = await context.newPage();
    const results = [];

    for (const item of routes) {
      results.push(await runRoute(context, page, project, item));
    }

    await context.close();
    allRuns.push({ project: project.name, results });
  }

  await browser.close();

  const summary = renderSummary(allRuns);
  const summaryPath = path.join(OUT, "summary.md");
  await fs.writeFile(summaryPath, summary, "utf8");

  console.log("Founder demo flow audit complete: " + summaryPath);
  console.log(summary);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
