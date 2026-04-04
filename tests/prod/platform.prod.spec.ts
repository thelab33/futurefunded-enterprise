import { test, expect } from '@playwright/test';

test.describe('Production platform routing + sales flow', () => {
  test('root redirects to platform', async ({ page }) => {
    await page.goto('/', { waitUntil: 'domcontentloaded' });
    await expect(page).toHaveURL(/\/platform\/?$/);
  });

  test('platform home renders core launch messaging', async ({ page }) => {
    await page.goto('/platform/', { waitUntil: 'domcontentloaded' });

    await expect(
      page.getByRole('heading', { name: /what you can launch/i })
    ).toBeVisible();

    await expect(
      page.getByRole('heading', { name: /launch status/i })
    ).toBeVisible();
  });

  test('platform onboarding renders organization + campaign blocks', async ({ page }) => {
    await page.goto('/platform/onboarding', { waitUntil: 'domcontentloaded' });

    await expect(
      page.getByRole('heading', { name: /^organization$/i })
    ).toBeVisible();

    await expect(
      page.getByRole('heading', { name: /^campaign$/i })
    ).toBeVisible();

    await expect(
      page.getByRole('button', { name: /create org \+ campaign/i })
    ).toBeVisible();
  });

  test('platform dashboard renders command center + overview', async ({ page }) => {
    await page.goto('/platform/dashboard', { waitUntil: 'domcontentloaded' });

    await expect(
      page.getByRole('heading', { name: /futurefunded command center/i })
    ).toBeVisible();

    await expect(
      page.getByRole('heading', { name: /overview/i })
    ).toBeVisible();

    await expect(page.getByText(/gold sponsor/i)).toBeVisible();
    await expect(page.getByText(/booster monthly/i)).toBeVisible();
  });
});
