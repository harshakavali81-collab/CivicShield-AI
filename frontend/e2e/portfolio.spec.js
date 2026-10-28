import { test, expect } from '@playwright/test';

test('dashboard presents its research scope and browser can explore the case study', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Situation overview' })).toBeVisible();
  await expect(page.getByText('NOT LIVE', { exact: true })).toBeVisible();

  await page.getByRole('navigation', { name: 'Application pages' })
    .getByRole('button', { name: 'Scenario lab' }).click();
  await expect(page.getByRole('heading', { name: 'Scenario lab' })).toBeVisible();
  await expect(page.getByText('Fictional portfolio exercise.')).toBeVisible();
  await expect(page.getByText('Invented rainfall total')).toBeVisible();
  await expect(page.getByRole('img', { name: /Invented hourly rainfall/ })).toBeVisible();

  await page.getByRole('button', { name: /3\. Separate reported events/ }).click();
  await expect(page.getByText(/Fictional submitted report counts illustrate/)).toBeVisible();
  await expect(page.getByText(/Human review is required/)).toBeVisible();
});

test('risk explorer visibly refuses stale input and never calls it an official warning', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('navigation', { name: 'Application pages' })
    .getByRole('button', { name: 'Risk explorer' }).click();
  await page.getByLabel('Input age (hours)').fill('7');
  await page.getByRole('button', { name: /Evaluate demo input/ }).click();
  await expect(page.getByText('STALE / unavailable')).toBeVisible();
  await expect(page.getByText(/EXPERIMENTAL ONLY/)).toBeVisible();
});

test('official source status remains disconnected in unconfigured demo', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('navigation', { name: 'Application pages' })
    .getByRole('button', { name: 'Official sources' }).click();
  await expect(page.getByRole('heading', { name: 'Official source connections' })).toBeVisible();
  await expect(page.getByText('IMD API connection: Not enabled / unknown')).toBeVisible();
  await expect(page.getByText('CWC status: Not connected.')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Request bulletin' })).toBeDisabled();
});

test('mobile navigation is keyboard-dismissable and focus moves into main content', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  const opener = page.getByRole('button', { name: 'Open menu' });
  await expect(opener).toHaveAttribute('aria-expanded', 'false');
  await opener.click();
  await expect(opener).toHaveAttribute('aria-expanded', 'true');
  await page.keyboard.press('Escape');
  await expect(opener).toHaveAttribute('aria-expanded', 'false');

  await opener.click();
  await page.getByRole('navigation', { name: 'Application pages' })
    .getByRole('button', { name: 'Scenario lab' }).click();
  await expect(opener).toHaveAttribute('aria-expanded', 'false');
  await expect(page.locator('#main-content')).toBeFocused();
  await expect(page.getByRole('heading', { name: 'Scenario lab' })).toBeVisible();
});

test('skip link is keyboard-accessible', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Tab');
  const skip = page.getByRole('link', { name: 'Skip to main content' });
  await expect(skip).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.locator('#main-content')).toBeFocused();
});
