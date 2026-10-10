/**
 * Antigravity Enterprise Model Context Protocol (MCP) Server
 * Exposes Tiered Skills, SQLite Memory Vault, System Domain Status,
 * and Squad Orchestrator tools via standard JSON-RPC 2.0 stdio.
 * 
 * Compatible with Claude Desktop, Claude Code, Cursor, Windsurf, Zed,
 * and any MCP-compliant AI engineering client.
 */

import { createInterface } from "node:readline";
import { spawn } from "node:child_process";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { DatabaseSync } from "node:sqlite";
import { searchRegistry, getSkill, installSkill, getRegistryStats } from "./catalog-compiler.ts";

export interface McpTool {
  name: string;
  description: string;
  inputSchema: {
    type: "object";
    properties: Record<string, any>;
    required?: string[];
  };
}

export const TOOLS: McpTool[] = [
  // --- Skill Catalog & Knowledge Tools ---
  {
    name: "skills_search",
    description: "Searches the 2,900+ Tiered Skill Registry (Tier 1 In-Tree + Tier 2 AAS Catalog) using SQLite FTS5 full-text search.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Keyword or semantic topic to search for (e.g., 'docker', 'pentest', 'react state', 'kafka')." },
        category: { type: "string", description: "Optional category filter (e.g., 'security', 'devops', 'frontend', 'ai-ml')." },
        tier: { type: "number", enum: [1, 2], description: "Optional tier filter (1 = In-Tree, 2 = AAS Indexed)." },
        limit: { type: "number", description: "Maximum results to return (default 10)." },
      },
      required: ["query"],
    },
  },
  {
    name: "skills_get",
    description: "Retrieves the full markdown specification and execution instructions of any skill by ID (sanitized with Zero-Raw-LaTeX Invariant).",
    inputSchema: {
      type: "object",
      properties: {
        skill_id: { type: "string", description: "Unique skill identifier (e.g., 'docker-patterns', '007', 'container-hardening')." },
      },
      required: ["skill_id"],
    },
  },
  {
    name: "skills_install",
    description: "Materializes a Tier 2 indexed skill into Tier 1 (.agents/skills/<skill_id>/SKILL.md) on-demand with validated frontmatter.",
    inputSchema: {
      type: "object",
      properties: {
        skill_id: { type: "string", description: "Unique skill identifier to materialize." },
      },
      required: ["skill_id"],
    },
  },
  {
    name: "memory_search",
    description: "Queries the persistent SQLite Memory Vault for cross-session decisions, architectural lessons, runbooks, and handoffs.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search query for Memory Vault." },
        kind: { type: "string", enum: ["decision", "lesson", "handoff", "fact", "runbook"], description: "Optional record kind." },
        domain: { type: "string", description: "Optional domain filter (e.g. 'ai_ml', 'software')." },
        limit: { type: "number", description: "Maximum records to return (default 5)." },
      },
      required: ["query"],
    },
  },
  {
    name: "domain_status",
    description: "Returns the active operating mode (Solo, Dual, Team Mesh), active domain, subdomains, statutory gates, and lease locks.",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "project_stack",
    description: "Returns the declarative project stack manifest, active frameworks, testing harnesses, and skill registry statistics.",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },

  // --- Agile Squad Orchestrator Tools ---
  {
    name: "orchestrator_solution",
    description: "Formulates a first-principles dynamic solution architecture with multi-hop live research and 4-moat defensibility matrix.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: { type: "string", description: "Problem statement or feature goal to formulate." },
      },
      required: ["prompt"],
    },
  },
  {
    name: "orchestrator_squad",
    description: "Executes the True Pipeline SDLC lifecycle on a feature with TDD self-healing, AST mutation testing, and living documentation.",
    inputSchema: {
      type: "object",
      properties: {
        feature: { type: "string", description: "Name of the feature to implement." },
        mode: { type: "string", enum: ["solo", "dual", "team"], description: "Execution mode." },
      },
      required: ["feature"],
    },
  },
  {
    name: "orchestrator_research",
    description: "Launches deep empirical research triangulation across 4 modes (EXPLORATION, FEASIBILITY, DIAGNOSTIC, IMPACT) with a minimum 120s deliberation timer.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: { type: "string", description: "Topic or issue to research deeply." },
        mode: { type: "string", enum: ["EXPLORATION", "FEASIBILITY", "DIAGNOSTIC", "IMPACT"], description: "Research operating mode." },
        min_time: { type: "number", description: "Minimum deliberation time budget in seconds (default 120)." },
      },
      required: ["prompt"],
    },
  },
  {
    name: "orchestrator_audit",
    description: "Executes an enterprise 5-pillar project diagnostic audit or brownfield onboarding remediation on an existing or in-progress codebase.",
    inputSchema: {
      type: "object",
      properties: {
        target: { type: "string", description: "Target directory or file path to audit." },
        auto_heal: { type: "boolean", description: "Whether to automatically heal broken stubs and failing tests." },
      },
      required: ["target"],
    },
  },
  {
    name: "orchestrator_team_status",
    description: "Displays the active N-person team roster, active domain lease locks, and cross-device workstation statuses.",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "orchestrator_attest",
    description: "Verifies the cryptographic SQLite attestation ledger and prints the latest verified execution provenance hashes.",
    inputSchema: {
      type: "object",
      properties: {
        verify: { type: "boolean", description: "True to verify the cryptographic ledger integrity." },
      },
    },
  },
];

function runSubprocessCommand(command: string, args: string[]): Promise<string> {
  return new Promise((resolve, reject) => {
    const proc = spawn(command, args, { cwd: process.cwd(), shell: true });
    let stdout = "";
    let stderr = "";
    proc.stdout.on("data", (d: Buffer | string) => { stdout += d.toString(); });
    proc.stderr.on("data", (d: Buffer | string) => { stderr += d.toString(); });
    proc.on("close", (code: number | null) => {
      if (code === 0) resolve(stdout);
      else resolve(`[Command completed with exit code ${code}]\n${stdout}\n${stderr}`);
    });
    proc.on("error", (err: Error) => reject(err));
  });
}

function handleMemorySearch(query: string, kind?: string, domain?: string, limit: number = 5): string {
  const dbPath = join(process.cwd(), ".agents/memory/vault.sqlite");
  if (!existsSync(dbPath)) {
    return JSON.stringify({ count: 0, results: [], message: "Memory Vault database not initialized yet." }, null, 2);
  }

  try {
    const db = new DatabaseSync(dbPath);
    const likePattern = `%${query}%`;
    let sql = `
      SELECT id, title, kind, scope, phase, operator, tags, created_at, body, file_path, domain_id
      FROM memories
      WHERE (title LIKE ? OR body LIKE ? OR tags LIKE ?)
    `;
    const params: any[] = [likePattern, likePattern, likePattern];

    if (kind) {
      sql += " AND kind = ?";
      params.push(kind);
    }
    if (domain) {
      sql += " AND domain_id = ?";
      params.push(domain);
    }

    sql += " ORDER BY created_at DESC LIMIT ?";
    params.push(limit);

    const rows = db.prepare(sql).all(...params) as any[];
    return JSON.stringify({ count: rows.length, results: rows }, null, 2);
  } catch (err: any) {
    return JSON.stringify({ error: err.message || "Failed to query Memory Vault" }, null, 2);
  }
}

function handleDomainStatus(): string {
  const stateDir = join(process.cwd(), ".agents/state");
  const rolePath = join(stateDir, "active-role.json");
  const domainPath = join(stateDir, "active-domain.json");
  const locksDir = join(stateDir, "locks");

  let roleData: any = { mode: "solo" };
  let domainData: any = { domain: "software", subdomains: [] };
  const activeLocks: string[] = [];

  if (existsSync(rolePath)) {
    try { roleData = JSON.parse(readFileSync(rolePath, "utf-8")); } catch {}
  }
  if (existsSync(domainPath)) {
    try { domainData = JSON.parse(readFileSync(domainPath, "utf-8")); } catch {}
  }
  if (existsSync(locksDir)) {
    try {
      const files = readdirSync(locksDir);
      for (const f of files) {
        if (f.endsWith(".lock.json")) {
          activeLocks.push(f.replace(".lock.json", ""));
        }
      }
    } catch {}
  }

  return JSON.stringify({
    operating_mode: roleData.mode || "solo",
    active_role: roleData.role || "Alpha (Lead 1)",
    workstation_operator: roleData.operator || "SoloOperator",
    domain: domainData.domain || "software",
    subdomains: domainData.subdomains || [],
    statutory_gates: domainData.statutory_gates || [],
    active_locks: activeLocks,
    collaborative_mesh: roleData.mode === "team" ? "active" : "standby",
  }, null, 2);
}

function handleProjectStack(): string {
  const stats = getRegistryStats ? getRegistryStats() : { totalSkills: 300, tier1Count: 300, tier2Count: 0 };
  return JSON.stringify({
    project_name: "Antigravity Enterprise Platform",
    architecture_model: "True Pipeline: Deep Surge, Multi-Project / Portfolio Multiplexing, and Collaborative Team Mode",
    personas: ["Product Manager", "System Architect", "Adversarial SDET", "Core Engineer", "Mutation & Security Auditor", "Technical Writer"],
    testing_harness: "Assertion-Backed Deterministic Verification (eval-runner.ts, 0 test theater)",
    skill_registry: {
      total_indexed: stats.totalSkills,
      tier1_in_tree: stats.tier1Count,
      tier2_aas_core: stats.tier2Count,
      protocol: "Model Context Protocol (JSON-RPC 2.0 stdio)",
    },
    invariants: [
      "Zero-Raw-LaTeX Invariant (Unicode math only)",
      "Zero-Secret Shield (Pre-commit hook gated)",
      "Anti-Hardcoding Guard (Mock path & constant rejector)",
      "75% Hardware Memory Ceiling (Kernel SIGKILL protection)",
      "Upstream Cascade Recall Gate (R_upstream >= target + 0.05)",
      "AST Mutation Survivability Gate (>= 80% kill rate)",
    ],
  }, null, 2);
}

export async function handleToolCall(name: string, args: Record<string, any>): Promise<string> {
  // 1. Skill Catalog Tools
  if (name === "skills_search") {
    const results = searchRegistry(args.query || "", {
      category: args.category,
      tier: args.tier,
      limit: args.limit || 10,
    });
    return JSON.stringify({ count: results.length, skills: results }, null, 2);
  } else if (name === "skills_get") {
    const result = getSkill(args.skill_id);
    if (!result) {
      throw new Error(`Skill '${args.skill_id}' not found in registry.`);
    }
    return JSON.stringify(result, null, 2);
  } else if (name === "skills_install") {
    const res = installSkill(args.skill_id);
    return JSON.stringify(res, null, 2);
  } else if (name === "memory_search") {
    return handleMemorySearch(args.query, args.kind, args.domain, args.limit || 5);
  } else if (name === "domain_status") {
    return handleDomainStatus();
  } else if (name === "project_stack") {
    return handleProjectStack();
  }

  // 2. Agile Orchestrator Tools
  else if (name === "orchestrator_solution") {
    return await runSubprocessCommand("python", ["-m", "scripts.orchestrator.task_dispatcher", "--task", "solution", "--prompt", `"${args.prompt}"`]);
  } else if (name === "orchestrator_squad") {
    return await runSubprocessCommand("python", ["-m", "scripts.orchestrator.task_dispatcher", "--task", "squad", "--feature", args.feature, "--mode", args.mode || "solo"]);
  } else if (name === "orchestrator_research") {
    const cmdArgs = ["-m", "scripts.orchestrator.task_dispatcher", "--task", "research", "--prompt", `"${args.prompt}"`];
    if (args.mode) cmdArgs.push("--research-mode", args.mode);
    if (args.min_time) cmdArgs.push("--min-time", String(args.min_time));
    return await runSubprocessCommand("python", cmdArgs);
  } else if (name === "orchestrator_audit") {
    const cmdArgs = ["-m", "scripts.orchestrator.task_dispatcher", "--task", "audit", "--target", `"${args.target}"`];
    if (args.auto_heal) cmdArgs.push("--auto-heal");
    return await runSubprocessCommand("python", cmdArgs);
  } else if (name === "orchestrator_team_status") {
    return await runSubprocessCommand("node", ["--experimental-strip-types", "scripts/role-switch.ts", "team-status"]);
  } else if (name === "orchestrator_attest") {
    return await runSubprocessCommand("python", ["-m", "scripts.orchestrator.squad_attestation", "--verify"]);
  }

  throw new Error(`Tool not found: ${name}`);
}

export function startMcpServer(): void {
  const rl = createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false,
  });

  rl.on("line", async (line: string) => {
    if (!line.trim()) return;
    try {
      const msg = JSON.parse(line);
      const { id, method, params } = msg;

      if (method === "initialize") {
        const response = {
          jsonrpc: "2.0",
          id,
          result: {
            protocolVersion: "2024-11-05",
            capabilities: { tools: {} },
            serverInfo: {
              name: "antigravity-enterprise-orchestrator",
              version: "2.0.0",
            },
          },
        };
        console.log(JSON.stringify(response));
      } else if (method === "tools/list") {
        const response = {
          jsonrpc: "2.0",
          id,
          result: { tools: TOOLS },
        };
        console.log(JSON.stringify(response));
      } else if (method === "tools/call") {
        const { name, arguments: toolArgs } = params;
        try {
          const resultText = await handleToolCall(name, toolArgs || {});
          const response = {
            jsonrpc: "2.0",
            id,
            result: {
              content: [{ type: "text", text: resultText }],
            },
          };
          console.log(JSON.stringify(response));
        } catch (e: any) {
          const response = {
            jsonrpc: "2.0",
            id,
            error: { code: -32603, message: e.message || "Internal Tool Execution Error" },
          };
          console.log(JSON.stringify(response));
        }
      } else if (method === "notifications/initialized") {
        // No response needed for notification
      } else {
        const response = {
          jsonrpc: "2.0",
          id,
          error: { code: -32601, message: `Method not found: ${method}` },
        };
        console.log(JSON.stringify(response));
      }
    } catch (e: any) {
      // Ignore unparseable lines or print JSON-RPC error
    }
  });
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("mcp-server.ts") ||
  process.argv[1].endsWith("mcp-server.js")
);

if (isMain) {
  startMcpServer();
}
