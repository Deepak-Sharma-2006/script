# Universal Autonomous Agentic Engineering Platform

> **An enterprise-grade, agent-agnostic multi-agent SDLC orchestration platform. Engineered under the True Pipeline Triple-Mode Architecture (Deep Surge, Multi-Project / Portfolio Multiplexing, Collaborative Team Mode) with closed-loop TDD self-healing, AST mutation testing, and deterministic task dispatching.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-v20%2B%20%7C%20v24%2B-339933.svg?logo=node.js)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-3.11%2B%20%7C%203.12%2B-3776AB.svg?logo=python)](https://python.org)
[![Universal Instructions](https://img.shields.io/badge/Instructions-Claude%20%7C%20Cursor%20%7C%20Windsurf%20%7C%20Copilot%20%7C%20Antigravity-blueviolet.svg)](UNIVERSAL_AGENT_INSTRUCTIONS.md)
[![Operational Verification](https://img.shields.io/badge/Behavioral%20Contracts-100%25%20Verified%20(6%2F6)-success.svg)](specs/benchmark_metrics.json)
[![Self-Healing Score](https://img.shields.io/badge/Closed--Loop%20Self--Healing-95.9%25-brightgreen.svg)](pipeline/scripts/self-healing-engine.ts)

---

## Executive Summary

The **Universal Autonomous Agentic Engineering Platform** provides an end-to-end operational framework for AI-assisted and fully autonomous software development. It eliminates the fragile prompt-and-pray paradigm by introducing structured multi-agent personas, red-first test-driven development, deterministic AST mutation testing, active runtime interception, and automated cross-agent synchronization.

Whether you develop with **Google Antigravity IDE**, **Claude Code**, **Cursor**, **Windsurf**, **GitHub Copilot**, **Codex / Aider**, or run headless scripts in **CI/CD**, this repository acts as a single, authoritative foundation that works identically across all environments with zero vendor lock-in.

---

## 🏆 The 6 Master Operational Super-Features

To eliminate command sprawl and cognitive overload, the entire platform is organized into **6 Master Super-Features**. Each master command encapsulates an entire phase of the enterprise software development lifecycle:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             THE 6 CONSOLIDATED SUPER-FEATURES                                    │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐  ┌──────────────────────────────────────────────┐
 │ 1. WORKSPACE GOVERNANCE KERNEL               │  │ 2. CURATED SKILL & MCP ENGINE                │
 │ Master: npm run governance                   │  │ Master: npm run skill <query>                │
 │ • Operating Modes: Surge, Portfolio, Team     │  │ • 300 Curated Production Skills              │
 │ • Domain Controller: 8 Domains / 46 Subdoms  │  │ • Local JSON-RPC 2.0 Stdio MCP Server       │
 │ • Distributed Lease Locks & Role Handoff     │  │ • JIT Skill Resolution & Drift Shield        │
 │ • Active Interception Runtime Guards         │  │ • Sub-5ms SQLite FTS5 Full-Text Search       │
 └──────────────────────┬───────────────────────┘  └──────────────────────┬───────────────────────┘
                        │                                                 │
                        ▼                                                 ▼
 ┌──────────────────────────────────────────────┐  ┌──────────────────────────────────────────────┐
 │ 3. TRUE PIPELINE TASK DISPATCH               │  │ 4. CLOSED-LOOP SELF-HEALING                  │
 │ Master: npm run squad:run                    │  │ Master: npm run self-heal                    │
 │ • Triple Modes: Surge | Portfolio | Team     │  │ • End-to-End Dynamic Closed-Loop Metric Audit│
 │ • Modular Dispatcher: solution | code | deck │  │ • Deterministic AST Mutation Gates (≥ 80%)   │
 │ • Out-of-Band Worktree Persona Specialization│  │ • Dynamic GroupChat Speaker Routing (AG2)    │
 │ • Deterministic Task DAG Pipeline (CrewAI)   │  │ • Continual Self-Evolution Patches           │
 └──────────────────────┬───────────────────────┘  └──────────────────────┬───────────────────────┘
                        │                                                 │
                        ▼                                                 ▼
 ┌──────────────────────────────────────────────┐  ┌──────────────────────────────────────────────┐
 │ 5. SYSTEM VERIFICATION BATTERY               │  │ 6. WEB WORKBENCH & SPEC SYNC                 │
 │ Master: npm run check                        │  │ Master: npm run workbench                    │
 │ • Parallel Sweep: Secrets + AST + Lints      │  │ • Pre-Commit Web Inspection HUD (Port 3042)  │
 │ • Anti-Hallucination & Anti-Hardcoding Guard │  │ • Zero-Process SpecSync Brain Mirroring      │
 │ • Node Unit Suites (40 suites) + 6 Evals     │  │ • Tree-Sitter AST Repo Map (<1,500 Tokens)   │
 │ • Markdown Zero-Raw-LaTeX Invariant Shield   │  │ • Cline Interactive AST Diff Streamer        │
 └──────────────────────────────────────────────┘  └──────────────────────────────────────────────┘
```

### Executive Master Command Overview

| # | Master Super-Command | Primary Responsibility | Primary Capabilities |
|---|---|---|---|
| **1** | `npm run governance` | System state, leases & mode switching | Operating mode switching (`mode:surge`, `mode:portfolio`, `mode:team`), atomic domain configuration, distributed locking, runtime interception |
| **2** | `npm run skill <query>` | Knowledge retrieval & tool serving | Sub-5ms SQLite FTS5 search across 300 curated skills, on-demand skill inspection, local JSON-RPC MCP server, drift detection |
| **3** | `npm run squad:run` | Autonomous end-to-end SDLC | True Pipeline Triple-Mode execution, first-principles solution formulation, autonomous red-to-green coding, vector pitch decks |
| **4** | `npm run self-heal` | Autonomous defect recovery & audit | 7-stage closed-loop self-healing scorecards, AST mutation testing (≥ 80% kill rate), cyclic state rollback, auto-evolution patches |
| **5** | `npm run check` | Pre-commit security & quality sweep | Zero-secret scanning, anti-hallucination AST checking, anti-hardcoding validation, subdomain compliance, Zero-LaTeX markdown linting |
| **6** | `npm run workbench` | Visual inspection & documentation | Browser HUD on port 3042, real-time brain-to-docs synchronization (`SpecSync`), AST repository call graph, interactive diff streaming |

> 💡 **Exhaustive CLI Execution Runbook**: For the complete reference of all subcommands, parameter flags, CLI options, and operational recipes, consult [SYSTEM_COMMANDS.md](file:///d:/BE_Research/SYSTEM_COMMANDS.md).

---

## 🔄 The True Pipeline Triple-Mode Operational Architecture

The platform operates strictly under the 3 proven operational modes established in the empirical frontier research (Sections 8 and 11 of `AGENTS.md` and `GEMINI.md`), eliminating conversational monologues and simulated waterfall delays:

```
                      THE TRUE PIPELINE TRIPLE-MODE ARCHITECTURE
                                          │
         ┌────────────────────────────────┼────────────────────────────────┐
         ▼                                ▼                                ▼
  ┌─────────────┐                  ┌─────────────┐                  ┌─────────────┐
  │   MODE 1    │                  │   MODE 2    │                  │   MODE 3    │
  │ DEEP SURGE  │                  │  PORTFOLIO  │                  │    TEAM     │
  │npm run      │                  │  MULTIPLEX  │                  │COLLABORATION│
  │mode:surge   │                  │npm run      │                  │npm run      │
  │             │                  │mode:port-   │                  │mode:team    │
  │             │                  │folio        │                  │             │
  └──────┬──────┘                  └──────┬──────┘                  └──────┬──────┘
         │                                │                                │
         ▼                                ▼                                ▼
  4 Worktree Slots                 4 Headless Slots                 Distributed Mesh
  1 Single Project                 Multi-Project Repos              LAN Sync (4040)
  Alpha/Beta/Gamma/Delta           Milestone Runway                 Domain Leases
  Zero Lock Contention             OmniDeck (<0.2s PPTX)            Cognitive Dossiers
```

### 1. Mode 1: Deep Surge (`npm run mode:surge`)
* **Focus**: All 4 Google accounts / developer slots focused exclusively on **1 single flagship project**.
* **Worktree Division**:
  * **Lead 1 Alpha (Strategic Council & Solution Formulation)**: Deconstructs requirements, live research triangulation, architecture contracts, and SQLite Memory Vault indexing.
  * **Lead 2 Beta (Adversarial SDET & Red-Team Testing)**: Authors black-box test suites first (asserted red), fuzzes edge cases, and verifies headless Playwright browser tests.
  * **Account 3 Gamma (Core Engineer & TDD Loop)**: Implements idiomatic business logic, turning red tests green in an autonomous self-healing loop.
  * **Account 4 Delta (Mutation & Hardening Auditor)**: Injects AST mutations (kill rate ≥ 80%), audits cryptographic invariants, and verifies pre-commit shields.

### 2. Mode 2: Multi-Project / Portfolio Multiplexing (`npm run mode:portfolio`)
* **Portfolio Runway**: 4 headless runner slots multiplexed across **multi-project repository portfolios** on disk (`demo/`) on a structured milestone runway.
* **OmniDeck Engine**: Compiles competition-winning pitch decks (<0.2s native PPTX) with 2D Flex/Grid geometry, 7 visual primitives, and cognitive layout density.

### 3. Mode 3: Collaborative Team Mode (`npm run mode:team`)
* **Frictionless Sync**: Seamless multi-developer collaboration via distributed Git domain leases (`.agents/state/locks/`).
* **LAN Synchronization**: Local zero-dependency LAN Sync Server on port 4040 (`npm run lan:start`) providing sub-10ms heartbeat visibility across venue networks.
* **Cognitive Dossiers**: Part 7 6-technique human comprehension dossiers (`docs/dossiers/`) generated at phase handoffs.

### 4. Direct High-Signal Engineering Standard (Rule 15 / Rule 12)
* **Zero Theatrical Monologues**: Interactive chat communicates directly, concisely, and technically. Emitting simulated persona monologue headings in chat is strictly prohibited, saving 1,500 to 2,500 tokens per turn.
* **Physical Worktree Specialization**: Persona specialization is decoupled from chat and executed where it physically matters: in dedicated, out-of-band headless CLI worker lanes operating across isolated Git Worktrees and modular tasks via [TaskDispatcher](file:///d:/BE_Research/pipeline/scripts/orchestrator/task_dispatcher.py).

---

## 🧠 Curated Production Skill Engine (300 Skills)

The platform provides access to **300 curated, production-grade engineering skills** physically maintained under `.agents/skills/` and indexed in high-performance SQLite (`.agents/skills/registry.sqlite`) with sub-5ms FTS5 full-text search:

```
                            CURATED SKILL ENGINE (300 SKILLS)
                                           │
                 ┌─────────────────────────┴─────────────────────────┐
                 ▼                                                   ▼
   ┌───────────────────────────┐                       ┌───────────────────────────┐
   │ 300 IN-TREE SKILLS        │                       │ SQLITE FTS5 SEARCH INDEX  │
   │ .agents/skills/<skill>/   │                       │ Sub-5ms Keyword Matching  │
   │ SHA-256 Drift Shield      │                       │ Zero Token Prompt Leakage │
   └─────────────┬─────────────┘                       └─────────────┬─────────────┘
                 │                                                   │
                 │ JIT Auto-Resolution                               │ Interactive CLI & MCP
                 │ (SkillResolver)                                   │ (npm run skill <query>)
                 ▼                                                   ▼
   ┌───────────────────────────────────────────────────────────────────────────────┐
   │ ACTIVE AGENT PROMPT CONTEXT (Only Curated Specialization Slots Loaded)        │
   └───────────────────────────────────────────────────────────────────────────────┘
```

1. **Curated In-Tree Skills (300 Skills)**:
   Physically maintained under `.agents/skills/`, including 172 high-priority subdomain slots (104 unique specialist skills) automatically resolved JIT by `SkillResolver` based on active domain rubrics. 100% verified against SHA-256 drift baselines.
2. **High-Performance SQLite FTS5 Index**:
   Indexed in `.agents/skills/registry.sqlite` with sub-5ms FTS5 full-text search (`npm run skill <query>`) and zero token footprint until explicitly referenced.
3. **Local Stdio MCP Server**:
   Exposes skill retrieval and inspection over standard Model Context Protocol (JSON-RPC 2.0 stdio) via `npm run mcp:start`.

---

## 🌐 Universal Domain Specialization (8 Domains, 46 Subdomains)

The platform dynamically hydrates specialized personas, curated skill slots, compiler toolchains, and behavioral evaluation contracts across 8 master engineering domains:

```
                          8 MASTER DOMAINS • 46 SUBDOMAINS
                                         │
        ┌───────────────────┬────────────┴────────┬───────────────────┐
        ▼                   ▼                     ▼                   ▼
  ┌───────────┐       ┌───────────┐         ┌───────────┐       ┌───────────┐
  │ SOFTWARE  │       │   AI/ML   │         │BLOCKCHAIN │       │ DEEP TECH │
  │Backend, UI│       │MLOps, RAG │         │DeFi, CEI  │       │HPC, Bio   │
  └─────┬─────┘       └─────┬─────┘         └─────┬─────┘       └─────┬─────┘
        │                   │                     │                   │
        └───────────────────┼─────────────────────┼───────────────────┘
                            │
        ┌───────────────────┼─────────────────────┼───────────────────┐
        ▼                   ▼                     ▼                   ▼
  ┌───────────┐       ┌───────────┐         ┌───────────┐       ┌───────────┐
  │CYBERSEC   │       │CLOUD INFRA│         │DATA ENG   │       │ VERTICAL  │
  │AppSec,DAST│       │K8s, SRE   │         │ETL, Stream│       │Health,Fin │
  └───────────┘       └───────────┘         └───────────┘       └───────────┘
```

---

## 📊 Empirical SLA Benchmark Metrics

Real empirical performance baselines measured and certified by the Behavioral Assertion Engine:

| Metric Category | Target Invariant Threshold | Measured Repository Result | Verification Harness |
|---|---|---|---|
| **AST Mutation Kill Rate** | ≥ 80.0% Kill Rate | **100.0% Killed** (3/3 mutants) | `npm run test:mutation` |
| **Self-Healing Capability** | > 95.0% Recovery Rate | **95.9% Autonomous Healing** | `npm run self-heal` |
| **Self-Improving Memory** | > 85.0% Knowledge Retention | **87.1% Continuous Retention** | `npm run self-heal` |
| **FTS5 Skill Search Latency** | < 50.0ms Query Latency | **0.82ms** (300 curated skill index) | `npm run skill` |
| **Tree-Sitter Repo Map Size** | < 1,500 Token Ceiling | **1,453 Tokens** (5,811 bytes) | `npm run repo:map` |
| **Pre-Commit Secret Scan** | < 1,000ms Execution Time | **290ms** (Full staged sweep) | `npm run check:secrets:staged` |
| **Unified Verification Sweep** | < 15.0s Total Runtime | **7.2s** (6 parallel scanners) | `npm run check` |
| **Node.js Unit Test Suites** | 100% Green Pass Rate | **40 / 40 Passed** (0 failures) | `npm test` |
| **Python Orchestrator Suites** | 100% Green Pass Rate | **131 / 131 Passed** (0 failures) | `pytest pipeline/tests/ -q` |
| **Behavioral Contract Assertions** | 100% Zero Test Theater | **6 / 6 Passed** (0.01ms - 0.43ms) | `npm run harness:eval` |

---

## 🚀 Quickstart & Onboarding

### Prerequisites
- **Node.js**: v20.x or v24.x LTS (with native `--experimental-strip-types`)
- **Python**: 3.11+ or 3.12+
- **Playwright**: Headless Chromium browser automation (`npx playwright install chromium`)

### 1. Installation
```bash
# 1. Clone repository
git clone https://github.com/Deepak-Sharma-2006/script.git my-project
cd my-project

# 2. Install dependencies
npm install

# 3. Execute unified pre-commit verification sweep
npm run check
```

### 2. Daily Developer Workflows

#### Option A: High-Signal Direct Engineering Chat (Recommended)
Simply type your project requirement or feature prompt directly into the IDE chat:
* `"START: Build a high-throughput, low-latency Redis caching cluster"`
* `"BUILD: Sovereign decentralized smart contract with reentrancy protection"`
* `"INNOVATE: Computer vision drone weed segmentation pipeline"`

The agent communicates directly and concisely with zero persona monologue fluff, executing red-to-green TDD with inline AST mutation testing (kill rate ≥ 80%), automatic SpecSync persistence, and empirical receipts.

#### Option B: The True Pipeline Multi-Mode Execution
```bash
# Mode 1: Deep Surge (4 Accounts, 1 Project via Git Worktrees)
npm run mode:surge

# Mode 2: Portfolio Dispatcher (4 Accounts multiplexed across multi-project portfolios)
npm run portfolio:dispatch
powershell pipeline/scripts/portfolio-dispatcher.ps1 -DryRun   # Preview queue and profile assignments

# Mode 3: Collaborative Team Mode (Launch local LAN sync server on port 4040)
npm run lan:start

# Ambient 16 GB RAM Hypervisor & SWE-Agent Output Slicer
npm run hypervisor:status
npm run hypervisor:daemon

# Pre-Commit System Verification Battery
npm run check
```

---

## 📁 Repository Topology & Structural Layout

```
.
├── .agents/                 # IDE rules, skills (300 in-tree), and SQLite Memory Vault
├── docs/                    # Living documentation (plans, walkthroughs, decisions, audits)
├── pipeline/                # The Unified True Pipeline Engineering Engine
│   ├── browser_tests/       # Playwright E2E browser verification
│   ├── demo/                # Multi-project portfolio multiplexing repositories
│   ├── scripts/             # Orchestrator, engines, distributed locks, scanners
│   ├── specs/               # Machine-readable PRD specs, contracts, benchmark metrics
│   ├── templates/           # Domain rubrics, SOP schemas, frontend workbench tokens
│   └── tests/               # Adversarial SDET, unit contracts, regression suites
├── projects/                # User engineering projects & domain workspaces (git-ignored)
├── src/                     # Production business logic & active services
├── package.json             # Consolidated 6-master-command script manifest
├── README.md                # Enterprise product architecture treatise
├── SYSTEM_COMMANDS.md       # Master executable CLI cheat sheet & runbook
└── UNIVERSAL_AGENT_INSTRUCTIONS.md # Single source of truth for all IDE harnesses
```

---

## 🔒 Security & Governance Guarantees

* **Zero-Secret Invariant**: Committing credentials of any kind is strictly forbidden and rejected at pre-commit by `npm run check:secrets:staged`.
* **Zero-Hallucination Policy**: AST imports are verified against `package.json`. Ghost dependencies trigger immediate failure.
* **Deterministic TDD**: All code changes are red-first verified before production implementation.
* **Mutation Survivability**: Code changes must survive AST fault injection with an empirical kill rate ≥ 80.0%.
* **Zero-Raw-LaTeX Invariant**: All documentation strictly enforces clean Unicode typography (`≥`, `≤`, `×`, `≠`, `→`, `≈`) without broken markdown formulas.

---

## 📚 References & Prior-Art Architecture

This platform synthesizes, adapts, and hardens architectural mechanisms and design patterns pioneered across the open-source autonomous agent ecosystem:

1. **All-Hands-AI/OpenHands** — Ephemeral container and process-jail sandbox isolation ([pipeline/scripts/sandbox-runner.ts](file:///d:/BE_Research/pipeline/scripts/sandbox-runner.ts)).
2. **geekan/MetaGPT** — Standard Operating Procedure (SOP) formal artifact schemas for PRD, architecture, and task graphs ([pipeline/templates/sops/sop-validator.ts](file:///d:/BE_Research/pipeline/templates/sops/sop-validator.ts)).
3. **cline/cline** — AST diff streaming and interactive destructive operation permission checkpoints ([pipeline/scripts/diff-streamer.ts](file:///d:/BE_Research/pipeline/scripts/diff-streamer.ts)).
4. **microsoft/autogen (AG2)** — Asynchronous multi-agent GroupChat manager with dynamic speaker routing ([pipeline/scripts/orchestrator/groupchat.py](file:///d:/BE_Research/pipeline/scripts/orchestrator/groupchat.py)).
5. **crewAIInc/crewAI** — Deterministic task DAG orchestration with output schema validation gates ([pipeline/scripts/orchestrator/task_dag_runner.py](file:///d:/BE_Research/pipeline/scripts/orchestrator/task_dag_runner.py)).
6. **RooVetGit/Roo-Code** — Role-based mode tool-whitelist sandboxing ([.agents/modes/](file:///d:/BE_Research/.agents/modes/)).
7. **Aider-AI/aider** — Tree-sitter AST monorepo topology mapping under a strict 1,500 token ceiling ([pipeline/scripts/repo-map-generator.ts](file:///d:/BE_Research/pipeline/scripts/repo-map-generator.ts)).
8. **sickn33/AAS Core** — SQLite FTS5 skill index registry and stdio JSON-RPC 2.0 MCP server architecture ([pipeline/scripts/mcp-server.ts](file:///d:/BE_Research/pipeline/scripts/mcp-server.ts)).
9. **langchain-ai/langgraph** — Cyclic state graphs with persistent SQLite rollback checkpoints ([pipeline/scripts/orchestrator/state_graph.py](file:///d:/BE_Research/pipeline/scripts/orchestrator/state_graph.py)).
10. **agno-agi/agno** — SQLite FTS5 Memory Vault with domain-weighted contextual recall ([pipeline/scripts/memory-vault.ts](file:///d:/BE_Research/pipeline/scripts/memory-vault.ts)).
11. **VoltAgent/awesome-skills** — Standardized agent instruction design patterns ([UNIVERSAL_AGENT_INSTRUCTIONS.md](file:///d:/BE_Research/UNIVERSAL_AGENT_INSTRUCTIONS.md)).
12. **assafelovic/gpt-researcher** — 4-angle statutory and competitive research triangulation ([pipeline/scripts/orchestrator/research_triangulator.py](file:///d:/BE_Research/pipeline/scripts/orchestrator/research_triangulator.py)).
13. **promptfoo/promptfoo** — Automated adversarial black-box test suites and LLM vulnerability probes ([pipeline/scripts/adversarial-suite-runner.ts](file:///d:/BE_Research/pipeline/scripts/adversarial-suite-runner.ts)).
14. **SWE-agent/SWE-agent** — Agent-Computer Interface (ACI) pre-commit syntax validation and guard rails ([pipeline/scripts/aci-guard.ts](file:///d:/BE_Research/pipeline/scripts/aci-guard.ts)).
15. **confident-ai/deepeval** — Deterministic behavioral contract assertion scorecards ([.agents/harness/eval-runner.ts](file:///d:/BE_Research/.agents/harness/eval-runner.ts)).
16. **camel-ai/camel** — Communicative agent persona inception prompting ([pipeline/scripts/orchestrator/squad_orchestrator.py](file:///d:/BE_Research/pipeline/scripts/orchestrator/squad_orchestrator.py)).
17. **e2b-dev/E2B** — Fast-boot microVM execution sandboxing with local mock fallbacks ([pipeline/scripts/sandbox-e2b.ts](file:///d:/BE_Research/pipeline/scripts/sandbox-e2b.ts)).
18. **agent-skills-standard** — Standardized skill specification schema and SHA-256 drift baselines ([pipeline/scripts/skill-validator.ts](file:///d:/BE_Research/pipeline/scripts/skill-validator.ts)).

