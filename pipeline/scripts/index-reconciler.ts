/**
 * Automated Team Mesh Living Index Reconciler & Conflict-Free Git Merge Driver
 * Reconciles living documentation catalogs (INDEX.md) across N developers,
 * ensuring deterministic, conflict-free branch merges and living index integrity.
 */

import { existsSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, basename } from "node:path";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";

export interface DocumentEntry {
  filename: string;
  title: string;
  timestamp: string;
  relativePath: string;
}

export const CATALOG_DIRECTORIES = [
  { name: "Plans", dir: "docs/plans", indexFile: "docs/plans/INDEX.md", prefix: "PLAN" },
  { name: "Walkthroughs", dir: "docs/walkthroughs", indexFile: "docs/walkthroughs/INDEX.md", prefix: "WALKTHROUGH" },
  { name: "Audits", dir: "docs/audits", indexFile: "docs/audits/INDEX.md", prefix: "AUDIT" },
  { name: "Decisions", dir: "docs/decisions", indexFile: "docs/decisions/INDEX.md", prefix: "DECISION" },
  { name: "Research", dir: "docs/research", indexFile: "docs/research/INDEX.md", prefix: "RESEARCH" },
  { name: "Specifications", dir: "docs/specifications", indexFile: "docs/specifications/INDEX.md", prefix: "SPECIFICATION" },
];

export function extractTitle(filePath: string, fallback: string): string {
  try {
    const content = readFileSync(filePath, "utf-8");
    for (const line of content.split("\n")) {
      const trimmed = line.trim();
      if (trimmed.startsWith("# ") && !trimmed.startsWith("##")) {
        return trimmed.replace(/^#\s+/, "").trim();
      }
    }
  } catch {
    // Fall back to filename
  }
  return fallback;
}

export function extractTimestamp(filename: string): string {
  // Pattern: YYYY-MM-DD_HH-MM-SS or YYYY-MM-DD
  const tsMatch = filename.match(/^(\d{4}-\d{2}-\d{2}(?:_\d{2}-\d{2}-\d{2})?)/);
  if (tsMatch) {
    return tsMatch[1].replace("_", " ");
  }
  return "2026-09-23 00:00:00";
}

export function reconcileDirectory(dirPath: string, indexFilePath: string, catalogName: string): number {
  const fullDir = join(process.cwd(), dirPath);
  if (!existsSync(fullDir)) {
    return 0;
  }

  // Reconcile all markdown documentation files, grouping timestamped revisions
  const allFiles = readdirSync(fullDir)
    .filter((f) => f.endsWith(".md") && f !== "INDEX.md" && f !== "README.md");

  // Map to deduplicate multiple timestamped revisions of the same document
  const slugMap = new Map<string, DocumentEntry>();

  for (const f of allFiles) {
    const fp = join(fullDir, f);
    const title = extractTitle(fp, f.replace(/\.md$/, ""));
    const timestamp = extractTimestamp(f);
    const baseSlug = f.replace(/^\d{4}-\d{2}-\d{2}(?:_\d{2}-\d{2}-\d{2})?_?/, "").replace(/\.md$/, "");

    const entry: DocumentEntry = {
      filename: f,
      title,
      timestamp,
      relativePath: join(dirPath, f).replace(/\\/g, "/"),
    };

    if (!slugMap.has(baseSlug)) {
      slugMap.set(baseSlug, entry);
    } else {
      const existing = slugMap.get(baseSlug)!;
      if (entry.timestamp > existing.timestamp) {
        slugMap.set(baseSlug, entry);
      }
    }
  }

  const entries: DocumentEntry[] = Array.from(slugMap.values());
  // Sort deterministically: latest timestamp first
  entries.sort((a, b) => b.timestamp.localeCompare(a.timestamp));

  const lines = [
    `# Master Living Catalog: ${catalogName}`,
    "",
    "> **Status**: ACTIVE | Automated Living Index | Reconciled via Team Mesh Engine",
    "",
    `Total Registered Documents: **${entries.length}**`,
    "",
    "| Timestamp | Document Title | File Name | Link |",
    "| :--- | :--- | :--- | :--- |",
  ];

  for (const e of entries) {
    lines.push(`| \`${e.timestamp}\` | **${e.title}** | \`${e.filename}\` | [View Document](file:///${e.relativePath}) |`);
  }

  lines.push("");

  const content = lines.join("\n");
  const fullIndexPath = join(process.cwd(), indexFilePath);
  writeFileSync(fullIndexPath, content, "utf-8");

  return entries.length;
}

export function reconcileAllCatalogs(): Record<string, number> {
  const results: Record<string, number> = {};
  console.log("\n================================================================================");
  console.log("       TEAM MESH LIVING INDEX RECONCILER & CONFLICT-FREE MERGE DRIVER");
  console.log("================================================================================");

  for (const cat of CATALOG_DIRECTORIES) {
    const count = reconcileDirectory(cat.dir, cat.indexFile, cat.name);
    results[cat.name] = count;
    console.log(`  [${cat.prefix.padEnd(14)}] ${cat.dir.padEnd(20)} -> ${count.toString().padStart(3, " ")} documents reconciled`);
  }

  console.log("================================================================================\n");
  return results;
}

export function handleGitMerge(ancestorPath: string, currentPath: string, otherPath: string): number {
  console.log(`⚡ [Team Mesh Git Merge Driver] Reconciling concurrent branch changes for: ${currentPath}`);
  try {
    // Find matching catalog definition
    const normalized = currentPath.replace(/\\/g, "/");
    const cat = CATALOG_DIRECTORIES.find((c) => normalized.endsWith(c.indexFile));

    if (cat) {
      reconcileDirectory(cat.dir, cat.indexFile, cat.name);
      console.log(`✅ [Team Mesh Git Merge Driver] Successfully resolved merge conflict on ${currentPath}`);
      return 0;
    } else {
      // Generic directory scan for parent folder
      const parentDir = basename(currentPath) === "INDEX.md" ? join(currentPath, "..") : currentPath;
      reconcileDirectory(parentDir, currentPath, "Living Catalog");
      return 0;
    }
  } catch (err) {
    console.error(`❌ [Team Mesh Git Merge Driver] Error during merge:`, err);
    return 1;
  }
}

export function installGitMergeDriver(): void {
  try {
    console.log("🔧 [Team Mesh] Configuring Git conflict-free merge driver for living index files...");
    execSync('git config merge.docs-index.name "Team Mesh Conflict-Free Living Index Merge Driver"', { stdio: "pipe" });
    execSync('git config merge.docs-index.driver "node --experimental-strip-types scripts/index-reconciler.ts --git-merge %O %A %B"', { stdio: "pipe" });

    // Ensure .gitattributes exists
    const gitattrPath = join(process.cwd(), ".gitattributes");
    let attrContent = "";
    if (existsSync(gitattrPath)) {
      attrContent = readFileSync(gitattrPath, "utf-8");
    }

    const driverRule = "docs/**/INDEX.md merge=docs-index";
    if (!attrContent.includes("merge=docs-index")) {
      attrContent = `${attrContent.trim()}\n${driverRule}\n`.trimStart();
      writeFileSync(gitattrPath, attrContent, "utf-8");
      console.log(`✅ [Team Mesh] Registered 'merge=docs-index' attribute in .gitattributes`);
    }

    console.log("✅ [Team Mesh] Git merge driver configured successfully.");
  } catch (err) {
    console.warn(`⚠️ [Team Mesh] Could not configure git merge driver:`, err);
  }
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("index-reconciler.ts") ||
  process.argv[1].endsWith("index-reconciler.js")
);

if (isMain) {
  const args = process.argv.slice(2);
  if (args.includes("--git-merge")) {
    const idx = args.indexOf("--git-merge");
    const anc = args[idx + 1] || "";
    const cur = args[idx + 2] || "";
    const oth = args[idx + 3] || "";
    const code = handleGitMerge(anc, cur, oth);
    process.exit(code);
  } else if (args.includes("--install-driver")) {
    installGitMergeDriver();
  } else {
    reconcileAllCatalogs();
  }
}
