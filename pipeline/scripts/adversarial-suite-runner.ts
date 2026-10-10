import { execSync } from "child_process";
import { fileURLToPath } from "node:url";

export interface AdversarialSuiteSummary {
  concurrencyPassed: boolean;
  fuzzingPassed: boolean;
  chaosRecoveryPassed: boolean;
  timingDefensePassed: boolean;
  totalTests: number;
  durationMs: number;
}

export function runAdversarialSuite(): boolean {
  console.log(`
================================================================================
     LEAD 2 ADVERSARIAL SDET, CHAOS & CONCURRENCY BATTERY
================================================================================
Role: Adversarial Systems & Product Lead (Co-Equal Lead 2)
Scope: Concurrency Races, Malicious Payloads, Fault Injection, Timing Defense
================================================================================`);

  const startTime = Date.now();
  let testsPassed = false;

  console.log("\n▶ [Executing Adversarial Black-Box Contract Suite]...");
  try {
    execSync("node --experimental-strip-types --test pipeline/tests/adversarial/adversarial-contract.test.ts", {
      stdio: "inherit",
    });
    testsPassed = true;
  } catch (err: any) {
    console.error("❌ Adversarial test suite failed.");
    testsPassed = false;
  }

  const durationMs = Date.now() - startTime;

  console.log(`
================================================================================
           ADVERSARIAL SYSTEMS LEAD (SDET) THREAT SCORECARD
================================================================================
  [Pillar 1] Concurrency & Race Condition Defense : ${testsPassed ? "✅ PASSED (Strict mutual exclusion)" : "❌ FAILED"}
  [Pillar 2] Malicious Payload & Fuzzing Defense   : ${testsPassed ? "✅ PASSED (Zero data leaks or crashes)" : "❌ FAILED"}
  [Pillar 3] State Corruption Chaos Recovery      : ${testsPassed ? "✅ PASSED (Resilient auto-recovery)" : "❌ FAILED"}
  [Pillar 4] Timing Attack & Constant-Time Crypto  : ${testsPassed ? "✅ PASSED (Safe constant-time equality)" : "❌ FAILED"}
================================================================================
  Execution Time   : ${durationMs}ms
  Overall Status   : ${testsPassed ? "🛡️ ADVERSARIALLY CERTIFIED" : "🚨 ADVERSARIAL VULNERABILITIES DETECTED"}
================================================================================
`);

  return testsPassed;
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("adversarial-suite-runner.ts") ||
  process.argv[1].endsWith("adversarial-suite-runner.js")
);

if (isMain) {
  const success = runAdversarialSuite();
  process.exit(success ? 0 : 1);
}
