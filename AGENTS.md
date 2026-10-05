# Antigravity Workspace Invariants & Operational Directives

> **Scope**: Applied automatically to all agent invocations (both Antigravity IDE and Antigravity CLI `agy`) across this entire workspace.

---

## 1. Zero-Hallucination & Dynamic Dependency Policy

1. **Dynamic Dependency Architecture & Zero Ghost Packages**:
   - Dependencies are dynamic and permitted if they provide a demonstrable, measurable advantage over standard library implementations (e.g., performance, robust schema parsing, standardized protocol handling).
   - Before introducing any new dependency, you MUST inspect `package.json`. If a new package is required, it must be explicitly declared in `package.json` with an exact pinned version.
   - NEVER invent, assume, or import an npm package or library that is not explicitly declared in `package.json`.
   - The Anti-Hallucination Shield (`npm run check:hallucinations`) strictly scans AST imports across the entire codebase to reject undeclared packages.
2. **Strict Symbol & File Grounding**:
   - Every citation of a file, type, function, or API must be grounded in verified project evidence.
   - You MUST cite clickable markdown links using the `file://` scheme with forward slashes: `[SymbolName](file:///path/to/file.ts#L15-L30)`.
   - If context is missing or ambiguous, you MUST state: `"INSUFFICIENT CONTEXT DETECTED: Unable to ground symbol in codebase."` DO NOT guess, fabricate, or improvise missing APIs.
3. **Empirical Execution Grounding**:
   - NEVER assert that "tests pass", "build succeeds", or "vulnerabilities are fixed" based on mental simulation.
   - You must execute the relevant shell command (`npm test`, `tsc --noEmit`, or test runner) and verify an exit code of `0`.

---

## 2. Enterprise 2-Person Dual-Lead Architecture & Domain Leases (50/50 Balance)

1. **50/50 Co-Equal Enterprise Leadership**:
   - The workspace operates as a balanced two-person engineering team, translating an entire enterprise engineering organization into two co-equal leads:
     - **Lead 1 (Alpha / Feature Architect & Core Domain Lead - 50% Workload)**: Owns domain modeling, business logic, public API contracts, white-box unit TDD (`tests/unit/`), and system architecture dossiers.
     - **Lead 2 (Beta / Adversarial Systems, SDET & Product Lead - 50% Workload)**: Owns independent black-box adversarial suites (`tests/adversarial/*.test.ts`), concurrency & race fuzzing, malicious payload injection, AppSec DAST pentesting, product/UX ergonomics certification, and production release sign-off.
2. **Independent Adversarial Test Authoring Mandate**:
   - Lead 1 (Alpha) is strictly prohibited from writing or tampering with `tests/adversarial/`. Only Lead 2 authors adversarial tests.
   - Lead 2 must probe edge cases, race conditions, memory bounds, and fault injections that Lead 1's unit tests never contemplated.
3. **Lead 2 Hardening Authority**:
   - Lead 2 is NOT a passive spectator. Upon receiving a phase handoff, Lead 2 holds the **Hardening & Verification Lease** and is fully authorized to directly author hardening patches, input sanitizers, race-condition mutexes, and performance optimizations directly in `src/`.
4. **Distributed Lease Locking & Multi-Domain Concurrency**:
   - Developers acquire exclusive domain leases via `npm run lock:acquire --domain <name>`.
   - Independent domains (e.g. `core` and `adversarial`) can be developed concurrently without collisions.
   - Phase handoffs (`npm run role:handoff`) atomically transfer domain leases, enforce zero-secret scans, and invert roles on phase advancement (N → N+1).

---

## 3. Human Operator Code Comprehension Protocol (Part 7 Mandate)

1. **Mandatory Phase Dossier Generation**:
   - At the completion of each feature phase, before opening a PR or requesting merge, the agent MUST generate a structured comprehension dossier in `docs/dossiers/phase-<X>-<domain>.md`.
2. **The 6-Technique Structure**:
   - Technique 1: The Human Mental Model (Plain-language purpose & boundary).
   - Technique 2: Visual Code Flow (ASCII / Mermaid call graph).
   - Technique 3: Variable Lifecycle Trace (Birth → Transformation → Egress).
   - Technique 4: Non-Blocking Noise Filtering (Bypassing telemetry/logging on Pass 1).
   - Technique 5: Audit Exactly One Failure Path (Account enumeration & timing differential checks).
   - Technique 6: 1-Sentence Feynman Compression Test.

---

## 4. Token Economy & Adaptive Multi-Model Optimizer

1. **Progressive Disclosure & Skill Search**:
   - Do NOT load massive raw documentation or all skills into prompt context. Search skills dynamically via `npm run skill:search` or `scripts/skill-finder.ts`. Read only relevant sections using bounded file reading (`StartLine`/`EndLine`).
2. **Slice-Targeted File Reading**:
   - Avoid reading files > 150 lines in their entirety. Use `grep_search` to locate target line numbers, then view the specific slice.
3. **Hard Loop Limits & Model Saturation**:
   - Max 5 auto-correction loops per task.
   - Respect model-specific context thresholds via `npm run token:budget`. If context saturation exceeds 70%, trigger context reduction, suppress verbose command outputs, and offload facts to Memory Vault.
4. **Token Budget Ceiling**:
   - Hard cap of 250,000 tokens per feature phase. If approaching warning thresholds, alert operator and prioritize context compression.

---

## 5. Code Quality & Security Standards

1. **Strict TypeScript**:
   - `strict: true` is enforced. Zero usage of `any`. Explicit interfaces/types for all function signatures.
2. **Deterministic TDD**:
   - Every new service, utility, or business logic component must have a corresponding test file (`*.test.ts`) using native Node test runner or Vitest.
3. **Millee 20-Point Security Hardening**:
   - Enforce row-level security (RLS), parameterized queries, constant-time comparisons (`crypto.timingSafeEqual`), and Argon2id password hashing.

---

## 6. Durable Context Persistence & Memory Vault

1. **Memory as Source of Truth**:
   - Cross-phase decisions, architectural rationales, and critical bug resolutions must be persisted to `.agents/memory/` using `npm run memory:save`.
   - Before starting complex tasks, recall relevant past learnings via `npm run memory:search`.
   - Phase handoffs must record a structured handoff document in `.agents/memory/team/handoffs/`.

---

## 7. Strict Zero-Secret Invariant & Pre-Commit Shield

1. **Absolute Zero Secrets Policy**:
   - Committing, staging, or pushing any secret, API key, access token, private key, or credential of any kind (including AWS, Stripe, GitHub, OpenAI, Anthropic, Google, Slack, RSA/SSH private keys, Bearer tokens, and `X-API-Key` values) to any git branch or repository is strictly forbidden.
   - Documentation, examples, and tests must EXCLUSIVELY use safe non-tokenized placeholders (e.g. `<YOUR_API_KEY>`, `YOUR_STRIPE_KEY`, `your-api-key-here`). NEVER use pseudo-realistic mock tokens (e.g. `sk_live_...`, `sk_test_...`) that trigger GitGuardian, Trufflehog, or GitHub Secret Scanning.
2. **Automated Shield & Hook Enforcement**:
   - All commits are gated by `.git/hooks/pre-commit`, which automatically executes `npm run check:secrets:staged`. Commits are rejected with exit code `1` if any secret or suspicious token pattern is detected.
   - The Zero-Secret Shield (`npm run check:secrets`) is permanently embedded as Layer 1 of the Adversarial Beta Audit (`npm run audit:beta`) and Probe 7/7 of the System Readiness Probe (`npm run readiness`).
   - Bypassing pre-commit hooks via `--no-verify` is strictly prohibited.

---

## 8. Universal Multi-Agent Orchestrator & Task Execution Directives

1. **Individual Modular Execution (Anti-Monolithic Invariant)**:
   - All tasks must be executed independently through [TaskDispatcher](file:///scripts/orchestrator/task_dispatcher.py) (`python -m scripts.orchestrator.task_dispatcher`):
     - **Task 1: Solution Formulation & White-Space Moat Strategy** (`--task solution`): Deconstructs problem statements, conducts mandatory live online search for real-world facts/regulations (anti-bias policy), benchmarks competitive commercial prior-art, establishes 10x technical moats, renders native ASCII/Unicode architecture diagrams, and commits architectural decisions to the SQLite Memory Vault (`.agents/memory/vault.sqlite`).
     - **Task 2: Code Implementation & Autonomous TDD Self-Healing** (`--task code`): Implements production business logic using an autonomous red-to-green TDD feedback loop (native Node or Python unittest). Mimics senior human experts to cover extreme edge cases (boundary limits, empty/null, malformed inputs, concurrency, unpredictable user actions). Enforces clean, idiomatic industry-standard code without unnecessary complexity, auto-patching up to 5 passes until 100% green, and emitting verifiable benchmark metrics (`specs/benchmark_metrics.json`).
     - **Task 3: Presentation Pitch Synthesis** (`--task presentation`): Generates competition-winning presentation pitch decks using [OmniDeck](file:///scripts/engine/) with 2D Flex/Grid geometry, 7 visual primitives, vector graphics, and cognitive layout density. Supports the default 6 championship archetypes as well as arbitrary user-defined custom slide archetypes and counts.
     - **System Audits & Readiness** (`--task audit`): Runs AppSec red-team scans and pre-commit secret scanners.
     - **Memory Vault Search & Recall** (`--task memory`): Retrieves indexed decisions, architectural notes, and handoffs from `.agents/memory/vault.sqlite`.
   - Never combine these 3 tasks into a single monolithic loop unless explicitly commanded by the operator.
2. **Two-Stage Presentation Protocol (Stage 1 PPTX -> Stage 2 Gated PDF)**:
   - OmniDeck compiles native `.pptx` first (<0.2s). Never auto-generate `.pdf` without explicit operator instruction (`--export-pdf`).

---

## 9. Enterprise Native Visual Documentation Standard

1. **Native Markdown Diagrams, Workflows & Charts**:
   - Human-facing documentation (`implementation_plan.md`, `walkthrough.md`, phase dossiers) must use clear, universally-rendering native Markdown diagrams (ASCII/Unicode box-drawing, workflow pipelines), structured data tables, and benchmark matrices.
2. **Zero Resource Waste & Zero Broken Image Icons**:
   - Do NOT waste system resources generating external image files for markdown documents.
   - Never embed fragile local image paths (`![Caption]` syntax) that risk failing to render or displaying broken image icons in markdown viewers.
3. **Executive Visual Design Hierarchy**:
   - Documentation must be styled as C-level Enterprise Engineering Deliverables: sleek typography, executive summary cards, comparative capability matrix tables, verified empirical benchmarks, and clear operational commands.
4. **Mandatory Zero-Raw-LaTeX Invariant**:
   - All human-facing and living markdown documents across the entire workspace (including `implementation_plan.md`, `walkthrough.md`, phase dossiers, and all files under `docs/`), **AS WELL AS ALL INTERACTIVE CHAT RESPONSES IN THE IDE/CLI**, are strictly prohibited from using raw LaTeX math delimiters (single-dollar or double-dollar math syntax) or raw LaTeX commands (`\mathcal`, `\frac`, `\text`, `\sin`, `\times`, etc.).
   - All mathematical expressions, bounds, percentages, and formulas must use clean, universally rendering Unicode typography (`≥`, `≤`, `×`, `≠`, `→`, `≈`, `±`, `²`, `³`, `α`, `β`, `Δt`, `∑`, `∏`) or fenced code blocks. Verified fail-closed by `npm run lint:markdown` and `FormatGuard.audit_response`.

---

## 10. Mandatory Adversarial Council Hardening Invariant (claude-council)

1. **Mandatory Council Hardening on All Plans & Solutions**:
   - Every implementation plan, architectural decision record (ADR), and solution blueprint MUST be hardened through the 5-Advisor Claude Council (`claude-council`) before execution or merge.
   - The 5 unaligned perspectives must be explicitly documented in the deliverable:
     - **The Contrarian (`01-contrarian`)**: Attacks foundational assumptions, seeks single points of failure, and demands failure-mode mitigations.
     - **The First-Principles Engineer (`02-first-principles`)**: Strips jargon, auditing raw algorithmic complexity, latency physics, and deterministic type safety.
     - **The Expansionist (`03-expansionist`)**: Identifies 10x defensible moats, asymmetrical leverage, and future-proof extensibility.
     - **The Naive Outsider (`04-outsider`)**: Audits cognitive ergonomics, eliminating over-engineering and obscure naming.
     - **The Pragmatic Executor (`05-executor`)**: Demands concrete migration runbooks, rollback mechanics, and verified empirical benchmarks.
2. **Unanimous Council Verdict & Non-Negotiable Moats**:
   - Every solution must achieve an explicit Council Verdict (`APPROVED WITH HARDENING`) and pass the **Contrarian 4-Moat Test** (Data Ingestion, Algorithmic, Sovereign/Statutory, and Financial Unit Economics).
   - Solutions must incorporate **Cryptographic Anti-Tamper & Enclave Isolation Specifications** (SHA-256 Merkle chain-of-custody, constant-time `timingSafeEqual` security, and fail-closed state transitions) to ensure solutions are non-reproducible by generic AI prompts and resilient against reverse-engineering.

---

## 11. Dual-Mode Operation (Solo Operator vs. 50/50 Dual-Lead Mode)

1. **Flexible Operating Modes**:
   - **Solo Operator Mode (`npm run mode:solo`)**: Designed for single developers building end-to-end applications. Bypasses distributed lease-lock collisions across workstations by assigning full domain ownership to the solo operator while preserving subagent persona separation.
   - **Dual-Lead Enterprise Mode (`npm run mode:dual`)**: Enforces co-equal 50/50 division across two distinct workstations (Computer 1: Lead 1 Alpha; Computer 2: Lead 2 Beta). Mandates atomic lease handoffs (`npm run role:handoff`) and distributed lock synchronization before cross-domain edits.
2. **Mode Status & Verification**:
   - Query active mode at any time via `npm run mode:status`.
   - The active mode is persisted in `.agents/state/active-role.json` and governs lease acquisition in `scripts/lock-manager.ts`.

---

## 12. Anti-Green Signal Trap & Red-First Testing Invariant

1. **Mandatory Red-Phase Pre-Flight Verification**:
   - Tests MUST be written FIRST by the Adversarial SDET before feature implementation begins.
   - The test must be executed against stubs/missing code and verified **RED (Exit code ≠ 0)**. Any test that passes immediately without business logic is classified as a **Tautological Test Defect** and rejected.
2. **Deterministic Mutation Testing Gate (≥ 80% Kill Rate)**:
   - All modules must be audited by the Mutation Testing Engine (`npm run test:mutation`).
   - The engine injects 4 fault classes:
     1. Boundary inversions (`>` to `<=`, `===` to `!==`).
     2. Return value overrides (`return true` to `return false`, `return data` to `return null`).
     3. Arithmetic and assignment mutations (`+` to `-`, `*` to `/`).
     4. State bypass mutations (omitted FSM transitions or event emits).
   - Test suites that fail to kill at least 80% of injected mutants are rejected with exit code `1`.
3. **Automated Headless Browser Verification for Frontend**:
   - Whenever frontend files (`.html`, `.tsx`, `.jsx`, `.vue`, `.svelte`) exist in the project, the Adversarial SDET automatically executes headless Playwright browser verification by default.
4. **Differentiated LLM Persona Routing**:
   - Enterprise product squads must execute using specialized reasoning profiles:
     - **Product Manager**: Balanced reasoning (`temp=0.7`, `effort=medium`).
     - **System Architect**: Rigorous deterministic schema contracts (`temp=0.2`, `effort=high`).
     - **Adversarial SDET**: Creative boundary probe and edge-case fuzzing (`temp=0.8`, `effort=high`).
     - **Core Engineer**: Deterministic idiomatic implementation (`temp=0.1`, `effort=medium`).
     - **Mutation Auditor**: Deterministic AST fault injection (`temp=0.0`, `effort=low`).
     - **Technical Writer**: Clear 6-technique cognitive synthesis (`temp=0.4`, `effort=low`).

---

## 13. Universal Centralized Reactive State Store Mandate

1. **Zero Data Reset Across View Navigations**:
   - Multi-tab and multi-view applications must store all domain state, telemetry outputs, and graph models in a single reactive, persistent store.
   - Switching tabs, selecting sample datasets, or navigating dashboards must NEVER clear or re-initialize previously computed pipeline data.
2. **Fail-Closed Statutory Action Gating**:
   - Downstream actions (statutory certificates, evidence exports, dockets) are strictly gated by the central Finite State Machine (FSM).
   - Certificates and export buttons must remain disabled until prerequisite engines transition to `COMPLETED` and computed confidence metrics meet statutory thresholds.
3. **Strict UI Binding Invariant**:
   - UI metrics, badges, and buttons must bind directly to live calculated outputs from the state store. Hardcoding mock scores or percentages in UI components is strictly prohibited.

---

## 14. Enterprise Frontend Component Shell & Design Token Invariant

1. **Universal Component Shell Structure**:
   - All web interfaces must adhere to a standardized 3-tier layout hierarchy:
     - `<header class="app-header">`: Navigation, environment badges, and global search.
     - `<main class="app-viewport">`: Dynamic tab views, analytical grids, and visualization stages.
     - `<footer class="app-action-dock">`: Fixed bottom-right anchor for workflow directive buttons, export triggers, and pipeline actions.
   - Placing workflow action buttons inside nested scrollable boxes, table cards, or arbitrary corners is strictly prohibited.
2. **Mandatory Semantic Design Tokens**:
   - UIs must import standard semantic tokens (`templates/frontend/design-tokens.css`). Ad-hoc inline styles and arbitrary hex codes are forbidden.
   - Use standard typography scales (`--font-family-display`), spacing increments (`--space-1` to `--space-12`), and elevation shadows.
3. **Safe DOM Re-rendering & Graph Viewport Clamping**:
   - Dynamic card updates must clear stale contents before appending to prevent duplicate text nodes.
   - D3/SVG graph canvas elements must clamp initial zoom scale and center coordinates prior to node injection to eliminate 1-second zoom glitching.
4. **Headless Geometry Verification**:
   - Playwright browser tests must assert element geometry (`getBoundingClientRect()`) to verify that buttons maintain fixed coordinates across all tab transitions.

---

## 15. Mandatory Chat Prompt 6-Persona Execution Lifecycle Invariant & Universal Playwright Frontend Mandate

1. **Zero Unstructured Generalist Responses in Chat**:
   - In interactive IDE chat conversations, the agent is strictly prohibited from answering as an unstructured generic assistant.
   - Every single prompt (regardless of perceived size, whether building a full system or tweaking a button) MUST visibly execute through the 6 Enterprise Personas:
     - 📋 **`[Product Manager]`**: Deconstruct intent into functional scope, target personas, acceptance criteria, and forbidden states.
     - 📐 **`[System Architect]`**: Define/verify typed data contracts, schemas, and FSM transition constraints.
     - 🛑 **`[Adversarial SDET]`**: Formulate red-phase acceptance criteria. Whenever frontend code exists, ALWAYS execute headless Playwright tests (`npm run test:e2e` or `npx playwright test`) with exhaustive elemental assertions.
     - 💻 **`[Core Engineer]`**: Write/refactor clean, production-grade business logic and UI components to turn tests green.
     - 🔬 **`[Mutation & Security Auditor]`**: Verify mutation survivability (≥ 80%), check zero secrets, constant-time checks, and fail-closed gates.
     - 📑 **`[Technical Writer]`**: Generate/update living documentation, Part 7 dossiers, and sync plans/walkthroughs.
2. **Universal Headless Playwright Mandate for Frontend**:
   - For all frontend projects in the workspace (`demo/chakra_mvp`, `demo/bhedak_mvp`, and any new web application), automated testing MUST execute via headless Playwright (`@playwright/test`) by default.
   - Do NOT use slow multimodal browser subagents for regression verification.
   - Tests must assert every button, badge, tab transition, calculation, modal, and console error with maximum accuracy. A thorough 30–60 second verification window is preferred over hasty shallow checks.
3. **Deterministic Tooling Delegation vs. Sub-Agent Model**:
   - Personas must NOT spawn uncontrolled recursive conversational LLM subagents (which causes exponential context degradation, token exhaustion, and 5-minute vision delays).
   - Instead, personas directly control high-speed, deterministic execution engines: Playwright for E2E DOM tests, AST mutation engines for fault injection, and native test runners for unit logic.
4. **Operator Empirical Proof Protocol (Anti-Hallucination & Verifiable Attestation Receipt)**:
   - In chat responses, the agent is strictly forbidden from claiming any test passed, build succeeded, or security gate cleared without executing the real command and printing the exact command line and return code.
   - Every prompt response must conclude with the **Verifiable Squad Attestation Receipt** emitted by `SquadAttestor` ([scripts/orchestrator/squad_attestation.py](file:///scripts/orchestrator/squad_attestation.py)), containing timestamp, provenance SHA-256 hash, active personas, verified executed commands, and empirical context telemetry.
   - Context telemetry metrics (`active_chat_context`, `remaining_before_compaction`, `saturation`, `compactions_occurred`, `cumulative_session_tokens`) MUST be directly acquired by executing `npm run context:yaml` or `npm run attest:telemetry`. Guessing, estimating, or hallucinating context window saturation numbers is strictly prohibited.
   - Attestations are permanently logged to `.agents/audit_trail.log` and SQLite memory vault, verifiable by the operator via `npm run attest:verify`.
5. **Automatic Twin-Documentation Sync Invariant**:
   - Whenever any component, CLI command, testing harness, persona lifecycle, or architectural directive of the agentic workflow is modified, the agent MUST automatically assess the impact and synchronize the two primary system documentation files without waiting for explicit operator instructions:
     1. `README.md`: High-level system overview, architectural pillars, onboarding prerequisites, and quickstarts.
     2. `SYSTEM_COMMANDS.md`: Master executable CLI command cheat sheet.
   - Deep architectural treatises and reference blueprints are maintained permanently in `docs/architecture/` (`docs/architecture/production_architecture_blueprint.md`).
   - Living feature artifacts are version-controlled in `docs/plans/`, `docs/walkthroughs/`, `docs/audits/`, `docs/decisions/`, `docs/research/`, and `docs/specifications/` via `SpecSync`.

---

## 16. Mandatory Human-Naming Invariant & Root Compactness Standard

1. **Human-Meaningful Naming (Zero Cryptic Acronyms)**:
   - All files and directories across the entire repository MUST use clear, standard, human-meaningful English words.
   - Strictly prohibit obscure abbreviations, truncated slang, and cryptic acronyms for files and directories (e.g. use `docs/decisions/` instead of `docs/adrs/`, `docs/specifications/` instead of `docs/rfcs/`, `scripts/security-audit-runner.ts` instead of `pen-test-runner.ts`, and `npm run verify:plan` instead of `peav:verify`).
   - File and folder names must be concise (2 to 3 words maximum), avoiding runaway compound names. Use kebab-case for TypeScript/web assets and snake_case for Python modules.
2. **Compact Root Directory Invariant**:
   - The repository root must remain pristine and compact (≤ 12 essential files: `package.json`, `package-lock.json`, `tsconfig.json`, `playwright.config.ts`, `pytest.ini`, `.gitignore`, `.env.example`, `LICENSE`, `README.md`, `SYSTEM_COMMANDS.md`, `AGENTS.md`, and `GEMINI.md`).
   - Tool-specific agent configurations must be placed in dedicated subdirectories or unified in `UNIVERSAL_AGENT_INSTRUCTIONS.md`. Loose harness or spell check files in root are strictly prohibited.

---

## 17. Mandatory Real-Time Brain Artifact-to-Docs Synchronous Mirroring

1. **Deterministic In-Repo Persistence**:
   - Whenever the agent creates, edits, or updates an artifact (such as `implementation_plan.md`, `walkthrough.md`, or any diagnostic audit) in the IDE brain directory, the agent MUST immediately synchronize that file to its in-repo catalog (`docs/plans/`, `docs/walkthroughs/`, `docs/audits/`) using `SpecSync` (or `python -m scripts.orchestrator.spec_sync --sync-brain`).
2. **Exact Real-Time Timestamping (Hours, Minutes, Seconds)**:
   - All persisted markdown files MUST use full real-time timestamp prefixes down to the second (`YYYY-MM-DD_HH-MM-SS_<slug>_<type>.md`, e.g. `2026-09-23_09-38-33_browser_tests_human_naming_plan.md`). Date-only filenames (`YYYY-MM-DD`) are strictly prohibited to prevent collisions and preserve chronological precision.
3. **Smart Human Title & Slug Extraction**:
   - Filenames and index entries must dynamically derive clean, human-meaningful 2 to 4 word slugs from the primary document `# Heading`.
4. **Autonomous Real-Time Watcher Daemon**:
   - The repository provides `RealtimeDocsWatcher` (`npm run docs:watch` or `python -m scripts.orchestrator.realtime_docs_watcher`), which continuously monitors the active brain folder using SHA-256 change detection to auto-sync any modified artifacts within 1.5 seconds.
5. **Living Catalog Deduplication**:
   - `INDEX.md` living catalogs in all 6 directories (`docs/plans/`, `docs/walkthroughs/`, `docs/audits/`, `docs/decisions/`, `docs/research/`, `docs/specifications/`) must record the exact second of execution (`YYYY-MM-DD HH:MM:SS`) and prevent duplicate line appends.




