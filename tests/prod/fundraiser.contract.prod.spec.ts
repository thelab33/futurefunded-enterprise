import { test, expect } from '@playwright/test';

const FUNDRAISER_PATH = process.env.FF_FUNDRAISER_PATH || '/c/spring-fundraiser';

test('fundraiser runtime contract hooks are present', async ({ page }) => {
  await page.goto(FUNDRAISER_PATH, { waitUntil: 'domcontentloaded' });

  const requiredSelectors = [
    '[data-ff-open-checkout]',
    '[data-ff-checkout-sheet]',
    '[data-ff-open-sponsor]',
    '[data-ff-sponsor-modal]',
    '[data-ff-share]',
    '[data-ff-live]',
    '[data-ff-toasts]',
    '[data-ff-tabs]',
    '[data-ff-floating-donate]',
  ];

  for (const selector of requiredSelectors) {
    await expect(page.locator(selector).first(), `Missing selector: ${selector}`).toBeAttached();
  }
});
