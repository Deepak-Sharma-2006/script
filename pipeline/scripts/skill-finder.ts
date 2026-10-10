import { existsSync, readdirSync, readFileSync, mkdirSync, writeFileSync } from "fs";
import { join } from "path";
import { fileURLToPath } from "node:url";
import { DatabaseSync } from "node:sqlite";

export interface SkillSummary {
  name: string;
  category: string;
  description: string;
  path: string;
  origin: "governance" | "ecc" | "custom";
}

const SKILLS_DIR = join(process.cwd(), ".agents/skills");
const CACHE_DB = join(process.cwd(), ".agents/state/skills-cache.sqlite");

const CORE_GOVERNANCE_SKILLS = new Set([
  "agentic-loop-runner",
  "claude-council",
  "code-reading-dossier",
  "git-sync-lock",
  "skill-finder",
  "skill-creator",
  "styx-pentest",
  "token-budget-guard",
  "grill-me",
]);

function categorizeSkill(name: string, description: string): string {
  if (CORE_GOVERNANCE_SKILLS.has(name)) return "governance";
  const text = (name + " " + description).toLowerCase();

  if (text.includes("product") || text.includes("grill") || text.includes("prompt") || text.includes("pdf") || text.includes("problem") || text.includes("spec") || text.includes("requirement") || text.includes("interview")) {
    return "product-discovery";
  }
  if (text.includes("react") || text.includes("vue") || text.includes("angular") || text.includes("frontend") || text.includes("css") || text.includes("motion") || text.includes("ui") || text.includes("accessibility")) {
    return "frontend";
  }
  if (text.includes("django") || text.includes("spring") || text.includes("fastapi") || text.includes("backend") || text.includes("api") || text.includes("express") || text.includes("database") || text.includes("postgres") || text.includes("redis") || text.includes("sql")) {
    return "backend";
  }
  if (text.includes("security") || text.includes("pentest") || text.includes("vuln") || text.includes("auth") || text.includes("audit") || text.includes("compliance") || text.includes("hipaa")) {
    return "security";
  }
  if (text.includes("rust") || text.includes("golang") || text.includes("go") || text.includes("cpp") || text.includes("csharp") || text.includes("swift") || text.includes("kotlin") || text.includes("java")) {
    return "languages-systems";
  }
  if (text.includes("ml") || text.includes("pytorch") || text.includes("eval") || text.includes("rag") || text.includes("recsys") || text.includes("model")) {
    return "ai-ml";
  }
  if (text.includes("docker") || text.includes("kubernetes") || text.includes("deploy") || text.includes("ci") || text.includes("ops") || text.includes("network") || text.includes("git")) {
    return "devops-infra";
  }
  if (text.includes("tdd") || text.includes("test") || text.includes("clean") || text.includes("refactor") || text.includes("pattern") || text.includes("architecture")) {
    return "quality-architecture";
  }
  return "general";
}

function getCacheDb(): DatabaseSync | null {
  try {
    const dbDir = join(process.cwd(), ".agents/state");
    if (!existsSync(dbDir)) mkdirSync(dbDir, { recursive: true });
    const db = new DatabaseSync(CACHE_DB);
    db.exec(`
      CREATE TABLE IF NOT EXISTS skills (
        name TEXT PRIMARY KEY,
        category TEXT,
        description TEXT,
        path TEXT,
        origin TEXT,
        lastModified INTEGER
      );
    `);
    return db;
  } catch {
    return null;
  }
}

export function listLocalSkills(): SkillSummary[] {
  if (!existsSync(SKILLS_DIR)) {
    return [];
  }

  const dirs = readdirSync(SKILLS_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  const skills: SkillSummary[] = [];

  for (const dir of dirs) {
    const skillPath = join(SKILLS_DIR, dir, "SKILL.md");
    if (existsSync(skillPath)) {
      try {
        const content = readFileSync(skillPath, "utf-8");
        const nameMatch = content.match(/name:\s*([^\n\r]+)/);
        const descMatch = content.match(/description:\s*>?-?\s*([^\n\r]+(?:\n\s+[^\n\r]+)*)/);

        const name = nameMatch ? nameMatch[1].trim() : dir;
        const description = descMatch ? descMatch[1].replace(/\n\s+/g, " ").trim() : "No description provided.";
        const category = categorizeSkill(name, description);
        const origin = CORE_GOVERNANCE_SKILLS.has(name) ? "governance" : "ecc";

        skills.push({
          name,
          category,
          description,
          path: skillPath,
          origin,
        });
      } catch {
        // Skip unreadable files
      }
    }
  }

  return skills.sort((a, b) => a.name.localeCompare(b.name));
}

export function searchSkills(query: string, category?: string): SkillSummary[] {
  const all = listLocalSkills();
  const q = query.toLowerCase();

  return all.filter((s) => {
    const matchesQuery = !query || s.name.toLowerCase().includes(q) || s.description.toLowerCase().includes(q);
    const matchesCat = !category || s.category.toLowerCase() === category.toLowerCase();
    return matchesQuery && matchesCat;
  });
}

export function viewSkill(name: string): string | null {
  const targetDir = join(SKILLS_DIR, name);
  const skillPath = join(targetDir, "SKILL.md");
  if (!existsSync(skillPath)) {
    return null;
  }
  return readFileSync(skillPath, "utf-8");
}

export function createNewSkill(name: string, description: string): boolean {
  const targetDir = join(SKILLS_DIR, name);
  if (existsSync(targetDir)) {
    console.error(`❌ Skill '${name}' already exists at: ${targetDir}`);
    return false;
  }

  mkdirSync(targetDir, { recursive: true });
  const template = `---
name: ${name}
description: >-
  ${description}
---

# ${name} Skill Manual

## 1. Trigger Conditions
- When should this skill be activated?

## 2. Operational Directives & Patterns
- Rule 1: ...
- Rule 2: ...

## 3. Verification Rubric
- [ ] Deterministic test written
- [ ] Verified clean execution
`;

  writeFileSync(join(targetDir, "SKILL.md"), template, "utf-8");
  console.log(`✅ [Skill Created] Initialized skill at: ${targetDir}/SKILL.md`);
  return true;
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
  process.argv[1].endsWith("skill-finder.ts") ||
  process.argv[1].endsWith("skill-finder.js")
);

if (isMain) {
  const rawArgs = process.argv.slice(2);
  const command = (rawArgs[0] && !rawArgs[0].startsWith("--") ? rawArgs[0] : "list").toLowerCase();
  const flags = parseCliFlags(rawArgs);

  if (command === "list") {
    const skills = listLocalSkills();
    console.log(`\n📚 [Agentic Skill Catalog] Total Skills: ${skills.length}`);
    console.log(`================================================================================`);
    const byCat = new Map<string, number>();
    for (const s of skills) {
      byCat.set(s.category, (byCat.get(s.category) || 0) + 1);
    }
    console.log("Categories:");
    for (const [cat, count] of byCat.entries()) {
      console.log(`  • ${cat.padEnd(22)} : ${count} skills`);
    }
    console.log("================================================================================\n");
    console.log("Core Governance Skills:");
    for (const s of skills.filter((x) => x.origin === "governance")) {
      console.log(`  ⭐ ${s.name.padEnd(24)} - ${s.description.slice(0, 70)}...`);
    }
    console.log(`\nTo search skills: npm run skill:search <query>`);
    console.log(`To view skill:   npm run skill:view <skill-name>\n`);
  } else if (command === "search") {
    const positional = rawArgs.filter((a) => !a.startsWith("--") && a !== command);
    const query = flags["query"] || flags["q"] || positional.join(" ") || "";
    const category = flags["category"] || flags["cat"];
    const results = searchSkills(query, category);
    console.log(`\n🔍 Found ${results.length} skill(s) matching '${query}'${category ? ` in [${category}]` : ""}:\n`);
    for (const r of results.slice(0, 25)) {
      const star = r.origin === "governance" ? "⭐ " : "  ";
      console.log(`${star}[${r.category}] ${r.name}`);
      console.log(`   ${r.description.slice(0, 95)}...\n`);
    }
    if (results.length > 25) {
      console.log(`... and ${results.length - 25} more skills. Refine query to narrow down.`);
    }
  } else if (command === "view") {
    const positional = rawArgs.filter((a) => !a.startsWith("--") && a !== command);
    const skillName = flags["skill"] || flags["name"] || positional[0];
    if (!skillName) {
      console.error("Usage: node scripts/skill-finder.ts view <skill-name>");
      process.exit(1);
    }
    const content = viewSkill(skillName);
    if (!content) {
      console.error(`❌ Skill '${skillName}' not found in .agents/skills/`);
      process.exit(1);
    }
    console.log(content);
  } else if (command === "new" || command === "create") {
    const positional = rawArgs.filter((a) => !a.startsWith("--") && a !== command);
    const name = flags["name"] || positional[0];
    const desc = flags["desc"] || flags["description"] || positional.slice(1).join(" ") || "Custom skill definition.";
    if (!name) {
      console.error("Usage: node scripts/skill-finder.ts new <skill-name> [description]");
      process.exit(1);
    }
    const ok = createNewSkill(name, desc);
    process.exit(ok ? 0 : 1);
  } else {
    console.log(`
Usage: node --experimental-strip-types scripts/skill-finder.ts <command> [options]

Commands:
  list                             List all installed skills by category
  search <query> [--cat <cat>]    Search skills by keyword and optional category
  view <skill-name>                Print full SKILL.md contents without context bloat
  new <name> [desc]                Scaffold a new custom skill
`);
  }
}
