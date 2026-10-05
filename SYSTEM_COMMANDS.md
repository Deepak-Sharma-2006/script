# Antigravity Enterprise — Master Command Cheat Sheet

> **Quick Reference**: Execute these commands in terminal/PowerShell or prompt the Antigravity agent directly.  
> **Status**: 100% Green & Production Hardened | 99/99 Pytest suites | 18/18 Adversarial suites | 13/13 Node unit suites + 6/6 Harness Evals | 7/7 System Readiness Probes  

---

## 1. System Setup & Environment Diagnostics

```bash
# 1. Full System Readiness Probe (Verifies 7 enterprise operational layers)
npm run readiness

# 2. Detect Codebase Scale (Small <5k LOC, Medium 5k-50k LOC, Large >50k LOC)
npm run project:scale

# 3. Inspect Active Chat Context Window & Compaction Headroom
npm run context:check
npm run context:yaml

# 4. Compile Universal Agent Instructions across Cursor, Claude Code, Windsurf, Copilot
npm run harness:sync
```

---

## 2. Enterprise Operating Modes

```bash
# 1. Inspect Active Mode, Leases, and Operator Role
npm run mode:status

# 2. Solo Operator Mode (Instant velocity for single developers; bypasses lease locks)
npm run mode:solo

# 3. Dual-Lead Mode (Symmetrical 50/50 Alpha/Beta enterprise rotation)
npm run mode:dual

# 4. Team Mesh Mode (N-person distributed parallel domain leases)
npm run mode:team
npm run team:status

# 5. Local LAN Team Mesh Synchronization Server (Optional zero-cloud laptop sync on port 4040)
npm run lan:start
```

---

## 3. Universal Master Domain & Subdomain Management

```bash
# 1. Inspect Active Domain, Subdomains, Stack, and Injected Curated Skills
npm run domain:status

# 2. List All 8 Master Domains and 46 Subdomains
npm run domain:list

# 3. Interactive CLI Domain Selector (Terminal Questionnaire)
npm run domain:select

# 4. Headless Atomic Domain Configuration
npm run domain:set -- --domain blockchain --subdomains smart_contracts,defi_protocols
npm run domain:set -- --domain software --subdomains backend_systems,web_frontend
npm run domain:set -- --domain ai_ml --subdomains agentic_ai,mlops_inference
npm run domain:set -- --domain cybersecurity --subdomains appsec_devsecops,zero_trust_network
npm run domain:set -- --domain deep_tech --subdomains hpc_supercomputing,computational_biology
npm run domain:set -- --domain cloud_infra --subdomains kubernetes_cloud_native,sre_observability
npm run domain:set -- --domain data_engineering --subdomains stream_processing,lakehouse_warehousing
npm run domain:set -- --domain vertical_applied --subdomains healthtech_informatics,fintech_banking

# 5. Domain Compiler & Toolchain Diagnostic Probes
npm run domain:doctor  # Probes Node, Python, and active compilers (forge, solc, cargo, gcc, kubectl)
```

---

## 4. Universal Task Dispatcher (Autonomous Subsystems)

```bash
# Task 1: Solution Formulation, Live Multi-Hop Research & 4-Moat Architecture
python -m scripts.orchestrator.task_dispatcher --task solution --prompt "Autonomous satellite wildfire early detection"
python -m scripts.orchestrator.task_dispatcher --task solution --title "PRAVAH Flood AI" --prompt "SAR flash flood forecasting" --domain "Hydrology"

# Task 2: Red-to-Green Autonomous TDD Implementation Loop (Red test -> Green code -> Refactor)
python -m scripts.orchestrator.task_dispatcher --task code --prompt "Implement rate-limiting token bucket middleware with constant-time security"

# Task 3: OmniDeck 2D Flex/Grid Presentation Pitch Synthesis
python -m scripts.orchestrator.task_dispatcher --task presentation --prompt "Universal Domain Specialization"
python -m scripts.orchestrator.task_dispatcher --task presentation --prompt "Web3 Security" --export-pdf  # Stage 2 PDF export

# Task 4: Brownfield Codebase Ingestion & 5-Pillar Health Audit
python -m scripts.orchestrator.task_dispatcher --task audit --prompt "Audit legacy backend repository and emit improvement PRD"

# Task 5: Developing Project Delta WBS & Resume Development
python -m scripts.orchestrator.task_dispatcher --task continue --prompt "Resume feature development from existing baseline"

# Task 6: Deep Research Triangulation (Multi-Hop Live Search with 120s deliberation)
python -m scripts.orchestrator.task_dispatcher --task research --prompt "NIST Post-Quantum Cryptography migration standards"
```

---

## 5. Quality Assurance, Testing & Mutation Gates

```bash
# 1. Full Python Orchestrator, Engine, and Hydration Test Suite (99 suites)
pytest tests/ -q

# 2. Lead 2 Adversarial Suite (Concurrency races, chaos fuzzing, timing attacks)
npm run test:adversarial

# 3. Node Unit Suites + Core 4 & Domain-Adaptive Behavioral Evaluations
npm test

# 4. Domain-Adaptive Behavioral Evaluations Dynamic Runner
npm run harness:eval

# 5. Deterministic AST Mutation Testing (Enforces ≥ 80% kill rate across TS and Python)
npm run test:mutation             # Full domain AST mutation suite
npm run test:mutation -- --diff    # Scoped mutation suite for Git-modified files only

# 6. Strict TypeScript Compilation Check (Zero error tolerance)
npx tsc --noEmit

# 7. Zero-LaTeX Markdown Compliance Linter
npm run lint:markdown docs
```

---

## 6. Distributed Domain Lease Locking

```bash
# 1. Acquire Exclusive Domain Lease
npm run lock:acquire --domain auth
npm run lock:acquire --domain billing --duration 30

# 2. Release Domain Lease
npm run lock:release --domain auth

# 3. List All Active Locks Across Workstations
npm run lock:list

# 4. Atomic 50/50 Dual-Lead Role Handoff (Alpha -> Beta rotation)
npm run role:handoff --domain auth
```

---

## 7. Living Documentation Lifecycle & SpecSync

```bash
# 1. Zero-Process Turn-Egress Sync (Mirrors IDE brain artifacts into docs/ catalogs instantly)
npm run docs:sync
python -m scripts.orchestrator.spec_sync --sync-brain

# 2. Living Catalog Reconciler & Conflict-Free Merge Driver
npm run docs:reconcile # Rebuilds all 6 INDEX.md catalogs sorted by timestamp descending

# 3. Optional Background Docs Watcher (With PID tracking)
npm run docs:start     # Launch background watcher
npm run docs:status    # Inspect watcher PID and status
npm run docs:stop      # Gracefully stop watcher
```

---

## 8. Memory Vault & Skills Discovery

```bash
# 1. Memory Vault Doctor & Integrity Audit
npm run memory:doctor

# 2. Search Memory Vault with Domain Relevance Boosting
npm run memory:search -- --query "reentrancy guards"

# 3. Ingest New Architectural Decision or Learning into Vault
npm run memory:save -- --category "decision" --title "Domain AST Mutations" --content "Implemented visit_Call for timingSafeEqual"

# 4. Search Master Skills Library (298 Verified Skills)
npm run skill:search <query>
python scripts/skill-finder.ts <query>
```

---

## 9. Operator Provenance & Attestation Ledger

```bash
# 1. Verify Cryptographic Squad Attestation Audit Trail (.agents/audit_trail.log)
npm run attest:verify

# 2. Extract Live Context Window Telemetry (Empirical & Anti-Hallucination)
npm run attest:telemetry
npm run context:yaml

# 3. Manually Generate Signed Execution Receipt
python -m scripts.orchestrator.squad_attestation --prompt "Verified domain behavioral evaluations and compiler sandboxing"
```

---

## 10. Tiered Execution Gates & Active Hardening (Tiered 10+1 Architecture)

```bash
# 1. Two-Tier Format Guard & Banned Sycophancy Scanner (INV-11)
npm run guard:format <path_to_markdown_or_text>

# 2. Programmatic GateGuard Fact-Forcing Middleware (INV-01)
npm run guard:gate <path_to_plan_or_doc>

# 3. Asymptotic Scale & 500-Item FLOP Profiler (INV-02)
npm run profile:scale 500 0.12 3800000 4.0

# 4. Contrarian Adversarial Falsification Engine (INV-03)
npm run audit:contrarian "<skepticism_prompt>" <path_to_response_file>

# 5. Headless Idempotent DAG Pipeline Runner with SHA-256 caching (INV-04)
npm run dag:run -- --pipeline pipeline.json --run

# 6. Hardware Memory Guard & 75% RAM Budget Enforcer (INV-05)
npm run guard:memory

# 7. Operational Deadline & T-4h Safe Submission Lockdown (INV-07)
npm run lockdown:deadline -- --status
npm run lockdown:deadline -- --duration 4h --threshold 30m    # Short burst hackathon
npm run lockdown:deadline -- --duration 72h                   # Long hackathon (auto T-4h threshold)
npm run lockdown:deadline -- --set "2026-10-01T12:00:00Z" 4.0 # Enterprise sprint deadline
npm run lockdown:deadline -- --clear                          # Reset / clear deadline
npm run lockdown:deadline -- --check "train_new_model"

# 8. Domain Prompt Hygiene & System Prompt Compression Engine (INV-10)
npm run prompt:hygiene

# 9. Generalized Pipeline Gate (Upstream Recall & Distractor Parity: INV-06, INV-09)
npm run gate:pipeline -- --recall 0.995 0.920
npm run gate:pipeline -- --parity 9000 100 100000 1000

# 10. Objective-Loss Calibration & Posterior Probability Auditor (INV-08)
npm run audit:calibration "[0.9, 0.8, 0.1]" "[1, 1, 0]"

# 11. Automatic Skill Resolution & Injection Engine (INV-13)
npm run skill:resolve -- "build scalable redis cache for web api"

# 12. Active Interception Kernel & 8-Domain Dynamic Guard (.agents/harness/active_kernel.py)
npm run harness:active -- --status
npm run harness:active -- --status --hardware
npm run harness:active -- --intercept "python match.py --dataset 3.8M_full_dataset"
```

---

## 11. Continual Self-Evolution & 7-Layer Agentic Harness

```bash
# 1. Inspect Active Harness 7 Pillars & Domain Health
npm run harness:active -- --status
npm run harness:active -- --status --hardware

# 2. Intercept Shell Commands (Safety Governance: ESCALATE on destructive commands)
npm run harness:active -- --intercept "rm -rf /var/data"
npm run harness:active -- --intercept "rm -rf /var/data --operator-approved"

# 3. Continual Evolution Engine: List Staged Patches Awaiting Operator Verification
npm run evolution:list

# 4. Continual Evolution Engine: Review & Approve Staged Patch
npm run evolution:approve -- <patch_id>

# 5. Continual Evolution Engine: Dismiss & Reject Staged Patch
npm run evolution:reject -- <patch_id>

# 6. Continual Evolution Engine: Run Trajectory Distillation
npm run evolution:distill
```


