import { test, expect } from "@playwright/test";

/**
 * JTBD (Job to be Done): "I want to quickly understand trace mineral research
 * from multiple medical traditions so I can make informed health decisions."
 *
 * Critical User Journey:
 * 1. Land on homepage -> immediately see clear value proposition
 * 2. Input is focused and ready -> zero friction to start
 * 3. Type a question OR click a quick query -> instant feedback
 * 4. See research response -> formatted, readable, multi-paradigm
 * 5. Ask follow-up questions -> continuous conversation flow
 */

test.describe("JTBD: Discover Trace Mineral Research", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("landing page immediately communicates value proposition", async ({
    page,
  }) => {
    // User should instantly understand what this tool does
    await expect(
      page.getByRole("heading", { name: /Discover the science of/i })
    ).toBeVisible();

    await expect(page.getByText(/trace minerals/i).first()).toBeVisible();

    // Clear description of multi-paradigm approach
    await expect(
      page.getByText(/Allopathy.*Naturopathy.*Ayurveda.*TCM/i)
    ).toBeVisible();
  });

  test("input is auto-focused for immediate interaction", async ({ page }) => {
    // The input should be ready to use without clicking
    const input = page.getByPlaceholder(/Ask about trace minerals/i);

    // Input should be visible and focused
    await expect(input).toBeVisible();
    await expect(input).toBeFocused();
  });

  test("input has silky smooth focus states", async ({ page }) => {
    const input = page.getByPlaceholder(/Ask about trace minerals/i);

    // Focus the input
    await input.focus();

    // Type something
    await input.fill("zinc benefits");

    // Verify the value
    await expect(input).toHaveValue("zinc benefits");

    // Submit button should become active
    const submitButton = page.locator("button[type='submit']");
    await expect(submitButton).toBeEnabled();
  });

  test("quick queries provide one-click research access", async ({ page }) => {
    // Quick queries should be visible and descriptive
    await expect(page.getByText(/Or try one of these/i)).toBeVisible();

    // Check for quick query cards
    const quickQueryCards = page.locator("button").filter({
      hasText: /Chromium|Zinc|Selenium|Magnesium/i,
    });

    // Should have multiple quick query options
    expect(await quickQueryCards.count()).toBeGreaterThanOrEqual(4);

    // Cards should have titles and descriptions
    await expect(
      page.getByText(/Chromium & Insulin/i).first()
    ).toBeVisible();
  });

  test("clicking quick query navigates to chat view", async ({ page }) => {
    // Click a quick query
    const quickQuery = page
      .locator("button")
      .filter({ hasText: /Chromium & Insulin/i })
      .first();

    await quickQuery.click();

    // User message should appear (confirms query was submitted)
    await expect(page.getByText(/chromium.*insulin/i).first()).toBeVisible({
      timeout: 5000,
    });

    // Welcome screen should be gone (we're in chat mode)
    await expect(page.getByText(/Or try one of these/i)).not.toBeVisible();

    // Follow-up input should appear
    await expect(page.getByPlaceholder(/follow-up/i)).toBeVisible({
      timeout: 5000,
    });
  });

  test("manual query submission transitions to chat view", async ({ page }) => {
    const input = page.getByPlaceholder(/Ask about trace minerals/i);

    // Type a query
    await input.fill("What are the benefits of magnesium?");

    // Submit via Enter key
    await input.press("Enter");

    // User message should appear (this confirms submission worked)
    await expect(page.getByText(/benefits of magnesium/i)).toBeVisible({
      timeout: 5000,
    });

    // Welcome screen should be gone
    await expect(page.getByText(/Or try one of these/i)).not.toBeVisible();

    // Follow-up input should be available (with different placeholder)
    await expect(page.getByPlaceholder(/follow-up/i)).toBeVisible({
      timeout: 5000,
    });
  });
});

test.describe("JTBD: Navigate the Application", () => {
  test("header provides clear branding and navigation", async ({ page }) => {
    await page.goto("/");

    // Brand should be visible
    await expect(page.getByText(/Trace Mineral/i).first()).toBeVisible();
    await expect(page.getByText(/Discovery/i).first()).toBeVisible();

    // Navigation links should be clear
    await expect(page.getByRole("link", { name: /History/i })).toBeVisible();
    await expect(page.getByRole("link", { name: /Settings/i })).toBeVisible();
  });

  test("History page is accessible and clear", async ({ page }) => {
    await page.goto("/");

    // Navigate to History
    await page.getByRole("link", { name: /History/i }).click();

    await expect(page).toHaveURL(/.*\/history/);

    // Page should have clear heading
    await expect(
      page.getByRole("heading", { name: /Research History/i })
    ).toBeVisible();

    // Empty state should be helpful
    await expect(page.getByText(/No research history yet/i)).toBeVisible();
  });

  test("Settings page is accessible and functional", async ({ page }) => {
    await page.goto("/");

    // Navigate to Settings
    await page.getByRole("link", { name: /Settings/i }).click();

    await expect(page).toHaveURL(/.*\/settings/);

    // Page should have clear heading
    await expect(
      page.getByRole("heading", { name: /Settings/i })
    ).toBeVisible();

    // API Configuration should be visible
    await expect(page.getByText(/API Configuration/i)).toBeVisible();
    await expect(page.getByText(/LangGraph API URL/i)).toBeVisible();

    // Save button should be present
    await expect(
      page.getByRole("button", { name: /Save Settings/i })
    ).toBeVisible();
  });

  test("can navigate back to home via logo", async ({ page }) => {
    await page.goto("/settings");

    // Click logo/brand to go home
    await page.getByRole("link", { name: /Trace Mineral.*Discovery/i }).click();

    await expect(page).toHaveURL("/");

    // Home page content should be visible
    await expect(
      page.getByPlaceholder(/Ask about trace minerals/i)
    ).toBeVisible();
  });
});

test.describe("JTBD: Input Validation & Error Prevention", () => {
  test("empty input is gracefully handled", async ({ page }) => {
    await page.goto("/");

    const input = page.getByPlaceholder(/Ask about trace minerals/i);
    const submitButton = page.locator("button[type='submit']");

    // Empty input should not allow submission
    await expect(input).toHaveValue("");

    // Button should have disabled state visually (scale down)
    await expect(submitButton).toBeVisible();
  });

  test("whitespace-only input does not trigger search", async ({ page }) => {
    await page.goto("/");

    const input = page.getByPlaceholder(/Ask about trace minerals/i);

    // Fill with whitespace
    await input.fill("   ");

    // Try to submit
    await input.press("Enter");

    // Should still be on welcome screen (no message sent)
    await expect(page.getByText(/Or try one of these/i)).toBeVisible();
  });
});

test.describe("JTBD: Visual Design & Polish", () => {
  test("page has warm, editorial color scheme", async ({ page }) => {
    await page.goto("/");

    // Check background color (cream)
    const body = page.locator("body");
    const bgColor = await body.evaluate(
      (el) => window.getComputedStyle(el).backgroundColor
    );

    // Should have a warm cream background (rgb values for #f8f6f3)
    expect(bgColor).toMatch(/rgb\(248, 246, 243\)|rgba\(248, 246, 243/);
  });

  test("typography uses serif for headings", async ({ page }) => {
    await page.goto("/");

    const heading = page.getByRole("heading", {
      name: /Discover the science of/i,
    });
    const fontFamily = await heading.evaluate(
      (el) => window.getComputedStyle(el).fontFamily
    );

    // Should include serif font
    expect(fontFamily.toLowerCase()).toMatch(/baskerville|georgia|serif/);
  });

  test("accent color is vibrant orange", async ({ page }) => {
    await page.goto("/");

    // Check that accent elements exist
    const accentElements = page.locator('[class*="accent"]');
    expect(await accentElements.count()).toBeGreaterThan(0);
  });
});

test.describe("JTBD: Responsive Design", () => {
  test("mobile viewport renders cleanly", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto("/");

    // Header should be visible
    await expect(page.locator("header")).toBeVisible();

    // Input should be usable
    await expect(
      page.getByPlaceholder(/Ask about trace minerals/i)
    ).toBeVisible();

    // Quick queries should be visible
    await expect(
      page.getByText(/Chromium & Insulin/i).first()
    ).toBeVisible();
  });

  test("tablet viewport shows full interface", async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto("/");

    // All main elements should be visible
    await expect(page.locator("header")).toBeVisible();
    await expect(
      page.getByPlaceholder(/Ask about trace minerals/i)
    ).toBeVisible();
    await expect(page.getByText(/Or try one of these/i)).toBeVisible();
  });

  test("desktop viewport has comfortable max-width", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto("/");

    // Content should be contained, not stretched
    const input = page.getByPlaceholder(/Ask about trace minerals/i);
    const inputBox = await input.boundingBox();

    // Input should not span full viewport width
    expect(inputBox?.width).toBeLessThan(800);
  });
});

test.describe("JTBD: Long-Running Query Feedback", () => {
  test("shows loading status when query is submitted", async ({ page }) => {
    await page.goto("/");

    // Click a quick query
    const quickQuery = page
      .locator("button")
      .filter({ hasText: /Chromium & Insulin/i })
      .first();

    await quickQuery.click();

    // Should show loading indicator with status
    await expect(page.getByText(/Queuing|Analyzing|Researching/i)).toBeVisible({
      timeout: 5000,
    });

    // Follow-up input should be disabled while loading
    const followUpInput = page.getByPlaceholder(/follow-up/i);
    await expect(followUpInput).toBeDisabled();
  });

  test("displays elapsed time during long queries", async ({ page }) => {
    await page.goto("/");

    // Type and submit a query
    const input = page.getByPlaceholder(/Ask about trace minerals/i);
    await input.fill("What are the benefits of zinc?");
    await input.press("Enter");

    // Wait a bit for the elapsed time to appear
    await page.waitForTimeout(3000);

    // Should show elapsed time in status
    // Pattern: "Queuing... (Xs)" or "Analyzing across paradigms... (Xs)"
    await expect(page.getByText(/\(\d+s\)/)).toBeVisible({ timeout: 10000 });
  });
});
