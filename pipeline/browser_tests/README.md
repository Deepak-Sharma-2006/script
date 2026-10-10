# Browser & End-to-End (E2E) Test Suite

This directory contains automated headless browser tests powered by Playwright (`@playwright/test`).

## Operational Guidelines
- **Universal Playwright Invariant**: Whenever frontend components (`.html`, `.tsx`, `.jsx`, `.vue`, `.svelte`) exist or are modified, the Adversarial SDET (`[Adversarial SDET]`) executes headless browser tests.
- **Mandatory Elemental Assertions**: Tests must assert element visibility, interaction flows, console error hygiene, and component shell geometry.
- **Execution Command**: Run `npx playwright test` or `npm run test:browser`.
- **Configuration**: Governed by `playwright.config.ts` at repository root.
