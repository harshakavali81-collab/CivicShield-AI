import { test, expect } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';

// Generated ONLY against the isolated local research demo in GitHub CI.
// Screenshot outputs are short-lived artifacts, not proof of public hosting,
// operational warning accuracy, or government-source integration.
test('capture reproducible demo screenshots with visible synthetic warnings', async ({ page }) => {
  const folder = resolve(process.cwd(), 'test-results/showcase');
  await mkdir(folder, { recursive: true });
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Situation overview' })).toBeVisible();
  await expect(page.getByText('NOT LIVE', { exact: true })).toBeVisible();
  await page.screenshot({ path: resolve(folder, '01-desktop-dashboard.png'), fullPage: true });

  const navigation = page.getByRole('navigation', { name: 'Application pages' });
  await navigation.getByRole('button', { name: 'Scenario lab' }).click();
  await expect(page.getByText('Fictional portfolio exercise.')).toBeVisible();
  await expect(page.getByRole('img', { name: /Invented hourly rainfall/ })).toBeVisible();
  await page.screenshot({ path: resolve(folder, '02-fictional-scenario-lab.png'), fullPage: true });

  await navigation.getByRole('button', { name: 'Official sources' }).click();
  await expect(page.getByText('CWC status: Not connected.')).toBeVisible();
  await page.screenshot({ path: resolve(folder, '03-disconnected-official-sources.png'), fullPage: true });

  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole('button', { name: 'Open menu' }).click();
  await navigation.getByRole('button', { name: 'Overview' }).click();
  await expect(page.getByText('NOT LIVE', { exact: true })).toBeVisible();
  await page.screenshot({ path: resolve(folder, '04-mobile-dashboard.png'), fullPage: true });
});
