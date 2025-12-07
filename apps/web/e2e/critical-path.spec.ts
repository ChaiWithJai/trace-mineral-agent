import { test, expect } from "@playwright/test";

/**
 * Critical Path E2E Tests for TraceMineralDiscoveryAgent
 *
 * These tests verify the core user journeys:
 * 1. Home page loads with research interface
 * 2. Quick query selection works
 * 3. Manual query submission works
 * 4. Response is displayed with markdown rendering
 * 5. Navigation to History and Settings works
 */

test.describe("TraceMineralDiscoveryAgent Critical Path", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("home page loads with correct title and header", async ({ page }) => {
    // Check page title
    await expect(page).toHaveTitle(/TraceMineralDiscoveryAgent/);

    // Check header is present
    const header = page.locator("header");
    await expect(header).toBeVisible();
    await expect(header).toContainText("TraceMineralDiscoveryAgent");

    // Check navigation links
    await expect(page.getByRole("link", { name: /history/i })).toBeVisible();
    await expect(page.getByRole("link", { name: /settings/i })).toBeVisible();
  });

  test("displays welcome message and quick queries", async ({ page }) => {
    // Check welcome heading
    await expect(
      page.getByRole("heading", { name: /TraceMineralDiscoveryAgent/i })
    ).toBeVisible();

    // Check description
    await expect(
      page.getByText(/Multi-paradigm research for trace mineral therapeutics/i)
    ).toBeVisible();

    // Check quick query buttons are present
    await expect(page.getByText(/Try one of these queries/i)).toBeVisible();

    // Verify at least one quick query button exists
    const quickQueryButtons = page.locator("button").filter({
      hasText: /chromium|zinc|selenium|magnesium/i,
    });
    await expect(quickQueryButtons.first()).toBeVisible();
  });

  test("chat input is functional", async ({ page }) => {
    // Find the input field
    const input = page.getByPlaceholder(/Ask about trace minerals/i);
    await expect(input).toBeVisible();
    await expect(input).toBeEnabled();

    // Find the submit button
    const submitButton = page.locator('button[type="submit"]');
    await expect(submitButton).toBeVisible();

    // Type in the input
    await input.fill("What is zinc?");
    await expect(input).toHaveValue("What is zinc?");

    // Submit button should be enabled when there's text
    await expect(submitButton).toBeEnabled();
  });

  test("can navigate to History page", async ({ page }) => {
    // Click History link
    await page.getByRole("link", { name: /history/i }).click();

    // Verify URL changed
    await expect(page).toHaveURL(/.*\/history/);

    // Check History page content
    await expect(
      page.getByRole("heading", { name: /Research History/i })
    ).toBeVisible();

    // Check empty state message
    await expect(page.getByText(/No research history yet/i)).toBeVisible();
  });

  test("can navigate to Settings page", async ({ page }) => {
    // Click Settings link
    await page.getByRole("link", { name: /settings/i }).click();

    // Verify URL changed
    await expect(page).toHaveURL(/.*\/settings/);

    // Check Settings page content
    await expect(
      page.getByRole("heading", { name: /Settings/i })
    ).toBeVisible();

    // Check API Configuration section
    await expect(page.getByText(/API Configuration/i)).toBeVisible();
    await expect(page.getByText(/LangGraph API URL/i)).toBeVisible();

    // Check About section
    await expect(page.getByText(/About/i)).toBeVisible();
    await expect(page.getByText(/Version:/i)).toBeVisible();
  });

  test("can navigate back to home from History", async ({ page }) => {
    // Go to History
    await page.getByRole("link", { name: /history/i }).click();
    await expect(page).toHaveURL(/.*\/history/);

    // Click logo/title to go back
    await page
      .getByRole("link", { name: /TraceMineralDiscoveryAgent/i })
      .click();

    // Should be back on home
    await expect(page).toHaveURL("/");
  });

  test("settings page has save button", async ({ page }) => {
    await page.goto("/settings");

    // Find save button
    const saveButton = page.getByRole("button", { name: /Save Settings/i });
    await expect(saveButton).toBeVisible();
    await expect(saveButton).toBeEnabled();
  });
});

test.describe("Research Query Flow", () => {
  test("quick query button triggers research", async ({ page }) => {
    await page.goto("/");

    // Click a quick query button
    const quickQuery = page
      .locator("button")
      .filter({ hasText: /chromium.*insulin/i })
      .first();

    // If quick query exists, click it
    if (await quickQuery.isVisible()) {
      await quickQuery.click();

      // Should show loading state
      await expect(
        page.getByText(/Processing|Creating|Submitting|Researching/i)
      ).toBeVisible({ timeout: 5000 });

      // User message should appear
      await expect(page.getByText(/chromium/i).first()).toBeVisible({
        timeout: 10000,
      });
    }
  });

  test("manual query submission shows user message", async ({ page }) => {
    await page.goto("/");

    const input = page.getByPlaceholder(/Ask about trace minerals/i);
    const submitButton = page.locator('button[type="submit"]');

    // Submit a query
    await input.fill("List trace minerals briefly");
    await submitButton.click();

    // Input should be cleared after submission
    await expect(input).toHaveValue("");

    // User message should appear in chat
    await expect(page.getByText(/List trace minerals briefly/i)).toBeVisible({
      timeout: 5000,
    });

    // Loading indicator should appear
    await expect(
      page.getByText(/Processing|Creating|Submitting|Researching/i)
    ).toBeVisible({ timeout: 5000 });
  });
});

test.describe("Responsive Design", () => {
  test("mobile viewport shows header", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto("/");

    // Header should still be visible
    const header = page.locator("header");
    await expect(header).toBeVisible();
  });

  test("tablet viewport shows full interface", async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto("/");

    // All main elements should be visible
    await expect(page.locator("header")).toBeVisible();
    await expect(
      page.getByPlaceholder(/Ask about trace minerals/i)
    ).toBeVisible();
  });
});

test.describe("Error Handling", () => {
  test("empty input does not submit", async ({ page }) => {
    await page.goto("/");

    const input = page.getByPlaceholder(/Ask about trace minerals/i);
    const submitButton = page.locator('button[type="submit"]');

    // Clear input and try to submit
    await input.fill("");

    // Button should be disabled with empty input
    await expect(submitButton).toBeDisabled();
  });

  test("whitespace-only input does not submit", async ({ page }) => {
    await page.goto("/");

    const input = page.getByPlaceholder(/Ask about trace minerals/i);
    const submitButton = page.locator('button[type="submit"]');

    // Fill with whitespace
    await input.fill("   ");

    // Button should be disabled
    await expect(submitButton).toBeDisabled();
  });
});
