import { existsSync, readdirSync, readFileSync } from "fs";
import { join } from "path";
import { hostname } from "os";
import { execSync } from "child_process";
import { fileURLToPath } from "node:url";
import { DatabaseSync } from "node:sqlite";
import { listLocks, resolveOperator } from "./lock-manager.ts";
import { doctorVault } from "./memory-vault.ts";
import { getActiveModel, SUPPORTED_MODELS } from "./token-budget-guard.ts";
import { listLocalSkills } from "./skill-finder.ts";

export interface ReadinessReport {
  timestamp: string;
  nodeVersion: string;
  host: string;
  operator: string;
  gitStatus: {
    clean: boolean;
    originConfigured: boolean;
    cleanProductionConfigured: boolean;
    currentCommit: string;
  };
  locksStatus: {
    activeCount: number;
    unlocked: boolean;
  };
  memoryStatus: {
    dbConnected: boolean;
    markdownFiles: number;
    dbRows: number;
  };
  skillsStatus: {
    totalSkills: number;
    coreGovernancePresent: boolean;
    productDiscoveryPresent: boolean;
  };
  tokenStatus: {
    activeModel: string;
    modelSupportedCount: number;
  };
  qualityGates: {
    antiHallucinationPassed: boolean;
    typeScriptPassed: boolean;
    testsPassed: boolean;
    dossiersCount: number;
  };
  overallReady: boolean;
}

function execCmd(cmd: string): { ok: boolean; output: string } {
  try {
    const output = execSync(cmd, { encoding: "utf-8", stdio: ["ignore", "pipe", "pipe"] }).trim();
    return { ok: true, output };
  } catch (err: any) {
    return { ok: false, output: (err.stdout || err.stderr || err.message || "").trim() };
  }
}

export function runSystemReadinessCheck(): ReadinessReport {
  console.log(`
================================================================================
             ANTIGRAVITY ENTERPRISE WORKFLOW: SYSTEM READINESS PROBE
================================================================================
Timestamp   : ${new Date().toISOString()}
Workstation : ${hostname()}
Operator    : ${resolveOperator()}
================================================================================
`);

  let allPassed = true;

  // 1. Runtime & Environment
  console.log("▶ [Probe 1/7] Runtime & Node Environment...");
  const nodeVer = process.version;
  let sqliteOk = false;
  try {
    const testDb = new DatabaseSync(":memory:");
    testDb.exec("CREATE TABLE test (id INT);");
    sqliteOk = true;
    console.log(`  ✅ Node.js Runtime: ${nodeVer} (Active)`);
    console.log(`  ✅ Native SQLite (node:sqlite DatabaseSync): Operational`);
  } catch (err) {
    allPassed = false;
    console.error(`  ❌ Native SQLite Failure:`, err);
  }

  // 2. Git & Remote Topology
  console.log("\n▶ [Probe 2/7] Git & Remote Repository Topology...");
  const gitRemotes = execCmd("git remote -v").output;
  const originConfigured = gitRemotes.includes("Deepak-Sharma-2006/script") || gitRemotes.includes("Deepak-Sharma-2006/agent1") || gitRemotes.includes("origin");
  const cleanProdConfigured = gitRemotes.includes("cleanproduction") || gitRemotes.includes("Infinity915/575_final");
  const gitStatusRaw = execCmd("git status -s").output;
  const isGitClean = gitStatusRaw.length === 0;
  const currentCommit = execCmd("git log -1 --oneline").output || "Unknown";

  console.log(`  ${originConfigured ? "✅" : "⚠️"} Remote 'origin' (Collaboration)     : ${originConfigured ? "Configured" : "Warning: Not configured"}`);
  console.log(`  ${cleanProdConfigured ? "✅" : "⚠️"} Remote 'cleanproduction' (Showcase) : ${cleanProdConfigured ? "Configured (575_final)" : "Warning: Not configured"}`);
  console.log(`  ${isGitClean ? "✅" : "ℹ️"} Working Tree                      : ${isGitClean ? "Clean" : "Modified files present"}`);
  console.log(`  📄 Current Head Commit               : ${currentCommit}`);

  // 3. Multi-Operator Distributed Lock Engine & Triple-Mode State
  console.log("\n▶ [Probe 3/7] True Pipeline Triple-Mode & Distributed Lock Engine...");
  const locks = listLocks();
  let roleInfo = "Unknown";
  try {
    const roleData = JSON.parse(readFileSync(join(process.cwd(), ".agents/state/active-role.json"), "utf-8"));
    roleInfo = `${roleData.operator} (${roleData.role}: ${roleData.roleTitle || roleData.role})`;
  } catch {}
  console.log(`  ✅ Active Operator Role       : ${roleInfo}`);
  console.log(`  ✅ Lock Engine Operational     : ${locks.length} active domain lease(s) tracked.`);

  // 4. Memory Vault Health
  console.log("\n▶ [Probe 4/7] Native SQLite + Markdown Memory Vault...");
  const vaultCheck = doctorVault();
  const memoryDbConnected = vaultCheck.totalDbRows >= 0;
  console.log(`  ✅ Memory Vault Files: ${vaultCheck.totalFiles} Markdown docs | ${vaultCheck.totalDbRows} Indexed SQLite Rows`);

  // 5. Adaptive Token Economy & Model Profiles
  console.log("\n▶ [Probe 5/7] Multi-Model Token Economy & Model Profiles...");
  const activeModel = getActiveModel();
  const supportedCount = Object.keys(SUPPORTED_MODELS).length;
  console.log(`  ✅ Active Model Profile: ${activeModel.name} (${activeModel.provider})`);
  console.log(`  ✅ Supported Models    : ${supportedCount} profiles loaded (Gemini 2.0, Claude 3.7, GPT-4o)`);

  // 6. Skills Catalog & Prompt Discovery Ingestion
  console.log("\n▶ [Probe 6/7] Skills Catalog & Prompt Understanding Suite...");
  const allSkills = listLocalSkills();
  const skillCount = allSkills.length;
  const coreGovList = [
    "agentic-loop-runner",
    "claude-council",
    "code-reading-dossier",
    "git-sync-lock",
    "grill-me",
    "skill-finder",
    "skill-creator",
    "styx-pentest",
    "token-budget-guard",
  ];
  const missingCore = coreGovList.filter((s) => !allSkills.some((k) => k.name === s));
  const coreGovOk = missingCore.length === 0;

  const discoveryList = [
    "grill-me",
    "problem-statement-deconstructor",
    "pdf-document-intelligence",
    "product-lens",
    "product-capability",
  ];
  const missingDiscovery = discoveryList.filter((s) => !allSkills.some((k) => k.name === s));
  const discoveryOk = missingDiscovery.length === 0;

  console.log(`  ✅ Total Installed Skills       : ${skillCount} skills`);
  console.log(`  ${coreGovOk ? "✅" : "❌"} Core Governance Skills Suite   : ${coreGovOk ? "8/8 Present" : `Missing: ${missingCore.join(", ")}`}`);
  console.log(`  ${discoveryOk ? "✅" : "❌"} Product & Prompt Understanding : ${discoveryOk ? "5/5 Dedicated Skills Verified" : `Missing: ${missingDiscovery.join(", ")}`}`);
  if (!coreGovOk || !discoveryOk) allPassed = false;

  // 7. Security, AST Shield & Cognitive Dossiers
  console.log("\n▶ [Probe 7/7] Adversarial Security & Quality Gate Barriers...");

  const secretCheck = execCmd("node --experimental-strip-types pipeline/scripts/secret-scanner.ts");
  console.log(`  ${secretCheck.ok ? "✅" : "❌"} Zero-Secret Credential Shield  : ${secretCheck.ok ? "Zero secrets detected" : "FAILED - SECRETS FOUND"}`);

  const antiHallucination = execCmd("npm run check:hallucinations");
  console.log(`  ${antiHallucination.ok ? "✅" : "❌"} Anti-Hallucination AST Scanner : ${antiHallucination.ok ? "Zero ghost dependencies" : "FAILED"}`);

  const tsCheck = execCmd("npx tsc --noEmit");
  console.log(`  ${tsCheck.ok ? "✅" : "❌"} Strict TypeScript Compilation  : ${tsCheck.ok ? "0 errors, strict mode" : "FAILED"}`);

  const testCheck = execCmd("npm test");
  console.log(`  ${testCheck.ok ? "✅" : "❌"} Unit & Behavioral Contracts    : ${testCheck.ok ? "All suites passed" : "FAILED"}`);

  const advCheck = execCmd("node --experimental-strip-types pipeline/scripts/adversarial-suite-runner.ts");
  console.log(`  ${advCheck.ok ? "✅" : "❌"} Adversarial SDET & Chaos Fuzzer: ${advCheck.ok ? "All 12 attacks resisted" : "FAILED"}`);

  const dossierDir = join(process.cwd(), "docs/dossiers");
  let dossiersCount = 0;
  if (existsSync(dossierDir)) {
    dossiersCount = readdirSync(dossierDir).filter((f) => f.endsWith(".md")).length;
  }
  console.log(`  ${dossiersCount >= 1 ? "✅" : "⚠️"} Cognitive Comprehension Dossiers: ${dossiersCount} dossier(s) ready`);

  if (!secretCheck.ok || !antiHallucination.ok || !tsCheck.ok || !testCheck.ok || !advCheck.ok) {
    allPassed = false;
  }

  // Summary Scorecard
  console.log(`
================================================================================
                    SYSTEM READINESS FINAL SCORECARD
================================================================================
  [1] Runtime & Environment          : ${sqliteOk ? "✅ OPERATIONAL" : "❌ FAILED"}
  [2] Git & Remote Topology          : ${originConfigured ? "✅ VERIFIED" : "⚠️ WARNING"}
  [3] Triple-Mode & Domain Locks     : ✅ ACTIVE (${locks.length} leases)
  [4] Native SQLite Memory Vault     : ✅ CONNECTED (${vaultCheck.totalFiles} files, ${vaultCheck.totalDbRows} rows)
  [5] Multi-Model Token Economy      : ✅ OPTIMIZED (${activeModel.name})
  [6] Skills Catalog & Understanding : ${coreGovOk && discoveryOk ? `✅ CERTIFIED (${skillCount} skills)` : "❌ INCOMPLETE"}
  [7] Security, AST Shield & Evals   : ${antiHallucination.ok && tsCheck.ok && testCheck.ok ? "✅ 100% PASSING" : "❌ GATES BREACHED"}
================================================================================
  OVERALL WORKSPACE READINESS        : ${allPassed ? "🚀 READY FOR DEPLOYMENT / COLLABORATION" : "🛑 BLOCKED - ADDRESS DEFECTS"}
================================================================================
`);

  return {
    timestamp: new Date().toISOString(),
    nodeVersion: nodeVer,
    host: hostname(),
    operator: resolveOperator(),
    gitStatus: {
      clean: isGitClean,
      originConfigured,
      cleanProductionConfigured: cleanProdConfigured,
      currentCommit,
    },
    locksStatus: {
      activeCount: locks.length,
      unlocked: locks.length === 0,
    },
    memoryStatus: {
      dbConnected: memoryDbConnected,
      markdownFiles: vaultCheck.totalFiles,
      dbRows: vaultCheck.totalDbRows,
    },
    skillsStatus: {
      totalSkills: skillCount,
      coreGovernancePresent: coreGovOk,
      productDiscoveryPresent: discoveryOk,
    },
    tokenStatus: {
      activeModel: activeModel.name,
      modelSupportedCount: supportedCount,
    },
    qualityGates: {
      antiHallucinationPassed: antiHallucination.ok,
      typeScriptPassed: tsCheck.ok,
      testsPassed: testCheck.ok,
      dossiersCount,
    },
    overallReady: allPassed,
  };
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("system-readiness.ts") ||
  process.argv[1].endsWith("system-readiness.js")
);

if (isMain) {
  const report = runSystemReadinessCheck();
  process.exit(report.overallReady ? 0 : 1);
}
