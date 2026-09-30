# Agent Behavioral Evaluation Harness

This directory contains the automated test harness used to evaluate agent behavior against security, anti-hallucination, and collaboration invariants.

## Key Files
- `active_kernel.py`: Active Interception Kernel & 8-Domain Pre/Post Gating (`npm run harness:active`).
- `eval-runner.ts`: Static behavioral contract validator (`npm run harness:eval`).
- `dynamic-eval-runner.ts`: Dynamic multi-turn behavioral simulation harness (`npm run harness:dynamic`).
- `golden-evals.json`: Golden benchmark dataset for anti-hallucination, lock compliance, and sycophancy resistance.
- `harness-contracts.json`: Schema definitions for evaluation scoring.
