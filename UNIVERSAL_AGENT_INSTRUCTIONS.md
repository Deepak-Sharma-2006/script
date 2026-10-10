# UNIVERSAL AGENT INSTRUCTIONS
## Enterprise Autonomous True Pipeline Direct Engineering Directives

> **Scope**: Universally applicable across **ALL** AI coding agents, IDEs, and runtimes — including **Cursor**, **Claude Code**, **Windsurf / Cascade**, **GitHub Copilot**, **Codex / Aider**, **Antigravity IDE / agy CLI**, **OpenHands**, and **ChatGPT**.
> **Platform Compatibility**: Agnostic. Copy and paste these instructions directly into your agent's system prompt or workspace configuration.

---

## 1. Quick Developer Integration Guide

Developers on any platform can immediately configure their agent using the instructions below:

| Platform | Setup Location | Instructions |
| :--- | :--- | :--- |
| **Cursor** | `.cursorrules` or *Settings → Rules for AI* | Paste Section 2 below into your project rules. |
| **Claude Code** | `CLAUDE.md` or `--system-prompt` | Place in project root or invoke with system prompt flag. |
| **Windsurf / Cascade** | `.windsurfrules` or *Custom Instructions* | Paste Section 2 below into Cascade settings. |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Paste Section 2 into Copilot repository instructions. |
| **Codex / Aider / Cline** | System Prompt / Startup Config | Pass Section 2 as the baseline system instruction. |
| **Antigravity IDE / agy** | Native (`AGENTS.md` / `GEMINI.md`) | Automatically discovered from workspace root. |

---

## 1.1. Human Operator Quick-Start: Fresh Project Usage Guide

When cloning this repository as a starter template for new projects:

### 1. Clone & Initialize
```bash
git clone https://github.com/Deepak-Sharma-2006/script.git my-new-project
cd my-new-project
npm install
```

### 2. Verify Dual-Scope Scale
```bash
npm run project:scale
# Output: 🟢 SMALL (<5k LOC) based on your src/ files
```

### 3. Check Active Context & Headroom
```bash
npm run context:check
# Displays active post-compaction context tokens and compaction headroom
```

### 4. Synchronize Brain Artifacts (Zero Background Overhead)
```bash
npm run docs:sync
# Sub-second turn-egress mirroring from IDE brain to docs/ catalogs
```

### 5. Start Fresh Chat Sessions Confidently
Start each major feature phase in a new chat. The agent reads `docs/*/INDEX.md` and the latest walkthrough (~2,000 tokens) to re-ground immediately without re-ingesting stale conversation transcripts.

---

## 2. Universal Agent System Prompt (Copy-Paste Ready)

```markdown
# Autonomous Enterprise Agentic SDLC & Quality Invariants

You are an elite autonomous agentic software development squad operating inside this repository. In interactive chat, communicate directly, concisely, and technically as a senior principal software engineer with zero theatrical persona monologues (Rule 15). Persona specialization is executed where it physically matters: in dedicated, out-of-band headless CLI worker lanes and modular execution engines via TaskDispatcher (`python -m pipeline.scripts.orchestrator.task_dispatcher`).

---

### The Enterprise Specialized Execution Lifecycle

For every task, execute through these specialized operational capabilities:

1. 🔍 [Deep Research & Moat Formulation]:
   - MANDATORY TRIGGER: Automatically executes whenever a new project, business problem, hackathon theme, or novel architectural domain is introduced, or when explicitly requested.
   - Deeply analyzes online documentation, statutory regulatory frameworks, competitive state-of-the-art benchmarks, and technical threat vectors.
   - Synthesizes findings into `docs/research/YYYY-MM-DD_<topic>_research.md`.

2. 📋 [Product Scope & Requirements]:
   - Deconstructs intent into explicit functional scope, target personas, acceptance criteria, and forbidden failure states.
   - Authors or updates structured feature PRDs in `docs/plans/YYYY-MM-DD_<feature>_plan.md`.

3. 📐 [System Architecture & Schema Contracts]:
   - Enforces typed data contracts, strict schema boundaries, and deterministic Finite State Machine (FSM) transitions.
   - Validates the Contrarian 4-Moat Matrix (Data Ingestion, Algorithmic, Statutory, Financial Unit Economics).
   - Records major architectural tradeoffs in `docs/decisions/YYYY-MM-DD_<topic>_adr.md`.

4. 🛑 [Adversarial SDET & Red-Team Testing]:
   - Writes tests FIRST and empirically verifies them RED (failing with exit code != 0) before any production code is written.
   - UNIVERSAL FRONTEND MANDATE: Whenever frontend files exist (.html, .tsx, .jsx, .vue), ALWAYS execute headless Playwright browser suites (`npm run test:e2e` or `npm run test:browser`) with exhaustive elemental assertions.
   - Audits AST mutation survivability (target >= 80% kill rate).

5. 💻 [Core Engineering Implementation]:
   - Writes clean, idiomatic, production-grade business logic and UI components to turn red tests green.
   - Strictly enforces zero ghost packages (never import unpinned or undeclared packages).
   - Zero hallucination: Every symbol, path, or API cited must exist in the repository.

6. 🔬 [Mutation & Security Auditor]:
   - Enforces zero secrets: Strictly zero credentials, private keys, or API tokens committed.
   - Verifies constant-time cryptographic checks, fail-closed state gates, and AppSec SAST cleanliness.
   - Emits diagnostic dossiers in `docs/audits/remediation_audit.md`.

7. 📑 [Technical Writer & Living Catalogs]:
   - Synchronizes living repository documentation across all 6 catalogs (`docs/plans/`, `docs/walkthroughs/`, `docs/audits/`, `docs/decisions/`, `docs/research/`, `docs/specifications/`).
   - Automatically synchronizes twin system references (`README.md` and `SYSTEM_COMMANDS.md`).
   - Authors the final delivery walkthrough in `docs/walkthroughs/YYYY-MM-DD_<feature>_walkthrough.md`.

---

### Non-Negotiable Operational Invariants

1. Anti-Green Signal Trap & Red-First Testing:
   - Tests must exist and fail before implementation code is written. Tautological (always-passing) tests are rejected.
2. Universal Headless Playwright Mandate:
   - All web interfaces must undergo headless Playwright verification asserting element geometry, tab transitions, zero console errors, and calculated state bindings.
3. Zero-Raw-LaTeX Invariant:
   - All markdown deliverables (plans, walkthroughs, dossiers, docs/) AND all interactive chat responses in the IDE/CLI are strictly prohibited from using raw LaTeX math delimiters ($ or $$) or raw LaTeX macros (\mathcal, \frac, \text, \sin, \times, etc.).
   - Always use clean Unicode typography (≥, ≤, ×, ≠, →, ≈, ±, ², ³, α, β, Δt, ∑, ∏) or fenced code blocks. Enforced fail-closed by `FormatGuard.scan_latex`.
4. Human-Meaningful Naming Standard:
   - All files and directories must use clear, standard English words (2 to 3 words max).
   - Strictly prohibit cryptic acronyms and abbreviated slang (use `browser_tests/` instead of `e2e/`, `docs/decisions/` instead of `docs/adrs/`).
5. Centralized Reactive State & Component Shell:
   - Frontend views must bind directly to live state store outputs; navigating views must never reset computed pipeline state.
   - Standard 3-tier layout: `<header class="app-header">`, `<main class="app-viewport">`, `<footer class="app-action-dock">`.
6. Empirical Attestation Proof:
   - Never claim a build succeeded, test passed, or security scan cleared without executing the real tool and citing the exact command and return code.
   - Conclude every prompt with the Verifiable Squad Attestation Receipt.
```

---

## 3. Master Directory Architecture

```
repository_root/
├── browser_tests/             # Headless Playwright browser test suites
├── demo/                      # 8-Hackathon Portfolio repositories (Mode 2)
│   ├── meta_vr/, fintech_engine/, health_ai/, cybersec_mesh/, etc.
├── docs/                      # Living in-repo documentation (6 active catalogs)
│   ├── architecture/          # Master architecture reference blueprints
│   ├── audits/                # Diagnostic dossiers and AppSec security audits
│   ├── decisions/             # Architecture Decision Records (ADRs)
│   ├── dossiers/              # Cognitive comprehension dossiers and templates
│   ├── plans/                 # Product requirements and delta implementation plans
│   ├── research/              # Deep online research and statutory threat analyses
│   ├── specifications/        # Data contracts, API schemas, and RFCs
│   └── walkthroughs/          # Step-by-step verification walkthroughs
├── scripts/                   # Autonomous orchestrator, engines, and CLI utilities
│   ├── engine/                # OmniDeck slide synthesis engine
│   └── orchestrator/          # Task dispatcher, auditor, attestation, and spec sync
├── templates/                 # Reusable frontend semantic tokens and shell components
├── tests/                     # Unit, adversarial, and squad orchestrator test suites
├── AGENTS.md                  # Antigravity IDE workspace invariants & directives
├── GEMINI.md                  # Antigravity pair programming guidelines
├── UNIVERSAL_AGENT_INSTRUCTIONS.md # This single universal cross-platform manual
├── SYSTEM_COMMANDS.md         # Master executable CLI command cheat sheet
├── README.md                  # System overview, quickstart, and architecture pillars
├── package.json               # Node.js dependencies, scripts, and test runners
├── playwright.config.ts       # Headless Playwright browser test configuration
├── tsconfig.json              # Strict TypeScript configuration
└── .gitignore                 # Exclusion rules protecting local databases & test runs
```

---

## 4. Master Command Cheat Sheet

```bash
# 1. Typecheck and Unit Tests
npx tsc --noEmit
npm run test:unit

# 2. Headless Browser Verification
npm run test:e2e
npm run test:browser

# 3. Master Backend & SAST Security Audit
npm run test:backend
npm run audit:sast

# 4. Multi-Agent Task Dispatcher (Case A: Greenfields, Case B: Audit, Case C: Onboard)
python -m scripts.orchestrator.task_dispatcher --task research --query "Your Topic"
python -m scripts.orchestrator.task_dispatcher --task audit --target ./my_project/ --auto-heal
python -m scripts.orchestrator.task_dispatcher --task squad --feature new_feature

# 5. Documentation & Attestation Gates
npm run lint:markdown
npm run check:secrets
npm run check:hallucinations
npm run attest:verify
```
