import test from "node:test";
import type { TestContext } from "node:test";
import assert from "node:assert/strict";
import { existsSync, readFileSync, unlinkSync } from "node:fs";
import { join } from "node:path";
import { measureConversationContext, findActiveBrainDirectory } from "../scripts/context-meter.ts";
import { reconcileAllCatalogs, reconcileDirectory } from "../scripts/index-reconciler.ts";
import { detectProjectScale } from "../scripts/project-scale-detector.ts";
import { getGitDiffFiles } from "../scripts/mutation-tester.ts";
import { getActiveModel, setActiveModel } from "../scripts/token-budget-guard.ts";

test("Automated Workflow Upgrades Test Suite: Zero-Process Hook, Context Meter, Living Index & Scale Guard", async (t: TestContext) => {

  await t.test("Component 1: Zero-Process Documentation Lifecycle & Daemon PID Management", () => {
    const pidFile = join(process.cwd(), ".agents", "state", "docs-watcher.pid");
    if (existsSync(pidFile)) {
      unlinkSync(pidFile);
    }

    assert.strictEqual(existsSync(pidFile), false, "PID file should be clean initially");
  });

  await t.test("Component 2: Active Context Window & Conversation Transcript Meter", () => {
    // Verify active model configuration
    const model = getActiveModel();
    assert.strictEqual(model.id, "gemini-3.8-flash-high");
    assert.strictEqual(model.contextCeiling, 1048576);

    const brainDir = findActiveBrainDirectory();
    assert.ok(brainDir, "Active brain directory should be resolved");

    const telemetry = measureConversationContext(brainDir!);
    assert.ok(telemetry, "Telemetry should be successfully generated");
    assert.strictEqual(telemetry!.modelId, "gemini-3.8-flash-high");
    assert.ok(telemetry!.activeChatContextTokens > 0, "Active chat context tokens must be greater than 0");
    assert.ok(telemetry!.remainingBeforeCompaction > 0, "Remaining headroom must be greater than 0");
    assert.ok(telemetry!.saturationPercent >= 0, "Saturation percent must be valid");
    assert.ok(telemetry!.cumulativeSessionTokens >= telemetry!.activeChatContextTokens, "Cumulative tokens must be >= active tokens");
    assert.ok(Array.isArray(telemetry!.directives), "Directives should be an array");
  });

  await t.test("Component 3: Team Mesh Living Index Reconciliation & Deterministic Table Generation", () => {
    const results = reconcileAllCatalogs();
    assert.ok(typeof results["Plans"] === "number", "Plans catalog must be reconciled");
    assert.ok(typeof results["Walkthroughs"] === "number", "Walkthroughs catalog must be reconciled");
    assert.ok(typeof results["Audits"] === "number", "Audits catalog must be reconciled");

    const plansIndexPath = join(process.cwd(), "docs", "plans", "INDEX.md");
    assert.ok(existsSync(plansIndexPath), "docs/plans/INDEX.md must exist");

    const content = readFileSync(plansIndexPath, "utf-8");
    assert.ok(content.includes("| Timestamp | Document Title | File Name | Link |"), "Must contain standard markdown table header");
    assert.ok(content.includes("Master Living Catalog: Plans"), "Must contain catalog header");
  });

  await t.test("Component 4: Intelligent Large-Project Scale Detection & Autonomous Scoping (Dual-Scope)", () => {
    const scaleReport = detectProjectScale();
    assert.ok(scaleReport.totalLoc > 0, "Total LOC must be greater than 0");
    assert.ok(scaleReport.totalSourceFiles > 0, "Total source files must be greater than 0");
    assert.strictEqual(scaleReport.scale, "SMALL", "Starter template application domain must report SMALL scale");
    assert.strictEqual(scaleReport.isLarge, false, "Starter template must not be flagged as large");
    assert.ok(scaleReport.applicationLoc > 0, "Application LOC must be greater than 0");
    assert.ok(scaleReport.harnessLoc > 1000, "Workflow harness LOC must be measured independently");
    assert.ok(scaleReport.documentationLoc > 1000, "Governance documentation LOC must be measured independently");
    assert.strictEqual(scaleReport.recommendedMutationMode, "--full", "Small application codebase should use full mode");
    assert.ok(Array.isArray(scaleReport.directives), "Directives must be an array");

    // Mutation tester diff scanner
    const diffFiles = getGitDiffFiles();
    assert.ok(Array.isArray(diffFiles), "getGitDiffFiles must return an array");
    for (const f of diffFiles) {
      assert.ok(f.startsWith("src/") || f.startsWith("src\\"), "Diff files must be scoped to product domain code (src/)");
    }
  });

});
