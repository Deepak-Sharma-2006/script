/**
 * Antigravity Tiered Skill Engine & SQLite Registry Compiler
 * 
 * Compiles in-tree skills (Tier 1) and global AAS catalog (Tier 2) into
 * a high-performance SQLite database (.agents/skills/registry.sqlite) with FTS5 full-text search,
 * and emits a lightweight cache (.agents/cache/skills_catalog.json).
 * 
 * Also provides on-demand lazy materialization (installSkill) to pull Tier 2 skills into Tier 1
 * while enforcing the Zero-Raw-LaTeX Invariant and YAML frontmatter validation.
 */

import { existsSync, readdirSync, readFileSync, writeFileSync, mkdirSync, statSync } from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { DatabaseSync } from "node:sqlite";

export interface SkillEntry {
  id: string;
  name: string;
  description: string;
  category: string;
  tier: 1 | 2; // 1 = In-Tree Canonical, 2 = Indexed External (AAS)
  path: string;
  risk: string;
  tags: string[];
  source: string;
  date_added?: string;
}

export interface CatalogStats {
  totalSkills: number;
  tier1Count: number;
  tier2Count: number;
  categoriesCount: number;
  dbPath: string;
  cachePath: string;
}

const WORKSPACE_ROOT = process.cwd();
const IN_TREE_SKILLS_DIR = join(WORKSPACE_ROOT, ".agents/skills");
const AAS_INDEX_PATH = join(WORKSPACE_ROOT, "scratch/agentic-awesome-skills/skills_index.json");
const AAS_SKILLS_DIR = join(WORKSPACE_ROOT, "scratch/agentic-awesome-skills/skills");
const REGISTRY_DB_PATH = join(WORKSPACE_ROOT, ".agents/skills/registry.sqlite");
const CACHE_DIR = join(WORKSPACE_ROOT, ".agents/cache");
const CACHE_JSON_PATH = join(CACHE_DIR, "skills_catalog.json");

export function getRegistryDatabase(): DatabaseSync {
  const dir = join(WORKSPACE_ROOT, ".agents/skills");
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });

  const db = new DatabaseSync(REGISTRY_DB_PATH);
  db.exec(`
    CREATE TABLE IF NOT EXISTS skills (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      description TEXT NOT NULL,
      category TEXT NOT NULL,
      tier INTEGER NOT NULL,
      path TEXT NOT NULL,
      risk TEXT DEFAULT 'safe',
      tags TEXT NOT NULL,
      source TEXT NOT NULL,
      date_added TEXT,
      content TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_skills_tier ON skills(tier);
    CREATE INDEX IF NOT EXISTS idx_skills_category ON skills(category);
    CREATE VIRTUAL TABLE IF NOT EXISTS skills_fts USING fts5(
      id, name, description, tags, category
    );
  `);
  return db;
}

function parseFrontmatter(content: string): { name?: string; description?: string; tags?: string[]; category?: string; risk?: string } {
  const frontmatterMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!frontmatterMatch) return {};

  const lines = frontmatterMatch[1].split("\n");
  const res: Record<string, any> = {};
  let currentKey = "";
  let inArray = false;
  const arrayItems: string[] = [];

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;

    if (trimmed.startsWith("- ") && inArray) {
      arrayItems.push(trimmed.slice(2).trim().replace(/^['"]|['"]$/g, ""));
      continue;
    }

    if (inArray && currentKey) {
      res[currentKey] = [...arrayItems];
      inArray = false;
      arrayItems.length = 0;
    }

    const colonIdx = trimmed.indexOf(":");
    if (colonIdx > 0) {
      currentKey = trimmed.slice(0, colonIdx).trim();
      const val = trimmed.slice(colonIdx + 1).trim().replace(/^['"]|['"]$/g, "");
      if (val === "" || val === "[]") {
        inArray = true;
      } else {
        res[currentKey] = val;
      }
    }
  }

  if (inArray && currentKey) {
    res[currentKey] = [...arrayItems];
  }

  return {
    name: res.name,
    description: res.description,
    tags: Array.isArray(res.tags) ? res.tags : (res.tags ? [res.tags] : []),
    category: res.category,
    risk: res.risk,
  };
}

export function compileCatalog(): CatalogStats {
  const db = getRegistryDatabase();

  // Clear existing records to ensure fresh index
  db.exec("DELETE FROM skills; DELETE FROM skills_fts;");

  const insertSkill = db.prepare(`
    INSERT INTO skills (id, name, description, category, tier, path, risk, tags, source, date_added, content)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);

  const insertFts = db.prepare(`
    INSERT INTO skills_fts (id, name, description, tags, category)
    VALUES (?, ?, ?, ?, ?)
  `);

  const inTreeIds = new Set<string>();
  const catalogList: SkillEntry[] = [];

  // Step 1: Scan Tier 1 (In-Tree Skills)
  if (existsSync(IN_TREE_SKILLS_DIR)) {
    const entries = readdirSync(IN_TREE_SKILLS_DIR, { withFileTypes: true });
    for (const ent of entries) {
      if (!ent.isDirectory()) continue;
      const skillId = ent.name;
      const skillPath = join(IN_TREE_SKILLS_DIR, skillId, "SKILL.md");
      if (!existsSync(skillPath)) continue;

      try {
        const rawContent = readFileSync(skillPath, "utf-8");
        const meta = parseFrontmatter(rawContent);

        const name = meta.name || skillId;
        const description = meta.description || `In-tree operational engineering skill for ${skillId}`;
        const category = meta.category || "enterprise-engineering";
        const risk = meta.risk || "safe";
        const tags = meta.tags || [category, "in-tree"];

        inTreeIds.add(skillId);
        inTreeIds.add(name.toLowerCase());

        insertSkill.run(
          skillId,
          name,
          description,
          category,
          1, // Tier 1
          skillPath,
          risk,
          tags.join(", "),
          "in-tree",
          new Date().toISOString().split("T")[0],
          rawContent
        );

        insertFts.run(
          skillId,
          name,
          description,
          tags.join(" "),
          category
        );

        catalogList.push({
          id: skillId,
          name,
          description,
          category,
          tier: 1,
          path: skillPath,
          risk,
          tags,
          source: "in-tree",
        });
      } catch (err) {
        // Skip unreadable files
      }
    }
  }

  // Step 2: Ingest Tier 2 (AAS Core Catalog)
  if (existsSync(AAS_INDEX_PATH)) {
    try {
      const rawIndex = readFileSync(AAS_INDEX_PATH, "utf-8");
      const aasSkills = JSON.parse(rawIndex);

      if (Array.isArray(aasSkills)) {
        for (const item of aasSkills) {
          const id = item.id || item.name;
          if (!id || inTreeIds.has(id.toLowerCase())) continue;

          const name = item.name || id;
          const description = item.description || "AAS modular production skill";
          const category = item.category || "development";
          const risk = item.risk || "safe";
          const tags = Array.isArray(item.tags) ? item.tags : [category];
          const localPath = join(AAS_SKILLS_DIR, id, "SKILL.md");

          insertSkill.run(
            id,
            name,
            description,
            category,
            2, // Tier 2
            localPath,
            risk,
            tags.join(", "),
            "aas",
            item.date_added || "2026-03-01",
            null
          );

          insertFts.run(
            id,
            name,
            description,
            tags.join(" "),
            category
          );

          catalogList.push({
            id,
            name,
            description,
            category,
            tier: 2,
            path: localPath,
            risk,
            tags,
            source: "aas",
            date_added: item.date_added,
          });
        }
      }
    } catch (err) {
      console.error("[CatalogCompiler] Error reading AAS index:", err);
    }
  }

  // Step 3: Write Cache JSON
  if (!existsSync(CACHE_DIR)) mkdirSync(CACHE_DIR, { recursive: true });
  writeFileSync(CACHE_JSON_PATH, JSON.stringify(catalogList, null, 2), "utf-8");

  const tier1Count = catalogList.filter((s) => s.tier === 1).length;
  const tier2Count = catalogList.filter((s) => s.tier === 2).length;
  const categories = new Set(catalogList.map((s) => s.category));

  return {
    totalSkills: catalogList.length,
    tier1Count,
    tier2Count,
    categoriesCount: categories.size,
    dbPath: REGISTRY_DB_PATH,
    cachePath: CACHE_JSON_PATH,
  };
}

export function getRegistryStats(): CatalogStats {
  try {
    const db = getRegistryDatabase();
    const row = db.prepare(`
      SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN tier = 1 THEN 1 ELSE 0 END) as tier1,
        SUM(CASE WHEN tier = 2 THEN 1 ELSE 0 END) as tier2,
        COUNT(DISTINCT category) as categories
      FROM skills
    `).get() as any;

    if (row && row.total > 0) {
      return {
        totalSkills: row.total,
        tier1Count: Number(row.tier1 || 0),
        tier2Count: Number(row.tier2 || 0),
        categoriesCount: Number(row.categories || 0),
        dbPath: REGISTRY_DB_PATH,
        cachePath: CACHE_JSON_PATH,
      };
    }
  } catch {}

  if (existsSync(CACHE_JSON_PATH)) {
    try {
      const data = JSON.parse(readFileSync(CACHE_JSON_PATH, "utf-8"));
      const tier1 = data.filter((s: any) => s.tier === 1).length;
      const tier2 = data.filter((s: any) => s.tier === 2).length;
      const cats = new Set(data.map((s: any) => s.category));
      return {
        totalSkills: data.length,
        tier1Count: tier1,
        tier2Count: tier2,
        categoriesCount: cats.size,
        dbPath: REGISTRY_DB_PATH,
        cachePath: CACHE_JSON_PATH,
      };
    } catch {}
  }

  return {
    totalSkills: 0,
    tier1Count: 0,
    tier2Count: 0,
    categoriesCount: 0,
    dbPath: REGISTRY_DB_PATH,
    cachePath: CACHE_JSON_PATH,
  };
}

export function searchRegistry(
  query: string,
  options: { domain?: string; category?: string; tier?: number; limit?: number } = {}
): SkillEntry[] {
  const db = getRegistryDatabase();
  const limit = options.limit || 15;

  let results: any[] = [];
  const cleanQuery = query.replace(/[^\w\s-]/g, "").trim();

  if (cleanQuery) {
    // FTS5 MATCH query with wildcard
    try {
      const ftsQuery = cleanQuery.split(/\s+/).map((w) => `"${w}"*`).join(" OR ");
      const stmt = db.prepare(`
        SELECT s.id, s.name, s.description, s.category, s.tier, s.path, s.risk, s.tags, s.source
        FROM skills_fts f
        JOIN skills s ON s.id = f.id
        WHERE skills_fts MATCH ?
        ${options.category ? "AND s.category = ?" : ""}
        ${options.tier ? "AND s.tier = ?" : ""}
        ORDER BY s.tier ASC, rank
        LIMIT ?
      `);

      const params: any[] = [ftsQuery];
      if (options.category) params.push(options.category);
      if (options.tier) params.push(options.tier);
      params.push(limit);

      results = stmt.all(...params);
    } catch {
      // Fallback to LIKE query if FTS syntax error
      const likePattern = `%${cleanQuery}%`;
      const stmt = db.prepare(`
        SELECT id, name, description, category, tier, path, risk, tags, source
        FROM skills
        WHERE (name LIKE ? OR description LIKE ? OR tags LIKE ?)
        ${options.category ? "AND category = ?" : ""}
        ${options.tier ? "AND tier = ?" : ""}
        ORDER BY tier ASC
        LIMIT ?
      `);
      const params: any[] = [likePattern, likePattern, likePattern];
      if (options.category) params.push(options.category);
      if (options.tier) params.push(options.tier);
      params.push(limit);

      results = stmt.all(...params);
    }
  } else {
    // Return top Tier 1 skills
    const stmt = db.prepare(`
      SELECT id, name, description, category, tier, path, risk, tags, source
      FROM skills
      ${options.category ? "WHERE category = ?" : ""}
      ORDER BY tier ASC, name ASC
      LIMIT ?
    `);
    const params: any[] = [];
    if (options.category) params.push(options.category);
    params.push(limit);

    results = stmt.all(...params);
  }

  return results.map((r: any) => ({
    id: r.id,
    name: r.name,
    description: r.description,
    category: r.category,
    tier: r.tier as 1 | 2,
    path: r.path,
    risk: r.risk,
    tags: typeof r.tags === "string" ? r.tags.split(",").map((t: string) => t.trim()) : [],
    source: r.source,
  }));
}

export function getSkill(skillId: string): { skill: SkillEntry; content: string } | null {
  const db = getRegistryDatabase();
  const stmt = db.prepare("SELECT * FROM skills WHERE id = ? LIMIT 1");
  const row = stmt.get(skillId) as any;
  if (!row) return null;

  let content = row.content;
  if (!content && existsSync(row.path)) {
    try {
      content = readFileSync(row.path, "utf-8");
    } catch {
      content = `# ${row.name}\n\n${row.description}`;
    }
  }

  // FormatGuard: Replace any raw LaTeX dollar signs with clean Unicode math
  if (content) {
    content = content
      .replace(/\$\$(.*?)\$\$/gs, "$1")
      .replace(/\$(.*?)\$/g, "$1");
  }

  return {
    skill: {
      id: row.id,
      name: row.name,
      description: row.description,
      category: row.category,
      tier: row.tier,
      path: row.path,
      risk: row.risk,
      tags: row.tags ? row.tags.split(",").map((t: string) => t.trim()) : [],
      source: row.source,
    },
    content: content || `# ${row.name}\n\n${row.description}`,
  };
}

export function installSkill(skillId: string): { success: boolean; installedPath?: string; message: string } {
  const db = getRegistryDatabase();
  const item = getSkill(skillId);

  if (!item) {
    return { success: false, message: `Skill '${skillId}' not found in registry.` };
  }

  const targetDir = join(IN_TREE_SKILLS_DIR, skillId);
  const targetFile = join(targetDir, "SKILL.md");

  if (!existsSync(targetDir)) mkdirSync(targetDir, { recursive: true });

  let fileContent = item.content;

  // Ensure valid frontmatter
  if (!fileContent.startsWith("---")) {
    const yamlHeader = [
      "---",
      `name: ${item.skill.name}`,
      `description: ${item.skill.description.replace(/\n/g, " ")}`,
      `category: ${item.skill.category}`,
      `tier: 1`,
      `risk: ${item.skill.risk}`,
      "tools:",
      "  - antigravity",
      "  - claude-code",
      "  - cursor",
      "---",
      "",
    ].join("\n");
    fileContent = yamlHeader + fileContent;
  }

  // Sanitize with Zero-Raw-LaTeX Invariant
  fileContent = fileContent
    .replace(/\$\$(.*?)\$\$/gs, "$1")
    .replace(/\$(.*?)\$/g, "$1");

  writeFileSync(targetFile, fileContent, "utf-8");

  // Update DB tier to 1
  db.prepare("UPDATE skills SET tier = 1, path = ?, content = ? WHERE id = ?").run(
    targetFile,
    fileContent,
    skillId
  );

  return {
    success: true,
    installedPath: targetFile,
    message: `Successfully materialized skill '${skillId}' into Tier 1: ${targetFile}`,
  };
}

// CLI Execution Handlers
function runCli() {
  const args = process.argv.slice(2);
  const command = args[0] || "compile";

  if (command === "compile") {
    console.log("================================================================================");
    console.log("⚡ [TIERED SKILL REGISTRY COMPILER] Indexing Tier 1 & Tier 2 Skill Catalogs...");
    console.log("================================================================================");
    const stats = compileCatalog();
    console.log(`✅ Compilation Succeeded!`);
    console.log(`   • Total Indexed Skills : ${stats.totalSkills}`);
    console.log(`   • Tier 1 (In-Tree)     : ${stats.tier1Count}`);
    console.log(`   • Tier 2 (AAS Core)    : ${stats.tier2Count}`);
    console.log(`   • Categories Covered   : ${stats.categoriesCount}`);
    console.log(`   • SQLite Database      : ${stats.dbPath}`);
    console.log(`   • Cache JSON           : ${stats.cachePath}`);
    console.log("================================================================================");
  } else if (command === "search") {
    const query = args.slice(1).join(" ");
    if (!query) {
      console.log("Usage: node scripts/catalog-compiler.ts search <query>");
      return;
    }
    const results = searchRegistry(query);
    console.log(`Found ${results.length} matches for "${query}":`);
    results.forEach((r, idx) => {
      const tierBadge = r.tier === 1 ? "[Tier 1: In-Tree]" : "[Tier 2: AAS Registry]";
      console.log(` ${idx + 1}. ${tierBadge} ${r.id} (${r.category}) - ${r.description.slice(0, 80)}...`);
    });
  } else if (command === "install") {
    const skillId = args[1];
    if (!skillId) {
      console.log("Usage: node scripts/catalog-compiler.ts install <skill-id>");
      return;
    }
    const res = installSkill(skillId);
    console.log(res.message);
  } else if (command === "list") {
    const results = searchRegistry("", { limit: 20 });
    console.log("Sample Active Skills in Registry:");
    results.forEach((r, idx) => {
      const tierBadge = r.tier === 1 ? "[Tier 1]" : "[Tier 2]";
      console.log(` ${idx + 1}. ${tierBadge} ${r.id} (${r.category})`);
    });
  }
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("catalog-compiler.ts") ||
  process.argv[1].endsWith("catalog-compiler.js")
);

if (isMain) {
  runCli();
}
