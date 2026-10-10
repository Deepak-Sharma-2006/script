import { existsSync, mkdirSync, readFileSync, readdirSync, unlinkSync, writeFileSync } from "fs";
import { join } from "path";
import { hostname } from "os";
import { execSync } from "child_process";
import { fileURLToPath } from "node:url";

export interface DomainLease {
  domain: string;
  operator: string;
  role: string; // "Alpha" | "Beta" | "DomainLead" | "SDETLead" | custom
  acquiredAt: string;
  expiresAt: string;
  ttlSeconds: number;
  lastHeartbeat: string;
  host: string;
}

export interface LockDriver {
  name: "local" | "cloud";
  acquire(lease: DomainLease): boolean;
  heartbeat(domain: string, operator: string, extensionSeconds: number): boolean;
  release(domain: string, operator: string): boolean;
  list(): DomainLease[];
}

const LOCKS_DIR = join(process.cwd(), ".agents/state/locks");
const GRACE_PERIOD_SECONDS = 900; // 15-minute grace period

function ensureLocksDir(): void {
  if (!existsSync(LOCKS_DIR)) {
    mkdirSync(LOCKS_DIR, { recursive: true });
  }
}

const ROLE_FILE = join(process.cwd(), ".agents/state/active-role.json");

export type OperatingMode = "surge" | "portfolio" | "team" | "solo" | "dual";

export function getOperatingMode(): OperatingMode {
  const envMode = (process.env.OPERATOR_MODE || "").toLowerCase();
  if (envMode === "portfolio") return "portfolio";
  if (envMode === "team" || envMode === "mesh") return "team";
  if (envMode === "surge" || envMode === "solo") return "surge";

  if (existsSync(ROLE_FILE)) {
    try {
      const data = JSON.parse(readFileSync(ROLE_FILE, "utf-8"));
      const m = (data.mode || "").toLowerCase();
      if (m === "portfolio") return "portfolio";
      if (m === "team" || m === "mesh") return "team";
      if (m === "surge" || m === "solo" || m === "dual") return "surge";
    } catch {
      return "surge";
    }
  }
  return "surge";
}

export function isSurgeMode(): boolean {
  const mode = getOperatingMode();
  return mode === "surge" || mode === "solo";
}

export function isPortfolioMode(): boolean {
  return getOperatingMode() === "portfolio";
}

export function isSoloMode(): boolean {
  return isSurgeMode();
}

export function isTeamMode(): boolean {
  return getOperatingMode() === "team";
}

export function resolveOperator(explicitOperator?: string): string {
  if (isSoloMode()) {
    return explicitOperator?.trim() || "SoloOperator";
  }
  if (explicitOperator && explicitOperator.trim()) {
    return explicitOperator.trim();
  }
  if (process.env.OPERATOR_NAME && process.env.OPERATOR_NAME.trim()) {
    return process.env.OPERATOR_NAME.trim();
  }
  try {
    const gitUser = execSync("git config user.name", { encoding: "utf-8" }).trim();
    if (gitUser) return gitUser;
  } catch {}
  const host = hostname();
  return host || "Developer";
}

/**
 * LocalGitDriver: Offline / Hackathon driver storing lock leases
 * in .agents/state/locks/<domain>.lock.json.
 */
export class LocalGitDriver implements LockDriver {
  name: "local" = "local";

  acquire(lease: DomainLease): boolean {
    ensureLocksDir();
    const lockFile = join(LOCKS_DIR, `${lease.domain}.lock.json`);

    if (existsSync(lockFile)) {
      try {
        const existing: DomainLease = JSON.parse(readFileSync(lockFile, "utf-8"));
        const now = new Date();
        const expiresAt = new Date(existing.expiresAt);
        const graceEnd = new Date(expiresAt.getTime() + GRACE_PERIOD_SECONDS * 1000);

        // In solo mode, the designated solo operator seamlessly supersedes previous domain locks
        if (isSoloMode() && (lease.operator === "SoloOperator" || existing.operator === lease.operator)) {
          // Seamless acquisition allowed for the designated solo operator
        } else if (now < expiresAt && existing.operator !== lease.operator) {
          console.error(`\n🚨 LOCK CONFLICT: Domain '${lease.domain}' is actively leased to '${existing.operator}' (${existing.role}) on host '${existing.host}'.`);
          console.error(`Expires at: ${existing.expiresAt}. Run 'npm run role:handoff' or wait for release.\n`);
          return false;
        } else if (now >= expiresAt && now < graceEnd && existing.operator !== lease.operator) {
          console.warn(`\n⚠️ LEASE GRACE PERIOD: Domain '${lease.domain}' expired at ${existing.expiresAt} but is in a 15-minute grace window for '${existing.operator}'.`);
          console.warn(`Attempting graceful transfer to '${lease.operator}'.\n`);
        }
      } catch {
        // Malformed lock file, proceed with overwrite
      }
    }

    writeFileSync(lockFile, JSON.stringify(lease, null, 2), "utf-8");
    console.log(`✅ [Local Lock Acquired] Domain '${lease.domain}' leased to '${lease.operator}' (${lease.role}) on '${lease.host}' until ${lease.expiresAt}`);
    return true;
  }

  heartbeat(domain: string, operator: string, extensionSeconds = 3600): boolean {
    ensureLocksDir();
    const lockFile = join(LOCKS_DIR, `${domain}.lock.json`);

    if (!existsSync(lockFile)) {
      console.warn(`⚠️ Cannot heartbeat: Domain '${domain}' has no active lock. Acquiring fresh lock.`);
      const now = new Date();
      const lease: DomainLease = {
        domain,
        operator,
        role: "Alpha",
        acquiredAt: now.toISOString(),
        expiresAt: new Date(now.getTime() + extensionSeconds * 1000).toISOString(),
        ttlSeconds: extensionSeconds,
        lastHeartbeat: now.toISOString(),
        host: hostname(),
      };
      return this.acquire(lease);
    }

    try {
      const lease: DomainLease = JSON.parse(readFileSync(lockFile, "utf-8"));
      const now = new Date();
      const newExpiresAt = new Date(now.getTime() + extensionSeconds * 1000).toISOString();

      lease.lastHeartbeat = now.toISOString();
      lease.expiresAt = newExpiresAt;
      lease.ttlSeconds = extensionSeconds;
      lease.host = lease.host || hostname();

      writeFileSync(lockFile, JSON.stringify(lease, null, 2), "utf-8");
      console.log(`💓 [Local Lock Heartbeat] Domain '${domain}' lease extended to ${newExpiresAt} for '${lease.operator}' on '${lease.host}'`);
      return true;
    } catch (err) {
      console.error(`❌ Failed to send heartbeat for '${domain}':`, err);
      return false;
    }
  }

  release(domain: string, operator: string): boolean {
    ensureLocksDir();
    const lockFile = join(LOCKS_DIR, `${domain}.lock.json`);

    if (!existsSync(lockFile)) {
      console.log(`ℹ️ No active lock found for domain '${domain}'.`);
      return true;
    }

    try {
      const existing: DomainLease = JSON.parse(readFileSync(lockFile, "utf-8"));
      if (existing.operator !== operator) {
        console.warn(`⚠️ Warning: Lock for '${domain}' was held by '${existing.operator}', released by '${operator}'.`);
      }
      unlinkSync(lockFile);
      console.log(`🔓 [Local Lock Released] Domain '${domain}' is now unlocked.`);
      return true;
    } catch (err) {
      console.error(`❌ Failed to release lock for '${domain}':`, err);
      return false;
    }
  }

  list(): DomainLease[] {
    ensureLocksDir();
    const files = readdirSync(LOCKS_DIR).filter((f: string) => f.endsWith(".lock.json"));
    const leases: DomainLease[] = [];
    const now = new Date();

    for (const f of files) {
      try {
        const lease: DomainLease = JSON.parse(readFileSync(join(LOCKS_DIR, f), "utf-8"));
        const expires = new Date(lease.expiresAt);
        const isExpired = now >= expires;
        const remainingMinutes = Math.max(0, Math.floor((expires.getTime() - now.getTime()) / 60000));

        const host = lease.host || "unknown";
        const op = lease.operator || "unknown";
        const role = lease.role || "Alpha";
        const domain = lease.domain || f.replace(/\.lock\.json$/, "");
        const statusTag = isExpired ? "🔴 EXPIRED" : `🟢 ACTIVE (${remainingMinutes}m left)`;

        console.log(`  • [${domain.padEnd(16)}] Operator: ${op.padEnd(14)} Role: ${role.padEnd(6)} Host: ${host.padEnd(14)} | ${statusTag}`);
        leases.push(lease);
      } catch (err) {
        console.warn(`⚠️ Warning: could not parse lock file ${f}:`, err);
      }
    }

    if (leases.length === 0) {
      console.log("  (Zero active locks. Workspace is fully unlocked.)");
    }

    return leases;
  }
}

/**
 * CloudHttpDriver: Remote REST / Webhook coordinator (Supabase, GitHub Actions, or Custom HTTP).
 * Eliminates Git merge conflicts on locks across multi-developer setups.
 * Gracefully falls back to LocalGitDriver if network or webhook is unavailable.
 */
export class CloudHttpDriver implements LockDriver {
  name: "cloud" = "cloud";
  private localFallback = new LocalGitDriver();
  private webhookUrl: string;
  private authToken: string;

  constructor(webhookUrl?: string, authToken?: string) {
    this.webhookUrl = webhookUrl || process.env.LOCK_WEBHOOK_URL || process.env.SUPABASE_LOCK_URL || "";
    this.authToken = authToken || process.env.LOCK_AUTH_TOKEN || process.env.SUPABASE_LOCK_KEY || "";
  }

  private hasEndpoint(): boolean {
    return Boolean(this.webhookUrl && this.webhookUrl.startsWith("http"));
  }

  acquire(lease: DomainLease): boolean {
    if (!this.hasEndpoint()) {
      console.warn("⚠️ [CloudHttpDriver] LOCK_WEBHOOK_URL is not configured. Falling back to LocalGitDriver.");
      return this.localFallback.acquire(lease);
    }

    try {
      const payload = JSON.stringify({ action: "acquire", lease });
      const authHeader = this.authToken ? `-H "Authorization: Bearer ${this.authToken}"` : "";
      const cmd = `curl.exe -s -m 5 -X POST "${this.webhookUrl}/acquire" -H "Content-Type: application/json" ${authHeader} -d '${payload.replace(/'/g, "\\'")}'`;
      const res = execSync(cmd, { encoding: "utf-8", stdio: ["pipe", "pipe", "pipe"] });
      console.log(`🌐 [Cloud Lock Acquired] Domain '${lease.domain}' registered with cloud coordinator.`);
      this.localFallback.acquire(lease); // Sync local mirror
      return true;
    } catch (err: any) {
      console.warn(`⚠️ [CloudHttpDriver] Cloud lock coordinator unreachable (${err.message}). Falling back to LocalGitDriver.`);
      return this.localFallback.acquire(lease);
    }
  }

  heartbeat(domain: string, operator: string, extensionSeconds = 3600): boolean {
    if (!this.hasEndpoint()) {
      return this.localFallback.heartbeat(domain, operator, extensionSeconds);
    }

    try {
      const payload = JSON.stringify({ action: "heartbeat", domain, operator, extensionSeconds });
      const authHeader = this.authToken ? `-H "Authorization: Bearer ${this.authToken}"` : "";
      const cmd = `curl.exe -s -m 5 -X POST "${this.webhookUrl}/heartbeat" -H "Content-Type: application/json" ${authHeader} -d '${payload.replace(/'/g, "\\'")}'`;
      execSync(cmd, { encoding: "utf-8", stdio: ["pipe", "pipe", "pipe"] });
      console.log(`💓 [Cloud Lock Heartbeat] Domain '${domain}' heartbeat registered with cloud coordinator.`);
      return this.localFallback.heartbeat(domain, operator, extensionSeconds);
    } catch (err: any) {
      console.warn(`⚠️ [CloudHttpDriver] Cloud heartbeat failed (${err.message}). Updating local mirror.`);
      return this.localFallback.heartbeat(domain, operator, extensionSeconds);
    }
  }

  release(domain: string, operator: string): boolean {
    if (!this.hasEndpoint()) {
      return this.localFallback.release(domain, operator);
    }

    try {
      const payload = JSON.stringify({ action: "release", domain, operator });
      const authHeader = this.authToken ? `-H "Authorization: Bearer ${this.authToken}"` : "";
      const cmd = `curl.exe -s -m 5 -X POST "${this.webhookUrl}/release" -H "Content-Type: application/json" ${authHeader} -d '${payload.replace(/'/g, "\\'")}'`;
      execSync(cmd, { encoding: "utf-8", stdio: ["pipe", "pipe", "pipe"] });
      console.log(`🌐 [Cloud Lock Released] Domain '${domain}' released on cloud coordinator.`);
      return this.localFallback.release(domain, operator);
    } catch (err: any) {
      console.warn(`⚠️ [CloudHttpDriver] Cloud release failed (${err.message}). Releasing local mirror.`);
      return this.localFallback.release(domain, operator);
    }
  }

  list(): DomainLease[] {
    if (!this.hasEndpoint()) {
      return this.localFallback.list();
    }

    try {
      const authHeader = this.authToken ? `-H "Authorization: Bearer ${this.authToken}"` : "";
      const cmd = `curl.exe -s -m 5 -X GET "${this.webhookUrl}/list" -H "Content-Type: application/json" ${authHeader}`;
      const res = execSync(cmd, { encoding: "utf-8", stdio: ["pipe", "pipe", "pipe"] });
      const leases: DomainLease[] = JSON.parse(res);
      console.log("🌐 [Cloud Coordinator Leases]:");
      for (const l of leases) {
        console.log(`  • [${l.domain.padEnd(16)}] Operator: ${l.operator.padEnd(14)} Role: ${l.role.padEnd(6)} Host: ${l.host.padEnd(14)} | ${l.expiresAt}`);
      }
      return leases;
    } catch (err: any) {
      console.warn(`⚠️ [CloudHttpDriver] Could not fetch cloud locks (${err.message}). Showing local mirror.`);
      return this.localFallback.list();
    }
  }
}

// Global Driver Factory
export function getLockDriver(driverName?: string): LockDriver {
  const mode = driverName || process.env.LOCK_DRIVER || (process.env.LOCK_WEBHOOK_URL ? "cloud" : "local");
  if (mode === "cloud") {
    return new CloudHttpDriver();
  }
  return new LocalGitDriver();
}

// Top-level API (Backwards-compatible)
export function acquireLock(domain: string, explicitOperator?: string, role: string = "Alpha", ttlSeconds = 7200, driverName?: string): boolean {
  const driver = getLockDriver(driverName);
  const operator = resolveOperator(explicitOperator);
  const host = hostname();
  const now = new Date();
  const expiresAt = new Date(now.getTime() + ttlSeconds * 1000).toISOString();

  const lease: DomainLease = {
    domain,
    operator,
    role,
    acquiredAt: now.toISOString(),
    expiresAt,
    ttlSeconds,
    lastHeartbeat: now.toISOString(),
    host,
  };

  return driver.acquire(lease);
}

export function heartbeatLock(domain: string, explicitOperator?: string, extensionSeconds = 3600, driverName?: string): boolean {
  const driver = getLockDriver(driverName);
  const operator = resolveOperator(explicitOperator);
  return driver.heartbeat(domain, operator, extensionSeconds);
}

export function releaseLock(domain: string, explicitOperator?: string, driverName?: string): boolean {
  const driver = getLockDriver(driverName);
  const operator = resolveOperator(explicitOperator);
  return driver.release(domain, operator);
}

export function transferLock(domain: string, fromOperator: string, toOperator: string, newRole: string = "Alpha", driverName?: string): boolean {
  console.log(`🔄 [Phase Handoff] Transferring domain '${domain}' from '${fromOperator}' to '${toOperator}' (${newRole})...`);
  releaseLock(domain, fromOperator, driverName);
  return acquireLock(domain, toOperator, newRole, 7200, driverName);
}

export function listLocks(driverName?: string): DomainLease[] {
  const driver = getLockDriver(driverName);
  return driver.list();
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
  process.argv[1].endsWith("lock-manager.ts") ||
  process.argv[1].endsWith("lock-manager.js")
);

if (isMain) {
  const rawArgs = process.argv.slice(2);
  const command = (rawArgs[0] && !rawArgs[0].startsWith("--") ? rawArgs[0] : "status").toLowerCase();
  const flags = parseCliFlags(rawArgs);
  const positional = rawArgs.filter((a: string) => !a.startsWith("--") && a !== command);
  const driverFlag = flags["driver"] || (flags["cloud"] ? "cloud" : undefined);

  if (command === "status") {
    console.log(`\n🔒 [Distributed Domain Lease Status - Driver: ${driverFlag || process.env.LOCK_DRIVER || "local"}]`);
    console.log("================================================================================");
    listLocks(driverFlag);
    console.log("================================================================================\n");
  } else if (command === "acquire") {
    const domain = flags["domain"] || positional[0] || "core";
    const op = flags["operator"] || flags["op"] || positional[1];
    const defaultRole = isTeamMode() ? "DomainLead" : "Alpha";
    const role = flags["role"] || positional[2] || defaultRole;
    acquireLock(domain, op, role, 7200, driverFlag);
  } else if (command === "heartbeat") {
    const domain = flags["domain"] || positional[0] || "core";
    const op = flags["operator"] || flags["op"] || positional[1];
    heartbeatLock(domain, op, 3600, driverFlag);
  } else if (command === "release") {
    const domain = flags["domain"] || positional[0] || "core";
    const op = flags["operator"] || flags["op"] || positional[1];
    releaseLock(domain, op, driverFlag);
  } else if (command === "transfer") {
    const domain = flags["domain"] || positional[0] || "core";
    const fromOp = flags["from"] || positional[1] || "Computer1";
    const toOp = flags["to"] || positional[2] || "Computer2";
    const role = flags["role"] || positional[3] || (isTeamMode() ? "DomainLead" : "Beta");
    transferLock(domain, fromOp, toOp, role, driverFlag);
  } else {
    console.log(`
Usage: node --experimental-strip-types scripts/lock-manager.ts <command> [options]

Commands:
  status                               Display active locks, hosts, and remaining TTL
  acquire <domain> [op] [role]         Acquire new domain lease
  heartbeat <domain> [op]              Auto-renew active lease TTL
  transfer <domain> <from> <to> [role] Atomically handoff lease to partner
  release <domain> [op]                Release active domain lease

Options:
  --driver [local|cloud]               Select storage driver (default: local)
  --cloud                              Shortcut for --driver cloud
`);
  }
}
