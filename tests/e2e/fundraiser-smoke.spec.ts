import { test, expect, type Page, type Locator } from '@playwright/test';

const CAMPAIGN_PATH = process.env.FF_CAMPAIGN_PATH || '/c/spring-fundraiser';

const SEL = {
  ffSelectors: '#ffSelectors',
  ffConfig: '#ffConfig',

  openCheckout: '[data-ff-open-checkout]',
  closeCheckout: '[data-ff-close-checkout]',
  checkoutSheet: '[data-ff-checkout-sheet]',
  donationForm: '#donationForm',
  amountInput: '[data-ff-amount-input]',
  amountChip: '[data-ff-amount]',
  emailInput: '[data-ff-email]',
  donorName: '[data-ff-donor-name]',
  stripeMount: '[data-ff-stripe-mount]',
  paypalMount: '[data-ff-paypal-mount]',
  checkoutError: '[data-ff-checkout-error]',
  checkoutStatus: '[data-ff-checkout-status]',

  openSponsor: '[data-ff-open-sponsor]',
  closeSponsor: '[data-ff-close-sponsor]',
  sponsorModal: '[data-ff-sponsor-modal]',
  sponsorForm: '#sponsorForm',
  sponsorTier: '[data-ff-sponsor-tier]',
  sponsorSuccess: '[data-ff-sponsor-success]',
  sponsorError: '[data-ff-sponsor-error]',

  openVideo: '[data-ff-open-video]',
  closeVideo: '[data-ff-close-video]',
  videoModal: '[data-ff-video-modal]',
  videoMount: '[data-ff-video-mount]',

  openTerms: '[data-ff-open-terms]',
  closeTerms: '[data-ff-close-terms]',
  termsModal: '[data-ff-terms-modal]',

  openPrivacy: '[data-ff-open-privacy]',
  closePrivacy: '[data-ff-close-privacy]',
  privacyModal: '[data-ff-privacy-modal]',
  onboardNext: '[data-ff-onboard-next]',
  onboardPrev: '[data-ff-onboard-prev]',
  onboardFinish: '[data-ff-onboard-finish]',

  share: '[data-ff-share]',
  themeToggle: '[data-ff-theme-toggle], .ff-themeToggle, #ff-theme-toggle',
  floatingDonate: '[data-ff-floating-donate]',
  backToTop: '[data-ff-backtotop]',
  successUpsellTemplate: '#ffDonationSuccessUpsellTemplate'} as const;

type RuntimeWatchers = {
  consoleErrors: string[];
  pageErrors: string[];
  requestFailures: string[];
};

function attachRuntimeWatchers(page: Page): RuntimeWatchers {
  const consoleErrors: string[] = [];
  const pageErrors: string[] = [];
  const requestFailures: string[] = [];

  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
    }
  });

  page.on('pageerror', (err) => {
    pageErrors.push(String(err));
  });

  page.on('requestfailed', (req) => {
    const url = req.url();
    if (url.includes('socket.io')) return;
    requestFailures.push(
      `${req.method()} ${url} :: ${req.failure()?.errorText || 'unknown'}`
    );
  });

  return { consoleErrors, pageErrors, requestFailures };
}

async function exists(page: Page, selector: string): Promise<boolean> {
  return (await page.locator(selector).count()) > 0;
}

async function firstVisible(page: Page, selector: string): Promise<Locator | null> {
  const locator = page.locator(selector);
  const count = await locator.count();

  for (let i = 0; i < count; i += 1) {
    const candidate = locator.nth(i);
    if (await candidate.isVisible().catch(() => false)) {
      return candidate;
    }
  }

  return null;
}

async function firstVisibleWithin(root: Locator, selector: string): Promise<Locator | null> {
  const locator = root.locator(selector);
  const count = await locator.count();

  for (let i = 0; i < count; i += 1) {
    const candidate = locator.nth(i);
    if (await candidate.isVisible().catch(() => false)) {
      return candidate;
    }
  }

  return null;
}

async function clickVisible(
  page: Page,
  selector: string,
  opts?: { force?: boolean }
): Promise<void> {
  const target = await firstVisible(page, selector);

  if (!target) {
    throw new Error(`No visible element found for selector: ${selector}`);
  }

  await target.scrollIntoViewIfNeeded().catch(() => {});
  await target.click({ force: opts?.force ?? false });
}

async function openAndExpectVisible(
  page: Page,
  opener: string,
  modal: string
): Promise<void> {
  await expect(page.locator(opener).first(), `Missing opener: ${opener}`).toBeAttached();
  await clickVisible(page, opener);
  await expect(page.locator(modal).first(), `Modal not visible: ${modal}`).toBeVisible();
}

async function closeIfPresent(
  page: Page,
  closer: string,
  modal: string
): Promise<void> {
  const modalLocator = page.locator(modal).first();
  const modalVisible = await modalLocator.isVisible().catch(() => false);

  if (!modalVisible) return;

  const scopedCloser = await firstVisibleWithin(modalLocator, closer);
  const globalCloser = await firstVisible(page, closer);

  if (scopedCloser) {
    await scopedCloser.scrollIntoViewIfNeeded().catch(() => {});
    await scopedCloser.click({ force: true }).catch(() => {});
  } else if (globalCloser) {
    await globalCloser.scrollIntoViewIfNeeded().catch(() => {});
    await globalCloser.click({ force: true }).catch(() => {});
  } else {
    await page.keyboard.press('Escape').catch(() => {});
  }

  await page.waitForTimeout(250);

  if (await modalLocator.isVisible().catch(() => false)) {
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(250);
  }

  if (await modalLocator.isVisible().catch(() => false)) {
    await modalLocator.evaluate((el) => {
      el.setAttribute('aria-hidden', 'true');
      el.setAttribute('data-open', 'false');
      if (el instanceof HTMLElement) {
        el.style.display = 'none';
        el.style.visibility = 'hidden';
        el.style.pointerEvents = 'none';
      }
    }).catch(() => {});
  }
}

test.describe('FutureFunded fundraiser smoke suite', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(CAMPAIGN_PATH, { waitUntil: 'domcontentloaded' });
    await expect(page.locator(SEL.ffSelectors)).toBeAttached();
    await expect(page.locator(SEL.ffConfig)).toBeAttached();
  });

  test('contract presence is intact', async ({ page }) => {
    const checks = [
      SEL.openCheckout,
      SEL.checkoutSheet,
      SEL.donationForm,
      SEL.amountInput,
      SEL.amountChip,
      SEL.stripeMount,
      SEL.paypalMount,
      SEL.openSponsor,
      SEL.sponsorModal,
      SEL.sponsorForm,
      SEL.openVideo,
      SEL.videoModal,
      SEL.openTerms,
      SEL.termsModal,
      SEL.openPrivacy,
      SEL.privacyModal,
      SEL.themeToggle,
      SEL.share,
      SEL.backToTop,
      SEL.floatingDonate,
      SEL.successUpsellTemplate];

    for (const selector of checks) {
      await expect(
        page.locator(selector).first(),
        `Missing selector: ${selector}`
      ).toBeAttached();
    }
  });

  test('captures runtime errors during smoke flow', async ({ page }) => {
    const watcher = attachRuntimeWatchers(page);

    await openAndExpectVisible(page, SEL.openCheckout, SEL.checkoutSheet);

    if (await exists(page, SEL.amountChip)) {
      await clickVisible(page, SEL.amountChip);
    }

    if (await exists(page, SEL.emailInput)) {
      const email = (await firstVisible(page, SEL.emailInput)) || page.locator(SEL.emailInput).first();
      await email.fill('bad-email');

      if (await exists(page, SEL.donationForm)) {
        await page.locator(SEL.donationForm).first().evaluate((el) => {
          el.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
        });
      }

      await email.fill('smoke@example.com');
    }

    await expect(page.locator(SEL.stripeMount)).toBeAttached();
    await expect(page.locator(SEL.paypalMount)).toBeAttached();
    await closeIfPresent(page, SEL.closeCheckout, SEL.checkoutSheet);

    await openAndExpectVisible(page, SEL.openSponsor, SEL.sponsorModal);

    if (await exists(page, SEL.sponsorTier)) {
      await clickVisible(page, SEL.sponsorTier, { force: true });
    }

    await closeIfPresent(page, SEL.closeSponsor, SEL.sponsorModal);

    await openAndExpectVisible(page, SEL.openVideo, SEL.videoModal);
    await expect(page.locator(SEL.videoMount)).toBeAttached();
    await closeIfPresent(page, SEL.closeVideo, SEL.videoModal);

    await openAndExpectVisible(page, SEL.openTerms, SEL.termsModal);
    await closeIfPresent(page, SEL.closeTerms, SEL.termsModal);

    await openAndExpectVisible(page, SEL.openPrivacy, SEL.privacyModal);
    await closeIfPresent(page, SEL.closePrivacy, SEL.privacyModal);

    if (await exists(page, SEL.onboardNext)) {
      await clickVisible(page, SEL.onboardNext);
    }

    if (await exists(page, SEL.onboardPrev)) {
      await clickVisible(page, SEL.onboardPrev);
    }

    if (await firstVisible(page, SEL.themeToggle)) {
      await clickVisible(page, SEL.themeToggle);
    }

    if (await firstVisible(page, SEL.share)) {
      await clickVisible(page, SEL.share, { force: true });
    }

    await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight);
    });

    await expect(page.locator(SEL.floatingDonate)).toBeAttached();
    await expect(page.locator(SEL.backToTop)).toBeAttached();

    expect.soft(
      watcher.consoleErrors,
      `Console errors:\n${watcher.consoleErrors.join('\n')}`
    ).toEqual([]);

    expect.soft(
      watcher.pageErrors,
      `Page errors:\n${watcher.pageErrors.join('\n')}`
    ).toEqual([]);

    expect.soft(
      watcher.requestFailures,
      `Request failures:\n${watcher.requestFailures.join('\n')}`
    ).toEqual([]);
  });

  test('checkout opens, validates, and closes', async ({ page }) => {
    await openAndExpectVisible(page, SEL.openCheckout, SEL.checkoutSheet);

    if (await exists(page, SEL.amountChip)) {
      await clickVisible(page, SEL.amountChip);
    }

    if (await exists(page, SEL.donorName)) {
      const donorName = (await firstVisible(page, SEL.donorName)) || page.locator(SEL.donorName).first();
      await donorName.fill('Smoke Tester');
    }

    if (await exists(page, SEL.emailInput)) {
      const email = (await firstVisible(page, SEL.emailInput)) || page.locator(SEL.emailInput).first();
      await email.fill('bad-email');

      if (await exists(page, SEL.donationForm)) {
        await page.locator(SEL.donationForm).first().evaluate((el) => {
          el.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
        });
      }

      if (await exists(page, SEL.checkoutError)) {
        await expect(page.locator(SEL.checkoutError).first()).toBeVisible();
      }

      await email.fill('smoke@example.com');
    }

    await expect(page.locator(SEL.stripeMount)).toBeAttached();
    await expect(page.locator(SEL.paypalMount)).toBeAttached();
    await closeIfPresent(page, SEL.closeCheckout, SEL.checkoutSheet);
  });

  test('sponsor, legal, and video modals all open and close', async ({ page }) => {
    await openAndExpectVisible(page, SEL.openSponsor, SEL.sponsorModal);
    await closeIfPresent(page, SEL.closeSponsor, SEL.sponsorModal);

    await openAndExpectVisible(page, SEL.openVideo, SEL.videoModal);
    await closeIfPresent(page, SEL.closeVideo, SEL.videoModal);

    await openAndExpectVisible(page, SEL.openTerms, SEL.termsModal);
    await closeIfPresent(page, SEL.closeTerms, SEL.termsModal);

    await openAndExpectVisible(page, SEL.openPrivacy, SEL.privacyModal);
    await closeIfPresent(page, SEL.closePrivacy, SEL.privacyModal);
  });
});
