# Antigravity Enterprise — Master Command Cheat Sheet

> **Executive Reference**: Consolidated 6-Super-Feature Command Hierarchy.  
> **Status**: 100% Operational & Production Hardened | 99/99 Python suites | 34/34 Node unit suites | 6/6 Behavioral Evals | Zero Stale Commands  
> **Compliance**: Zero-Raw-LaTeX Invariant (Pure Unicode Math), Zero-Secret Shield, Rule 14 3-Tier Architecture  

---

## 🏆 The 6 Master Commands (Executive Summary)

The entire workspace command surface is consolidated into **6 Unified Master Commands**, eliminating command sprawl:

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
#   2. SkillResolver programmatically cites relevant skills from the 2,922 registry.
#   3. The 6-Persona Squad executes sequentially: [PM] -> [Architect] -> [SDET] -> [Coder] -> [Auditor] -> [Writer].
#   4. claude-council 5-perspective hardening is automatically applied to architectural designs.
#   5. SpecSync automatically mirrors brain artifacts to docs/plans/ and docs/walkthroughs/.
#   6. SquadAttestor concludes each turn with a verified cryptographic attestation receipt.
```

---

## 1. Super-Feature 1: Workspace Governance Kernel (`npm run governance`)

Manages operating modes, domain specializations, distributed lease locks, and cross-harness instruction synchronization.

```bash
# MASTER COMMAND: Inspect Active Mode, Leases, Operator Profile, and Locks
npm run governance

# ------------------------------------------------------------------------------
# SUBCOMMANDS: OPERATING MODES & LEASE LOCKS
# ------------------------------------------------------------------------------
# Switch to Solo Operator Mode (Bypasses multi-host locks; single unified developer)
npm run mode:solo

# Switch to Dual-Lead Mode (Symmetrical 50/50 Alpha/Beta enterprise rotation)
npm run mode:dual

# Switch to Team Mesh Mode (N-person distributed parallel domain leases)
npm run mode:team

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
# SUBCOMMANDS: UNIVERSAL HARNESS & RUNTIME INTERCEPTION
# ------------------------------------------------------------------------------
# Compile Universal Instructions across Cursor, Claude Code, Windsurf, Copilot, Antigravity
npm run harness:sync

# Execute Active Interception Kernel (Memory ceilings, O(N²) scale, destructive command guards)
npm run harness:active
```

---

## 2. Super-Feature 2: Tiered Skill & MCP Engine (`npm run skill`)

Enables on-demand search and installation across 2,922 skills via SQLite FTS5, stdio MCP serving, and schema drift prevention.

```bash
# MASTER COMMAND: Search Skills across Tier 1 and Tier 2 via SQLite FTS5 (<5ms)
npm run skill <query>
npm run skill docker
npm run skill "reentrancy guard"

# ------------------------------------------------------------------------------
# SUBCOMMANDS: SKILL REGISTRY & MCP SERVER
# ------------------------------------------------------------------------------
# Install / Materialize a Tier 2 Skill into Local .agents/skills/ Workspace
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

## 3. Super-Feature 3: 6+1 Agile Squad & Task Dispatch (`npm run squad:run`)

Executes structured multi-persona SDLC workflows and headless task dispatching backed by Claude Council consensus.

```bash
# MASTER COMMAND: Run Full 6+1 Persona Agile Product Squad Lifecycle
# (PM -> Architect -> SDET -> Coder -> Mutation Auditor -> Tech Writer)
npm run squad:run

# ------------------------------------------------------------------------------
# SUBCOMMANDS: TASK DISPATCHER (MODULAR EXECUTION)
# ------------------------------------------------------------------------------
# Task 1: Autonomous Solution Formulation & 4-Moat Council Hardening
python -m scripts.orchestrator.task_dispatcher --task solution --prompt "Build autonomous edge drone vision"
python -m scripts.orchestrator.task_dispatcher --task solution --title "PRAVAH Flood AI" --prompt "SAR flash flood forecasting" --domain "Hydrology"

# Task 2: Autonomous Red-to-Green TDD Implementation Loop (Up to 5 Auto-Fix Passes)
python -m scripts.orchestrator.task_dispatcher --task code --prompt "Implement rate-limiting token bucket middleware with constant-time security"

# Task 3: OmniDeck 2D Flex/Grid Pitch Deck Synthesis (<0.2s Native PPTX)
python -m scripts.orchestrator.task_dispatcher --task presentation --prompt "Universal Domain Specialization"
python -m scripts.orchestrator.task_dispatcher --task presentation --prompt "Web3 Security" --export-pdf  # Stage 2 PDF export

# Task 4: Brownfield Codebase Ingestion & 5-Pillar Health Audit
python -m scripts.orchestrator.task_dispatcher --task audit --prompt "Audit legacy backend repository and emit improvement PRD"

# Task 5: Search & Recall Indexed Decisions from SQLite Memory Vault
python -m scripts.orchestrator.task_dispatcher --task memory --search "architectural tradeoff"

# ------------------------------------------------------------------------------
# SUBCOMMANDS: MULTI-AGENT ADVERSARIAL ENGINES
# ------------------------------------------------------------------------------
# Run AutoGen Dynamic GroupChat Manager with Keyword Speaker Routing
python -m scripts.orchestrator.groupchat

# Execute CrewAI Deterministic Task DAG Pipeline with Output Schema Validation
python -m scripts.orchestrator.dag_runner
python -m scripts.orchestrator.task_dag_runner

# Execute OpenHands Ephemeral Sandbox Runner (Process jail with secret strip)
node --experimental-strip-types scripts/sandbox-runner.ts python -c "print('sandbox_active')"

# Execute E2B MicroVM Execution Runner (Sub-100ms boot with local mock fallback)
node --experimental-strip-types scripts/sandbox-e2b.ts

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
python -m scripts.orchestrator.state_graph

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
node --experimental-strip-types scripts/diff-streamer.ts

# Inspect Active Chat Context Window Saturation & Compaction Headroom
npm run context:check
npm run context:yaml

# Probe Cryptographic Squad Attestation Provenance & Live Context Telemetry
npm run attest:telemetry
npm run attest:verify
```
