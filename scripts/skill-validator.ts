/**
 * Antigravity Skill Schema Validator & Automated Drift Baseline Engine
 * 
 * Validates in-tree SKILL.md files against enterprise schema specifications:
 * - YAML frontmatter integrity (name, description, category/tags)
 * - 'When to Use' operational trigger section presence
 * - Zero-Raw-LaTeX Invariant enforcement (rejecting $ and $$ in favor of Unicode math)
 * 
 * Tracks SHA-256 drift baselines in .agents/state/skills_drift_baseline.json to detect
 * unauthorized skill mutations, upstream drift, or silent degradation.
 */

import { existsSync, readdirSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";

export interface SkillValidationResult {
  skillId: string;
  path: string;
  valid: boolean;
  errors: string[];
  warnings: string[];
  sha256: string;
}

export interface DriftReport {
  totalChecked: number;
  untouched: number;
  modified: string[];
  newSkills: string[];
  deletedSkills: string[];
  hasDrift: boolean;
}

const WORKSPACE_ROOT = process.cwd();
const SKILLS_DIR = join(WORKSPACE_ROOT, ".agents/skills");
const STATE_DIR = join(WORKSPACE_ROOT, ".agents/state");
const BASELINE_FILE = join(STATE_DIR, "skills_drift_baseline.json");

function computeSha256(content: string): string {
  return createHash("sha256").update(content, "utf8").digest("hex");
}

export function validateSkillContent(content: string, skillId: string, filePath: string): SkillValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];

  // 1. YAML frontmatter check
  const frontmatterMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!frontmatterMatch) {
    errors.push("Missing YAML frontmatter (must start and end with '---')");
  } else {
    const fmLines = frontmatterMatch[1].split("\n");
    let hasName = false;
    let hasDesc = false;

    for (const l of fmLines) {
      const trimmed = l.trim();
      if (/^name\s*:\s*.+/.test(trimmed)) hasName = true;
      if (/^description\s*:\s*.+/.test(trimmed)) hasDesc = true;
    }

    if (!hasName) errors.push("Frontmatter missing required 'name' field");
    if (!hasDesc) errors.push("Frontmatter missing required 'description' field");
  }

  // 2. Operational trigger section check
  const lower = content.toLowerCase();
  if (!lower.includes("when to use") && !lower.includes("trigger") && !lower.includes("usage")) {
    warnings.push("Missing explicit 'When to Use' operational trigger section");
  }

  // 3. Zero-Raw-LaTeX Invariant enforcement
  if (/\$\$[\s\S]*?\$\$/.test(content)) {
    errors.push("Zero-Raw-LaTeX Invariant violation: contains raw '$$' LaTeX block math delimiters");
  }
  if (/\$[^$\n\r]+\$/.test(content)) {
    errors.push("Zero-Raw-LaTeX Invariant violation: contains raw '$' LaTeX inline math delimiters");
  }

  const sha256 = computeSha256(content);

  return {
    skillId,
    path: filePath,
    valid: errors.length === 0,
    errors,
    warnings,
    sha256,
  };
}

export function validateAllSkills(options: { autoFix?: boolean } = {}): {
  total: number;
  validCount: number;
  invalidCount: number;
  results: SkillValidationResult[];
} {
  if (!existsSync(SKILLS_DIR)) {
    return { total: 0, validCount: 0, invalidCount: 0, results: [] };
  }

  const entries = readdirSync(SKILLS_DIR, { withFileTypes: true });
  const results: SkillValidationResult[] = [];

  for (const ent of entries) {
    if (!ent.isDirectory()) continue;
    const skillId = ent.name;
    const skillPath = join(SKILLS_DIR, skillId, "SKILL.md");
    if (!existsSync(skillPath)) continue;

    let content = readFileSync(skillPath, "utf-8");

    if (options.autoFix) {
      let modified = false;

      // Fix raw LaTeX if present
      if (content.includes("$")) {
        content = content
          .replace(/\$\$(.*?)\$\$/gs, "$1")
          .replace(/\$([^$\n]+)\$/g, "$1");
        modified = true;
      }

      // Fix frontmatter if missing
      if (!content.startsWith("---")) {
        const header = `---\nname: ${skillId}\ndescription: Operational skill instructions for ${skillId}\ntools:\n  - antigravity\n  - claude-code\n---\n\n`;
        content = header + content;
        modified = true;
      }

      if (modified) {
        writeFileSync(skillPath, content, "utf-8");
      }
    }

    const res = validateSkillContent(content, skillId, skillPath);
    results.push(res);
  }

  const validCount = results.filter((r) => r.valid).length;
  const invalidCount = results.filter((r) => !r.valid).length;

  return {
    total: results.length,
    validCount,
    invalidCount,
    results,
  };
}

export function updateDriftBaseline(): { baselinePath: string; skillCount: number } {
  if (!existsSync(STATE_DIR)) mkdirSync(STATE_DIR, { recursive: true });

  const { results } = validateAllSkills({ autoFix: false });
  const baseline: Record<string, { sha256: string; path: string; updatedAt: string }> = {};

  const now = new Date().toISOString();
  for (const r of results) {
    baseline[r.skillId] = {
      sha256: r.sha256,
      path: r.path,
      updatedAt: now,
    };
  }

  writeFileSync(BASELINE_FILE, JSON.stringify(baseline, null, 2), "utf-8");
  return {
    baselinePath: BASELINE_FILE,
    skillCount: Object.keys(baseline).length,
  };
}

export function checkDrift(): DriftReport {
  if (!existsSync(BASELINE_FILE)) {
    // Generate baseline if it doesn't exist yet
    updateDriftBaseline();
  }

  const rawBaseline = readFileSync(BASELINE_FILE, "utf-8");
  const baseline: Record<string, { sha256: string; path: string }> = JSON.parse(rawBaseline);

  const { results } = validateAllSkills();
  const currentSkills = new Map(results.map((r) => [r.skillId, r]));

  const modified: string[] = [];
  const newSkills: string[] = [];
  const deletedSkills: string[] = [];
  let untouched = 0;

  for (const [id, base] of Object.entries(baseline)) {
    const cur = currentSkills.get(id);
    if (!cur) {
      deletedSkills.push(id);
    } else if (cur.sha256 !== base.sha256) {
      modified.push(id);
    } else {
      untouched++;
    }
  }

  for (const [id] of currentSkills) {
    if (!baseline[id]) {
      newSkills.push(id);
    }
  }

  const hasDrift = modified.length > 0 || deletedSkills.length > 0;

  return {
    totalChecked: results.length,
    untouched,
    modified,
    newSkills,
    deletedSkills,
    hasDrift,
  };
}

// CLI Execution Handler
function runCli() {
  const args = process.argv.slice(2);
  const command = args[0] || "check";
  const autoFix = args.includes("--fix");

  if (command === "check") {
    console.log("================================================================================");
    console.log("🛡️  [SKILL SCHEMA VALIDATOR] Auditing In-Tree Skills for Enterprise Compliance");
    console.log("================================================================================");
    const { total, validCount, invalidCount, results } = validateAllSkills({ autoFix });

    if (invalidCount > 0) {
      console.log(`⚠️  Found ${invalidCount} / ${total} skills with schema violations:\n`);
      for (const r of results.filter((x) => !x.valid)) {
        console.log(`  ❌ ${r.skillId}:`);
        r.errors.forEach((e) => console.log(`     • [ERROR] ${e}`));
        r.warnings.forEach((w) => console.log(`     • [WARN]  ${w}`));
      }
      console.log("\nRun with --fix to automatically synthesize frontmatter and sanitize LaTeX.");
      process.exit(1);
    } else {
      console.log(`✅ All ${total} in-tree skills adhere strictly to Enterprise Specifications & Zero-LaTeX!`);
      console.log("================================================================================");
    }
  } else if (command === "drift") {
    console.log("================================================================================");
    console.log("🔍 [SKILL DRIFT SHIELD] Checking Cryptographic SHA-256 Baseline Integrity");
    console.log("================================================================================");
    const report = checkDrift();

    console.log(`Checked ${report.totalChecked} skills against canonical baseline:`);
    console.log(`  • Untouched   : ${report.untouched}`);
    console.log(`  • Modified    : ${report.modified.length}`);
    console.log(`  • New Skills  : ${report.newSkills.length}`);
    console.log(`  • Deleted     : ${report.deletedSkills.length}`);

    if (report.modified.length > 0) {
      console.log("\n🚨 MODIFIED SKILLS DETECTED (Drift Alert):");
      report.modified.forEach((s) => console.log(`  - ${s}`));
    }
    if (report.newSkills.length > 0) {
      console.log("\n✨ NEW UNTRACKED SKILLS:");
      report.newSkills.forEach((s) => console.log(`  + ${s}`));
    }
    if (report.deletedSkills.length > 0) {
      console.log("\n🗑️  DELETED CANONICAL SKILLS:");
      report.deletedSkills.forEach((s) => console.log(`  x ${s}`));
    }

    if (report.hasDrift) {
      console.log("\nRun 'npm run skills:drift:update' to intentionally record new baseline hashes.");
      process.exit(1);
    } else {
      console.log("\n✅ Zero unauthorized skill drift detected. Canonical baseline is 100% verified.");
      console.log("================================================================================");
    }
  } else if (command === "update-baseline") {
    const { baselinePath, skillCount } = updateDriftBaseline();
    console.log(`✅ Updated canonical skill drift baseline (${skillCount} skills indexed): ${baselinePath}`);
  }
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("skill-validator.ts") ||
  process.argv[1].endsWith("skill-validator.js")
);

if (isMain) {
  runCli();
}
