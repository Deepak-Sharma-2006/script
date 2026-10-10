import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./pipeline/browser_tests",
  timeout: 60000,
  expect: {
    timeout: 10000
  },
  fullyParallel: false,
  workers: 1,
  reporter: [["list"], ["json", { outputFile: "test-results/playwright-results.json" }]],
  use: {
    baseURL: "http://localhost:5173",
    trace: "on-first-retry",
    headless: true,
    viewport: { width: 1440, height: 900 }
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] }
    }
  ]
});
