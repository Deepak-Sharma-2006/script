# Independent Adversarial Test Suite (`tests/adversarial/`)

This directory contains independent black-box adversarial test suites strictly owned and authored by the Adversarial SDET persona (`[Adversarial SDET]`) and Lead 2.

## Principles & Invariants
- Lead 1 (Alpha) is strictly prohibited from writing or tampering with files in this directory.
- Probes concurrency race conditions, malicious payloads, boundary value fuzzing, state corruption, and timing attack resistance.
- All token comparisons must enforce `crypto.timingSafeEqual`.
