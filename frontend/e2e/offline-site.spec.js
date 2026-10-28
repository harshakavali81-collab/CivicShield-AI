import { test, expect } from '@playwright/test';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

// file:// deliberately exercises extraction-and-open with no HTTP server.
const url = pathToFileURL(resolve(process.cwd(), '../site/demo.html')).href;

test('fully offline case study renders canonical fictional data and working chart', async ({ page }) => {
  await page.goto(url);
  await expect(page.getByRole('heading', { name: /Explore a fictional monsoon/ })).toBeVisible();
  await expect(page.getByText(/NOT AN EMERGENCY SERVICE/)).toBeVisible();
  await expect(page.locator('#metric-hours')).toHaveText('24 h');
  await expect(page.locator('#metric-rain')).not.toHaveText('—');
  await expect(page.locator('#chart polyline')).toHaveCount(1);
  await expect(page.locator('#data-rows tr')).toHaveCount(24);

  await page.getByRole('button', { name: /2\. Reject stale inputs/ }).click();
  await expect(page.locator('#stage-title')).toHaveText('2. Reject stale inputs');
  await expect(page.locator('#selected-hour')).toHaveText('09:00');
  await expect(page.locator('#takeaway')).toContainText('unavailable');

  await page.locator('#hour-slider').focus();
  await page.keyboard.press('Home');
  await page.keyboard.press('ArrowRight');
  await expect(page.locator('#selected-hour')).toHaveText('01:00');
});

test('offline demo works at mobile size and does not request any network resources', async ({ page }) => {
  const external = [];
  page.on('request', req => {
    if (/^https?:/.test(req.url())) external.push(req.url());
  });
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto(url);
  await page.getByRole('button', { name: /4\. Evaluate errors before any real use/ }).click();
  await expect(page.locator('#stage-title')).toContainText('Evaluate errors');
  await expect(page.locator('#selected-hour')).toHaveText('23:00');
  await page.getByText('Accessible complete data table').click();
  await expect(page.locator('#data-rows tr')).toHaveCount(24);
  expect(external).toEqual([]);
});

test('offline site keyboard skip link reaches main and remains clearly fictional', async ({ page }) => {
  await page.goto(url);
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: 'Skip to case study' })).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/#main-content$/);
  await expect(page.getByText(/All figures are fabricated for a software demo/)).toHaveCount(1);
});
