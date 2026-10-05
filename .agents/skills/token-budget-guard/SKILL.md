---
name: token-budget-guard
description: >-
  Monitors, tracks, and enforces strict token economy and time budgets for agent loops.
  Use this skill to track session token consumption, calculate cost metrics, and enforce hard brakes
  when approaching phase limits.
---

# Token Economy & Cost Limiter

This skill enforces financial and execution safety across all autonomous loops, preventing runaway token consumption and excessive operational costs.

## Budget Thresholds

- **Phase Token Ceiling**: 250,000 tokens (approx. 0.75–1.50).
- **Warning Threshold**: 200,000 tokens (triggers context compaction).
- **Loop Iteration Brake**: Max 5 iterations per auto-correction loop.
- **Execution Timeout**: 300 seconds (5 minutes) per autonomous task.

## Directives

1. Inspect `.agents/state/metrics/phase-<X>-tokens.json` before initiating multi-step workflows.
2. Utilize slice-bounded file reading (`view_file` with `StartLine`/`EndLine`) to conserve tokens.
3. If an agentic loop reaches 5 failed attempts without achieving exit code `0`, abort immediately and log failure diagnostics.
