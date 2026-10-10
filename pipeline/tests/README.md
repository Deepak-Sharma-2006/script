# Automated Test Suites (`tests/`)

This directory contains white-box unit tests, adversarial integration suites, engine verification tests, and multi-agent orchestrator unit tests.

## Subdirectories
- `adversarial/`: Independent black-box adversarial tests authored strictly by Lead 2 (`[Adversarial SDET]`).

## Test Runners
- Node.js Built-in Test Runner:
  ```bash
  npm run test:unit
  ```
- Adversarial Contract Suite:
  ```bash
  npm run test:adversarial
  ```
- Python Engine & Orchestrator Tests:
  ```bash
  pytest tests/
  ```
