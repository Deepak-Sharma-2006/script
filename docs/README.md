# Enterprise Governance & Living Documentation (`docs/`)

This directory houses all version-controlled architectural specifications, decision records, research triangulations, implementation plans, execution walkthroughs, and security audits across the platform.

## Architecture & Subdirectories
- `architecture/`: Master system blueprints and production reference architecture.
- `audits/`: Adversarial red-team audits, SAST/DAST reports, and system readiness certifications.
- `decisions/`: Architectural Decision Records (ADRs) capturing fundamental technical trade-offs.
- `dossiers/`: Part 7 human code comprehension dossiers created at phase handoffs.
- `plans/`: Feature implementation plans generated during solution formulation and task execution.
- `research/`: Multi-hop deep research dossiers on regulations, APIs, and competitor baselines.
- `specifications/`: Formal RFCs, typed schema specifications, and state machine models.
- `walkthroughs/`: Step-by-step verification walkthroughs and empirical proof logs.

## In-Repo Synchronization
Documentation is continuously synchronized and mirrored in real time using `SpecSync` (`npm run docs:sync`) and reconciled using `npm run docs:reconcile`.
