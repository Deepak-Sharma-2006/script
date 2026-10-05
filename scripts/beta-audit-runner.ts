import { existsSync, readdirSync, readFileSync } from "fs";
import { join } from "path";
import { execSync } from "child_process";
import { fileURLToPath } from "node:url";

export interface AuditPillarResult {
  pillar: number;
  name: string;
  passed: boolean;
  details: string;
}

export function runBetaAudit(): boolean {
  console.log(`
================================================================================
     ENTERPRISE 2-PERSON DUAL-LEAD AUDIT BATTERY (6 PILLARS)
================================================================================
Assigned Lead : Adversarial Systems, SDET & Product Lead (Lead 2 / Beta)
Mandate       : Independent Adversarial Probes, Chaos Fuzzing, AppSec & Release
================================================================================`);

  const results: AuditPillarResult[] = [];

  // Pillar 1: Zero-Secret & Anti-Hallucination Shield
  console.log("\n▶ [Pillar 1/6] Zero-Secret & Anti-Hallucination Shield...");
  let p1Ok = true;
  let p1Details = "Zero secrets and zero ghost packages detected";
  try {
    execSync("node --experimental-strip-types scripts/secret-scanner.ts", { stdio: "inherit" });
    execSync("node --experimental-strip-types scripts/anti-hallucination-checker.ts scripts src tests", { stdio: "inherit" });
  } catch {
    p1Ok = false;
    p1Details = "Secret leak or undeclared dependency detected";
  }
  results.push({ pillar: 1, name: "Zero-Secret & Anti-Hallucination Shield", passed: p1Ok, details: p1Details });

  // Pillar 2: Strict Typing & Architectural Invariants
  console.log("\n▶ [Pillar 2/6] Strict TypeScript & Architectural Contracts (tsc --noEmit)...");
  let p2Ok = true;
  let p2Details = "0 errors, strict mode enforced";
  try {
    execSync("npx tsc --noEmit", { stdio: "inherit" });
  } catch {
    p2Ok = false;
    p2Details = "TypeScript type-checking or contract compilation errors";
  }
  results.push({ pillar: 2, name: "Strict TypeScript & Contract Check", passed: p2Ok, details: p2Details });

  // Pillar 3: Core Domain Unit & Behavioral Contracts
  console.log("\n▶ [Pillar 3/6] Core Domain Unit & Golden Behavioral Evals...");
  let p3Ok = true;
  let p3Details = "Unit contracts and 4/4 behavioral evals passed";
  try {
    execSync("node --experimental-strip-types --test tests/bootstrap.test.ts", { stdio: "inherit" });
    execSync("node --experimental-strip-types .agents/harness/eval-runner.ts", { stdio: "inherit" });
  } catch {
    p3Ok = false;
    p3Details = "Core unit or behavioral evaluation failure";
  }
  results.push({ pillar: 3, name: "Domain Unit & Behavioral Contracts", passed: p3Ok, details: p3Details });

  // Pillar 4: Independent Adversarial SDET & Concurrency Battery (Authored by Lead 2)
  console.log("\n▶ [Pillar 4/6] Independent Adversarial SDET & Concurrency Battery...");
  let p4Ok = true;
  let p4Details = "All 12 adversarial, concurrency, fuzzing & chaos tests passed";
  try {
    execSync("node --experimental-strip-types scripts/adversarial-suite-runner.ts", { stdio: "inherit" });
  } catch {
    p4Ok = false;
    p4Details = "Adversarial concurrency or payload vulnerability detected";
  }
  results.push({ pillar: 4, name: "Adversarial SDET & Concurrency Fuzzer", passed: p4Ok, details: p4Details });

  // Pillar 5: Strix AI Dynamic DAST & Privilege Escalation Pentest
  console.log("\n▶ [Pillar 5/6] Strix/Styx AI Dynamic DAST & Privilege Escalation Pentest...");
  let p5Ok = true;
  let p5Details = "Zero unverified exploits detected";
  try {
    execSync("node --experimental-strip-types scripts/security-audit-runner.ts", { stdio: "inherit" });
  } catch {
    p5Ok = false;
    p5Details = "Penetration test exploit detected";
  }
  results.push({ pillar: 5, name: "Dynamic DAST & AppSec Pentest", passed: p5Ok, details: p5Details });

  // Pillar 6: Product UX Acceptance & Cognitive Dossier Certification
  console.log("\n▶ [Pillar 6/6] Product UX Acceptance & Cognitive Dossier Certification...");
  const dossierDir = join(process.cwd(), "docs/dossiers");
  let p6Ok = false;
  let p6Details = "No dossier found";

  if (existsSync(dossierDir)) {
    const files = readdirSync(dossierDir).filter((f) => f.startsWith("phase-") && f.endsWith(".md"));
    if (files.length > 0) {
      let allTechniquesPresent = true;
      const requiredTechniques = [
        "Technique 1",
        "Technique 2",
        "Technique 3",
        "Technique 4",
        "Technique 5",
        "Technique 6",
      ];

      for (const file of files) {
        const content = readFileSync(join(dossierDir, file), "utf-8");
        for (const t of requiredTechniques) {
          if (!content.includes(t)) {
            allTechniquesPresent = false;
          }
        }
      }

      if (allTechniquesPresent) {
        p6Ok = true;
        p6Details = `Validated ${files.length} dossier(s) with all 6 required cognitive techniques`;
        console.log(`✅ [Dossiers Validated] Found ${files.length} compliant cognitive comprehension dossier(s).`);
      } else {
        p6Details = "Dossier missing one or more of the 6 mandatory techniques";
        console.error("❌ [Dossier Incomplete] Missing mandatory cognitive reading techniques.");
      }
    }
  }
  results.push({ pillar: 6, name: "Product UX & Cognitive Dossier Sign-Off", passed: p6Ok, details: p6Details });

  // Summary Scorecard
  console.log(`
================================================================================
            ENTERPRISE DUAL-LEAD AUDIT SCORECARD & CERTIFICATION
================================================================================`);

  let allPassed = true;
  for (const r of results) {
    const icon = r.passed ? "✅" : "❌";
    console.log(`  [Pillar ${r.pillar}] ${r.name.padEnd(40)} : ${icon} ${r.details}`);
    if (!r.passed) allPassed = false;
  }

  console.log("================================================================================");

  if (allPassed) {
    console.log(`
🎉 [ENTERPRISE CERTIFIED] All 6 Verification Pillars Passed!
   Lead 2 (Adversarial Systems & Product Lead) has signed off on this release.
   The codebase is hardened, adversarially verified, and ready for production handoff.
`);
    return true;
  } else {
    console.error(`
🚨 [AUDIT REJECTED] One or more verification pillars failed.
   Lead 2 must either apply hardening fixes or request architectural remediation.
`);
    return false;
  }
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("beta-audit-runner.ts") ||
  process.argv[1].endsWith("beta-audit-runner.js")
);

if (isMain) {
  const success = runBetaAudit();
  process.exit(success ? 0 : 1);
}
