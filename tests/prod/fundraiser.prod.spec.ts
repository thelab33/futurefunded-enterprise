import { test, expect, Page } from '@playwright/test';

const FUNDRAISER_PATH = process.env.FF_FUNDRAISER_PATH || '/c/spring-fundraiser';

async function openFundraiser(page: Page) {
  await page.goto(FUNDRAISER_PATH, { waitUntil: 'domcontentloaded' });
  await expect(page).toHaveURL(new RegExp(`${FUNDRAISER_PATH.replace(/\//g, '\\/')}`));
  await expect(page.locator('body[data-ff-page="fundraiser"]')).toBeVisible();
}

test.describe('Production fundraiser smoke', () => {
  test('renders hero + major sections', async ({ page }) => {
    await openFundraiser(page);

    await expect(
      page.getByRole('heading', { name: /fuel the season\. fund the future\./i })
    ).toBeVisible();

    await expect(
      page.getByRole('heading', { name: /support the season\./i })
    ).toBeVisible();

    await expect(
      page.getByRole('heading', { name: /what support covers/i })
    ).toBeVisible();

    await expect(
      page.getByRole('heading', { name: /teams in the program/i })
    ).toBeVisible();

    await expect(
      page.getByRole('heading', { name: /become a featured sponsor/i })
    ).toBeVisible();

    await expect(
      page.getByRole('heading', { name: /questions before you support\?/i })
    ).toBeVisible();

    await expect(
      page.getByRole('heading', { name: /support this fundraiser with confidence\./i })
    ).toBeVisible();
  });

  test('top donate CTA opens checkout without submitting payment', async ({ page }) => {
    await openFundraiser(page);

    const donateCta = page.locator('[data-ff-open-checkout]').first();
    await expect(donateCta).toBeVisible();
    await donateCta.click();

    const checkoutSheet = page.locator('[data-ff-checkout-sheet]');
    await expect(checkoutSheet).toBeVisible();
    await expect(checkoutSheet).toHaveAttribute('data-open', /true/);

    await page.keyboard.press('Escape');
    await expect(checkoutSheet).toBeHidden({ timeout: 5000 });
  });

  test('sponsor CTA opens sponsor modal', async ({ page }) => {
    await openFundraiser(page);

    const sponsorCta = page.locator('[data-ff-open-sponsor]').first();
    await expect(sponsorCta).toBeVisible();
    await sponsorCta.click();

    const sponsorModal = page.locator('[data-ff-sponsor-modal]');
    await expect(sponsorModal).toBeVisible();
    await expect(sponsorModal).toHaveAttribute('data-open', /true/);

    await page.keyboard.press('Escape');
    await expect(sponsorModal).toBeHidden({ timeout: 5000 });
  });

  test('faq disclosure expands safely', async ({ page }) => {
    await openFundraiser(page);

    const faqHeading = page.getByRole('heading', { name: /questions before you support\?/i });
    await expect(faqHeading).toBeVisible();

    const firstDisclosure = page.locator('#faq details').first();
    await expect(firstDisclosure).toBeVisible();

    await firstDisclosure.locator('summary').click();
    await expect(firstDisclosure).toHaveAttribute('open', '');

    // Toggle closed again
    await firstDisclosure.locator('summary').click();
    await expect(firstDisclosure).not.toHaveAttribute('open', '');
  });

  test('footer trust area and key links exist', async ({ page }) => {
    await openFundraiser(page);

    await expect(
      page.getByRole('heading', { name: /support this fundraiser with confidence\./i })
    ).toBeVisible();

    await expect(page.getByRole('link', { name: /terms/i })).toBeVisible();
    await expect(page.getByRole('link', { name: /privacy/i })).toBeVisible();
  });
});
