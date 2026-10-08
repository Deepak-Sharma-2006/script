# Universal Autonomous Agentic Engineering Platform

> **An enterprise-grade, agent-agnostic multi-agent SDLC orchestration platform. Built to transform any AI coding agent or human engineering team into an autonomous, self-healing 6+1 Agile Product Squad across any development environment.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-v20%2B%20%7C%20v24%2B-339933.svg?logo=node.js)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-3.11%2B%20%7C%203.12%2B-3776AB.svg?logo=python)](https://python.org)
[![Universal Harness](https://img.shields.io/badge/Universal-Claude%20%7C%20Cursor%20%7C%20Windsurf%20%7C%20Copilot%20%7C%20Antigravity-blueviolet.svg)](UNIVERSAL_AGENT_INSTRUCTIONS.md)
[![Operational Verification](https://img.shields.io/badge/Behavioral%20Contracts-100%25%20Verified%20(6%2F6)-success.svg)](specs/benchmark_metrics.json)
[![Self-Healing Score](https://img.shields.io/badge/Closed--Loop%20Self--Healing-95.9%25-brightgreen.svg)](scripts/self-healing-engine.ts)

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
 │ 1. WORKSPACE GOVERNANCE KERNEL               │  │ 2. TIERED SKILL & MCP ENGINE                 │
 │ Master: npm run governance                   │  │ Master: npm run skill <query>                │
 │ • Operating Modes: Solo, Dual, Team Mesh     │  │ • 300 In-Tree + 2,622 SQLite FTS5 Registry   │
 │ • Domain Controller: 8 Domains / 46 Subdoms  │  │ • Local JSON-RPC 2.0 Stdio MCP Server       │
 │ • Distributed Lease Locks & Role Handoff     │  │ • JIT Skill Resolution & Drift Shield        │
 │ • Universal Sync: Cursor/Claude/Agy/Copilot  │  │ • Lazy On-Demand Materialization             │
 └──────────────────────┬───────────────────────┘  └──────────────────────┬───────────────────────┘
                        │                                                 │
                        ▼                                                 ▼
 ┌──────────────────────────────────────────────┐  ┌──────────────────────────────────────────────┐
 │ 3. 6+1 AGILE SQUAD & DISPATCH                │  │ 4. CLOSED-LOOP SELF-HEALING                  │
 │ Master: npm run squad:run                    │  │ Master: npm run self-heal                    │
 │ • Multi-Persona SDLC: PM → Arch → SDET...    │  │ • End-to-End Metric Audit (95.9% / 87.1%)    │
 │ • Modular Dispatcher: solution | code | deck │  │ • Deterministic AST Mutation Gates (≥ 80%)   │
 │ • Dynamic GroupChat Speaker Routing (AG2)    │  │ • LangGraph Cyclic State Graph & Rollback    │
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
| **1** | `npm run governance` | System state, leases & harness sync | Operating mode switching (`solo`, `dual`, `team`), atomic domain configuration, distributed locking, universal rule synchronization |
| **2** | `npm run skill <query>` | Knowledge retrieval & tool serving | Sub-5ms SQLite FTS5 search across 2,922 skills, on-demand skill materialization, local JSON-RPC MCP server, drift detection |
| **3** | `npm run squad:run` | Autonomous end-to-end SDLC | Full 6+1 Agile Squad lifecycle, first-principles solution formulation, autonomous red-to-green coding, vector pitch decks |
| **4** | `npm run self-heal` | Autonomous defect recovery & audit | 7-stage closed-loop self-healing scorecards, AST mutation testing (≥ 80% kill rate), cyclic state rollback, auto-evolution patches |
| **5** | `npm run check` | Pre-commit security & quality sweep | Zero-secret scanning, anti-hallucination AST checking, anti-hardcoding validation, subdomain compliance, Zero-LaTeX markdown linting |
| **6** | `npm run workbench` | Visual inspection & documentation | Browser HUD on port 3042, real-time brain-to-docs synchronization (`SpecSync`), AST repository call graph, interactive diff streaming |

> 💡 **Exhaustive CLI Execution Runbook**: For the complete reference of all subcommands, parameter flags, CLI options, and operational recipes, consult [SYSTEM_COMMANDS.md](file:///d:/BE_Research/SYSTEM_COMMANDS.md).

---

## 🔄 Universal Cross-Harness Interoperability

All agent instruction surfaces are generated from a single, authoritative root contract: [UNIVERSAL_AGENT_INSTRUCTIONS.md](file:///d:/BE_Research/UNIVERSAL_AGENT_INSTRUCTIONS.md). This guarantees that every AI assistant adheres to the exact same enterprise standards, zero-secret gates, and architectural constraints:

```
                          UNIVERSAL INSTRUCTION MATRIX
                                       │
                 ┌─────────────────────┴─────────────────────┐
                 ▼                                           ▼
   ┌───────────────────────────┐               ┌───────────────────────────┐
   │ UNIVERSAL_AGENT_INSTRUCT- │               │ .agents/rules/ & skills/  │
   │ IONS.md (Root Contract)   │               │ (Domain Specialization)   │
   └─────────────┬─────────────┘               └─────────────┬─────────────┘
                 │                                           │
                 └─────────────────────┬─────────────────────┘
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │ scripts/universal-harness-sync.ts │
                     └─────────────────┬─────────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
 ┌───────────────┐             ┌───────────────┐             ┌───────────────┐
 │  CLAUDE.md    │             │ .cursorrules  │             │.windsurfrules │
 │ (Claude Code) │             │   (Cursor)    │             │  (Windsurf)   │
 └───────────────┘             └───────────────┘             └───────────────┘
         │                             │                             │
         └─────────────────────────────┼─────────────────────────────┘
                                       │
         ┌─────────────────────────────┴─────────────────────────────┐
         ▼                                                           ▼
 ┌───────────────────────────────┐           ┌───────────────────────────────┐
 │ .github/copilot-instructions  │           │ AGENTS.md & GEMINI.md         │
 │       (GitHub Copilot)        │           │     (Google Antigravity)      │
 └───────────────────────────────┘           └───────────────────────────────┘
```

| Environment | Integration Surface | Configuration & Sync |
| :--- | :--- | :--- |
| **Google Antigravity** | Native `AGENTS.md` & `GEMINI.md` | Automatically discovered from repository root |
| **Claude Code** | `CLAUDE.md` / CLI | Directly ingests root instructions or via `--system-prompt` |
| **Cursor** | `.cursorrules` / *Rules for AI* | Generated from universal instructions via `npm run harness:sync` |
| **Windsurf / Cascade** | `.windsurfrules` / *Cascade Rules* | Generated from universal instructions via `npm run harness:sync` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Generated from universal instructions via `npm run harness:sync` |
| **Codex / Aider / OpenHands** | System Prompt / Startup Config | Direct markdown ingestion from repository root |
| **Headless CLI / CI/CD** | `python -m scripts.orchestrator.task_dispatcher` | Deterministic headless task execution |

---

## 👥 The 6+1 Agile Product Squad

Rather than relying on unstructured generalist prompting, every software change executes through structured enterprise personas with differentiated temperature, reasoning effort, and validation boundaries:

```
                           THE 6+1 PERSONA EXECUTION LIFECYCLE
                                            │
                                            ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────┐
 │ PHASE 0: DEEP RESEARCH SPECIALIST (temp: 0.3, effort: high)                          │
 │ Multi-hop statutory research, IEEE literature, CVE audits & commercial prior-art     │
 └──────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────┐
 │ PHASE 1: PRODUCT MANAGER (temp: 0.7, effort: medium)                                 │
 │ Deconstructs problem statement into Functional PRD, user journeys & forbidden states │
 └──────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────┐
 │ PHASE 2: SYSTEM ARCHITECT (temp: 0.2, effort: high)                                  │
 │ Emits typed interface contracts, FSM state machines & Claude Council Hardening (ADRs)│
 └──────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────┐
 │ PHASE 3: ADVERSARIAL SDET (temp: 0.8, effort: high)                                  │
 │ Authors black-box tests FIRST; verifies RED phase before implementation starts        │
 └──────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────┐
 │ PHASE 4: CORE ENGINEER (temp: 0.1, effort: medium)                                   │
 │ Implements idiomatic business logic; turns RED tests GREEN in closed feedback loop    │
 └──────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────┐
 │ PHASE 5: MUTATION & SECURITY AUDITOR (temp: 0.0, effort: low)                        │
 │ Injects AST mutations (≥ 80% kill requirement); verifies Zero-Secret Shield          │
 └──────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────┐
 │ PHASE 6: TECHNICAL WRITER (temp: 0.4, effort: low)                                   │
 │ Synthesizes Part 7 6-Technique Comprehension Dossier; mirrors brain artifacts         │
 └───────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Tiered Progressive Skill Architecture (2,922 Skills)

The platform provides access to **2,922 production-grade skills** while preserving strict context window economy:

```
                              TIERED SKILL ARCHITECTURE
                                          │
                 ┌────────────────────────┴────────────────────────┐
                 ▼                                                 ▼
   ┌───────────────────────────┐                     ┌───────────────────────────┐
   │ TIER 1: IN-TREE CANONICAL │                     │ TIER 2: COMPILED SQLITE   │
   │ 300 Hardened Skills       │                     │ 2,622 Production Skills   │
   │ .agents/skills/<skill>/   │                     │ .agents/skills/registry.db│
   │ SHA-256 Drift Shield      │                     │ Zero Token Prompt Footprint│
   └─────────────┬─────────────┘                     └─────────────┬─────────────┘
                 │                                                 │
                 │ JIT Auto-Resolution                             │ On-Demand Lazy Materialization
                 │ (SkillResolver)                                 │ (npm run skill:install <name>)
                 ▼                                                 ▼
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │ ACTIVE AGENT PROMPT CONTEXT (Only Curated Specialization Slots Loaded)      │
   └─────────────────────────────────────────────────────────────────────────────┘
```

1. **Tier 1 (In-Tree Canonical Skills — 300 Skills)**:
   Physically maintained under `.agents/skills/`, including 172 high-priority subdomain slots (104 unique specialist skills) automatically resolved JIT by `SkillResolver` based on active domain rubrics. 100% verified against SHA-256 drift baselines.
2. **Tier 2 (Compiled SQLite Registry — 2,622 Skills)**:
   Indexed in `.agents/skills/registry.sqlite` (2,922 total skills, 27 MB self-contained with full markdown content) with sub-5ms FTS5 full-text search (`npm run skill <query>`) and zero token footprint.
3. **Lazy On-Demand Materialization**:
   Any Tier 2 skill can be materialized into Tier 1 on-demand via `npm run skill:install <name>` or over the local stdio MCP server (`skills_install`).

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
| **FTS5 Skill Search Latency** | < 50.0ms Query Latency | **0.82ms** (2,922 skill index) | `npm run skill` |
| **Tree-Sitter Repo Map Size** | < 1,500 Token Ceiling | **1,453 Tokens** (5,811 bytes) | `npm run repo:map` |
| **Pre-Commit Secret Scan** | < 1,000ms Execution Time | **290ms** (Full staged sweep) | `npm run check:secrets:staged` |
| **Unified Verification Sweep** | < 15.0s Total Runtime | **7.2s** (6 parallel scanners) | `npm run check` |
| **Node.js Unit Test Suites** | 100% Green Pass Rate | **40 / 40 Passed** (0 failures) | `npm test` |
| **Python Orchestrator Suites** | 100% Green Pass Rate | **99 / 99 Passed** (0 failures) | `pytest tests/ -q` |
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

# 3. Synchronize universal agent instructions across IDEs
npm run harness:sync

# 4. Execute unified pre-commit verification sweep
npm run check
```

### 2. Daily Developer Workflows

#### Option A: Ambient IDE Chat Kickoff (Recommended)
Simply type your project requirement or feature prompt directly into the IDE chat:
* `"START: Build a high-throughput, low-latency Redis caching cluster"`
* `"BUILD: Sovereign decentralized smart contract with reentrancy protection"`
* `"INNOVATE: Computer vision drone weed segmentation pipeline"`

The agent autonomously resolves skills, runs the 6-persona lifecycle, hardens architecture via Claude Council, executes red-to-green TDD, and emits an empirical attestation receipt with zero human micromanagement.

#### Option B: Headless Master CLI Execution
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

## 📁 Repository Topology & Structural Layout

```
.
├── .agents/
│   ├── harness/             # Behavioral assertion runner (eval-runner.ts, active_kernel.py)
│   ├── memory/              # SQLite FTS5 Memory Vault (vault.sqlite)
│   ├── modes/               # Role-based tool whitelists (architect, sdet, core, docs)
│   ├── rules/               # Immutable operational rules (anti-hallucination, security)
│   ├── skills/              # Tier 1 in-tree skills (300) & SQLite registry (2,922 skills)
│   └── state/               # Active domain, active role, and skill drift baselines
├── docs/
│   ├── architecture/        # Production architecture blueprints & reference specs
│   ├── audits/              # Pre-commit audits & adversarial penetration reports
│   ├── decisions/           # Architecture Decision Records (ADRs)
│   ├── plans/               # Feature implementation plans
│   ├── specifications/      # Typed interface contracts & PRD schemas
│   └── walkthroughs/        # Verified execution walkthroughs
├── scripts/
│   ├── orchestrator/        # TaskDispatcher, GroupChat, StateGraph, DAG runner, SpecSync
│   ├── catalog-compiler.ts  # SQLite FTS5 skill registry compiler & installer
│   ├── repo-map-generator.ts# Tree-sitter AST monorepo topology mapper
│   ├── role-switch.ts       # Tri-mode operating switcher (solo, dual, team)
│   ├── secret-scanner.ts    # Pre-commit zero-secret scanner
│   ├── self-healing-engine.ts# Closed-loop healing auditor & fixture synthesizer
│   ├── skill-validator.ts   # Schema validator & SHA-256 drift shield
│   └── workbench-server.ts  # Pre-commit Web Workbench server (Port 3042)
├── templates/
│   ├── sops/                # Standard Operating Procedure JSON schemas (PRD, Architecture)
│   └── workbench/           # Web Workbench 3-tier inspection HUD
├── tests/
│   ├── adversarial/         # Black-box penetration, fuzzing & race suites (Lead 2 SDET)
│   ├── regression/          # Synthesized regression fixtures from historical incidents
│   ├── sota-18-ingestion.test.ts # Operational test suite for 18 upstream SOTA components
│   └── sota-milestones.test.ts   # Multi-tier verification suite
├── package.json             # Consolidated 6-master-command script manifest
├── README.md                # Flagship enterprise product architecture treatise
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

1. **All-Hands-AI/OpenHands** — Ephemeral container and process-jail sandbox isolation ([scripts/sandbox-runner.ts](file:///d:/BE_Research/scripts/sandbox-runner.ts)).
2. **geekan/MetaGPT** — Standard Operating Procedure (SOP) formal artifact schemas for PRD, architecture, and task graphs ([templates/sops/sop-validator.ts](file:///d:/BE_Research/templates/sops/sop-validator.ts)).
3. **cline/cline** — AST diff streaming and interactive destructive operation permission checkpoints ([scripts/diff-streamer.ts](file:///d:/BE_Research/scripts/diff-streamer.ts)).
4. **microsoft/autogen (AG2)** — Asynchronous multi-agent GroupChat manager with dynamic speaker routing ([scripts/orchestrator/groupchat.py](file:///d:/BE_Research/scripts/orchestrator/groupchat.py)).
5. **crewAIInc/crewAI** — Deterministic task DAG orchestration with output schema validation gates ([scripts/orchestrator/task_dag_runner.py](file:///d:/BE_Research/scripts/orchestrator/task_dag_runner.py)).
6. **RooVetGit/Roo-Code** — Role-based mode tool-whitelist sandboxing ([.agents/modes/](file:///d:/BE_Research/.agents/modes/)).
7. **Aider-AI/aider** — Tree-sitter AST monorepo topology mapping under a strict 1,500 token ceiling ([scripts/repo-map-generator.ts](file:///d:/BE_Research/scripts/repo-map-generator.ts)).
8. **sickn33/AAS Core** — SQLite FTS5 skill index registry and stdio JSON-RPC 2.0 MCP server architecture ([scripts/mcp-server.ts](file:///d:/BE_Research/scripts/mcp-server.ts)).
9. **langchain-ai/langgraph** — Cyclic state graphs with persistent SQLite rollback checkpoints ([scripts/orchestrator/state_graph.py](file:///d:/BE_Research/scripts/orchestrator/state_graph.py)).
10. **agno-agi/agno** — SQLite FTS5 Memory Vault with domain-weighted contextual recall ([scripts/memory-vault.ts](file:///d:/BE_Research/scripts/memory-vault.ts)).
11. **VoltAgent/awesome-skills** — Universal cross-harness instruction synthesis matrix ([UNIVERSAL_AGENT_INSTRUCTIONS.md](file:///d:/BE_Research/UNIVERSAL_AGENT_INSTRUCTIONS.md)).
12. **assafelovic/gpt-researcher** — 4-angle statutory and competitive research triangulation ([scripts/orchestrator/research_triangulator.py](file:///d:/BE_Research/scripts/orchestrator/research_triangulator.py)).
13. **promptfoo/promptfoo** — Automated adversarial black-box test suites and LLM vulnerability probes ([scripts/adversarial-suite-runner.ts](file:///d:/BE_Research/scripts/adversarial-suite-runner.ts)).
14. **SWE-agent/SWE-agent** — Agent-Computer Interface (ACI) pre-commit syntax validation and guard rails ([scripts/aci-guard.ts](file:///d:/BE_Research/scripts/aci-guard.ts)).
15. **confident-ai/deepeval** — Deterministic behavioral contract assertion scorecards ([.agents/harness/eval-runner.ts](file:///d:/BE_Research/.agents/harness/eval-runner.ts)).
16. **camel-ai/camel** — Communicative agent persona inception prompting ([scripts/orchestrator/squad_orchestrator.py](file:///d:/BE_Research/scripts/orchestrator/squad_orchestrator.py)).
17. **e2b-dev/E2B** — Fast-boot microVM execution sandboxing with local mock fallbacks ([scripts/sandbox-e2b.ts](file:///d:/BE_Research/scripts/sandbox-e2b.ts)).
18. **agent-skills-standard** — Standardized skill specification schema and SHA-256 drift baselines ([scripts/skill-validator.ts](file:///d:/BE_Research/scripts/skill-validator.ts)).

