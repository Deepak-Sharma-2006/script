# Universal Autonomous Agentic Engineering Platform

An enterprise-grade, agent-agnostic multi-agent SDLC orchestration framework. Built to transform any AI coding agent or human engineering team into an autonomous, self-healing **6+1 Agile Product Squad** across any development environment.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-v20%2B%20%7C%20v24%2B-339933.svg?logo=node.js)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-3.11%2B%20%7C%203.12%2B-3776AB.svg?logo=python)](https://python.org)
[![Universal Harness](https://img.shields.io/badge/Universal-Claude%20%7C%20Cursor%20%7C%20Windsurf%20%7C%20Copilot%20%7C%20Antigravity-blueviolet.svg)](UNIVERSAL_AGENT_INSTRUCTIONS.md)

---

## Overview

The **Universal Autonomous Agentic Engineering Platform** provides an end-to-end operational framework for AI-assisted and fully autonomous software development. It eliminates the fragile prompt-and-pray paradigm by introducing structured multi-agent personas, red-first test-driven development, deterministic AST mutation testing, active runtime interception, and automated cross-agent synchronization.

Whether you develop with **Claude Code**, **Cursor**, **Windsurf**, **GitHub Copilot**, **Codex / Aider**, **Google Antigravity IDE**, or run headless scripts in **CI/CD**, this repository acts as a single, authoritative foundation that works identically across all environments with zero vendor lock-in.

---

## Universal Agent Harness Compatibility

All agent-specific instruction surfaces are generated and validated from a single source of truth ([UNIVERSAL_AGENT_INSTRUCTIONS.md](file:///d:/BE_Research/UNIVERSAL_AGENT_INSTRUCTIONS.md)), ensuring zero instruction drift across tooling:

| Environment | Integration Surface | Configuration & Sync |
| :--- | :--- | :--- |
| **Claude Code** | `CLAUDE.md` / CLI | Directly ingests root instructions or via `--system-prompt` |
| **Cursor** | `.cursorrules` / *Rules for AI* | Ingests root instructions via `npm run harness:sync` |
| **Windsurf / Cascade** | `.windsurfrules` / *Cascade Rules* | Ingests root instructions via `npm run harness:sync` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Ingests root instructions via `npm run harness:sync` |
| **Google Antigravity** | Native `AGENTS.md` & `GEMINI.md` | Automatically discovered from repository root |
| **Codex / Aider / OpenHands** | System Prompt / Startup Config | Direct markdown ingestion from repository root |
| **Headless CLI / CI/CD** | `python -m scripts.orchestrator.task_dispatcher` | Deterministic headless task execution |

Synchronize and validate cross-harness instructions at any time:
```bash
npm run harness:sync
```

---

## Core Capabilities

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

### 1. 6+1 Agile Product Squad
Every request executes through structured enterprise personas rather than an unstructured generalist model:
- **Phase 0: Deep Research Specialist**: Real-world evidence, statutory regulations, and prior-art benchmarking.
- **Phase 1: Product Manager**: Scope decomposition, user acceptance criteria, and invariant definitions.
- **Phase 2: System Architect**: Typed schema contracts, state machines, and Architecture Decision Records (ADRs).
- **Phase 3: Adversarial SDET**: Red-first test creation, edge-case probing, concurrency testing, and Playwright verification.
- **Phase 4: Core Engineer**: Idiomatic green implementation in the active domain's dominant tech stack.
- **Phase 5: Mutation & Security Auditor**: AST fault injection (≥ 80% kill rate requirement) and zero-secret scanning.
- **Phase 6: Technical Writer**: Living documentation synchronization and cognitive comprehension dossiers.

### 2. Universal Domain Specialization (8 Domains, 46 Subdomains)
Dynamically hydrates personas, skills, behavioral checks, and compiler toolchains across:
- **Software Engineering**: Full-stack web, distributed systems, mobile, APIs, microservices.
- **AI/ML & MLOps**: Model training, evaluation harnesses, ECE calibration, pipeline automation.
- **Blockchain & Web3**: Smart contracts, DeFi protocols, reentrancy guards, formal verification.
- **Deep Tech & Science**: High-performance compute, scientific modeling, simulation algorithms.
- **Cybersecurity & AppSec**: DAST penetration testing, constant-time cryptography, vulnerability remediation.
- **Cloud Infrastructure & DevOps**: Kubernetes, Terraform, zero-trust networking, CI/CD pipelines.
- **Data Engineering**: High-throughput ETL, stream processing, OLAP analytics, ClickHouse / PostgreSQL.
- **Vertical Applied IT**: Domain-specific compliance, statutory reporting, and enterprise integrations.

### 3. 7-Layer Enterprise Agentic Harness (`active_kernel.py`)
Intercepts execution to ensure system safety, active governance, and continual self-evolution:
- **Layer 1: Safety & Governance**: Microsoft Agent Governance join points (`PERMIT`, `BLOCK`, `MODIFY`, `ESCALATE`). Destructive shell commands (`rm -rf`, `DROP TABLE`, `terraform destroy`, cluster wipes) mandate explicit operator approval (`ESCALATE`).
- **Layer 2: Telemetry & Observability**: AWS Dogwood continuous runtime verification with non-blocking event streaming to audit trails and JSONL telemetry.
- **Layer 3: Context Steering & Reshaping**: Stripe positive error prompt injection and Deep Agents context truncation (35-line maximum output ceiling).
- **Layer 4: In-Flight Verification Loop**: DeepCode real-time AST syntax parsing, zero ghost packages, and zero-raw-LaTeX verification.
- **Layer 5: Continual Self-Evolution**: Trajectory failure signature tracking with empirical recurrence threshold (count ≥ 2 or critical invariant breach) and staging barrier (`.agents/state/evolution_patches/`) with automated operator verification requests.
- **Layer 6: Cognitive Memory Vault**: Hermes Agent SQLite injection retrieving past architectural decisions before execution.
- **Layer 7: Multi-Agent Personas & Domain Contracts**: Omnigent 6+1 agile squad execution with domain lease locking.

### 4. 2-Tier Progressive Skill Disclosure (298 Skills)
- **Tier 1 (Curated Subdomain Skills)**: 172 high-priority slots (104 unique specialist skills) automatically resolved JIT by `SkillResolver` based on active subdomains and prompt intent.
- **Tier 2 (Universal Skill Vault)**: All 298 physical skills in `.agents/skills/` are searchable on demand via `npm run skill:search <query>`.
- **Zero Ghost Skills**: Every referenced skill is physically grounded in verified repository files, with activated skills explicitly reported in execution receipts.

### 5. Tri-Mode Operating Flexibility
- **Solo Mode (`npm run mode:solo`)**: Streamlined single-operator workflow with full persona separation without lease collisions.
- **Dual-Lead Enterprise Mode (`npm run mode:dual`)**: Balanced 50/50 division of responsibility between Lead 1 (Feature Architect) and Lead 2 (Adversarial SDET).
- **Team Mesh Mode (`npm run mode:team`)**: Multi-developer parallel domain leases with Git-native shared state synchronization.

---

## Quickstart

### Prerequisites
- **Node.js**: v20.x or v24.x LTS (with native `--experimental-strip-types`)
- **Python**: 3.11+ or 3.12+
- **Playwright**: Headless Chromium browser automation

### Installation
```bash
# 1. Clone starter template
git clone https://github.com/Deepak-Sharma-2006/script.git my-project
cd my-project

# 2. Install dependencies
npm install

# 3. Install browser binaries for automated testing
npx playwright install chromium

# 4. Synchronize universal agent instructions
npm run harness:sync

# 5. Verify system readiness (all 7 operational layers)
npm run readiness
```

---

## Essential Runbook

### Domain Selection & Stack Diagnostics
```bash
# Check current active domain and hydrated toolchains
npm run domain:status

# Interactive CLI domain questionnaire
npm run domain:select

# Programmatically switch domains and subdomains
npm run domain:set -- --domain blockchain --subdomains smart_contracts,defi_protocols

# Probe required system runtimes and compilers
npm run domain:doctor
```

### Autonomous Task Execution
```bash
# Task 1: First-principles solution formulation, research & economics
python -m scripts.orchestrator.task_dispatcher --task solution --prompt "Autonomous wildfire early detection"

# Task 2: Red-to-green autonomous TDD implementation loop
python -m scripts.orchestrator.task_dispatcher --task code --prompt "Implement rate-limiting token bucket middleware"

# Task 3: Vector presentation pitch deck synthesis
python -m scripts.orchestrator.task_dispatcher --task presentation --prompt "Universal Domain Specialization"
```

### Testing, Quality Gates & Audits
```bash
# Run full orchestrator test suite
pytest tests/ -q

# Run black-box adversarial tests (concurrency races, chaos fuzzing, fault injection)
npm run test:adversarial

# Run Node unit tests & domain-adaptive behavioral evaluations
npm test

# Run AST Mutation Testing Gate (ensures ≥ 80% mutation kill rate)
npm run test:mutation

# Validate documentation compliance (zero raw LaTeX, clean formatting)
npm run lint:markdown docs README.md
```

### Documentation & Memory Vault
```bash
# Synchronize session artifacts into living documentation catalogs
npm run docs:sync

# Reconcile living catalog indexes sorted by timestamp descending
npm run docs:reconcile

# Query the SQLite Memory Vault with domain relevance boosting
npm run memory:search -- --query "reentrancy guards"

# Verify cryptographic squad attestation audit trail
npm run attest:verify
```

---

## Repository Structure

```
.
├── .agents/                    # Governance, state, leases, and skills
│   ├── harness/                # Behavioral eval runner & active interception kernel
│   ├── memory/                 # SQLite Memory Vault (vault.sqlite & JSONL)
│   ├── skills/                 # 298 verified modular skills
│   └── state/                  # Active domain, role, and lock descriptors
├── docs/                       # Living documentation catalogs (PRDs, ADRs, specs)
│   ├── plans/                  # Implementation plans & PRDs
│   ├── walkthroughs/           # Verification proofs & execution walkthroughs
│   ├── audits/                 # Security reviews & system readiness audits
│   ├── decisions/              # Architecture Decision Records (ADRs)
│   ├── research/               # Multi-hop research & competitive analyses
│   └── specifications/         # Typed schema contracts & interfaces
├── scripts/                    # Core TypeScript & Python orchestrators
│   ├── orchestrator/           # TaskDispatcher, SquadOrchestrator, SpecSync
│   ├── domain-selector.ts      # Domain catalog controller & CLI
│   ├── domain-doctor.ts        # Compiler diagnostic probes
│   ├── lock-manager.ts         # Distributed lease locking engine
│   ├── mutation-tester.ts      # Deterministic AST mutation engine
│   └── universal-harness-sync.ts # Cross-agent harness synchronization
├── templates/domains/          # 8 Master Domain rubrics & catalog index
├── tests/                      # Pytest, Node unit, and adversarial test suites
├── UNIVERSAL_AGENT_INSTRUCTIONS.md # Authoritative cross-agent instructions
├── AGENTS.md                   # Universal workspace operational directives & invariants
├── GEMINI.md                   # Pair programming guidelines & 6-persona lifecycle
├── SYSTEM_COMMANDS.md          # Master CLI command reference
└── package.json                # Project dependencies & executable npm scripts
```

---

## License & Compliance

Licensed under the **MIT License**. Strictly enforces the Zero-Hallucination, Zero-Secret Pre-Commit Shield, and Zero-Raw-LaTeX Invariants fail-closed across all CI/CD pipelines, IDE sessions, and headless agent executions.
