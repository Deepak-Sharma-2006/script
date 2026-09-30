# Enterprise Multi-Persona Orchestrator Engine

This directory contains the core Python orchestration engines that power multi-persona lifecycle execution, task dispatching, and specification synchronization across the platform.

## Subsystems & Architecture
- `task_dispatcher.py`: Universal command-line gateway (`python -m scripts.orchestrator.task_dispatcher`).
- `squad_orchestrator.py`: Implements the 6-persona enterprise squad lifecycle (PM, System Architect, Adversarial SDET, Core Engineer, Mutation Auditor, Technical Writer).
- `squad_attestation.py`: Cryptographic SquadAttestor generating verifiable SHA-256 execution receipts.
- `spec_sync.py`: Dual-syncs brain artifacts to `docs/` and appends to `.agents/memory/vault/records.jsonl`.
- `solution_council.py`: 5-advisor adversarial Claude Council consensus engine (`claude-council`).
- `research_triangulator.py`: Multi-hop research engine for statutory and competitor benchmarking.
- `realtime_docs_watcher.py`: Background daemon for zero-process documentation synchronization.
- `coding_engine.py`: Autonomous TDD red-to-green loop runner.
- `project_auditor.py`: AppSec and architecture compliance auditor.
