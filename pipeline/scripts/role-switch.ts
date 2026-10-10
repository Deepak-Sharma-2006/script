import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import { join } from "path";
import { execSync } from "child_process";
import { fileURLToPath } from "node:url";
import { acquireLock, listLocks, releaseLock, resolveOperator, transferLock } from "./lock-manager.ts";
import { saveMemory } from "./memory-vault.ts";

export interface ActiveRoleProfile {
  operator: string;
  role: string; // "Alpha" | "Beta" | "DomainLead" | custom
  roleTitle: string;
  phase: number;
  activeLeaseDomain: string;
  updatedAt: string;
  mode?: "surge" | "portfolio" | "team" | "solo" | "dual";
}

const STATE_DIR = join(process.cwd(), ".agents/state");
const ROLE_FILE = join(STATE_DIR, "active-role.json");

function getRoleTitle(role: string, mode?: string): string {
  if (mode === "solo") {
    return role === "Alpha"
      ? "Solo Enterprise Lead (Autonomous Alpha Architect)"
      : "Solo Enterprise Auditor (Autonomous Beta SDET)";
  }
  if (mode === "team" || mode === "mesh") {
    return `Team Domain Lead (${role}) - Distributed Architecture Mesh`;
  }
  return role === "Alpha"
    ? "Feature Architect & Core Domain Lead"
    : "Adversarial Systems, SDET & Product Lead";
}

function execGit(cmd: string): string {
  try {
    return execSync(cmd, { encoding: "utf-8" }).trim();
  } catch (err: any) {
    return "";
  }
}

export function getActiveProfile(): ActiveRoleProfile {
  if (!existsSync(STATE_DIR)) {
    mkdirSync(STATE_DIR, { recursive: true });
  }

  if (existsSync(ROLE_FILE)) {
    try {
      const parsed: ActiveRoleProfile = JSON.parse(readFileSync(ROLE_FILE, "utf-8"));
      if (!parsed.roleTitle) {
        parsed.roleTitle = getRoleTitle(parsed.role);
      }
      return parsed;
    } catch {
      // Fall through to default
    }
  }

  const role: "Alpha" | "Beta" = (process.env.ROLE as "Alpha" | "Beta") || "Alpha";
  const defaultProfile: ActiveRoleProfile = {
    operator: resolveOperator(),
    role,
    roleTitle: getRoleTitle(role),
    phase: parseInt(process.env.PHASE || "1", 10),
    activeLeaseDomain: "core",
    updatedAt: new Date().toISOString(),
  };

  saveProfile(defaultProfile);
  return defaultProfile;
}

export function saveProfile(profile: ActiveRoleProfile): void {
  if (!existsSync(STATE_DIR)) {
    mkdirSync(STATE_DIR, { recursive: true });
  }
  profile.roleTitle = getRoleTitle(profile.role);
  profile.updatedAt = new Date().toISOString();
  writeFileSync(ROLE_FILE, JSON.stringify(profile, null, 2), "utf-8");
}

export function printRoleMatrix(): void {
  console.log(`
================================================================================
             TRUE PIPELINE THREE-MODE ARCHITECTURAL MATRIX
================================================================================

┌──────────────────────────────────────────────────────────────────────────────┐
│ MODE 1: DEEP SURGE (All 4 Accounts Focused on 1 Single Project)              │
├──────────────────────────────────────────────────────────────────────────────┤
│ • Account 1 (Strategic Council) : Problem deconstruction, 4 moats, specs     │
│ • Account 2 (Adversarial SDET)  : Red-first test suites, mutation gates      │
│ • Account 3 (Core Engineer)     : 5-stage closed loop, typed microservices   │
│ • Account 4 (Hardening Auditor) : AST mutation oracle, pre-commit shield     │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ MODE 2: 8-HACKATHON PORTFOLIO MULTIPLEXING (Batch Runway, 17-25 Days)        │
├──────────────────────────────────────────────────────────────────────────────┤
│ • 4 Headless Runner Slots       : Multiplexed across 8 hackathon repos on disk│
│ • 25-Day Milestone Runway       : Phased formulation, TDD, hardening, decks  │
│ • Portfolio Dispatcher          : scripts/portfolio-dispatcher.ps1           │
│ • OmniDeck Compiler             : Native PPTX/HTML deck generation in < 0.2s  │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ MODE 3: COLLABORATIVE TEAM MODE (Zero-Friction Human Synchronization)         │
├──────────────────────────────────────────────────────────────────────────────┤
│ • Part 7 Cognitive Dossiers     : 6-Technique comprehension in docs/dossiers/ │
│ • Local LAN Sync Server         : Zero-dependency HTTP on port 4040           │
│ • Living Index Reconciliation   : Auto-updated docs/*/INDEX.md on git pull   │
│ • Distributed Domain Leases     : Conflict-free parallel locks (.agents/locks)│
└──────────────────────────────────────────────────────────────────────────────┘
================================================================================`);
}

export function setOperatingMode(mode: "surge" | "portfolio" | "team" | "solo" | "dual" | "mesh"): boolean {
  const profile = getActiveProfile();
  let normalizedMode: "surge" | "portfolio" | "team" = "surge";

  if (mode === "portfolio") {
    normalizedMode = "portfolio";
  } else if (mode === "team" || mode === "mesh") {
    normalizedMode = "team";
  } else {
    normalizedMode = "surge"; // "surge", "solo", and legacy "dual" map to primary Deep Surge
  }

  profile.mode = normalizedMode as any;

  if (normalizedMode === "surge") {
    profile.operator = "SoloOperator";
    profile.role = "Alpha";
    profile.roleTitle = "Deep Surge Lead (All 4 Accounts Focused on 1 Project)";
    saveProfile(profile);
    console.log(`\n🎯 [OPERATING MODE 1: DEEP SURGE ACTIVATED]`);
    console.log(`   Scope                 : All 4 Google Accounts focused on 1 Single Project`);
    console.log(`   Squad Architecture    : Account 1 (Solution) + Account 2 (SDET) + Account 3 (Code) + Account 4 (Hardening)`);
    console.log(`   Multi-Host Collision  : Bypassed (Single project fast-track execution)`);
    console.log(`   Mechanical Gates      : Gated via 5-Stage Autonomous Pipeline Harness & Mutation Testing\n`);
  } else if (normalizedMode === "portfolio") {
    profile.operator = resolveOperator();
    profile.role = "PortfolioLead";
    profile.roleTitle = "Portfolio Lead (8-Hackathon Multiplexing Engine)";
    saveProfile(profile);
    console.log(`\n🚀 [OPERATING MODE 2: 8-HACKATHON PORTFOLIO MULTIPLEXING ACTIVATED]`);
    console.log(`   Scope                 : 4 Headless Runner Slots multiplexed across 8 Hackathon Repositories`);
    console.log(`   Runway                : 25-Day Phased Submission Timeline (Days 17-25 Deadlines)`);
    console.log(`   Worker Scheduling     : Round-Robin Batch Dispatcher (scripts/portfolio-dispatcher.ps1)`);
    console.log(`   Asset Synthesis       : Autonomous OmniDeck Pitch Deck Compiler (<0.2s PPTX)\n`);
  } else if (normalizedMode === "team") {
    profile.operator = resolveOperator();
    profile.role = "DomainLead";
    profile.roleTitle = "Collaborative Team Lead (Local LAN & Distributed Mesh)";
    saveProfile(profile);
    console.log(`\n🌐 [OPERATING MODE 3: COLLABORATIVE TEAM MODE ACTIVATED]`);
    console.log(`   Scope                 : Zero-Friction Human Synchronization & Multi-Developer Mesh`);
    console.log(`   Local LAN HUD         : Port 4040 Real-Time Server (scripts/lan-sync-server.ts)`);
    console.log(`   Cognitive Sync        : Part 7 6-Technique Comprehension Dossiers (docs/dossiers/)`);
    console.log(`   Living Indexes        : Living Catalog Auto-Reconciliation on Git Pull (scripts/index-reconciler.ts)`);
    console.log(`   Domain Leases         : Distributed Git Locks (.agents/state/locks/<domain>.lock.json)\n`);
  }
  return true;
}

export function printTeamStatus(): void {
  const profile = getActiveProfile();
  const currentHost = resolveOperator();
  console.log(`
================================================================================
             COLLABORATIVE TEAM MODE & ACTIVE LEASE ROSTER
================================================================================
  Operating Mode        : ${profile.mode ? profile.mode.toUpperCase() : "SURGE"}
  Current Workstation   : ${currentHost}
  Active Operator       : ${profile.operator}
  Assigned Role         : ${profile.role} (${profile.roleTitle})
================================================================================`);

  console.log("\nActive Domain Leases across Team Workstations:");
  const locks = listLocks();
  if (locks.length === 0) {
    console.log("  (No active domain leases held. Run 'npm run lock:acquire --domain <name>' to lease a domain.)");
  } else {
    for (const l of locks) {
      console.log(`  - Domain: [${l.domain}] | Operator: ${l.operator} (${l.role}) | Host: ${l.host} | Expires: ${l.expiresAt}`);
    }
  }
  console.log("================================================================================\n");
}

export function printRoleStatus(): void {
  const profile = getActiveProfile();
  const currentHost = resolveOperator();
  const mode = profile.mode || "surge";

  const modeDescription = mode === "surge" || mode === "solo"
    ? "Mode 1: Deep Surge (All 4 Accounts on 1 Project)"
    : mode === "portfolio"
    ? "Mode 2: 8-Hackathon Portfolio Multiplexing (17-25 Day Runway)"
    : "Mode 3: Collaborative Team Mode (LAN Port 4040 & Context Sync)";

  console.log(`
================================================================================
               ACTIVE WORKSPACE ROLE & LEASE PROFILE
================================================================================
  Operating Mode        : ${mode.toUpperCase()} (${modeDescription})
  Current Workstation   : ${currentHost}
  Active Profile Leader : ${profile.operator}
  Assigned Role         : ${profile.role} (${profile.roleTitle})
  Current Phase         : Phase ${profile.phase}
  Active Domain Lease   : ${profile.activeLeaseDomain}
  Last Synchronized     : ${profile.updatedAt}
================================================================================`);

  console.log("\nActive Domain Locks in Repository:");
  listLocks();
  console.log("");
}

export function switchToAlpha(domain = "core", operator?: string): boolean {
  const profile = getActiveProfile();
  const currentOp = resolveOperator(operator);
  console.log(`\n⚙️ [Role Switch] Switching ${currentOp} to ALPHA (Feature Architect & Core Domain Lead) for '${domain}'...`);

  const ok = acquireLock(domain, currentOp, "Alpha", 7200);
  if (ok) {
    profile.operator = currentOp;
    profile.role = "Alpha";
    profile.roleTitle = getRoleTitle("Alpha");
    profile.activeLeaseDomain = domain;
    saveProfile(profile);
    console.log(`✅ [Role Confirmed] ${currentOp} is now ALPHA (Core Domain Lead) for Phase ${profile.phase}.\n`);
  }
  return ok;
}

export function switchToBeta(domain = "core", operator?: string): boolean {
  const profile = getActiveProfile();
  const currentOp = resolveOperator(operator);
  console.log(`\n⚙️ [Role Switch] Configuring ${currentOp} as BETA (Adversarial Systems, SDET & Product Lead) for Phase ${profile.phase}...`);

  const ok = acquireLock(domain, currentOp, "Beta", 7200);
  if (ok) {
    profile.operator = currentOp;
    profile.role = "Beta";
    profile.roleTitle = getRoleTitle("Beta");
    profile.activeLeaseDomain = domain;
    saveProfile(profile);
    console.log(`✅ [Role Confirmed] ${currentOp} is now BETA (Adversarial Systems Lead) for Phase ${profile.phase}.\n`);
  }
  return ok;
}

export function executeRoleHandoff(toOperator?: string, customNotes?: string): boolean {
  const profile = getActiveProfile();
  const currentOp = profile.operator;
  const targetOp = resolveOperator(toOperator || (currentOp === "Computer1" ? "Computer2" : "Computer1"));

  console.log(`\n🔄 [Enterprise Handoff] Initiating atomic role handoff from ${currentOp} (${profile.role}) to ${targetOp}...`);

  // Step 1: Pre-Commit Secret Scanner Check
  console.log("🔒 [Zero-Secret Gate] Verifying clean workspace before handoff...");
  try {
    execSync("node --experimental-strip-types scripts/secret-scanner.ts", { stdio: "inherit" });
  } catch {
    console.error("🛑 [HANDOFF ABORTED] Secret detected in workspace! Purge secrets before handoff.");
    return false;
  }

  // Step 2: Check git status
  const status = execGit("git status -s");
  if (status) {
    console.log("📦 Staging and committing modified workspace state for handoff...");
    try {
      execSync("git add -A", { stdio: "inherit" });
      execSync(`git commit -m "chore(handoff): Phase ${profile.phase} handoff from ${currentOp} to ${targetOp}"`, { stdio: "inherit" });
    } catch {
      console.warn("⚠️ Git commit encountered no changes or skipped.");
    }
  }

  // Step 3: Transfer lease lock
  if (profile.role === "Alpha") {
    // Alpha completed domain development -> handoff to Beta for Adversarial SDET, Chaos, and 6-Pillar Audit
    const ok = transferLock(profile.activeLeaseDomain, currentOp, targetOp, "Beta");
    if (ok) {
      profile.role = "Beta";
      profile.roleTitle = getRoleTitle("Beta");
      saveProfile(profile);

      // Record in memory vault
      saveMemory({
        title: `Phase ${profile.phase} Handoff: Alpha -> Beta`,
        kind: "handoff",
        scope: "team",
        phase: profile.phase,
        operator: currentOp,
        body: customNotes || `Phase ${profile.phase} core implementation complete for domain '${profile.activeLeaseDomain}'. Transferred to ${targetOp} for independent adversarial testing, fuzzing, AppSec, and 6-pillar enterprise certification.`,
      });

      // Push state
      console.log("🚀 Synchronizing handoff state to origin...");
      try {
        execSync("git push origin main", { stdio: "inherit" });
      } catch {
        console.warn("⚠️ Git push failed or remote unreachable. Push manually before partner continues.");
      }

      console.log(`\n================================================================================`);
      console.log(`✅ [HANDOFF COMPLETE] Domain '${profile.activeLeaseDomain}' transferred to ${targetOp} (Lead 2 / Beta).`);
      console.log(`👉 Partner Actions for ${targetOp} (Adversarial Systems & Product Lead):`);
      console.log(`   1. git pull`);
      console.log(`   2. npm run test:adversarial`);
      console.log(`   3. npm run audit:beta`);
      console.log(`================================================================================\n`);
      return true;
    }
    return false;
  } else {
    // Beta completed 6-pillar audit & approved -> advance phase and invert roles!
    releaseLock(profile.activeLeaseDomain, currentOp);
    profile.phase += 1;
    profile.role = "Alpha";
    profile.roleTitle = getRoleTitle("Alpha");
    profile.operator = targetOp;
    saveProfile(profile);

    saveMemory({
      title: `Phase ${profile.phase - 1} Certified & Phase ${profile.phase} Inversion`,
      kind: "decision",
      scope: "team",
      phase: profile.phase - 1,
      operator: currentOp,
      body: `Phase ${profile.phase - 1} passed 6-pillar enterprise verification. Roles inverted for Phase ${profile.phase}. ${profile.operator} is now Alpha (Feature Architect & Core Domain Lead).`,
    });

    console.log("🚀 Synchronizing phase inversion state to origin...");
    try {
      execSync("git add .agents/state/active-role.json .agents/state/locks/", { stdio: "inherit" });
      execSync(`git commit -m "chore(role): Phase ${profile.phase} start - ${profile.operator} assumed Alpha"`, { stdio: "inherit" });
      execSync("git push origin main", { stdio: "inherit" });
    } catch {
      // Ignored if clean
    }

    console.log(`\n================================================================================`);
    console.log(`🎉 [PHASE ADVANCED] Phase ${profile.phase - 1} certified and merged!`);
    console.log(`🚀 [ROLE INVERSION] ${profile.operator} is now ALPHA for Phase ${profile.phase}.`);
    console.log(`👉 Partner Command for ${profile.operator} (Core Domain Lead):`);
    console.log(`   git pull && npm run build:alpha`);
    console.log(`================================================================================\n`);
    return true;
  }
}

function parseCliFlags(args: string[]): Record<string, string> {
  const flags: Record<string, string> = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      if (i + 1 < args.length && !args[i + 1].startsWith("--")) {
        flags[key] = args[i + 1];
        i++;
      } else {
        flags[key] = "true";
      }
    }
  }
  return flags;
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("role-switch.ts") ||
  process.argv[1].endsWith("role-switch.js")
);

if (isMain) {
  const rawArgs = process.argv.slice(2);
  const command = (rawArgs[0] && !rawArgs[0].startsWith("--") ? rawArgs[0] : "status").toLowerCase();
  const flags = parseCliFlags(rawArgs);
  const positional = rawArgs.filter((a: string) => !a.startsWith("--") && a !== command);

  if (command === "status") {
    printRoleStatus();
  } else if (command === "team-status" || command === "roster" || command === "team") {
    printTeamStatus();
  } else if (command === "mode") {
    const targetMode = (positional[0] || flags["set"] || "status").toLowerCase();
    if (targetMode === "surge" || targetMode === "portfolio" || targetMode === "team" || targetMode === "solo" || targetMode === "dual" || targetMode === "mesh") {
      setOperatingMode(targetMode as any);
    } else {
      printRoleStatus();
    }
  } else if (command === "matrix") {
    printRoleMatrix();
  } else if (command === "alpha") {
    const domain = flags["domain"] || positional[0] || "core";
    const op = flags["operator"] || flags["op"] || positional[1];
    switchToAlpha(domain, op);
  } else if (command === "beta") {
    const domain = flags["domain"] || positional[0] || "core";
    const op = flags["operator"] || flags["op"] || positional[1];
    switchToBeta(domain, op);
  } else if (command === "handoff") {
    const toOp = flags["to"] || flags["target"] || positional[0];
    const notes = flags["notes"] || flags["msg"] || positional.slice(1).join(" ");
    executeRoleHandoff(toOp, notes);
  } else {
    console.log(`
Usage: node --experimental-strip-types scripts/role-switch.ts <command> [options]

Commands:
  status                   Display active operator, role title, phase, and domain lease
  mode [surge|portfolio|team] Switch True Pipeline operating mode (Deep Surge, Portfolio, Team)
  team-status              Display active team roster, machines, and domain leases
  matrix                   Display the True Pipeline 3-mode architectural matrix
  alpha [domain] [op]      Acquire domain lease and set workstation as Lead 1 (Alpha)
  beta [domain] [op]       Configure workstation as Lead 2 (Beta) with Hardening Authority
  handoff [toOp] [msg]     Execute atomic git-synchronized role handoff to partner
`);
  }
}
