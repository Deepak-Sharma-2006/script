/**
 * Antigravity LAN Synchronization Server
 * Lightweight zero-dependency HTTP server for hackathons and local multi-device sync.
 * Runs on one team member's laptop, providing instant sub-10ms lock heartbeats and shared state.
 */

import { createServer, IncomingMessage, ServerResponse } from "node:http";
import { existsSync, mkdirSync, readFileSync, readdirSync, unlinkSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { networkInterfaces, hostname } from "node:os";

const PORT = parseInt(process.env.PORT || "4040", 10);
const LOCKS_DIR = join(process.cwd(), ".agents/state/locks");

function ensureLocksDir(): void {
  if (!existsSync(LOCKS_DIR)) {
    mkdirSync(LOCKS_DIR, { recursive: true });
  }
}

function getLocalIpAddresses(): string[] {
  const nets = networkInterfaces();
  const results: string[] = [];
  for (const name of Object.keys(nets)) {
    for (const net of nets[name] || []) {
      if (net.family === "IPv4" && !net.internal) {
        results.push(net.address);
      }
    }
  }
  return results.length > 0 ? results : ["127.0.0.1"];
}

function parseJsonBody(req: IncomingMessage): Promise<Record<string, any>> {
  return new Promise((resolve, reject) => {
    let body = "";
    req.on("data", (chunk: Buffer | string) => { body += chunk; });
    req.on("end", () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (e) {
        reject(e);
      }
    });
    req.on("error", reject);
  });
}

function sendJson(res: ServerResponse, statusCode: number, data: unknown): void {
  const json = JSON.stringify(data, null, 2);
  res.writeHead(statusCode, {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  });
  res.end(json);
}

export function startLanServer(port = PORT): void {
  ensureLocksDir();

  const server = createServer(async (req: IncomingMessage, res: ServerResponse) => {
    const url = new URL(req.url || "/", `http://${req.headers.host || "localhost"}`);
    const method = req.method || "GET";

    if (method === "OPTIONS") {
      res.writeHead(204, {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
      });
      res.end();
      return;
    }

    try {
      if (url.pathname === "/health" || url.pathname === "/") {
        sendJson(res, 200, {
          status: "HEALTHY",
          serverHost: hostname(),
          uptimeSeconds: Math.floor(process.uptime()),
          activeLocksCount: existsSync(LOCKS_DIR) ? readdirSync(LOCKS_DIR).filter((f: string) => f.endsWith(".lock.json")).length : 0,
        });
      } else if (url.pathname === "/status" && method === "GET") {
        const portfolioPath = existsSync(join(process.cwd(), "pipeline/specs/hackathon_portfolio.json"))
          ? join(process.cwd(), "pipeline/specs/hackathon_portfolio.json")
          : join(process.cwd(), "specs/hackathon_portfolio.json");
        let portfolioData: any = null;
        if (existsSync(portfolioPath)) {
          try {
            portfolioData = JSON.parse(readFileSync(portfolioPath, "utf-8"));
          } catch {}
        }
        sendJson(res, 200, {
          status: "TRUE_PIPELINE_OPERATIONAL",
          host: hostname(),
          uptimeSeconds: Math.floor(process.uptime()),
          operatingModes: {
            mode1_surge: "4 Isolated Git Worktrees Configured in D:/BE_Research_lanes",
            mode2_portfolio: "8 Concurrent Hackathons Active (17-25 Days Runway)",
            mode3_team: "Active LAN Sync Server on Port " + PORT
          },
          portfolio: portfolioData
        });
      } else if (url.pathname === "/locks" && method === "GET") {
        ensureLocksDir();
        const files = readdirSync(LOCKS_DIR).filter((f: string) => f.endsWith(".lock.json"));
        const leases = [];
        for (const file of files) {
          try {
            leases.push(JSON.parse(readFileSync(join(LOCKS_DIR, file), "utf-8")));
          } catch {}
        }
        sendJson(res, 200, { leases });
      } else if (url.pathname === "/locks/acquire" && method === "POST") {
        const body = await parseJsonBody(req);
        const { domain, operator, role, ttlSeconds, host } = body;
        if (!domain || !operator) {
          sendJson(res, 400, { error: "Missing required fields: domain, operator" });
          return;
        }

        const lockFile = join(LOCKS_DIR, `${domain}.lock.json`);
        const now = new Date();
        const ttl = ttlSeconds || 7200;
        const expiresAt = new Date(now.getTime() + ttl * 1000).toISOString();

        if (existsSync(lockFile)) {
          try {
            const existing = JSON.parse(readFileSync(lockFile, "utf-8"));
            const currentExpiry = new Date(existing.expiresAt);
            if (now < currentExpiry && existing.operator !== operator) {
              sendJson(res, 409, {
                error: "LOCK_CONFLICT",
                message: `Domain '${domain}' is actively leased to '${existing.operator}' until ${existing.expiresAt}`,
                existing,
              });
              return;
            }
          } catch {}
        }

        const lease = {
          domain,
          operator,
          role: role || "DomainLead",
          acquiredAt: now.toISOString(),
          expiresAt,
          ttlSeconds: ttl,
          lastHeartbeat: now.toISOString(),
          host: host || "remote-client",
        };

        writeFileSync(lockFile, JSON.stringify(lease, null, 2), "utf-8");
        console.log(`🌐 [LAN SYNC] Lease acquired: ${domain} -> ${operator} (${lease.role})`);
        sendJson(res, 200, { success: true, lease });
      } else if (url.pathname === "/locks/heartbeat" && method === "POST") {
        const body = await parseJsonBody(req);
        const { domain, operator, extensionSeconds } = body;
        const lockFile = join(LOCKS_DIR, `${domain}.lock.json`);

        if (!existsSync(lockFile)) {
          sendJson(res, 404, { error: "NOT_FOUND", message: `Domain '${domain}' has no active lease.` });
          return;
        }

        const lease = JSON.parse(readFileSync(lockFile, "utf-8"));
        const now = new Date();
        const ttl = extensionSeconds || 3600;
        lease.lastHeartbeat = now.toISOString();
        lease.expiresAt = new Date(now.getTime() + ttl * 1000).toISOString();
        lease.ttlSeconds = ttl;

        writeFileSync(lockFile, JSON.stringify(lease, null, 2), "utf-8");
        sendJson(res, 200, { success: true, lease });
      } else if (url.pathname === "/locks/release" && method === "POST") {
        const body = await parseJsonBody(req);
        const { domain, operator } = body;
        const lockFile = join(LOCKS_DIR, `${domain}.lock.json`);

        if (existsSync(lockFile)) {
          unlinkSync(lockFile);
          console.log(`🌐 [LAN SYNC] Lease released: ${domain} by ${operator}`);
        }
        sendJson(res, 200, { success: true, releasedDomain: domain });
      } else {
        sendJson(res, 404, { error: "NOT_FOUND", message: `Route ${url.pathname} not recognized` });
      }
    } catch (err: any) {
      console.error("[LAN SYNC SERVER ERROR]", err);
      sendJson(res, 500, { error: "INTERNAL_ERROR", message: err.message });
    }
  });

  server.listen(port, "0.0.0.0", () => {
    const ips = getLocalIpAddresses();
    console.log(`\n================================================================================`);
    console.log(`🌐 [ANTIGRAVITY LAN SYNC SERVER] Listening on port ${port}`);
    console.log(`================================================================================`);
    console.log(`Teammates can sync real-time domain locks across laptops using:`);
    for (const ip of ips) {
      console.log(`  👉 Windows PowerShell: $env:LOCK_WEBHOOK_URL="http://${ip}:${port}"`);
      console.log(`  👉 Mac / Linux Bash  : export LOCK_WEBHOOK_URL="http://${ip}:${port}"`);
    }
    console.log(`================================================================================\n`);
  });
}

// Auto-start if run directly
import { fileURLToPath } from "node:url";
const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("lan-sync-server.ts") ||
  process.argv[1].endsWith("lan-sync-server.js")
);

if (isMain) {
  startLanServer();
}
