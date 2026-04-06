import { defineConfig, devices } from '@playwright/test';
import os from 'node:os';

const PORT = process.env.PORT ?? '5000';
const BASE_URL = process.env.FF_BASE_URL ?? `http://127.0.0.1:${PORT}`;
const IS_CI = !!process.env.CI;

const DEFAULT_LOCAL_WORKERS = Math.min(
  2,
  Math.max(1, Math.floor(os.availableParallelism() / 2))
);

const WORKERS = Number(
  process.env.PW_WORKERS ?? (IS_CI ? 4 : DEFAULT_LOCAL_WORKERS)
);

const HEADLESS = process.env.PW_HEADED === '1' ? false : true;
const REPORT_DIR = process.env.PW_REPORT_DIR ?? 'playwright-report';
const OUTPUT_DIR = process.env.PW_OUTPUT_DIR ?? 'test-results/playwright';

export default defineConfig({
  testDir: './tests',
  outputDir: OUTPUT_DIR,

  fullyParallel: false,
  workers: WORKERS,
  retries: IS_CI ? 2 : 0,
  forbidOnly: IS_CI,
  maxFailures: IS_CI ? 10 : undefined,

  timeout: 45000,
  expect: {
    timeout: 8000,
  },

  reporter: [
    ['list'],
    ['html', { open: 'never', outputFolder: REPORT_DIR }],
  ],

  use: {
    baseURL: BASE_URL,
    headless: HEADLESS,

    trace: IS_CI ? 'retain-on-failure' : 'on-first-retry',
    video: 'retain-on-failure',
    screenshot: 'only-on-failure',

    actionTimeout: 12000,
    navigationTimeout: 20000,
    ignoreHTTPSErrors: true,

    viewport: { width: 1440, height: 1200 },
  },

  projects: [
    {
      name: 'chromium-desktop',
      use: {
        ...devices['Desktop Chrome'],
        browserName: 'chromium',
        viewport: { width: 1440, height: 1200 },
      },
    },
    {
      name: 'mobile-chrome',
      use: {
        ...devices['Pixel 7'],
        browserName: 'chromium',
      },
    },
  ],

  webServer: process.env.PW_REUSE_SERVER
    ? undefined
    : {
        command:
          'PYTHONPATH=../..:../../apps/web ../../.venv/bin/flask --app wsgi:app run --debug --host 127.0.0.1 --port 5000',
        url: BASE_URL,
        reuseExistingServer: true,
        timeout: 120000,
      },
});
