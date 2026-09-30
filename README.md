# Antigravity Enterprise Autonomous Agentic Platform

> **Target Environment**: Google Antigravity IDE & Antigravity CLI (`agy`)  
> **Status**: Production Ready | 99/99 Pytest suites green | 18/18 Adversarial suites passing | 13/13 Node unit suites + 6/6 Harness Evals passing | 7/7 System Readiness Probes green  
> **Governance Standard**: Enterprise 2-Person 50/50 Dual-Lead Architecture & Part 7 Protocol ([AGENTS.md](file:///d:/BE_Research/AGENTS.md))  

---

## 1. Executive Overview

Antigravity Enterprise is an autonomous multi-agent engineering platform that translates an entire enterprise engineering organization into a specialized **6+1 Agile Product Squad**. It operates seamlessly across **Solo Developers**, **2-Person Dual-Lead Rotations**, and **Multi-Developer Team Meshes (N persons)** with parallel domain locking.

The system dynamically specializes into any of **8 Master Domains** and **46 Subdomains** without hardcoded domain bias, hydrating expert personas, curated skills, behavioral evaluations, domain-specific AST mutation fault injections, and sandboxed compiler toolchains JIT.

```
                    UNIVERSAL MULTI-DOMAIN SQUAD ARCHITECTURE

        ┌─────────────────────────────────────────────────────────────────┐
        │  Domain Controller & Selection Engine (scripts/domain-selector) │
        │  8 Master Domains • 46 Subdomains • templates/domains/catalog   │
        └────────────────────────────────┬────────────────────────────────┘
                                         │
                                         ▼
        ┌─────────────────────────────────────────────────────────────────┐
        │  Active Domain State (.agents/state/active-domain.json)         │
        └────────────────────────────────┬────────────────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
     ┌───────────────────────┐                       ┌───────────────────────┐
     │  Curated Skills Map   │                       │ Dynamic JIT Hydrator  │
     │  172 Subdomain Slots  │                       │ (DomainPersonaEngine) │
     │  (298 Physical Skills)│                       │ 6 Specialized Personas│
     └───────────┬───────────┘                       └───────────┬───────────┘
                 │                                               │
                 └───────────────────────┬───────────────────────┘
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         ▼                               ▼                               ▼
 ┌───────────────┐               ┌───────────────┐               ┌───────────────┐
 │ Behavioral    │               │ AST Mutation  │               │ Sandboxed     │
 │ Harness Evals │               │ Engine        │               │ Compilers     │
 │ (domain-evals)│               │ (Domain AST)  │               │ (forge/cargo) │
 └───────┬───────┘               └───────┬───────┘               └───────┬───────┘
         │                               │                               │
         └───────────────────────────────┼───────────────────────────────┘
                                         │
                                         ▼
                         ┌───────────────────────────────┐
                         │ Domain-Partitioned SQLite     │
                         │ Memory Vault & Living Catalogs│
                         └───────────────────────────────┘
```

---

## 2. Core Architectural Pillars

### 1. Universal Master Domain Specialization (8 Domains, 46 Subdomains)
- Dynamically transforms the 6-Persona SDLC squad into senior domain specialists across Software Engineering, AI/ML, Blockchain/Web3, Deep Tech & Scientific Research, Cybersecurity, Cloud Infrastructure, Data Engineering, and Vertical Applied IT.
- Interactive switching via `npm run domain:select` or programmatic configuration via `npm run domain:set`.
- Active compiler and runtime verification via `npm run domain:doctor`.

### 2. 2-Tier Progressive Skill Disclosure (298 Skills, Zero Ghost Packages)
- **Tier 1 (Curated Subdomain Skills)**: 172 high-priority skill slots (104 unique specialist skills) mapped directly into the 46 subdomains. Dynamically resolved by `DomainPersonaEngine` and injected into prompt overlays as clickable markdown links (`<150 tokens`).
- **Tier 2 (Universal Skills Vault)**: All 298 physical skills in `.agents/skills/` remain searchable on-demand via `npm run skill:search <query>`.

### 3. Tri-Mode Operator Collaboration (Solo, Dual, Team Mesh)
- **Solo Mode (`npm run mode:solo`)**: Instant solo-developer velocity. Bypasses multi-host lease locks while retaining autonomous persona separation.
- **Dual Mode (`npm run mode:dual`)**: Co-equal 50/50 dual-lead workflow alternating across Computer 1 (Alpha: Feature Architect) and Computer 2 (Beta: Adversarial SDET).
- **Team Mesh Mode (`npm run mode:team`)**: Multi-developer parallel domain leases (`.agents/state/locks/<domain>.lock.json`) with Git-native shared state and LAN sync server (`npm run lan:start`).

### 4. 6+1 Agile Product Squad & Complete SDLC Lifecycle
Simulates an expert enterprise product team executing across all 9 SDLC phases:
- **Phase 0: Deep Research**: Triangulates live regulations, commercial prior-art, and CVEs (`deep_research_specialist`).
- **Phase 1: Requirements Formulation**: PRDs, user stories, and statutory KPIs (`product_manager`).
- **Phase 2: Architectural Modeling**: Typed schema contracts and ADRs (`system_architect`).
- **Phase 3: Adversarial TDD**: Red-first testing, concurrency races, and headless Playwright verification (`adversarial_sdet`).
- **Phase 4: Idiomatic Implementation**: Green business logic in the domain's dominant stack (`core_engineer`).
- **Phase 5: Mutation & Hardening**: AST fault injection (≥ 80% kill rate) and secret scans (`mutation_auditor`).
- **Phase 6: Cognitive Dossiers**: Part 7 6-technique comprehension dossiers and living doc sync (`technical_writer`).
- **Phase 7: Packaging & Release**: Release gating and statutory export certifications.
- **Phase 8: Telemetry & Impact**: Real empirical benchmarks and impact analyses.

### 5. Tiered 10+1 Active Interception Architecture & Dynamic Multi-Domain Harness
- **Active Interception Kernel (`.agents/harness/active_kernel.py`)**: Intercepts shell execution and file writes across all 8 Master Domains and 46 Subdomains.
- **Universal Pre-Execution Guards**:
  - `MemoryGuard`: Enforces 75% physical RAM allocation ceiling, preventing unhandled kernel OOM kills (SIGKILL / 137).
  - `DeadlineLockdown`: Enforces automatic T-4h code freeze, prohibiting late-stage rewrites and restricting execution strictly to submission packaging and validation.
  - `ScaleProfiler`: Mandates 500-item micro-benchmarks before executing jobs >10,000 items, detecting O(N²) quadratic bottlenecks in < 0.2s.
  - `GateGuard`: Fact-forcing middleware rejecting empirical metric claims that lack raw tool execution proof.
  - `PromptHygiene`: Compresses monolithic 25 KB prompts into a 4 KB Core Kernel, pruning foreign domain rules to eliminate attention dilution.
- **Dynamic Domain-Specific Verification**: Tailored invariant gates for each of the 8 domains (CEI in Blockchain, ECE Calibration in AI/ML, constant-time `timingSafeEqual` in Cybersecurity, strict TS and RFC 7807 in Software).
- **Deterministic AST Mutation Testing**: Enforces ≥ 80% mutation kill rate in both TypeScript (`scripts/mutation-tester.ts`) and Python (`scripts/orchestrator/python_mutation_tester.py`).
- **Cryptographic Squad Attestation Ledger**: Every prompt execution emits an immutable SHA-256 execution receipt with `active_personas`, `domain`, `subdomains`, and verified `activated_skills` logged to SQLite Memory Vault (`npm run attest:verify`).

### 6. Automatic Skill Resolution & Transparent Attestation (298 Skills, Zero Ghost Packages)
- **Automatic Keyword & Subdomain Resolution (`SkillResolver`)**: Automatically parses prompt keywords and active subdomain mappings to resolve the exact matching skills from the 298 installed catalog before execution.
- **Mandatory Attestation Invariant**: Every turn receipt explicitly outputs `activated_skills` with relative paths and match reasons, eliminating operator blindness and guaranteeing 100% visibility.
- **Zero Ghost Skills**: Every referenced skill is grounded against physical `.agents/skills/<name>/SKILL.md` files.

### 7. Domain-Aware Memory Vault & Living Documentation
- **SQLite Memory Vault (`.agents/memory/vault.sqlite`)**: Indexed full-text search with `domain_id` partitioning and active-domain relevance boosting.
- **6 Living Documentation Catalogs**: `docs/plans/`, `docs/walkthroughs/`, `docs/audits/`, `docs/decisions/`, `docs/research/`, and `docs/specifications/` synchronized in sub-seconds via `SpecSync` (`npm run docs:sync`, `npm run docs:reconcile`).

---

## 3. Quickstart & Installation

### Prerequisites
- **Node.js**: v20.x or v24.x LTS (with native `--experimental-strip-types`)
- **Python**: 3.11+ or 3.12+
- **Playwright**: Headless Chromium browser automation

### 1-Command Setup
```bash
# 1. Install Node.js dependencies
npm install

# 2. Install Playwright browser binaries
npx playwright install chromium

# 3. Verify Full System Readiness (7/7 Probes Green)
npm run readiness
```

---

## 4. Essential Workflow Runbook

### Domain Selection & Compiler Diagnostics
```bash
# Inspect active domain, subdomains, and hydrated stack
npm run domain:status

# Interactive CLI domain questionnaire
npm run domain:select

# Explicitly set domain and subdomains headlessly
npm run domain:set -- --domain blockchain --subdomains smart_contracts,defi_protocols

# Probe required runtimes and compilers for active domain
npm run domain:doctor
```

### Autonomous Task Execution
```bash
# Task 1: First-principles solution, live research & cloud unit economics
python -m scripts.orchestrator.task_dispatcher --task solution --prompt "Autonomous satellite wildfire early detection"

# Task 2: Red-to-green autonomous TDD implementation loop
python -m scripts.orchestrator.task_dispatcher --task code --prompt "Implement rate-limiting token bucket middleware"

# Task 3: 2D Flex/Grid presentation pitch deck compilation
python -m scripts.orchestrator.task_dispatcher --task presentation --prompt "Universal Domain Specialization"
```

### Quality Assurance & Security Gates
```bash
# Run full Python orchestrator and engine test suite (99 suites)
pytest tests/ -q

# Run Lead 2 adversarial suite (concurrency races, chaos fuzzing, timing attacks)
npm run test:adversarial

# Run Node unit suites + Core 4 & Domain-Adaptive Behavioral Evaluations
npm test

# Run Domain-Adaptive Behavioral Evaluations dynamically
npm run harness:eval

# Run AST Mutation Testing Gate (≥ 80% kill rate)
npm run test:mutation

# Validate zero raw LaTeX math syntax across all documentation
npm run lint:markdown docs
```

### Documentation & Memory Vault
```bash
# Synchronously mirror brain artifacts to docs/ living catalogs
npm run docs:sync

# Reconcile living catalog indexes sorted by timestamp descending
npm run docs:reconcile

# Search SQLite Memory Vault with domain relevance boosting
npm run memory:search -- --query "reentrancy guards"

# Verify cryptographic squad attestation audit log
npm run attest:verify
```

---

## 5. Repository Topology

```
.
├── .agents/                    # Governance, state, locks, and skills
│   ├── harness/                # Behavioral evals runner & domain test contracts
│   ├── memory/                 # SQLite Memory Vault (vault.sqlite & JSONL)
│   ├── skills/                 # 298 verified modular skills
│   └── state/                  # Active domain, role, and lock JSON descriptors
├── docs/                       # Living in-repo documentation catalogs
│   ├── plans/                  # Feature PRDs & implementation plans (INDEX.md)
│   ├── walkthroughs/           # Execution walkthroughs & proofs (INDEX.md)
│   ├── audits/                 # System readiness probes & security audits (INDEX.md)
│   ├── decisions/              # Architecture Decision Records (ADRs) (INDEX.md)
│   ├── research/               # Multi-hop research triangulation dossiers (INDEX.md)
│   └── specifications/         # Typed schema contracts & interfaces (INDEX.md)
├── scripts/                    # Core TypeScript & Python orchestrators
│   ├── orchestrator/           # TaskDispatcher, SquadOrchestrator, SandboxBridge, SpecSync
│   ├── domain-selector.ts      # Domain catalog controller & CLI
│   ├── domain-doctor.ts        # Compiler diagnostic probes
│   ├── lock-manager.ts         # Distributed lease locking engine
│   └── mutation-tester.ts      # Deterministic AST mutation engine
├── templates/domains/          # 8 Master Domain rubric definitions & catalog index
├── tests/                      # Pytest, Node unit, and Lead 2 adversarial test suites
├── AGENTS.md                   # Universal workspace operational directives & invariants
├── GEMINI.md                   # Google Antigravity IDE pair programming guidelines
├── SYSTEM_COMMANDS.md          # Master executable CLI command cheat sheet
└── package.json                # Pinned dependencies & executable npm scripts
```

---

## 6. License & Compliance
Licensed under the **MIT License**. Strictly enforces the Zero-Hallucination, Zero-Secret, and Zero-Raw-LaTeX Invariants fail-closed across all CI/CD pipelines and interactive agent sessions.
