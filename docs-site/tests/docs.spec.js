const {test, expect} = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const productDocs = require('../product-docs.json');

test('desktop documentation surface matches the shared contract', async ({page}) => {
  await page.goto('developer/documentation-system?docusaurus-theme=light');
  await expect(page.locator('h1')).toHaveText('Documentation system contract');
  await expect(page.locator('.navbar__link')).toHaveText([
    'Home',
    'Overview',
    'Guides',
    'Reference',
    'Developer',
    'Packages',
    'GitHub',
  ]);
  await expect(page.locator('a', {hasText: 'Edit this page'})).toHaveAttribute(
    'href',
    `${productDocs.sourceRepoUrl}/edit/main/docs/Developer/Documentation-System.md`
  );
  const geometry = await page.locator('.theme-doc-markdown').evaluate((element) => ({
    width: element.getBoundingClientRect().width,
    font: getComputedStyle(element).fontFamily,
    size: getComputedStyle(element).fontSize,
    navbar: document.querySelector('.navbar').getBoundingClientRect().height,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  }));
  expect(geometry.width).toBeLessThanOrEqual(680);
  expect(geometry.font).toContain('IBM Plex Sans');
  expect(geometry.size).toBe('17px');
  expect(geometry.navbar).toBe(56);
  expect(geometry.overflow).toBe(0);
  const accessibility = await new AxeBuilder({page}).withTags(['wcag2a', 'wcag2aa']).analyze();
  expect(accessibility.violations).toEqual([]);
});

test('search and mobile behavior remain functional', async ({page}) => {
  await page.goto('?docusaurus-theme=light');
  await page.locator('input[aria-label="Search"]').fill('Documentation system');
  await expect(page.locator('[role="listbox"]')).toBeVisible();
  await expect(page.locator('[role="listbox"]')).toContainText('Documentation system contract');

  await page.setViewportSize({width: 390, height: 844});
  await page.goto('developer/documentation-system?docusaurus-theme=dark');
  await expect(page.locator('.navbar__toggle')).toBeVisible();
  await expect(page.locator('.theme-doc-sidebar-container')).toBeHidden();
  const mobile = await page.evaluate(() => ({
    theme: document.documentElement.dataset.theme,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  }));
  expect(mobile.theme).toBe('dark');
  expect(mobile.overflow).toBe(0);
});
