/**
 * Antigravity Web Workbench Server
 * 
 * Zero-dependency local HTTP server (node:http) serving the pre-commit inspection UI
 * and providing REST APIs for Tiered Skill Registry searches, skill materialization,
 * AST repo-map visualization, and statutory gate status.
 */

import { createServer, IncomingMessage, ServerResponse } from "node:http";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { searchRegistry, installSkill, getRegistryStats } from "./catalog-compiler.ts";
import { checkRepoMap, generateRepoMap } from "./repo-map-generator.ts";

const WORKSPACE_ROOT = process.cwd();
const HTML_PATH = join(WORKSPACE_ROOT, "templates/workbench/index.html");
const REPO_MAP_TXT = join(WORKSPACE_ROOT, ".agents/cache/repo_map.txt");

export function createWorkbenchServer(port: number = 4500) {
  const server = createServer(async (req: IncomingMessage, res: ServerResponse) => {
    const parsedUrl = new URL(req.url || "/", `http://${req.headers.host || "localhost"}`);
    const pathname = parsedUrl.pathname;

    // Enable CORS for local testing
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");

    if (req.method === "OPTIONS") {
      res.writeHead(204);
      res.end();
      return;
    }

    // 1. Serve Workbench HTML
    if (pathname === "/" || pathname === "/index.html") {
      if (existsSync(HTML_PATH)) {
        const html = readFileSync(HTML_PATH, "utf-8");
        res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
        res.end(html);
      } else {
        res.writeHead(404, { "Content-Type": "text/plain" });
        res.end("Workbench HTML template not found.");
      }
      return;
    }

    // 2. API: System Status
    if (pathname === "/api/status") {
      const stats = getRegistryStats();
      const payload = {
        operating_mode: "solo",
        active_domain: "ai_ml",
        subdomains: ["computer_vision", "deep_learning"],
        statutory_gates: [
          "Zero-Raw-LaTeX Invariant",
          "Zero-Secret Pre-Commit Shield",
          "Deterministic Mutation Testing Gate (>=80%)",
          "Anti-Hardcoding & Distractor Parity Guard",
          "Hardware Memory Guard (75% RAM)",
        ],
        registry: stats,
      };
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify(payload, null, 2));
      return;
    }

    // 3. API: Search Skills
    if (pathname === "/api/skills") {
      const q = parsedUrl.searchParams.get("q") || "";
      const results = searchRegistry(q, { limit: 25 });
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ count: results.length, skills: results }));
      return;
    }

    // 4. API: Install Skill
    if (pathname === "/api/skills/install" && req.method === "POST") {
      let body = "";
      req.on("data", (chunk) => { body += chunk; });
      req.on("end", () => {
        try {
          const parsed = JSON.parse(body || "{}");
          const skillId = parsed.skillId;
          if (!skillId) {
            res.writeHead(400, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ success: false, message: "Missing skillId parameter." }));
            return;
          }
          const installRes = installSkill(skillId);
          res.writeHead(200, { "Content-Type": "application/json" });
          res.end(JSON.stringify(installRes));
        } catch (err: any) {
          res.writeHead(500, { "Content-Type": "application/json" });
          res.end(JSON.stringify({ success: false, message: err.message }));
        }
      });
      return;
    }

    // 5. API: AST Repo-Map
    if (pathname === "/api/repo-map") {
      let mapText = "";
      let tokenEstimate = 0;
      if (existsSync(REPO_MAP_TXT)) {
        mapText = readFileSync(REPO_MAP_TXT, "utf-8");
        tokenEstimate = Math.ceil(mapText.length / 4);
      } else {
        const genRes = generateRepoMap();
        mapText = genRes.mapText;
        tokenEstimate = genRes.tokenCountEstimate;
      }
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ mapText, tokenEstimate }));
      return;
    }

    // 6. 404 Fallback
    res.writeHead(404, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "Endpoint not found", path: pathname }));
  });

  return {
    server,
    listen: (customPort?: number) => {
      const p = customPort !== undefined ? customPort : port;
      return new Promise<number>((resolve) => {
        server.listen(p, "127.0.0.1", () => {
          const addr = server.address();
          const actualPort = typeof addr === "object" && addr ? addr.port : p;
          resolve(actualPort);
        });
      });
    },
    close: () => new Promise<void>((resolve) => server.close(() => resolve())),
  };
}

// CLI Execution Handler
async function runCli() {
  const args = process.argv.slice(2);
  let port = 4500;
  const portIdx = args.indexOf("--port");
  if (portIdx !== -1 && args[portIdx + 1]) {
    port = parseInt(args[portIdx + 1], 10);
  }

  const { listen } = createWorkbenchServer(port);
  const actualPort = await listen(port);

  console.log("================================================================================");
  console.log(`🌐 [ANTIGRAVITY WORKBENCH] Local Pre-Commit Inspection UI is Live!`);
  console.log(`   • URL: http://localhost:${actualPort}`);
  console.log(`   • Press Ctrl+C to stop`);
  console.log("================================================================================");
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("workbench-server.ts") ||
  process.argv[1].endsWith("workbench-server.js")
);

if (isMain) {
  runCli();
}
