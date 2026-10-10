# Antigravity Enterprise — Master Command Cheat Sheet & Developer Runbook

> **Executive Reference**: Consolidated 6-Super-Feature Command Hierarchy & Developer Runbook.  
> **Architectural Overview**: For the complete system architecture, operational benchmarks, and design pillars, refer to [README.md](file:///d:/BE_Research/README.md).

---

## 🏆 The 6 Master Commands (Executive Summary)

The entire workspace command surface is consolidated into **6 Unified Master Commands**, eliminating command sprawl:

```bash
# 1. WORKSPACE GOVERNANCE KERNEL (Mode, Active Domain, Leases, Runtime Interception)
npm run governance

# 2. CURATED SKILL & MCP ENGINE (Search 300 curated skills via SQLite FTS5, Materialize & Validate)
npm run skill <query>

# 3. TRUE PIPELINE TASK DISPATCH (Autonomous SDLC: Solution Formulation -> TDD Loop -> Presentation Pitch)
npm run squad:run

# 4. CLOSED-LOOP SELF-HEALING (Score Healing Metrics, Run Mutation Tests, Review Patches)
npm run self-heal

# 5. UNIFIED SYSTEM VERIFICATION BATTERY (Parallel Sweep: Secrets + AST + Hardcoding + Subdomains + Markdown)
npm run check

# 6. WEB WORKBENCH & SPEC SYNC (Launch Inspection HUD on port 3042, Sync Docs, AST Repo Map)
npm run workbench
```

---

## 0. Ambient IDE Chat Kickoff (Zero Terminal Commands)

You can trigger the entire agentic pipeline directly from chat with zero manual terminal commands:

```bash
# ==============================================================================
# AMBIENT IDE CHAT KICKOFF (Zero Human Babysitting)
# ==============================================================================
# Simply enter your project intent or feature requirement into the Antigravity chat:
#   Example 1: "START: Build a high-throughput, low-latency Redis caching cluster"
#   Example 2: "BUILD: Sovereign decentralized smart contract with reentrancy protection"
#   Example 3: "INNOVATE: Computer vision drone weed segmentation pipeline"
#   Example 4: Use slash commands: /goal <project> or /plan <feature>
#
# Ambient Autonomous Execution Workflow:
#   1. PromptHygiene extracts domain intent and injects the 4 KB Core Kernel.
#   2. SkillResolver programmatically cites relevant skills from the 300 curated registry.
#   3. Direct High-Signal Engineering: Modular task execution via TaskDispatcher (Rule 15, zero in-chat monologues).
#   4. claude-council 5-perspective hardening is automatically applied to architectural designs.
#   5. SpecSync automatically mirrors brain artifacts to docs/plans/ and docs/walkthroughs/.
#   6. SquadAttestor concludes each turn with a verified cryptographic attestation receipt.
```

---

## 1. Super-Feature 1: Workspace Governance Kernel (`npm run governance`)

Manages operating modes, domain specializations, and distributed lease locks.

```bash
# MASTER COMMAND: Inspect Active Mode, Leases, Operator Profile, and Locks
npm run governance

# ------------------------------------------------------------------------------
# SUBCOMMANDS: OPERATING MODES & LEASE LOCKS
# ------------------------------------------------------------------------------
# Mode 1: Deep Surge (All 4 Google accounts focused on 1 single project)
npm run mode:surge

# Mode 2: Multi-Project / Portfolio Multiplexing (4 runner slots multiplexed across repos)
npm run mode:portfolio

# Mode 3: Collaborative Team Mode (LAN Port 4040, 6-technique dossiers, living catalog sync)
npm run mode:team

# Start Local LAN Synchronization Server (Port 4040)
npm run lan:start

# Inspect Operating Mode Status
npm run mode:status

# Acquire Exclusive Domain Lease (Prevents collision across developers)
npm run lock:acquire --domain <domain-name>
npm run lock:acquire --domain auth --duration 30

# Release Domain Lease
npm run lock:release --domain <domain-name>

# Inspect Active Distributed Locks
npm run lock:status

# Perform Atomic Role Handoff (Alpha -> Beta rotation with secret audit)
npm run role:handoff --domain <domain-name>

# ------------------------------------------------------------------------------
# SUBCOMMANDS: DOMAIN & SUBDOMAIN SPECIALIZATION
# ------------------------------------------------------------------------------
# Inspect Active Domain, Subdomains, Stack, and Injected Curated Skills
npm run domain:status

# List All 8 Master Domains and 46 Subdomains
npm run domain:list

# Interactive CLI Domain Selector (Terminal Questionnaire)
npm run domain:select

# Headless Atomic Domain Configuration
npm run domain:set -- --domain blockchain --subdomains smart_contracts,defi_protocols
npm run domain:set -- --domain software --subdomains backend_systems,web_frontend
npm run domain:set -- --domain ai_ml --subdomains agentic_ai,mlops_inference
npm run domain:set -- --domain cybersecurity --subdomains appsec_devsecops,zero_trust_network
npm run domain:set -- --domain deep_tech --subdomains hpc_supercomputing,computational_biology
npm run domain:set -- --domain cloud_infra --subdomains kubernetes_cloud_native,sre_observability
npm run domain:set -- --domain data_engineering --subdomains stream_processing,lakehouse_warehousing
npm run domain:set -- --domain vertical_applied --subdomains healthtech_informatics,fintech_banking

# ------------------------------------------------------------------------------
# SUBCOMMANDS: RUNTIME INTERCEPTION KERNEL
# ------------------------------------------------------------------------------
# Execute Active Interception Kernel (Memory ceilings, O(N²) scale, destructive command guards)
npm run harness:active
```

---

## 2. Super-Feature 2: Curated Skill & MCP Engine (`npm run skill`)

Enables on-demand search and installation across 300 curated skills via SQLite FTS5, stdio MCP serving, and schema drift prevention.

```bash
# MASTER COMMAND: Search Skills via SQLite FTS5 (<5ms)
npm run skill <query>
npm run skill docker
npm run skill "reentrancy guard"

# ------------------------------------------------------------------------------
# SUBCOMMANDS: SKILL REGISTRY & MCP SERVER
# ------------------------------------------------------------------------------
# Install / Materialize a Skill into Local .agents/skills/ Workspace
npm run skill:install <skill-name>
npm run skill:install kubernetes-operator

# Launch Local JSON-RPC 2.0 Stdio MCP Server (Connects Cursor/Claude Code/Antigravity)
npm run mcp:start

# Recompile SQLite Skill Registry from In-Tree Skills and Upstream Catalogs
npm run catalog:compile

# Validate All Skills against Schema (Frontmatter, tags, descriptions, Zero-LaTeX)
npm run check:skills

# Check for Unauthorized Skill Drift / Tampering against SHA-256 Baseline
npm run check:skills:drift

# Update Skill Drift Baseline Hash after Authorized Modifications
npm run skills:drift:update

# Programmatic Skill Resolver (Validates active subdomain skills against prompt)
npm run skill:resolve
```

---

## 3. Super-Feature 3: True Pipeline Multi-Mode Execution & Task Dispatch (`npm run squad:run`)

Executes True Pipeline Triple-Mode SDLC workflows and headless task dispatching backed by Claude Council consensus.

```bash
# MASTER COMMAND: Run True Pipeline Autonomous SDLC Lifecycle
# (Solution Formulation -> TDD Self-Healing -> Presentation Pitch -> Attestation)
npm run squad:run

# ------------------------------------------------------------------------------
# SUBCOMMANDS: TASK DISPATCHER (MODULAR EXECUTION)
# ------------------------------------------------------------------------------
# Task 1: Autonomous Solution Formulation & 4-Moat Council Hardening
python -m pipeline.scripts.orchestrator.task_dispatcher --task solution --prompt "Build autonomous edge drone vision"
python -m pipeline.scripts.orchestrator.task_dispatcher --task solution --title "PRAVAH Flood AI" --prompt "SAR flash flood forecasting" --domain "Hydrology"

# Task 2: Autonomous Red-to-Green TDD Implementation Loop (Up to 5 Auto-Fix Passes)
python -m pipeline.scripts.orchestrator.task_dispatcher --task code --prompt "Implement rate-limiting token bucket middleware with constant-time security"

# Task 3: OmniDeck 2D Flex/Grid Pitch Deck Synthesis (<0.2s Native PPTX)
python -m pipeline.scripts.orchestrator.task_dispatcher --task presentation --prompt "Universal Domain Specialization"
python -m pipeline.scripts.orchestrator.task_dispatcher --task presentation --prompt "Web3 Security" --export-pdf  # Stage 2 PDF export

# Task 4: Brownfield Codebase Ingestion & 5-Pillar Health Audit
python -m pipeline.scripts.orchestrator.task_dispatcher --task audit --prompt "Audit legacy backend repository and emit improvement PRD"

# Task 5: Search & Recall Indexed Decisions from SQLite Memory Vault
python -m pipeline.scripts.orchestrator.task_dispatcher --task memory --search "architectural tradeoff"

# ------------------------------------------------------------------------------
# SUBCOMMANDS: MULTI-AGENT ADVERSARIAL ENGINES
# ------------------------------------------------------------------------------
# Run AutoGen Dynamic GroupChat Manager with Keyword Speaker Routing
python -m pipeline.scripts.orchestrator.groupchat

# Execute CrewAI Deterministic Task DAG Pipeline with Output Schema Validation
python -m pipeline.scripts.orchestrator.dag_runner
python -m pipeline.scripts.orchestrator.task_dag_runner

# Execute OpenHands Ephemeral Sandbox Runner (Process jail with secret strip)
node --experimental-strip-types pipeline/scripts/sandbox-runner.ts python -c "print('sandbox_active')"

# Execute E2B MicroVM Execution Runner (Sub-100ms boot with local mock fallback)
node --experimental-strip-types pipeline/scripts/sandbox-e2b.ts

# Prompt Hygiene Engine (Compresses 25 KB prompts to 4 KB Core Kernel; saves 21k tokens)
npm run prompt:hygiene
```

---

## 4. Super-Feature 4: Closed-Loop Self-Healing (`npm run self-heal`)

Enforces autonomous defect self-healing (>95% score), AST mutation survival (≥80% kill rate), and state graph rollbacks.

```bash
# MASTER COMMAND: Audit End-to-End Closed-Loop Self-Healing & Self-Improving Scores
npm run self-heal

# ------------------------------------------------------------------------------
# SUBCOMMANDS: MUTATION TESTING & STATE GRAPH ROLLBACK
# ------------------------------------------------------------------------------
# Deterministic AST Mutation Testing Engine (Boundary, Arithmetic, Return, State Bypass)
npm run test:mutation              # Full AST mutation battery
npm run test:mutation -- --diff    # Scoped mutation suite for Git-modified files only

# LangGraph Cyclic State Graph with Persistent SQLite Checkpoints & Time-Travel Rollback
python -m pipeline.scripts.orchestrator.state_graph

# ------------------------------------------------------------------------------
# SUBCOMMANDS: CONTINUAL EVOLUTION & REGRESSION FIXTURES
# ------------------------------------------------------------------------------
# List Discovered Failure Signatures and Generated Auto-Evolution Patches
npm run evolution:list

# Approve and Commit an Evolution Patch to Permanent Regression Shield
npm run evolution:approve -- --patch-id <patch-id>

# Reject an Evolution Patch
npm run evolution:reject -- --patch-id <patch-id>

# Distill Evolution Patches into Hard Invariant Rules
npm run evolution:distill
```

---

## 5. Super-Feature 5: Unified System Verification Battery (`npm run check`)

Runs all 6 defensive security and static code checks in a single rapid pass.

```bash
# MASTER COMMAND: Unified Pre-Commit Verification Battery (Secrets + AST + Hardcoding + Subdomain + Skills + Markdown)
npm run check

# ------------------------------------------------------------------------------
# SUBCOMMANDS: INDIVIDUAL VERIFICATION SUITES
# ------------------------------------------------------------------------------
# Run Node.js Unit Suites + Behavioral Eval Runner
npm test

# Full Secret Scanner (Probes full repository for forbidden tokens)
npm run check:secrets

# Staged Pre-Commit Secret Scanner (Gates git commits in <300ms)
npm run check:secrets:staged

# Anti-Hallucination AST Scanner (Rejects ghost packages missing from package.json)
npm run check:hallucinations

# Anti-Hardcoding Parameterized Schema Guard (Rejects Kaggle artifacts and competition relics)
npm run check:anti-hardcoding

# Subdomain Compliance & Active Stack Linter (Verifies active domain rigor)
npm run check:subdomain

# Markdown Zero-LaTeX & Broken Image Linter (Enforces Unicode math typography)
npm run lint:markdown docs

# Behavioral Harness Contracts (11/11 deterministic behavioral assertions)
npm run harness:eval

# Full 7-Layer System Readiness Probe (Operational baseline certification)
npm run readiness

# Adversarial Beta Penetration & Chaos Suite
npm run audit:beta

# Headless E2E Browser Testing (Playwright)
npm run test:e2e
```

---

## 6. Super-Feature 6: Web Workbench & SpecSync (`npm run workbench`)

Provides zero-dependency visual HUD inspection, real-time documentation synchronization, and AST repository mapping.

```bash
# MASTER COMMAND: Launch Pre-Commit Web Workbench HUD on Port 3042
npm run workbench

# ------------------------------------------------------------------------------
# SUBCOMMANDS: DOCUMENTATION LIFECYCLE & REPOSITORY TOPOLOGY
# ------------------------------------------------------------------------------
# Zero-Process SpecSync (Instantly mirrors IDE brain artifacts to docs/ catalogs)
npm run docs:sync

# Start Background Real-Time Brain Documentation Watcher
npm run docs:start

# Inspect Documentation Watcher Status
npm run docs:status

# Stop Background Documentation Watcher
npm run docs:stop

# Living Index Reconciler (Updates INDEX.md across all docs/ subdirectories)
npm run docs:reconcile

# Compile Tree-Sitter AST Repository Topology Map (<1,500 token ceiling)
npm run repo:map

# Verify Existing AST Repository Map Cache Validity
npm run repo:map:check

# Cline Interactive AST Diff Streamer with Permission Checkpoints
node --experimental-strip-types pipeline/scripts/diff-streamer.ts

# Probe Cryptographic Squad Attestation Provenance & Live Context Telemetry
npm run attest:telemetry
npm run attest:verify
```

---

## 7. Super-Feature 7: Enterprise Production Upgrade Commands (Active Harness, Git Mesh & Grounding)

Provides real runtime command interception, cross-workstation Git lease locking, AST mutation testing, and empirical hardware grounding:

```bash
# ==============================================================================
# 1. ACTIVE RUNTIME INTERCEPTION HARNESS & GROUNDING
# ==============================================================================
# Execute shell command safely via ActiveInterceptor (truncates >35 lines, logs audit SHA256)
npm run harness:run -- "echo Hello World"

# Verify empirical grounding against physical hardware bounds and audit logs
npm run check:grounding

# Run all 5 pre-commit barrier gates manually
node --experimental-strip-types pipeline/scripts/install-hooks.ts

# ==============================================================================
# 2. MODE 3: GIT-BACKED COLLABORATIVE TEAM MESH (Multi-Workstation Team Sync)
# ==============================================================================
# Query lease status across all domains
npm run lock:status

# Acquire exclusive domain lease lock for this physical workstation
npm run lock:acquire -- --domain ml_engine --role alpha

# Release domain lease lock
npm run lock:release -- --domain ml_engine

# List all active domain leases across machines
npm run lock:list

# Execute cross-workstation phase handoff (e.g. Workstation Alpha -> Workstation Beta)
npm run role:handoff -- --phase 3 --domain ml_engine --summary "Phase 3 complete, handing off to Beta"

# Inspect latest cross-workstation handoff brief (Collaborator Node)
npm run role:handoff -- --check

# Synchronize Git, peer handoff briefs, domain locks, and Memory Vault across devices
npm run sync:context

# Broadcast mesh node heartbeat (Local Collaborator Node)
npm run mesh:heartbeat

# Inspect live status of all peer workstations in the mesh
npm run mesh:status

# Prune stale node heartbeats older than 24h
npm run mesh:prune

# ==============================================================================
# 3. DUAL-STACK AST MUTATION TESTING GATES (>=80% Kill Rate)
# ==============================================================================
# Run TypeScript AST mutation testing against src/
npm run test:mutation

# Run native Python AST mutation testing against target module
npm run test:mutation:py src/math_ops.py "python -m unittest tests/test_math_ops.py"

# ==============================================================================
# 4. CROSS-MACHINE MEMORY VAULT & ADVERSARIAL COUNCIL EVALUATION
# ==============================================================================
# Re-index Git Markdown ADRs and handoffs into SQLite FTS5 virtual table
python -m pipeline.scripts.orchestrator.memory_vault_sync

# Full-text search indexed memories and architectural decisions
python -m pipeline.scripts.orchestrator.memory_vault_sync --search "harness"

# Run dynamic 5-Advisor Claude Council adversarial evaluation against an implementation plan
python -m pipeline.scripts.orchestrator.solution_council --evaluate docs/plans/sample_plan.md

# ==============================================================================
# 5. PHYSICAL COMPUTE BENCHMARKING & GPU MICRO-PROFILER
# ==============================================================================
# Profile exact GPU step latency and project realistic training time without hallucination
python pipeline/scripts/ml/profile_gpu_step.py

# ==============================================================================
# 6. TRUE PIPELINE MULTI-MODE EXECUTION & 16 GB HARDWARE HYPERVISOR
# ==============================================================================
# Inspect ambient 16 GB RAM utilization and process safety status
npm run hypervisor:status

# Start background 16 GB RAM safety hypervisor daemon (75% limit + 35-line slicing)
npm run hypervisor:daemon

# Mode 1: Deep Surge (Configure 4 Git Worktrees for 4 Accounts on 1 Project)
npm run mode:surge

# Mode 2: Portfolio Dispatcher (Batch dispatch across project repositories)
npm run portfolio:dispatch

# Mode 2 Dry Run: Inspect project queue, tiers, and profile assignments without execution
powershell pipeline/scripts/portfolio-dispatcher.ps1 -DryRun

# Mode 3: Collaborative Team Mode (Launch LAN sync server on port 4040)
node --experimental-strip-types pipeline/scripts/lan-sync-server.ts --port 4040

# Stage-Gated Physical Filesystem Guard (Anti-cheating write interceptor)
python pipeline/scripts/harness/filesystem_guard.py --path "src/service.ts" --stage "GREEN"
```

