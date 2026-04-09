import { chromium } from "playwright";

const URL = process.env.FF_AUDIT_URL || "http://127.0.0.1:5000/c/spring-fundraiser";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({
  viewport: { width: 390, height: 844 },
  deviceScaleFactor: 2,
  isMobile: true,
  hasTouch: true,
});

await page.goto(URL, { waitUntil: "networkidle" });

const report = await page.evaluate(() => {
  const shell = document.querySelector("#teams .ff-teamsShell");
  if (!shell) return { error: "missing #teams .ff-teamsShell" };

  const shellRect = shell.getBoundingClientRect();
  const shellStyle = getComputedStyle(shell);

  const children = [...shell.children].map((el, index) => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return {
      index,
      tag: el.tagName,
      id: el.id || null,
      className: el.className || null,
      width: Math.round(r.width),
      height: Math.round(r.height),
      minHeight: cs.minHeight,
      maxHeight: cs.maxHeight,
      display: cs.display,
      position: cs.position,
      overflow: cs.overflow,
      backgroundColor: cs.backgroundColor,
      backgroundImage: cs.backgroundImage,
      borderRadius: cs.borderRadius,
      text: (el.textContent || "").replace(/\s+/g, " ").trim().slice(0, 220),
    };
  });

  return {
    shell: {
      width: Math.round(shellRect.width),
      height: Math.round(shellRect.height),
      className: shell.className || null,
      backgroundColor: shellStyle.backgroundColor,
      backgroundImage: shellStyle.backgroundImage,
      borderRadius: shellStyle.borderRadius,
      overflow: shellStyle.overflow,
    },
    children,
  };
});

console.log(JSON.stringify(report, null, 2));

await browser.close();
