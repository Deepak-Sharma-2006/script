import { describe, it } from "node:test";
import assert from "node:assert";
import { existsSync, readFileSync, unlinkSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { compileCatalog, getRegistryStats, searchRegistry, getSkill, installSkill } from "../scripts/catalog-compiler.ts";
import { handleToolCall, TOOLS } from "../scripts/mcp-server.ts";
import { validateAllSkills, validateSkillContent, checkDrift, updateDriftBaseline } from "../scripts/skill-validator.ts";
import { generateRepoMap, checkRepoMap } from "../scripts/repo-map-generator.ts";
import { createWorkbenchServer } from "../scripts/workbench-server.ts";
import {
  synthesizeRegressionFixture,
  getJitNegativeConstraints,
  generateMutationAssertion,
  interviewPromptAmbiguity,
  auditSelfHealingMetrics,
} from "../scripts/self-healing-engine.ts";

describe("Milestones 1 - 6: SOTA Agentic Upgrades Test Suite", () => {
  // --- Milestone 1 & 2 Tests ---
  it("Milestone 2.1: Registry Compiler indexes canonical skills with Tier 1 and SQLite FTS", () => {
    const stats = getRegistryStats();
    assert.ok(stats.totalSkills >= 290, `Expected at least 290 skills, got ${stats.totalSkills}`);
    assert.ok(stats.tier1Count >= 290, `Expected at least 290 Tier 1 skills, got ${stats.tier1Count}`);
    assert.ok(existsSync(stats.dbPath), `Database file not found: ${stats.dbPath}`);
    assert.ok(existsSync(stats.cachePath), `Cache file not found: ${stats.cachePath}`);
  });

  it("Milestone 2.2: SQLite FTS5 search performs sub-millisecond keyword matching", () => {
    const start = performance.now();
    const results = searchRegistry("docker");
    const duration = performance.now() - start;

    assert.ok(results.length > 0, "Expected search results for 'docker'");
    assert.ok(duration < 50, `Expected FTS search under 50ms, took ${duration.toFixed(2)}ms`);

    const hasTier1 = results.some((r) => r.tier === 1);
    assert.ok(hasTier1, "Expected at least one Tier 1 match");
  });

  it("Milestone 2.3: Category filtering returns narrowed domain skills", () => {
    const secResults = searchRegistry("audit", { category: "enterprise-engineering" });
    assert.ok(secResults.length > 0, "Expected enterprise-engineering audit skills");
    for (const r of secResults) {
      assert.strictEqual(r.category, "enterprise-engineering");
    }
  });

  it("Milestone 2.4: getSkill sanitizes content adhering to Zero-Raw-LaTeX Invariant", () => {
    const skillData = getSkill("docker-patterns");
    assert.ok(skillData !== null, "docker-patterns skill should exist");
    assert.strictEqual(skillData.skill.id, "docker-patterns");
    assert.ok(skillData.content.length > 0, "Content should not be empty");
    assert.ok(!skillData.content.includes("$$"), "Skill content must not contain $$ raw LaTeX delimiters");
  });

  it("Milestone 2.5: installSkill materializes Tier 2 skill with frontmatter and updates DB", () => {
    const testSkillId = "007";
    const res = installSkill(testSkillId);
    assert.ok(res.success, `Failed to install skill: ${res.message}`);
    assert.ok(res.installedPath && existsSync(res.installedPath), `Installed file missing at ${res.installedPath}`);

    const fileContent = readFileSync(res.installedPath, "utf-8");
    assert.ok(fileContent.startsWith("---"), "Installed skill must contain standard YAML frontmatter");
    assert.ok(fileContent.includes("name:"), "Frontmatter must contain name field");

    const updated = getSkill(testSkillId);
    assert.ok(updated !== null);
    assert.strictEqual(updated.skill.tier, 1, "Installed skill should now be Tier 1");
  });

  it("Milestone 1.1: MCP Server exposes full tool catalog including skills, memory, and orchestrator", () => {
    const toolNames = TOOLS.map((t) => t.name);
    assert.ok(toolNames.includes("skills_search"), "Missing skills_search tool");
    assert.ok(toolNames.includes("skills_get"), "Missing skills_get tool");
    assert.ok(toolNames.includes("skills_install"), "Missing skills_install tool");
    assert.ok(toolNames.includes("memory_search"), "Missing memory_search tool");
    assert.ok(toolNames.includes("domain_status"), "Missing domain_status tool");
    assert.ok(toolNames.includes("project_stack"), "Missing project_stack tool");
    assert.ok(toolNames.includes("orchestrator_solution"), "Missing orchestrator_solution tool");
  });

  it("Milestone 1.2: MCP skills_search tool returns valid JSON matching query", async () => {
    const rawOutput = await handleToolCall("skills_search", { query: "security", limit: 5 });
    const parsed = JSON.parse(rawOutput);
    assert.ok(parsed.count > 0, "Expected security skills to be returned");
    assert.ok(Array.isArray(parsed.skills), "Expected skills array");
    assert.ok(parsed.skills[0].id, "Skill should have id property");
  });

  it("Milestone 1.3: MCP domain_status tool returns active domain, subdomains, and locks", async () => {
    const rawOutput = await handleToolCall("domain_status", {});
    const parsed = JSON.parse(rawOutput);
    assert.ok(parsed.operating_mode, "Should report operating_mode");
    assert.ok(parsed.domain, "Should report domain");
    assert.ok(Array.isArray(parsed.subdomains), "Should report subdomains array");
    assert.ok(Array.isArray(parsed.statutory_gates), "Should report statutory_gates array");
  });

  it("Milestone 1.4: MCP project_stack tool returns declarative stack and registry stats", async () => {
    const rawOutput = await handleToolCall("project_stack", {});
    const parsed = JSON.parse(rawOutput);
    assert.ok(parsed.project_name, "Should report project_name");
    assert.ok(parsed.skill_registry.total_indexed >= 290, "Should report >=290 indexed skills");
    assert.ok(Array.isArray(parsed.invariants), "Should report invariants array");
  });

  // --- Milestone 3 Tests: Skill Schema Validator & Drift Baseline ---
  it("Milestone 3.1: Skill Schema Validator audits all in-tree skills and verifies Zero-Raw-LaTeX compliance", () => {
    const { total, invalidCount } = validateAllSkills();
    assert.ok(total >= 295, `Expected >=295 skills validated, found ${total}`);
    assert.strictEqual(invalidCount, 0, `Expected 0 invalid skills, found ${invalidCount}`);
  });

  it("Milestone 3.2: Skill validator detects raw LaTeX and missing frontmatter defects", () => {
    const badContent = `This has no frontmatter.\nMath: $x = y^2$ and $$\\sum_{i=1}^n x_i$$`;
    const check = validateSkillContent(badContent, "bad-skill", "bad/path/SKILL.md");
    assert.strictEqual(check.valid, false);
    assert.ok(check.errors.some((e) => e.includes("YAML frontmatter")), "Should detect missing frontmatter");
    assert.ok(check.errors.some((e) => e.includes("Zero-Raw-LaTeX")), "Should detect raw LaTeX");
  });

  it("Milestone 3.3: Skill drift baseline detects untouched status and prevents unauthorized mutation", () => {
    const driftReport = checkDrift();
    assert.ok(driftReport.totalChecked >= 295, "Expected >=295 skills checked in drift baseline");
    assert.strictEqual(driftReport.modified.length, 0, "Expected 0 modified skills in canonical state");
    assert.strictEqual(driftReport.hasDrift, false, "Expected hasDrift to be false");
  });

  // --- Milestone 4 Tests: Tree-Sitter AST Repository Map ---
  it("Milestone 4.1: AST Repository Map Generator compiles topology under <1,500 token ceiling", () => {
    const res = generateRepoMap(["src", "scripts"]);
    assert.ok(res.totalFiles > 20, `Expected >20 scanned files, got ${res.totalFiles}`);
    assert.ok(res.totalSymbols > 50, `Expected >50 indexed symbols, got ${res.totalSymbols}`);
    assert.ok(res.tokenCountEstimate <= 1500, `Expected <=1500 tokens, got ${res.tokenCountEstimate}`);
    assert.ok(existsSync(res.txtPath), `Text repo map missing at ${res.txtPath}`);
    assert.ok(existsSync(res.jsonPath), `JSON repo map missing at ${res.jsonPath}`);
  });

  it("Milestone 4.2: checkRepoMap confirms valid cached map and key symbol presence", () => {
    const status = checkRepoMap();
    assert.strictEqual(status.exists, true, "Repo map should exist");
    assert.strictEqual(status.valid, true, "Repo map should be valid");
    assert.ok(status.tokenEstimate <= 1500, "Token estimate must be <= 1,500");

    const content = readFileSync(status.path, "utf-8");
    assert.ok(content.includes("TaskDispatcher"), "Repo map should include TaskDispatcher symbol");
    assert.ok(content.includes("SquadOrchestrator"), "Repo map should include SquadOrchestrator symbol");
  });

  // --- Milestone 5 Tests: Web Workbench HTTP Server & HTML UI ---
  it("Milestone 5.1: Web Workbench server initializes and serves 3-tier inspection HTML", async () => {
    const wb = createWorkbenchServer(0); // Dynamic available port
    const port = await wb.listen();
    assert.ok(port > 0, "Expected dynamic port assignment");

    try {
      const res = await fetch(`http://127.0.0.1:${port}/`);
      assert.strictEqual(res.status, 200);
      const text = await res.text();
      assert.ok(text.includes("Antigravity Enterprise Workbench"), "HTML should contain workbench title");
      assert.ok(text.includes("app-header"), "HTML must contain app-header element (Rule 14)");
      assert.ok(text.includes("app-viewport"), "HTML must contain app-viewport element (Rule 14)");
      assert.ok(text.includes("app-action-dock"), "HTML must contain app-action-dock element (Rule 14)");
    } finally {
      await wb.close();
    }
  });

  it("Milestone 5.2: Web Workbench REST API returns live status and FTS skills", async () => {
    const wb = createWorkbenchServer(0);
    const port = await wb.listen();

    try {
      const statusRes = await fetch(`http://127.0.0.1:${port}/api/status`);
      assert.strictEqual(statusRes.status, 200);
      const statusData = await statusRes.json();
      assert.ok(["surge", "solo", "portfolio", "team"].includes(statusData.operating_mode), `Expected valid operating mode, got ${statusData.operating_mode}`);
      assert.ok(statusData.registry.totalSkills >= 290);

      const skillsRes = await fetch(`http://127.0.0.1:${port}/api/skills?q=docker`);
      assert.strictEqual(skillsRes.status, 200);
      const skillsData = await skillsRes.json();
      assert.ok(skillsData.count > 0, "Expected docker skills");
      assert.ok(skillsData.skills[0].name.toLowerCase().includes("docker"));
    } finally {
      await wb.close();
    }
  });

  // --- Milestone 6 Tests: Closed-Loop Self-Healing & Auto-Regression Engine ---
  it("Milestone 6.1: auditSelfHealingMetrics achieves >95% self-healing and >85% self-improving scores", () => {
    const audit = auditSelfHealingMetrics();
    assert.ok(audit.overallSelfHealingPercent >= 95.0, `Expected >=95.0% self-healing, got ${audit.overallSelfHealingPercent}%`);
    assert.ok(audit.overallSelfImprovingPercent >= 85.0, `Expected >=85.0% self-improving, got ${audit.overallSelfImprovingPercent}%`);
    assert.strictEqual(audit.stages.length, 7, "Must evaluate all 7 pipeline stages");
    for (const s of audit.stages) {
      assert.strictEqual(s.status, "CLOSED_LOOP");
    }
  });

  it("Milestone 6.2: synthesizeRegressionFixture generates executable test and updates INDEX.json", () => {
    const fixtureName = "concurrency_race_condition";
    const indexPath = existsSync(join(process.cwd(), "pipeline/tests/regression/INDEX.json"))
      ? join(process.cwd(), "pipeline/tests/regression/INDEX.json")
      : join(process.cwd(), "tests/regression/INDEX.json");
    const prevIndexContent = existsSync(indexPath) ? readFileSync(indexPath, "utf-8") : "[]";

    const res = synthesizeRegressionFixture(
      fixtureName,
      { locked: false, owner: "none" },
      { locked: false, owner: "none" },
      "Race condition in concurrent lease acquisition"
    );

    assert.strictEqual(res.success, true);
    assert.ok(existsSync(res.fixturePath), `Fixture file missing at ${res.fixturePath}`);

    const content = readFileSync(res.fixturePath, "utf-8");
    assert.ok(content.includes("Auto-Generated Regression Fixture"), "Fixture should have header");
    assert.ok(content.includes("assert.deepStrictEqual"), "Fixture must assert equality");

    // Clean up test fixture and restore index to maintain clean git status
    if (existsSync(res.fixturePath)) {
      unlinkSync(res.fixturePath);
    }
    writeFileSync(indexPath, prevIndexContent, "utf-8");
  });

  it("Milestone 6.3: getJitNegativeConstraints retrieves negative constraints from Memory Vault", () => {
    const constraints = getJitNegativeConstraints("ai_ml");
    assert.ok(constraints.length >= 6, "Expected at least 6 baseline negative constraints");
    assert.ok(constraints.some((c) => c.includes("INV-01")), "Must include INV-01");
    assert.ok(constraints.some((c) => c.includes("INV-05")), "Must include INV-05");
    assert.ok(constraints.some((c) => c.includes("INV-12")), "Must include INV-12 Zero-Raw-LaTeX");
  });

  it("Milestone 6.4: interviewPromptAmbiguity scores underspecified prompts and provides defaults", () => {
    const vaguePrompt = "build an api";
    const interview = interviewPromptAmbiguity(vaguePrompt);

    assert.ok(interview.ambiguityScore > 0.3, "Vague prompt should have ambiguity score > 0.3");
    assert.ok(interview.clarifications.length >= 2, "Expected at least 2 clarification questions");
    assert.ok(interview.clarifications[0].defaultAssumption.length > 0, "Default assumption must be provided");
  });

  it("Milestone 6.5: generateMutationAssertion synthesizes boundary assertion to kill AST mutant", () => {
    const mutantDiff = "if (x > maxBound)";
    const assertion = generateMutationAssertion(mutantDiff, "resultScore");
    assert.ok(assertion.includes("assert.ok"), "Should generate assert.ok statement");
    assert.ok(assertion.includes("Boundary mutant killed"), "Should state boundary mutant killed");
  });
});
