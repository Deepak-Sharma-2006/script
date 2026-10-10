import { describe, it } from "node:test";
import assert from "node:assert";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

import { SandboxRunner } from "../scripts/sandbox-runner.ts";
import { SopValidator } from "../templates/sops/sop-validator.ts";
import { DiffStreamer } from "../scripts/diff-streamer.ts";
import { AciGuard } from "../scripts/aci-guard.ts";
import { E2BSandboxRunner } from "../scripts/sandbox-e2b.ts";

describe("18 SOTA Repositories Ingestion & Operational Readiness Test Suite", () => {
  it("Touchpoint 1 (OpenHands): SandboxRunner executes commands with secret sanitization", async () => {
    const cleanEnv = SandboxRunner.sanitizeEnv({
      AWS_SECRET_KEY: "forbidden_token",
      CUSTOM_SAFE_VAR: "allowed_value"
    });
    assert.strictEqual(cleanEnv.AWS_SECRET_KEY, undefined, "Forbidden secret must be stripped");
    assert.strictEqual(cleanEnv.CUSTOM_SAFE_VAR, "allowed_value", "Safe environment variable must be retained");

    const result = await SandboxRunner.execute(["python", "-c", "print('sandbox_ok')"]);
    assert.strictEqual(result.exitCode, 0);
    assert.ok(result.stdout.includes("sandbox_ok"));
    assert.strictEqual(result.timedOut, false);
  });

  it("Touchpoint 2 (MetaGPT): SopValidator enforces typed PRD and Architecture schemas", () => {
    assert.ok(existsSync("pipeline/templates/sops/prd.schema.json") || existsSync("templates/sops/prd.schema.json"));
    assert.ok(existsSync("pipeline/templates/sops/architecture.schema.json") || existsSync("templates/sops/architecture.schema.json"));

    const validPrd = {
      feature_name: "AuthService",
      target_domain: "Security",
      problem_statement: "Enterprise passwordless authentication with FIDO2 WebAuthn.",
      user_personas: ["Enterprise Admin", "End User"],
      acceptance_criteria: ["Sub-200ms latency", "Fail-closed rate limiting"],
      forbidden_states: ["Unauthenticated token issuance"]
    };

    const res = SopValidator.validate(validPrd, "prd");
    assert.strictEqual(res.valid, true);
    assert.strictEqual(res.errors.length, 0);

    const invalidPrd = { feature_name: "Bad" };
    const badRes = SopValidator.validate(invalidPrd, "prd");
    assert.strictEqual(badRes.valid, false);
    assert.ok(badRes.errors.length > 0);
  });

  it("Touchpoint 3 (Cline): DiffStreamer computes AST diffs and flags destructive checkpoints", () => {
    const oldCode = "function test() { return false; }";
    const newCode = "function test() { return true;\n console.log('applied'); }";

    const diff = DiffStreamer.computeDiff("test.ts", oldCode, newCode);
    assert.strictEqual(diff.filePath, "test.ts");
    assert.ok(diff.additions > 0);
    assert.strictEqual(diff.isDestructive, false);

    const formatted = DiffStreamer.renderFormattedDiff(diff);
    assert.ok(formatted.includes("Diff: test.ts"));

    // Destructive SQL mutation check
    const destructiveDiff = DiffStreamer.computeDiff("migration.sql", "CREATE TABLE users();", "DROP TABLE users;");
    assert.strictEqual(destructiveDiff.isDestructive, true);
    assert.strictEqual(DiffStreamer.verifyCheckpoint(destructiveDiff), false);
  });

  it("Touchpoint 6 (Roo-Code): Role-Based Mode configurations enforce tool whitelists", () => {
    const modes = ["architect", "sdet", "core", "docs"];
    for (const m of modes) {
      const modePath = join(".agents", "modes", `${m}.json`);
      assert.ok(existsSync(modePath), `Mode configuration missing: ${modePath}`);

      const content = JSON.parse(readFileSync(modePath, "utf-8"));
      assert.ok(content.mode_id === m);
      assert.ok(Array.isArray(content.tool_whitelist) && content.tool_whitelist.length > 0);
      assert.ok(Array.isArray(content.forbidden_actions));
    }
  });

  it("Touchpoint 14 (SWE-agent): AciGuard validates bracket balance and zero-raw-LaTeX compliance", () => {
    const balancedCode = "const obj = { arr: [1, 2, (3 + 4)] };";
    assert.strictEqual(AciGuard.checkBracketBalance(balancedCode).balanced, true);

    const unbalancedCode = "const obj = { arr: [1, 2, (3 + 4) };";
    const unbalRes = AciGuard.checkBracketBalance(unbalancedCode);
    assert.strictEqual(unbalRes.balanced, false);
    assert.ok(unbalRes.error?.includes("Mismatched bracket") || unbalRes.error?.includes("Unclosed bracket"));

    const latexDoc = "The probability is $P(X) = \\frac{1}{2}$";
    const latexCheck = AciGuard.checkZeroRawLatex(latexDoc, "spec.md");
    assert.strictEqual(latexCheck.compliant, false);

    const unicodeDoc = "The probability is P(X) = 0.5 (≥ 99%)";
    const unicodeCheck = AciGuard.checkZeroRawLatex(unicodeDoc, "spec.md");
    assert.strictEqual(unicodeCheck.compliant, true);
  });

  it("Touchpoint 17 (E2B): E2BSandboxRunner executes code in fast-boot micro-environment", async () => {
    const res = await E2BSandboxRunner.execute("print('e2b_micro_vm_ok')", "python");
    assert.strictEqual(res.exitCode, 0);
    assert.ok(res.stdout.includes("e2b_micro_vm_ok"));
    assert.ok(res.bootTimeMs < 300, `Boot time expected < 300ms, got ${res.bootTimeMs}ms`);
  });
});
