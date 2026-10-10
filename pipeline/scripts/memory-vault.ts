import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "fs";
import { join } from "path";
import { fileURLToPath } from "node:url";
import { DatabaseSync } from "node:sqlite";
import { randomBytes } from "node:crypto";

export type MemoryKind = "decision" | "lesson" | "handoff" | "fact" | "runbook";

export interface MemoryRecord {
  id: string;
  schema: "antigravity.memory.v1";
  title: string;
  kind: MemoryKind;
  scope: "project" | "team";
  phase: number;
  operator: string;
  tags: string[];
  createdAt: string;
  body: string;
  filePath: string;
}

const MEMORY_DIR = join(process.cwd(), ".agents/memory");
const DB_PATH = join(MEMORY_DIR, "vault.sqlite");

function ensureMemoryDirs(): void {
  const scopes = ["project", "team"];
  const kinds: MemoryKind[] = ["decision", "lesson", "handoff", "fact", "runbook"];

  for (const s of scopes) {
    for (const k of kinds) {
      const dir = join(MEMORY_DIR, s, `${k}s`);
      if (!existsSync(dir)) {
        mkdirSync(dir, { recursive: true });
      }
    }
  }
}

function getDatabase(): DatabaseSync {
  ensureMemoryDirs();
  const db = new DatabaseSync(DB_PATH);
  db.exec(`
    CREATE TABLE IF NOT EXISTS memories (
      id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      kind TEXT NOT NULL,
      scope TEXT NOT NULL,
      phase INTEGER NOT NULL,
      operator TEXT NOT NULL,
      tags TEXT NOT NULL,
      created_at TEXT NOT NULL,
      body TEXT NOT NULL,
      file_path TEXT NOT NULL,
      domain_id TEXT DEFAULT 'software'
    );
    CREATE INDEX IF NOT EXISTS idx_mem_kind ON memories(kind);
    CREATE INDEX IF NOT EXISTS idx_mem_phase ON memories(phase);
    CREATE INDEX IF NOT EXISTS idx_mem_operator ON memories(operator);
  `);

  try {
    db.exec("ALTER TABLE memories ADD COLUMN domain_id TEXT DEFAULT 'software'");
    db.exec("CREATE INDEX IF NOT EXISTS idx_mem_domain ON memories(domain_id)");
  } catch {
    // column already exists
  }

  return db;
}

export function saveMemory(params: {
  title: string;
  kind: MemoryKind;
  body: string;
  scope?: "project" | "team";
  phase?: number;
  operator?: string;
  tags?: string[];
  domain_id?: string;
}): MemoryRecord {
  ensureMemoryDirs();
  const scope = params.scope || "project";
  const phase = params.phase ?? 1;
  const operator = params.operator || process.env.OPERATOR_NAME || "Computer1";
  const tags = params.tags || [];

  let domainId: string = params.domain_id || "software";
  if (!params.domain_id) {
    const statePath = join(process.cwd(), ".agents", "state", "active-domain.json");
    if (existsSync(statePath)) {
      try {
        const state = JSON.parse(readFileSync(statePath, "utf-8"));
        domainId = state.domain_id || "software";
      } catch {
        domainId = "software";
      }
    }
  }

  const now = new Date().toISOString();
  const slug = params.title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40);
  const id = `mem_${now.slice(0, 10).replace(/-/g, "")}_${randomBytes(4).toString("hex")}`;

  const fileName = `${slug || id}.md`;
  const validKinds: MemoryKind[] = ["decision", "lesson", "handoff", "fact", "runbook"];
  const kind: MemoryKind = validKinds.includes(params.kind) ? params.kind : "decision";
  const relativeSubdir = `${kind}s`;
  const targetDir = join(MEMORY_DIR, scope, relativeSubdir);
  if (!existsSync(targetDir)) {
    mkdirSync(targetDir, { recursive: true });
  }
  const fullPath = join(targetDir, fileName);

  const frontmatter = [
    "---",
    'schema: "antigravity.memory.v1"',
    `id: "${id}"`,
    `title: ${JSON.stringify(params.title)}`,
    `kind: "${kind}"`,
    `scope: "${scope}"`,
    `phase: ${phase}`,
    `operator: "${operator}"`,
    `domainId: "${domainId}"`,
    `tags: ${JSON.stringify(tags)}`,
    `createdAt: "${now}"`,
    "---",
    "",
    params.body.trim(),
    "",
  ].join("\n");

  writeFileSync(fullPath, frontmatter, "utf-8");

  // Index into SQLite
  const db = getDatabase();
  const insert = db.prepare(`
    INSERT OR REPLACE INTO memories (id, title, kind, scope, phase, operator, tags, created_at, body, file_path, domain_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);
  insert.run(id, params.title, kind, scope, phase, operator, JSON.stringify(tags), now, params.body.trim(), fullPath, domainId);

  console.log(`💾 [Memory Vault] Saved ${kind}: "${params.title}" (ID: ${id}, Domain: ${domainId})`);
  console.log(`   📄 File: ${fullPath}`);

  return {
    id,
    schema: "antigravity.memory.v1",
    title: params.title,
    kind,
    scope,
    phase,
    operator,
    tags,
    createdAt: now,
    body: params.body.trim(),
    filePath: fullPath,
  };
}

export function searchMemories(query: string, kind?: MemoryKind, phase?: number, domainId?: string): MemoryRecord[] {
  const db = getDatabase();
  let sql = "SELECT * FROM memories WHERE 1=1";
  const args: any[] = [];

  if (query && query.trim()) {
    sql += " AND (title LIKE ? OR body LIKE ? OR tags LIKE ?)";
    const term = `%${query.trim()}%`;
    args.push(term, term, term);
  }
  if (kind) {
    sql += " AND kind = ?";
    args.push(kind);
  }
  if (phase !== undefined) {
    sql += " AND phase = ?";
    args.push(phase);
  }

  let activeDomain = domainId;
  if (!activeDomain) {
    const statePath = join(process.cwd(), ".agents", "state", "active-domain.json");
    if (existsSync(statePath)) {
      try {
        const state = JSON.parse(readFileSync(statePath, "utf-8"));
        activeDomain = state.domain_id;
      } catch {
        // ignore
      }
    }
  }

  if (activeDomain) {
    sql += " ORDER BY (CASE WHEN domain_id = ? THEN 0 ELSE 1 END), created_at DESC LIMIT 50";
    args.push(activeDomain);
  } else {
    sql += " ORDER BY created_at DESC LIMIT 50";
  }

  const rows = db.prepare(sql).all(...args) as any[];
  return rows.map((r) => ({
    id: r.id,
    schema: "antigravity.memory.v1",
    title: r.title,
    kind: r.kind as MemoryKind,
    scope: r.scope as "project" | "team",
    phase: r.phase,
    operator: r.operator,
    tags: (() => {
      try {
        const parsed = JSON.parse(r.tags || "[]");
        return Array.isArray(parsed) ? parsed : [String(parsed)];
      } catch {
        return (r.tags || "").split(",").map((t: string) => t.trim()).filter(Boolean);
      }
    })(),
    createdAt: r.created_at,
    body: r.body,
    filePath: r.file_path,
  }));
}

export function recallLessons(domain: string, limit = 5): MemoryRecord[] {
  return searchMemories(domain, "lesson").slice(0, limit);
}

export function doctorVault(): { totalFiles: number; totalDbRows: number; reindexed: number } {
  ensureMemoryDirs();
  const db = getDatabase();
  let fileCount = 0;
  let reindexedCount = 0;

  const scopes = ["project", "team"];
  const kinds: MemoryKind[] = ["decision", "lesson", "handoff", "fact", "runbook"];

  const upsert = db.prepare(`
    INSERT OR REPLACE INTO memories (id, title, kind, scope, phase, operator, tags, created_at, body, file_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);

  for (const s of scopes) {
    for (const k of kinds) {
      const dir = join(MEMORY_DIR, s, `${k}s`);
      if (existsSync(dir)) {
        const files = readdirSync(dir).filter((f) => f.endsWith(".md"));
        for (const f of files) {
          fileCount++;
          try {
            const content = readFileSync(join(dir, f), "utf-8");
            const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
            if (match) {
              const meta: any = {};
              for (const line of match[1].split("\n")) {
                const parts = line.split(":");
                if (parts.length >= 2) {
                  const key = parts[0].trim();
                  const val = parts.slice(1).join(":").trim().replace(/^["']|["']$/g, "");
                  meta[key] = val;
                }
              }
              const id = meta.id || `mem_${f.replace(/\.md$/, "")}`;
              const title = meta.title || f.replace(/\.md$/, "");
              const phase = parseInt(meta.phase || "1", 10);
              const operator = meta.operator || "Computer1";
              const rawTags = meta.tags || "[]";
              let tags = rawTags;
              try {
                const parsed = JSON.parse(rawTags);
                tags = JSON.stringify(Array.isArray(parsed) ? parsed : [parsed]);
              } catch {
                tags = JSON.stringify(rawTags.split(",").map((t: string) => t.trim()).filter(Boolean));
              }
              const createdAt = meta.createdAt || new Date().toISOString();
              const body = match[2].trim();

              upsert.run(id, title, k, s, phase, operator, tags, createdAt, body, join(dir, f));
              reindexedCount++;
            }
          } catch {
            // Malformed
          }
        }
      }
    }
  }

  const row = db.prepare("SELECT COUNT(*) as count FROM memories").get() as any;
  const totalDbRows = row ? row.count : 0;

  console.log(`\n🏥 [Memory Vault Doctor] Check Complete`);
  console.log(`   Markdown Files in Vault : ${fileCount}`);
  console.log(`   Indexed SQLite Rows     : ${totalDbRows}`);
  console.log(`   Re-Indexed Entries      : ${reindexedCount}\n`);

  return { totalFiles: fileCount, totalDbRows, reindexed: reindexedCount };
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
  process.argv[1].endsWith("memory-vault.ts") ||
  process.argv[1].endsWith("memory-vault.js")
);

if (isMain) {
  const rawArgs = process.argv.slice(2);
  const command = (rawArgs[0] && !rawArgs[0].startsWith("--") ? rawArgs[0] : "doctor").toLowerCase();
  const flags = parseCliFlags(rawArgs);

  if (command === "save") {
    const positional = rawArgs.filter((a) => !a.startsWith("--") && a !== command);
    const rawKind = flags["type"] || flags["kind"] || positional[0] || "decision";
    const validKinds: MemoryKind[] = ["decision", "lesson", "handoff", "fact", "runbook"];
    const kind: MemoryKind = validKinds.includes(rawKind as MemoryKind) ? (rawKind as MemoryKind) : "decision";

    const title = flags["title"] || positional[1] || "Untitled Memory";
    const body = flags["body"] || flags["summary"] || positional.slice(2).join(" ") || "No content provided.";
    const tags = flags["tags"] ? flags["tags"].split(",").map((t) => t.trim()) : [];
    const scope = (flags["scope"] as "project" | "team") || "project";
    const phase = flags["phase"] ? parseInt(flags["phase"], 10) : 1;

    saveMemory({ kind, title, body, tags, scope, phase });
  } else if (command === "search") {
    const positional = rawArgs.filter((a) => !a.startsWith("--") && a !== command);
    const q = flags["query"] || flags["q"] || positional.join(" ") || "";
    const rawKind = flags["type"] || flags["kind"];
    const kind = rawKind as MemoryKind | undefined;
    const results = searchMemories(q, kind);
    console.log(`\n🔍 Found ${results.length} memory record(s) matching '${q}':\n`);
    for (const r of results) {
      console.log(`[${r.kind.toUpperCase()}] ${r.title} (Phase ${r.phase} by ${r.operator})`);
      console.log(`   ${r.body.slice(0, 120)}...`);
      console.log(`   📁 ${r.filePath}\n`);
    }
  } else if (command === "doctor") {
    doctorVault();
  } else {
    console.log(`
Usage: node --experimental-strip-types scripts/memory-vault.ts <command> [options]

Commands:
  save --type <kind> --title <title> --body <body> [--tags tag1,tag2] [--scope project|team]
  search <query> [--type <kind>]
  doctor                       Validate files and re-index SQLite search catalog
`);
  }
}
