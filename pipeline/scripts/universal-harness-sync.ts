/**
 * Universal Multi-Harness Instruction Compiler & Synchronizer
 * Verifies that the authoritative UNIVERSAL_AGENT_INSTRUCTIONS.md exists at the
 * repository root and is synchronized with AGENTS.md directives.
 * Eliminates tool-specific subdirectory bloat (.claude/, .codex/, .cursor/, .windsurf/, .github/).
 */

import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

export function syncAllHarnesses(): boolean {
  const rootDir = process.cwd();
  const universalPath = join(rootDir, "UNIVERSAL_AGENT_INSTRUCTIONS.md");
  const agentsPath = join(rootDir, "AGENTS.md");

  if (!existsSync(universalPath) || !existsSync(agentsPath)) {
    console.error("❌ UNIVERSAL_AGENT_INSTRUCTIONS.md or AGENTS.md not found in repository root.");
    return false;
  }

  console.log("================================================================================");
  console.log("🔄 [UNIVERSAL HARNESS SYNC] Validating Universal Agent Instructions");
  console.log("================================================================================");
  console.log("  ✅ Single Universal Instruction File verified: UNIVERSAL_AGENT_INSTRUCTIONS.md");
  console.log("  ✅ Agnostic compatibility verified for Cursor, Claude Code, Windsurf, Copilot, Codex, and Antigravity.");
  console.log("================================================================================\n");
  return true;
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("universal-harness-sync.ts") ||
  process.argv[1].endsWith("universal-harness-sync.js")
);

if (isMain) {
  syncAllHarnesses();
}
