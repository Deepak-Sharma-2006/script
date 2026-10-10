/**
 * Real-Time Active Context Window & Conversation Transcript Meter
 * Measures the active attention window of the current chat/conversation,
 * tracking real memory buffer saturation and remaining headroom before
 * the IDE triggers automatic context compaction.
 */

import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join, basename } from "node:path";
import { homedir } from "node:os";
import { fileURLToPath } from "node:url";
import { getActiveModel, type ModelProfile } from "./token-budget-guard.ts";

export interface ContextTelemetry {
  conversationId: string;
  transcriptPath: string;
  modelId: string;
  modelName: string;
  contextCeiling: number;
  activeChatContextTokens: number;
  remainingBeforeCompaction: number;
  saturationPercent: number;
  cumulativeSessionTokens: number;
  compactionsCount: number;
  statusBracket: "OPTIMAL" | "MODERATE" | "WARNING" | "CRITICAL";
  statusColor: string;
  directives: string[];
}

export function findActiveBrainDirectory(overridePath?: string): string | null {
  if (overridePath && existsSync(overridePath)) {
    return overridePath;
  }

  const appData = join(homedir(), ".gemini", "antigravity-ide", "brain");
  if (!existsSync(appData)) {
    return null;
  }

  const dirs = readdirSync(appData)
    .filter((d) => !d.startsWith(".") && d !== "tempmediaStorage")
    .map((d) => join(appData, d))
    .filter((p) => {
      try {
        return statSync(p).isDirectory();
      } catch {
        return false;
      }
    });

  if (dirs.length === 0) {
    return null;
  }

  // Sort by latest modified time
  dirs.sort((a, b) => statSync(b).mtimeMs - statSync(a).mtimeMs);
  return dirs[0];
}

export function measureConversationContext(brainDir?: string): ContextTelemetry | null {
  const targetDir = brainDir || findActiveBrainDirectory();
  if (!targetDir || !existsSync(targetDir)) {
    return null;
  }

  const conversationId = basename(targetDir);
  const transcriptPath = join(targetDir, ".system_generated", "logs", "transcript.jsonl");

  if (!existsSync(transcriptPath)) {
    return null;
  }

  const model: ModelProfile = getActiveModel();
  const rawContent = readFileSync(transcriptPath, "utf-8");
  const lines = rawContent.split("\n").filter((l) => l.trim().length > 0);

  let totalBytes = 0;
  let postCompactionBytes = 0;
  let compactionsCount = 0;
  let foundCheckpoint = false;

  for (const line of lines) {
    const lineBytes = Buffer.byteLength(line, "utf-8");
    totalBytes += lineBytes;

    try {
      const data = JSON.parse(line);
      const isCompaction =
        data.type === "CHECKPOINT" &&
        (typeof data.content === "string" && data.content.includes("Resuming from a compaction"));

      if (isCompaction) {
        postCompactionBytes = 0;
        compactionsCount++;
        foundCheckpoint = true;
      }
    } catch {
      // Ignore JSON parse errors in malformed lines
    }

    postCompactionBytes += lineBytes;
  }

  // Calibration: 3.8 bytes per token for code, json, and text
  const BYTES_PER_TOKEN = 3.8;
  const activeChatContextTokens = Math.round(postCompactionBytes / BYTES_PER_TOKEN);
  const cumulativeSessionTokens = Math.round(totalBytes / BYTES_PER_TOKEN);

  const contextCeiling = model.contextCeiling;
  const remainingBeforeCompaction = Math.max(0, contextCeiling - activeChatContextTokens);
  const saturationPercent = Number(((activeChatContextTokens / contextCeiling) * 100).toFixed(1));

  let statusBracket: "OPTIMAL" | "MODERATE" | "WARNING" | "CRITICAL" = "OPTIMAL";
  let statusColor = "🟢";
  const directives: string[] = [];

  if (saturationPercent < 40) {
    statusBracket = "OPTIMAL";
    statusColor = "🟢";
    directives.push("Context buffer healthy. Normal execution with standard progressive disclosure.");
  } else if (saturationPercent < 65) {
    statusBracket = "MODERATE";
    statusColor = "🟡";
    directives.push("Context buffer moderately filled. Enforce slice-reading (max 150 lines per view).");
    directives.push("Avoid printing raw command blobs or full files into prompt context.");
  } else if (saturationPercent < 80) {
    statusBracket = "WARNING";
    statusColor = "🟠";
    directives.push("Approaching IDE auto-compaction boundary. Flush key architectural state to Memory Vault.");
    directives.push("Do not re-summarize created artifacts in assistant messages.");
  } else {
    statusBracket = "CRITICAL";
    statusColor = "🔴";
    directives.push("Context window near capacity! Auto-compaction imminent.");
    directives.push("Mandatory state checkpointing: commit pending memory vault notes and prepare for compaction.");
  }

  return {
    conversationId,
    transcriptPath,
    modelId: model.id,
    modelName: model.name,
    contextCeiling,
    activeChatContextTokens,
    remainingBeforeCompaction,
    saturationPercent,
    cumulativeSessionTokens,
    compactionsCount,
    statusBracket,
    statusColor,
    directives,
  };
}

export function printContextStatus(brainDir?: string): void {
  const telemetry = measureConversationContext(brainDir);

  if (!telemetry) {
    console.error("❌ [Context Meter] Could not locate active conversation transcript in brain directory.");
    process.exit(1);
  }

  console.log(`
================================================================================
          ACTIVE CONVERSATION CONTEXT WINDOW & TRANSCRIPT METER
================================================================================
  Conversation ID     : ${telemetry.conversationId}
  Active Model        : ${telemetry.modelName} (${telemetry.modelId})
  Model Ceiling       : ${telemetry.contextCeiling.toLocaleString()} tokens
--------------------------------------------------------------------------------
  ACTIVE WORKING CONTEXT (Current Working Memory Buffer):
    • Active Tokens   : ${telemetry.activeChatContextTokens.toLocaleString()} tokens
    • Remaining Head  : ${telemetry.remainingBeforeCompaction.toLocaleString()} tokens before compaction
    • Saturation      : ${telemetry.saturationPercent}% ${telemetry.statusColor} [${telemetry.statusBracket}]
--------------------------------------------------------------------------------
  LIFETIME CHAT METRICS:
    • Cumulative Total: ${telemetry.cumulativeSessionTokens.toLocaleString()} tokens generated across all turns
    • Compactions Run : ${telemetry.compactionsCount} auto-compaction checkpoints
================================================================================
Active Context Window Directives:`);

  for (const d of telemetry.directives) {
    console.log(`  • ${d}`);
  }
  console.log("================================================================================\n");
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("context-meter.ts") ||
  process.argv[1].endsWith("context-meter.js")
);

if (isMain) {
  const args = process.argv.slice(2);
  if (args.includes("--json")) {
    const telemetry = measureConversationContext();
    console.log(JSON.stringify(telemetry, null, 2));
  } else if (args.includes("--yaml")) {
    const telemetry = measureConversationContext();
    if (telemetry) {
      console.log("  context_telemetry:");
      console.log(`    active_chat_context: ${telemetry.activeChatContextTokens}`);
      console.log(`    remaining_before_compaction: ${telemetry.remainingBeforeCompaction}`);
      console.log(`    saturation: \"${telemetry.saturationPercent}% [${telemetry.statusBracket}]\"`);
      console.log(`    compactions_occurred: ${telemetry.compactionsCount}`);
      console.log(`    cumulative_session_tokens: ${telemetry.cumulativeSessionTokens}`);
    } else {
      console.log("  context_telemetry: null");
    }
  } else {
    printContextStatus();
  }
}
