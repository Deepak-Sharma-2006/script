import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import { join } from "path";
import { fileURLToPath } from "node:url";

export interface ModelProfile {
  id: string;
  name: string;
  provider: string;
  contextCeiling: number;
  inputCostPerMillion: number;
  outputCostPerMillion: number;
  recommendedMaxLoopIterations: number;
  criticalSaturationThreshold: number; // percentage (e.g. 80)
}

export const SUPPORTED_MODELS: Record<string, ModelProfile> = {
  // --- Google Gemini 3.8 Flash (Low, Medium, High) ---
  "gemini-3.8-flash-high": {
    id: "gemini-3.8-flash-high",
    name: "Gemini 3.8 Flash High",
    provider: "Google DeepMind",
    contextCeiling: 1048576,
    inputCostPerMillion: 0.15,
    outputCostPerMillion: 0.60,
    recommendedMaxLoopIterations: 10,
    criticalSaturationThreshold: 75,
  },
  "gemini-3.8-flash-medium": {
    id: "gemini-3.8-flash-medium",
    name: "Gemini 3.8 Flash Medium",
    provider: "Google DeepMind",
    contextCeiling: 1048576,
    inputCostPerMillion: 0.15,
    outputCostPerMillion: 0.60,
    recommendedMaxLoopIterations: 8,
    criticalSaturationThreshold: 75,
  },
  "gemini-3.8-flash-low": {
    id: "gemini-3.8-flash-low",
    name: "Gemini 3.8 Flash Low",
    provider: "Google DeepMind",
    contextCeiling: 1048576,
    inputCostPerMillion: 0.10,
    outputCostPerMillion: 0.40,
    recommendedMaxLoopIterations: 6,
    criticalSaturationThreshold: 75,
  },

  // --- Google Gemini 3.7 Flash (Low, Medium, High) ---
  "gemini-3.7-flash-high": {
    id: "gemini-3.7-flash-high",
    name: "Gemini 3.7 Flash High",
    provider: "Google DeepMind",
    contextCeiling: 1048576,
    inputCostPerMillion: 0.15,
    outputCostPerMillion: 0.60,
    recommendedMaxLoopIterations: 10,
    criticalSaturationThreshold: 75,
  },
  "gemini-3.7-flash-medium": {
    id: "gemini-3.7-flash-medium",
    name: "Gemini 3.7 Flash Medium",
    provider: "Google DeepMind",
    contextCeiling: 1048576,
    inputCostPerMillion: 0.12,
    outputCostPerMillion: 0.50,
    recommendedMaxLoopIterations: 8,
    criticalSaturationThreshold: 75,
  },
  "gemini-3.7-flash-low": {
    id: "gemini-3.7-flash-low",
    name: "Gemini 3.7 Flash Low",
    provider: "Google DeepMind",
    contextCeiling: 1048576,
    inputCostPerMillion: 0.10,
    outputCostPerMillion: 0.40,
    recommendedMaxLoopIterations: 6,
    criticalSaturationThreshold: 75,
  },

  // --- Google Gemini 3.6 Flash (Low, Medium, High) ---
  "gemini-3.6-flash-high": {
    id: "gemini-3.6-flash-high",
    name: "Gemini 3.6 Flash High",
    provider: "Google DeepMind",
    contextCeiling: 1048576,
    inputCostPerMillion: 0.12,
    outputCostPerMillion: 0.50,
    recommendedMaxLoopIterations: 8,
    criticalSaturationThreshold: 75,
  },
  "gemini-3.6-flash-medium": {
    id: "gemini-3.6-flash-medium",
    name: "Gemini 3.6 Flash Medium",
    provider: "Google DeepMind",
    contextCeiling: 1048576,
    inputCostPerMillion: 0.10,
    outputCostPerMillion: 0.40,
    recommendedMaxLoopIterations: 8,
    criticalSaturationThreshold: 75,
  },
  "gemini-3.6-flash-low": {
    id: "gemini-3.6-flash-low",
    name: "Gemini 3.6 Flash Low",
    provider: "Google DeepMind",
    contextCeiling: 1048576,
    inputCostPerMillion: 0.08,
    outputCostPerMillion: 0.30,
    recommendedMaxLoopIterations: 6,
    criticalSaturationThreshold: 75,
  },

  // --- Google Gemini 3.1 Pro (Low & High Only) ---
  "gemini-3.1-pro-high": {
    id: "gemini-3.1-pro-high",
    name: "Gemini 3.1 Pro High",
    provider: "Google DeepMind",
    contextCeiling: 2097152,
    inputCostPerMillion: 1.50,
    outputCostPerMillion: 6.00,
    recommendedMaxLoopIterations: 12,
    criticalSaturationThreshold: 70,
  },
  "gemini-3.1-pro-low": {
    id: "gemini-3.1-pro-low",
    name: "Gemini 3.1 Pro Low",
    provider: "Google DeepMind",
    contextCeiling: 2097152,
    inputCostPerMillion: 1.25,
    outputCostPerMillion: 5.00,
    recommendedMaxLoopIterations: 8,
    criticalSaturationThreshold: 70,
  },

  // --- Anthropic Claude Models ---
  "claude-sonnet-4-6-thinking": {
    id: "claude-sonnet-4-6-thinking",
    name: "Claude Sonnet 4.6 (Thinking)",
    provider: "Anthropic",
    contextCeiling: 200000,
    inputCostPerMillion: 3.00,
    outputCostPerMillion: 15.00,
    recommendedMaxLoopIterations: 6,
    criticalSaturationThreshold: 65,
  },
  "claude-opus-4-6-thinking": {
    id: "claude-opus-4-6-thinking",
    name: "Claude Opus 4.6 (Thinking)",
    provider: "Anthropic",
    contextCeiling: 200000,
    inputCostPerMillion: 15.00,
    outputCostPerMillion: 75.00,
    recommendedMaxLoopIterations: 5,
    criticalSaturationThreshold: 60,
  },

  // --- Open-Source / Local OSS ---
  "gpt-oss-120b-medium": {
    id: "gpt-oss-120b-medium",
    name: "GPT-OSS 120B (Medium)",
    provider: "Open-Source Foundation",
    contextCeiling: 128000,
    inputCostPerMillion: 0.50,
    outputCostPerMillion: 1.50,
    recommendedMaxLoopIterations: 6,
    criticalSaturationThreshold: 65,
  },

  // --- Backwards Compatibility Aliases ---
  "gemini-2.0-flash": {
    id: "gemini-2.0-flash",
    name: "Gemini 2.0 Flash",
    provider: "Google DeepMind",
    contextCeiling: 1048576,
    inputCostPerMillion: 0.10,
    outputCostPerMillion: 0.40,
    recommendedMaxLoopIterations: 8,
    criticalSaturationThreshold: 75,
  },
  "claude-3-5-sonnet": {
    id: "claude-3-5-sonnet",
    name: "Claude 3.5 Sonnet",
    provider: "Anthropic",
    contextCeiling: 200000,
    inputCostPerMillion: 3.00,
    outputCostPerMillion: 15.00,
    recommendedMaxLoopIterations: 5,
    criticalSaturationThreshold: 65,
  },
};

const METRICS_DIR = join(process.cwd(), ".agents/state/metrics");
const ACTIVE_MODEL_FILE = join(process.cwd(), ".agents/state/active-model.json");

export interface PhaseMetrics {
  phase: string;
  modelId: string;
  totalTokensUsed: number;
  inputTokens: number;
  outputTokens: number;
  contextSaturationPercent: number;
  estimatedCostUsd: number;
  lastUpdated: string;
  isBreached: boolean;
  activeDirectives: string[];
}

function ensureMetricsDir(): void {
  if (!existsSync(METRICS_DIR)) {
    mkdirSync(METRICS_DIR, { recursive: true });
  }
}

export function getActiveModel(): ModelProfile {
  if (existsSync(ACTIVE_MODEL_FILE)) {
    try {
      const data = JSON.parse(readFileSync(ACTIVE_MODEL_FILE, "utf-8"));
      if (data.modelId && SUPPORTED_MODELS[data.modelId]) {
        return SUPPORTED_MODELS[data.modelId];
      }
    } catch {
      // Fall through
    }
  }

  // Auto-detect from environment or fallback to gemini-2.0-flash / sonnet
  const envModel = (process.env.MODEL_NAME || "").toLowerCase();
  for (const [key, profile] of Object.entries(SUPPORTED_MODELS)) {
    if (envModel.includes(key) || envModel.includes(profile.name.toLowerCase())) {
      return profile;
    }
  }

  return SUPPORTED_MODELS["gemini-2.0-flash"];
}

export function setActiveModel(modelId: string): boolean {
  if (!SUPPORTED_MODELS[modelId]) {
    console.error(`❌ Unsupported model ID '${modelId}'. Supported: ${Object.keys(SUPPORTED_MODELS).join(", ")}`);
    return false;
  }
  ensureMetricsDir();
  writeFileSync(ACTIVE_MODEL_FILE, JSON.stringify({ modelId, updatedAt: new Date().toISOString() }, null, 2), "utf-8");
  console.log(`✅ [Active Model Set] Workspace configured for '${SUPPORTED_MODELS[modelId].name}' (${SUPPORTED_MODELS[modelId].provider})`);
  return true;
}

export function evaluateOptimizationDirectives(saturationPercent: number, model: ModelProfile): string[] {
  const directives: string[] = [];

  if (saturationPercent < 40) {
    directives.push("🟢 Context Optimal: Normal execution. Maintain progressive disclosure for skill lookups.");
  } else if (saturationPercent < 65) {
    directives.push("🟡 Moderate Saturation: Enforce bounded file slices (max 150 lines per view). Avoid reading files whole.");
    directives.push("🟡 Command Discipline: Suppress verbose terminal outputs; pipe through grep/head/tail.");
  } else if (saturationPercent < model.criticalSaturationThreshold) {
    directives.push("🟠 High Saturation Warning: Do not load full skill manuals. Rely on indexed summaries.");
    directives.push("🟠 Artifact Economy: Do not re-summarize created artifacts in assistant messages.");
    directives.push("🟠 State Offloading: Flush intermediate decisions into Memory Vault (.agents/memory/).");
  } else {
    directives.push("🔴 CRITICAL SATURATION BREACH: Model context window near capacity!");
    directives.push("🔴 Compaction Mandate: Trigger memory compaction. Export phase state and reset turn context.");
    directives.push("🔴 Subagent Delegation: Offload remaining tasks to isolated subagents to preserve root context.");
  }

  return directives;
}

export function recordTokenUsage(params: {
  phase?: string;
  addedInput?: number;
  addedOutput?: number;
  modelId?: string;
}): PhaseMetrics {
  ensureMetricsDir();
  const phase = params.phase || "phase-1";
  const model = params.modelId && SUPPORTED_MODELS[params.modelId] ? SUPPORTED_MODELS[params.modelId] : getActiveModel();
  const metricFile = join(METRICS_DIR, `${phase}-tokens.json`);

  let metrics: PhaseMetrics = {
    phase,
    modelId: model.id,
    totalTokensUsed: 0,
    inputTokens: 0,
    outputTokens: 0,
    contextSaturationPercent: 0,
    estimatedCostUsd: 0,
    lastUpdated: new Date().toISOString(),
    isBreached: false,
    activeDirectives: [],
  };

  if (existsSync(metricFile)) {
    try {
      metrics = JSON.parse(readFileSync(metricFile, "utf-8"));
    } catch {
      // Use defaults
    }
  }

  metrics.modelId = model.id;
  metrics.inputTokens += params.addedInput || 0;
  metrics.outputTokens += params.addedOutput || 0;
  metrics.totalTokensUsed = metrics.inputTokens + metrics.outputTokens;

  // Dynamic cost calculation based on model pricing tier
  const inputCost = (metrics.inputTokens / 1_000_000) * model.inputCostPerMillion;
  const outputCost = (metrics.outputTokens / 1_000_000) * model.outputCostPerMillion;
  metrics.estimatedCostUsd = Number((inputCost + outputCost).toFixed(4));

  // Context saturation
  metrics.contextSaturationPercent = Number(((metrics.totalTokensUsed / model.contextCeiling) * 100).toFixed(2));
  metrics.isBreached = metrics.contextSaturationPercent >= model.criticalSaturationThreshold;
  metrics.activeDirectives = evaluateOptimizationDirectives(metrics.contextSaturationPercent, model);
  metrics.lastUpdated = new Date().toISOString();

  writeFileSync(metricFile, JSON.stringify(metrics, null, 2), "utf-8");

  return metrics;
}

export function printTokenStatus(phase = "phase-1", modelOverride?: string): void {
  const model = modelOverride && SUPPORTED_MODELS[modelOverride] ? SUPPORTED_MODELS[modelOverride] : getActiveModel();
  const metrics = recordTokenUsage({ phase, modelId: model.id });

  console.log(`
================================================================================
           ADAPTIVE MULTI-MODEL TOKEN ECONOMY & CONTEXT OPTIMIZER
================================================================================
  Target Model        : ${model.name} (${model.provider})
  Context Ceiling     : ${model.contextCeiling.toLocaleString()} tokens
  Phase Monitored     : ${phase}
  Tokens Consumed     : ${metrics.totalTokensUsed.toLocaleString()} tokens
    • Input Tokens    : ${metrics.inputTokens.toLocaleString()} (${model.inputCostPerMillion}/M)
    • Output Tokens   : ${metrics.outputTokens.toLocaleString()} (${model.outputCostPerMillion}/M)
  Context Saturation  : ${metrics.contextSaturationPercent}% ${metrics.isBreached ? "🚨 [CRITICAL]" : "🟢 [OPTIMAL]"}
  Estimated Cost      : $${metrics.estimatedCostUsd.toFixed(4)} USD
================================================================================`);

  console.log("Active Context Optimization Directives:");
  for (const d of metrics.activeDirectives) {
    console.log(`  ${d}`);
  }
  console.log("================================================================================\n");
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
  process.argv[1].endsWith("token-budget-guard.ts") ||
  process.argv[1].endsWith("token-budget-guard.js")
);

if (isMain) {
  const rawArgs = process.argv.slice(2);
  const command = (rawArgs[0] && !rawArgs[0].startsWith("--") ? rawArgs[0] : "status").toLowerCase();
  const flags = parseCliFlags(rawArgs);

  if (command === "status") {
    const positional = rawArgs.filter((a) => !a.startsWith("--") && a !== command);
    const phase = flags["phase"] || positional[0] || "phase-1";
    const model = flags["model"] || flags["modelId"] || positional[1];
    printTokenStatus(phase, model);
  } else if (command === "models") {
    console.log("\n🤖 [Supported Antigravity Model Profiles]:\n");
    for (const [id, m] of Object.entries(SUPPORTED_MODELS)) {
      console.log(`• ${m.name.padEnd(22)} (${id})`);
      console.log(`  Provider: ${m.provider} | Context: ${m.contextCeiling.toLocaleString()} tokens`);
      console.log(`  Cost: $${m.inputCostPerMillion}/M in, $${m.outputCostPerMillion}/M out | Max Iterations: ${m.recommendedMaxLoopIterations}\n`);
    }
  } else if (command === "set-model") {
    const positional = rawArgs.filter((a) => !a.startsWith("--") && a !== command);
    const modelId = flags["model"] || flags["modelId"] || positional[0];
    if (!modelId) {
      console.error("Usage: node scripts/token-budget-guard.ts set-model <model-id>");
      process.exit(1);
    }
    setActiveModel(modelId);
  } else if (command === "record") {
    const positional = rawArgs.filter((a) => !a.startsWith("--") && a !== command);
    const phase = flags["phase"] || positional[0] || "phase-1";
    const inp = parseInt(flags["input"] || flags["in"] || positional[1] || "1500", 10);
    const out = parseInt(flags["output"] || flags["out"] || positional[2] || "500", 10);
    const model = flags["model"] || flags["modelId"];
    recordTokenUsage({ phase, addedInput: inp, addedOutput: out, modelId: model });
    printTokenStatus(phase, model);
  } else {
    console.log(`
Usage: node --experimental-strip-types scripts/token-budget-guard.ts <command> [options]

Commands:
  status [--phase <p>] [--model <m>]     Display saturation percentage, cost, and optimization directives
  models                                  List all supported Antigravity model profiles and rate cards
  set-model <model-id>                    Configure active model profile
  record [--phase <p>] [--in <i>] [--out <o>] Record incremental token consumption
`);
  }
}
