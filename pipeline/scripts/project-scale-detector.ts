/**
 * Enterprise Project Scale Detector & Autonomous Resource Optimizer
 * Measures repository lines of code (LOC), file counts, and architecture complexity,
 * separating Application Domain code from the Agentic Workflow Harness and Governance Catalogs.
 */

import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { join, extname, relative } from "node:path";
import { fileURLToPath } from "node:url";

export interface ProjectScaleReport {
  totalLoc: number;
  totalSourceFiles: number;

  // Dual-Scope Metrics
  applicationLoc: number;
  applicationFiles: number;
  harnessLoc: number;
  harnessFiles: number;
  documentationLoc: number;
  documentationFiles: number;

  scale: "SMALL" | "MEDIUM" | "LARGE";
  isLarge: boolean;
  breakdownByExtension: Record<string, { files: number; loc: number }>;
  recommendedMutationMode: "--diff" | "--full";
  sliceViewStrictness: "NORMAL" | "STRICT" | "MANDATORY";
  backgroundDaemonPolicy: "ACTIVE_POLLING_PERMITTED" | "ZERO_PROCESS_EGRESS_RECOMMENDED";
  directives: string[];
}

const EXCLUDED_DIRS = new Set([
  "node_modules",
  ".git",
  "dist",
  "build",
  "test-results",
  ".agents",
  ".vscode",
  "tempmediaStorage",
  ".next",
  "coverage",
]);

const APPLICATION_DIRS = new Set([
  "src",
  "app",
  "pkg",
  "packages",
  "lib",
  "backend",
  "frontend",
  "api",
  "services",
  "demo",
]);

const HARNESS_DIRS = new Set(["scripts", "templates", "browser_tests", "tests"]);

const SOURCE_EXTENSIONS = new Set([
  ".ts",
  ".tsx",
  ".js",
  ".jsx",
  ".py",
  ".json",
  ".css",
  ".html",
  ".md",
  ".rs",
  ".go",
  ".java",
  ".cs",
  ".cpp",
  ".c",
  ".h",
]);

export function countFileLoc(filePath: string): number {
  try {
    const content = readFileSync(filePath, "utf-8");
    return content.split("\n").filter((l) => l.trim().length > 0).length;
  } catch {
    return 0;
  }
}

interface ScanStats {
  totalLoc: number;
  totalFiles: number;
  applicationLoc: number;
  applicationFiles: number;
  harnessLoc: number;
  harnessFiles: number;
  documentationLoc: number;
  documentationFiles: number;
  breakdown: Record<string, { files: number; loc: number }>;
}

export function scanDirectory(
  dirPath: string,
  stats: ScanStats,
  rootDir = process.cwd()
): void {
  if (!existsSync(dirPath)) return;

  try {
    const entries = readdirSync(dirPath);
    for (const entry of entries) {
      if (EXCLUDED_DIRS.has(entry) || entry.startsWith(".")) continue;

      const fullPath = join(dirPath, entry);
      let s;
      try {
        s = statSync(fullPath);
      } catch {
        continue;
      }

      if (s.isDirectory()) {
        scanDirectory(fullPath, stats, rootDir);
      } else if (s.isFile()) {
        const ext = extname(entry).toLowerCase();
        if (SOURCE_EXTENSIONS.has(ext)) {
          const loc = countFileLoc(fullPath);
          stats.totalLoc += loc;
          stats.totalFiles += 1;

          if (!stats.breakdown[ext]) {
            stats.breakdown[ext] = { files: 0, loc: 0 };
          }
          stats.breakdown[ext].files += 1;
          stats.breakdown[ext].loc += loc;

          // Scope Classification
          const rel = relative(rootDir, fullPath).replace(/\\/g, "/");
          const topFolder = rel.split("/")[0];

          if (topFolder === "docs") {
            stats.documentationLoc += loc;
            stats.documentationFiles += 1;
          } else if (HARNESS_DIRS.has(topFolder)) {
            stats.harnessLoc += loc;
            stats.harnessFiles += 1;
          } else if (APPLICATION_DIRS.has(topFolder) || rel.startsWith("src/")) {
            // Note: If demo/ exists in the template, separate pure starter src/ vs demo
            stats.applicationLoc += loc;
            stats.applicationFiles += 1;
          } else {
            // Root-level source files or other folders
            stats.harnessLoc += loc;
            stats.harnessFiles += 1;
          }
        }
      }
    }
  } catch {
    // Ignore permissions/read errors
  }
}

export function detectProjectScale(rootDir = process.cwd()): ProjectScaleReport {
  const stats: ScanStats = {
    totalLoc: 0,
    totalFiles: 0,
    applicationLoc: 0,
    applicationFiles: 0,
    harnessLoc: 0,
    harnessFiles: 0,
    documentationLoc: 0,
    documentationFiles: 0,
    breakdown: {},
  };

  scanDirectory(rootDir, stats, rootDir);

  // Isolate pure core application code (src/ or custom app domain)
  // For a freshly cloned template, demo/ is sample prototype code; src/ is active product code.
  // We classify scale strictly based on application code that will be developed.
  const coreAppDir = join(rootDir, "src");
  let coreAppLoc = 0;
  let coreAppFiles = 0;
  if (existsSync(coreAppDir)) {
    const appStats: ScanStats = {
      totalLoc: 0,
      totalFiles: 0,
      applicationLoc: 0,
      applicationFiles: 0,
      harnessLoc: 0,
      harnessFiles: 0,
      documentationLoc: 0,
      documentationFiles: 0,
      breakdown: {},
    };
    scanDirectory(coreAppDir, appStats, rootDir);
    coreAppLoc = appStats.totalLoc;
    coreAppFiles = appStats.totalFiles;
  }

  // The primary evaluation basis for codebase scale is the active Application Domain
  const evaluationLoc = coreAppLoc > 0 ? coreAppLoc : stats.applicationLoc;
  const evaluationFiles = coreAppFiles > 0 ? coreAppFiles : stats.applicationFiles;

  let scale: "SMALL" | "MEDIUM" | "LARGE" = "SMALL";
  let isLarge = false;
  let recommendedMutationMode: "--diff" | "--full" = "--full";
  let sliceViewStrictness: "NORMAL" | "STRICT" | "MANDATORY" = "NORMAL";
  let backgroundDaemonPolicy: "ACTIVE_POLLING_PERMITTED" | "ZERO_PROCESS_EGRESS_RECOMMENDED" = "ACTIVE_POLLING_PERMITTED";
  const directives: string[] = [];

  if (evaluationLoc < 5000) {
    scale = "SMALL";
    recommendedMutationMode = "--full";
    sliceViewStrictness = "NORMAL";
    backgroundDaemonPolicy = "ACTIVE_POLLING_PERMITTED";
    directives.push(`🟢 Small Application Codebase (${evaluationLoc.toLocaleString()} LOC): Full domain mutation testing enabled without restrictions.`);
    directives.push("🟢 Minimal Resource Footprint: Rapid TDD cycles (<3 seconds); optimal token economy.");
  } else if (evaluationLoc <= 50000) {
    scale = "MEDIUM";
    recommendedMutationMode = "--full";
    sliceViewStrictness = "STRICT";
    backgroundDaemonPolicy = "ACTIVE_POLLING_PERMITTED";
    directives.push(`🟡 Medium Application Codebase (${evaluationLoc.toLocaleString()} LOC): Keep Playwright tests headless to preserve RAM.`);
    directives.push("🟡 Slice Discipline: Enforce max 150 lines per view_file to maintain token budget.");
  } else {
    scale = "LARGE";
    isLarge = true;
    recommendedMutationMode = "--diff";
    sliceViewStrictness = "MANDATORY";
    backgroundDaemonPolicy = "ZERO_PROCESS_EGRESS_RECOMMENDED";
    directives.push(`🔴 Large Enterprise Monorepo (${evaluationLoc.toLocaleString()} LOC): Auto-Guard activates --diff for mutation testing.`);
    directives.push("🔴 Zero-Process Architecture: Terminate background watchers to preserve workstation CPU/battery.");
    directives.push("🔴 Bounded Context Mandate: Whole-file ingestion is strictly prohibited; rely exclusively on grep_search and slices.");
  }

  return {
    totalLoc: stats.totalLoc,
    totalSourceFiles: stats.totalFiles,
    applicationLoc: evaluationLoc,
    applicationFiles: evaluationFiles,
    harnessLoc: stats.harnessLoc,
    harnessFiles: stats.harnessFiles,
    documentationLoc: stats.documentationLoc,
    documentationFiles: stats.documentationFiles,
    scale,
    isLarge,
    breakdownByExtension: stats.breakdown,
    recommendedMutationMode,
    sliceViewStrictness,
    backgroundDaemonPolicy,
    directives,
  };
}

export function printProjectScaleReport(rootDir = process.cwd()): void {
  const report = detectProjectScale(rootDir);

  console.log(`
================================================================================
          ENTERPRISE CODEBASE SCALE DETECTOR (DUAL-SCOPE SEPARATION)
================================================================================
  APPLICATION CODEBASE SCALE       : ${report.scale === "SMALL" ? "🟢 SMALL (<5k LOC)" : report.scale === "MEDIUM" ? "🟡 MEDIUM (5k-50k LOC)" : "🔴 LARGE (>50k LOC)"}
  Application Domain Lines of Code : ${report.applicationLoc.toLocaleString()} LOC across ${report.applicationFiles} file(s)
  Mutation Testing Auto-Policy     : Scoping ${report.recommendedMutationMode === "--diff" ? "[--diff] (Git Diff Scoped)" : "[--full] (Full Domain Scoped)"}
  File Slice Viewing Strictness    : [${report.sliceViewStrictness}] (Max 150 lines/slice)
--------------------------------------------------------------------------------
  DUAL-SCOPE REPOSITORY BREAKDOWN:
    • Application Domain (src/)    : ${report.applicationLoc.toLocaleString().padStart(8, " ")} LOC across ${report.applicationFiles} file(s)  [Governs scale policy]
    • Agentic Workflow Harness     : ${report.harnessLoc.toLocaleString().padStart(8, " ")} LOC across ${report.harnessFiles} file(s)  [Framework tooling]
    • Living Catalogs & Specs      : ${report.documentationLoc.toLocaleString().padStart(8, " ")} LOC across ${report.documentationFiles} file(s)  [Governance & docs]
    • Total Workspace Inode Footprint: ${report.totalLoc.toLocaleString().padStart(8, " ")} LOC across ${report.totalSourceFiles} file(s)
================================================================================
Top File Extensions Breakdown:`);

  const sortedExts = Object.entries(report.breakdownByExtension).sort((a, b) => b[1].loc - a[1].loc);
  for (const [ext, data] of sortedExts.slice(0, 6)) {
    console.log(`  • ${ext.padEnd(8)}: ${data.loc.toLocaleString().padStart(8, " ")} LOC across ${data.files} file(s)`);
  }

  console.log("\nAutonomous Scale Directives:");
  for (const d of report.directives) {
    console.log(`  ${d}`);
  }
  console.log("================================================================================\n");
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("project-scale-detector.ts") ||
  process.argv[1].endsWith("project-scale-detector.js")
);

if (isMain) {
  printProjectScaleReport();
}
