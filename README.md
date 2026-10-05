# Universal Autonomous Agentic Engineering Platform

An enterprise-grade, agent-agnostic multi-agent SDLC orchestration framework. Built to transform any AI coding agent or human engineering team into an autonomous, self-healing **6+1 Agile Product Squad** across any development environment.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-v20%2B%20%7C%20v24%2B-339933.svg?logo=node.js)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-3.11%2B%20%7C%203.12%2B-3776AB.svg?logo=python)](https://python.org)
[![Universal Harness](https://img.shields.io/badge/Universal-Claude%20%7C%20Cursor%20%7C%20Windsurf%20%7C%20Copilot%20%7C%20Antigravity-blueviolet.svg)](UNIVERSAL_AGENT_INSTRUCTIONS.md)

---

## 🏆 The 6 Master Commands & Operational Hierarchy

The entire workspace command surface is consolidated into **6 Unified Master Commands**, eliminating command bloat and providing clean, intuitive developer ergonomics:

```bash
# 1. WORKSPACE GOVERNANCE KERNEL (Mode, Active Domain, Leases, Universal Sync)
npm run governance

# 2. TIERED SKILL & MCP ENGINE (Search 2,922 skills via SQLite FTS5, Materialize & Validate)
npm run skill <query>

# 3. 6+1 AGILE SQUAD & DISPATCH (Full Autonomous SDLC: PM -> Arch -> SDET -> Code -> Audit -> Writer)
npm run squad:run

# 4. CLOSED-LOOP SELF-HEALING (Score Healing Metrics, Run Mutation Tests, Review Patches)
npm run self-heal

# 5. UNIFIED SYSTEM VERIFICATION BATTERY (Parallel Sweep: Secrets + AST + Hardcoding + Subdomains + Markdown)
npm run check

# 6. WEB WORKBENCH & SPEC SYNC (Launch Inspection HUD on port 3042, Sync Docs, AST Repo Map)
npm run workbench
```

### Master Command to Subcommand Mapping:

| # | Master Command | Purpose | Primary Subcommands |
|---|---|---|---|
| **1** | `npm run governance` | Mode, locks, domains, sync | `npm run mode:[solo\|dual\|team]`, `npm run domain:[status\|list\|set]`, `npm run lock:[status\|acquire\|release]`, `npm run harness:sync` |
| **2** | `npm run skill <query>` | Tiered skill search & MCP | `npm run skill:install <name>`, `npm run mcp:start`, `npm run check:skills`, `npm run check:skills:drift`, `npm run catalog:compile` |
| **3** | `npm run squad:run` | Multi-persona SDLC dispatch | `python -m scripts.orchestrator.task_dispatcher [--task solution\|code\|presentation\|audit\|memory]`, `scripts/orchestrator/groupchat.py` |
| **4** | `npm run self-heal` | Closed-loop auto-healing | `npm run self-heal:audit`, `npm run test:mutation`, `python -m scripts.orchestrator.state_graph`, `npm run evolution:list` |
| **5** | `npm run check` | Pre-commit verification sweep | `npm test`, `npm run check:secrets`, `npm run check:hallucinations`, `npm run check:anti-hardcoding`, `npm run lint:markdown`, `npm run readiness` |
| **6** | `npm run workbench` | Web HUD & SpecSync | `npm run docs:sync`, `npm run docs:watch`, `npm run docs:reconcile`, `npm run repo:map`, `npm run context:check`, `npm run attest:telemetry` |

---

## 🏛️ 18/18 Upstream SOTA Ingestion Architecture

Every mechanism analyzed across the 18 industry-leading agentic repositories is **100% delivered, physically present, and operational** in the codebase:

| # | Upstream Repository | Delivered In-Tree Mechanism | Target Implementation Path | Operational Status |
|---|---|---|---|:---:|
| 1 | `All-Hands-AI/OpenHands` (81.1k) | Ephemeral Container & Process Jail Sandbox | [scripts/sandbox-runner.ts](file:///d:/BE_Research/scripts/sandbox-runner.ts) | 🟢 **100% Operational** |
| 2 | `geekan/MetaGPT` (70.7k) | SOP Schemas (PRD, Architecture, Sequence) | [templates/sops/sop-validator.ts](file:///d:/BE_Research/templates/sops/sop-validator.ts) | 🟢 **100% Operational** |
| 3 | `cline/cline` (69.9k) | AST Diff Streaming & Permission Checkpoints | [scripts/diff-streamer.ts](file:///d:/BE_Research/scripts/diff-streamer.ts) | 🟢 **100% Operational** |
| 4 | `microsoft/autogen - AG2` (61.3k) | Asynchronous GroupChat & Dynamic Speaker Routing | [scripts/orchestrator/groupchat.py](file:///d:/BE_Research/scripts/orchestrator/groupchat.py) | 🟢 **100% Operational** |
| 5 | `crewAIInc/crewAI` (59.4k) | Deterministic Task DAG with Output Validation | [scripts/orchestrator/task_dag_runner.py](file:///d:/BE_Research/scripts/orchestrator/task_dag_runner.py) | 🟢 **100% Operational** |
| 6 | `RooVetGit/Roo-Code` (50.0k) | Role-Based Mode Tool Whitelist Sandboxing | [.agents/modes/](file:///d:/BE_Research/.agents/modes/) (`architect.json`, `sdet.json`) | 🟢 **100% Operational** |
| 7 | `Aider-AI/aider` (49.4k) | Tree-Sitter AST Repo Map (<1,500 token ceiling) | [scripts/repo-map-generator.ts](file:///d:/BE_Research/scripts/repo-map-generator.ts) | 🟢 **100% Operational** |
| 8 | `sickn33/AAS Core` (47.1k) | 2,922 Skill SQLite FTS5 Registry & Stdio MCP | [scripts/mcp-server.ts](file:///d:/BE_Research/scripts/mcp-server.ts) & [workbench-server.ts](file:///d:/BE_Research/scripts/workbench-server.ts) | 🟢 **100% Operational** |
| 9 | `langchain-ai/langgraph` (42.7k) | Cyclic State Graph with SQLite Rollback | [scripts/orchestrator/state_graph.py](file:///d:/BE_Research/scripts/orchestrator/state_graph.py) | 🟢 **100% Operational** |
| 10 | `agno-agi/agno` (42.6k) | SQLite FTS5 Memory Vault with Domain Boosting | [scripts/memory-vault.ts](file:///d:/BE_Research/scripts/memory-vault.ts) | 🟢 **100% Operational** |
| 11 | `VoltAgent/awesome-skills` (35.2k) | Universal Cross-Harness Instruction Matrix | [UNIVERSAL_AGENT_INSTRUCTIONS.md](file:///d:/BE_Research/UNIVERSAL_AGENT_INSTRUCTIONS.md) | 🟢 **100% Operational** |
| 12 | `assafelovic/gpt-researcher` (30k) | 4-Angle Multi-Hop Research Triangulator | [scripts/orchestrator/research_triangulator.py](file:///d:/BE_Research/scripts/orchestrator/research_triangulator.py) | 🟢 **100% Operational** |
| 13 | `promptfoo/promptfoo` (25.7k) | Adversarial Suite Runner & Pentesting Gates | [scripts/adversarial-suite-runner.ts](file:///d:/BE_Research/scripts/adversarial-suite-runner.ts) | 🟢 **100% Operational** |
| 14 | `SWE-agent/SWE-agent` (20.5k) | ACI Pre-Commit Syntax & Bracket Validation | [scripts/aci-guard.ts](file:///d:/BE_Research/scripts/aci-guard.ts) | 🟢 **100% Operational** |
| 15 | `confident-ai/deepeval` (18.6k) | Deterministic Behavioral Assertions & SLA Cards | [.agents/harness/eval-runner.ts](file:///d:/BE_Research/.agents/harness/eval-runner.ts) | 🟢 **100% Operational** |
| 16 | `camel-ai/camel` (17.7k) | 6+1 Agile Persona Inception Prompting | [scripts/orchestrator/squad_orchestrator.py](file:///d:/BE_Research/scripts/orchestrator/squad_orchestrator.py) | 🟢 **100% Operational** |
| 17 | `e2b-dev/E2B` (14.2k) | Fast-Boot MicroVM Runner (<200ms local mock) | [scripts/sandbox-e2b.ts](file:///d:/BE_Research/scripts/sandbox-e2b.ts) | 🟢 **100% Operational** |
| 18 | `agent-skills-standard` (0.6k) | Skill Spec Schema & SHA-256 Drift Shield | [scripts/skill-validator.ts](file:///d:/BE_Research/scripts/skill-validator.ts) | 🟢 **100% Operational** |

---

## Universal Agent Harness Compatibility

All agent-specific instruction surfaces are synchronized and validated from a single source of truth ([UNIVERSAL_AGENT_INSTRUCTIONS.md](file:///d:/BE_Research/UNIVERSAL_AGENT_INSTRUCTIONS.md)), ensuring zero instruction drift across tooling:

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
     │  (300 Tier 1 Skills)  │                       │ 6 Specialized Personas│
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

### 3. Tiered Progressive Skill Architecture (2,900+ Skills)
- **Tier 1 (In-Tree Canonical Skills)**: 300 hardened in-tree skills physically maintained in `.agents/skills/`, including 172 high-priority subdomain slots (104 unique specialist skills) automatically resolved JIT by `SkillResolver` based on active domain rubrics and prompt intent. 100% verified against SHA-256 drift baselines and Zero-Raw-LaTeX standards.
- **Tier 2 (Compiled SQLite Skill Registry)**: 2,622+ catalog skills indexed in `.agents/skills/registry.sqlite` (2,922 total indexed skills across 12 high-level categories) with sub-millisecond FTS5 search (`npm run skill <query>`) and zero prompt token footprint.
- **Lazy On-Demand Materialization**: Any Tier 2 skill can be materialized into Tier 1 on demand via `npm run skill:install <name>` or via the local JSON-RPC stdio MCP server (`skills_install`).
- **Zero Ghost Skills**: Every referenced skill is physically grounded in verified repository files or the SQLite registry, with activated skills explicitly reported in cryptographic execution receipts.

### 4. Tri-Mode Operating Flexibility
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
# 1. Clone repository
git clone https://github.com/Deepak-Sharma-2006/script.git my-project
cd my-project

# 2. Install dependencies
npm install

# 3. Install browser binaries for automated testing
npx playwright install chromium

# 4. Synchronize universal agent instructions across IDEs
npm run harness:sync

# 5. Execute unified pre-commit verification sweep
npm run check
```

---

## Daily Developer Workflows

### Option A: Ambient IDE Chat Kickoff (Recommended)
Simply type your project requirement or feature prompt directly into the IDE chat:
* `"START: Build a high-throughput, low-latency Redis caching cluster"`
* `"BUILD: Sovereign decentralized smart contract with reentrancy protection"`
* `"INNOVATE: Computer vision drone weed segmentation pipeline"`

The agent autonomously resolves skills, runs the 6-persona lifecycle, hardens architecture via Claude Council, executes red-to-green TDD, and emits an empirical attestation receipt with zero human micromanagement.

### Option B: Headless Terminal Execution
```bash
# 1. Inspect workspace governance, active domain, and mode
npm run governance

# 2. Search skills across the 2,922 SQLite registry
npm run skill docker

# 3. Dispatch end-to-end agile squad lifecycle
npm run squad:run

# 4. Run closed-loop self-healing audit and mutation gates
npm run self-heal

# 5. Run unified verification battery
npm run check

# 6. Launch pre-commit Web Workbench HUD on port 3042
npm run workbench
```

---

## Testing & Quality Certification

```bash
# 1. Full Node unit test suite (34 suites) + 6 behavioral eval contracts
npm test

# 2. Python orchestrator & multi-agent test suite (99 suites)
pytest tests/ -q

# 3. SOTA Ingestion & Operational Readiness Suite (OpenHands, MetaGPT, Cline, E2B, SWE-agent)
npx tsx --test tests/sota-18-ingestion.test.ts

# 4. Deterministic AST Mutation Testing (≥ 80% kill rate requirement)
npm run test:mutation

# 5. Pre-Commit Verification Sweep (Secrets + AST + Hardcoding + Subdomain + Markdown)
npm run check
```
