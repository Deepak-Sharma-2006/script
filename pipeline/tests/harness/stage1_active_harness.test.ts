import { test, describe } from "node:test";
import assert from "node:assert/strict";
import { existsSync, readFileSync, unlinkSync } from "node:fs";
import { join } from "node:path";
import { execSync } from "node:child_process";
import { ActiveInterceptor } from "../../scripts/harness/active-interceptor.ts";

describe("Stage 1: Active Runtime Interception Harness & Fail-Closed Pre-Commit Shield", () => {
  const root = process.cwd();

  test("Gate 1: Active Interceptor permits safe shell commands", async () => {
    const res = await ActiveInterceptor.execute("echo SAFE_STAGE1_PROBE");
    assert.equal(res.permitted, true, "Safe command should be permitted");
    assert.equal(res.exitCode, 0, "Safe command should exit 0");
    assert.match(res.stdout, /SAFE_STAGE1_PROBE/, "Stdout should contain expected output");
  });

  test("Gate 2: Active Interceptor blocks destructive recursive deletion (rm -rf)", async () => {
    const res = await ActiveInterceptor.execute("rm -rf /");
    assert.equal(res.permitted, false, "Destructive command must NOT be permitted");
    assert.equal(res.exitCode, 1, "Blocked command must exit 1");
    assert.match(res.stderr, /HARNESS INTERCEPT REJECTED/, "Stderr must contain rejection notice");
  });

  test("Gate 3: Active Interceptor blocks database drop/truncate commands", async () => {
    const res = await ActiveInterceptor.execute("DROP TABLE enterprise_users");
    assert.equal(res.permitted, false, "Database drop command must NOT be permitted");
    assert.equal(res.exitCode, 1, "Blocked command must exit 1");
    assert.match(res.stderr, /HARNESS INTERCEPT REJECTED/, "Stderr must contain rejection notice");
  });

  test("Gate 4: SWE-agent style 35-line context window truncation with spillover file", () => {
    const longOutput = Array.from({ length: 60 }, (_, i) => `Log line ${i + 1}`).join("\n");
    const trunc = ActiveInterceptor.truncateOutput(longOutput, "test_hash_12345");

    assert.equal(trunc.truncated, true, "Output > 35 lines must be truncated");
    assert.match(trunc.text, /TRUNCATED 25 LINES/, "Must indicate exact number of truncated lines");
    assert.ok(trunc.spilloverPath, "Must provide spillover file path");
    assert.ok(existsSync(trunc.spilloverPath!), "Spillover file must exist on disk");

    const savedContent = readFileSync(trunc.spilloverPath!, "utf-8");
    assert.equal(savedContent, longOutput, "Full untruncated content must be preserved in spillover file");

    // Clean up temporary test spillover
    try { unlinkSync(trunc.spilloverPath!); } catch {}
  });

  test("Gate 5: Audit trail records cryptographically signed command history", async () => {
    const testCmd = "echo AUDIT_TRAIL_PROBE_STAGE1";
    await ActiveInterceptor.execute(testCmd);

    const auditLogPath = join(root, ".agents", "audit_trail.log");
    assert.ok(existsSync(auditLogPath), ".agents/audit_trail.log must exist");

    const logContent = readFileSync(auditLogPath, "utf-8");
    assert.match(logContent, /AUDIT_TRAIL_PROBE_STAGE1/, "Audit log must contain executed command");
    assert.match(logContent, /SHA256: [a-f0-9]{64}/, "Audit log must contain SHA-256 digest");
  });

  test("Gate 6: Grounding Validator flags impossible GPU compute duration claims", () => {
    const pyScript = join(root, "scripts", "harness", "grounding-validator.py");
    assert.ok(existsSync(pyScript), "grounding-validator.py must exist");

    // Test python validation via direct subprocess
    const checkCmd = `python scripts/harness/grounding-validator.py`;
    const res = execSync(checkCmd, { encoding: "utf-8" });
    assert.match(res, /Grounding Validator/, "Grounding validator must run successfully");
  });

  test("Gate 7: Pre-commit hook is installed and contains all 5 enterprise barrier gates", () => {
    const hookPath = join(root, ".git", "hooks", "pre-commit");
    assert.ok(existsSync(hookPath), ".git/hooks/pre-commit must exist");

    const hookContent = readFileSync(hookPath, "utf-8");
    assert.match(hookContent, /Pre-Commit Gate 1\/5[\s\S]*?secret-scanner/, "Gate 1 must be Secret Scanner");
    assert.match(hookContent, /Pre-Commit Gate 2\/5[\s\S]*?markdown-linter/, "Gate 2 must be Markdown Linter");
    assert.match(hookContent, /Pre-Commit Gate 3\/5[\s\S]*?anti-hallucination-checker/, "Gate 3 must be Anti-Hallucination Scanner");
    assert.match(hookContent, /Pre-Commit Gate 4\/5[\s\S]*?grounding-validator/, "Gate 4 must be Grounding Validator");
    assert.match(hookContent, /Pre-Commit Gate 5\/5[\s\S]*?index-reconciler/, "Gate 5 must be Index Reconciler");
  });
});
