/**
 * Git-Backed Distributed Lease Lock Manager (INV-02 / Stage 2)
 * 
 * Manages distributed domain leases across collaborating team workstations in Mode 3 (Collaborative Team Mode):
 * 1. Tracks domain ownership in Git-versioned JSON manifests (.agents/locks/<domain>.lock.json).
 * 2. Enforces non-overlapping exclusive leases with automated TTL expiration.
 * 3. Prevents cross-workstation file write collisions.
 */

import { existsSync, readFileSync, writeFileSync, unlinkSync, readdirSync, mkdirSync } from "fs";
import { join } from "path";
import { execSync } from "child_process";
import { hostname } from "os";
import { fileURLToPath } from "url";

export interface DomainLease {
  domain: string;
  leaseId: string;
  ownerWorkstationId: string;
  ownerRole: "alpha" | "beta";
  acquiredAt: string;
  ttlSeconds: number;
  expiresAt: string;
  gitCommitSha: string;
}

export interface LockOperationResult {
  success: boolean;
  action: "acquire" | "release" | "status" | "heartbeat";
  domain: string;
  lease?: DomainLease;
  message: string;
  error?: string;
}

export class GitLockManager {
  private static readonly WORKSPACE_ROOT = process.cwd();
  private static readonly LOCKS_DIR = join(process.cwd(), ".agents", "locks");
  private static readonly DEFAULT_TTL_SECONDS = 3600; // 1 hour default

  public static getWorkstationId(): string {
    return process.env.WORKSTATION_ID || hostname() || "UNKNOWN_NODE";
  }

  public static getLockFilePath(domain: string): string {
    return join(this.LOCKS_DIR, `${domain.toLowerCase()}.lock.json`);
  }

  private static getCurrentGitSha(): string {
    try {
      return execSync("git rev-parse HEAD", { encoding: "utf-8", stdio: ["ignore", "pipe", "ignore"] }).trim();
    } catch {
      return "0000000000000000000000000000000000000000";
    }
  }

  /**
   * Synchronizes lock changes to Git remote origin if configured and reachable.
   */
  private static syncGitRemote(action: "acquire" | "release", domain: string, lockPath: string): { synced: boolean; message: string } {
    try {
      const remotes = execSync("git remote", { encoding: "utf-8", stdio: ["ignore", "pipe", "ignore"] }).trim();
      if (!remotes.includes("origin")) {
        return { synced: false, message: "Local lease stored (no 'origin' git remote configured)." };
      }

      // Stage the lock file
      if (action === "acquire") {
        execSync(`git add "${lockPath}"`, { stdio: ["ignore", "ignore", "ignore"] });
        execSync(`git commit -m "chore(lock): acquire ${domain} lease [skip ci]"`, { stdio: ["ignore", "ignore", "ignore"] });
      } else {
        execSync(`git add -u "${lockPath}"`, { stdio: ["ignore", "ignore", "ignore"] });
        execSync(`git commit -m "chore(lock): release ${domain} lease [skip ci]"`, { stdio: ["ignore", "ignore", "ignore"] });
      }

      // Push to remote with 5-second timeout
      execSync("git push origin HEAD --quiet", { stdio: ["ignore", "ignore", "ignore"], timeout: 5000 });
      return { synced: true, message: `Lease ${action} synchronized with remote origin.` };
    } catch {
      return { synced: false, message: `Local lease stored (git remote sync skipped or offline).` };
    }
  }

  /**
   * Reads existing lock for domain if present.
   */
  public static readLock(domain: string): DomainLease | null {
    const lockPath = this.getLockFilePath(domain);
    if (!existsSync(lockPath)) return null;

    try {
      const data = JSON.parse(readFileSync(lockPath, "utf-8"));
      return data as DomainLease;
    } catch {
      return null;
    }
  }

  /**
   * Checks if an existing lease has expired past its TTL.
   */
  public static isLeaseExpired(lease: DomainLease): boolean {
    const expireTime = new Date(lease.expiresAt).getTime();
    return Date.now() > expireTime;
  }

  /**
   * Acquires exclusive domain lease for this workstation.
   */
  public static acquireLock(
    domain: string,
    role: "alpha" | "beta" = "alpha",
    ttlSeconds: number = this.DEFAULT_TTL_SECONDS,
    customWorkstationId?: string
  ): LockOperationResult {
    if (!existsSync(this.LOCKS_DIR)) {
      mkdirSync(this.LOCKS_DIR, { recursive: true });
    }

    const currentWs = customWorkstationId || this.getWorkstationId();
    const existing = this.readLock(domain);

    if (existing) {
      const expired = this.isLeaseExpired(existing);
      if (!expired && existing.ownerWorkstationId !== currentWs) {
        return {
          success: false,
          action: "acquire",
          domain,
          lease: existing,
          message: `Lease conflict: Domain '${domain}' is actively locked by workstation '${existing.ownerWorkstationId}' (${existing.ownerRole}) until ${existing.expiresAt}.`,
          error: "LOCK_ACQUISITION_DENIED_ALREADY_HELD",
        };
      }
    }

    const now = new Date();
    const expires = new Date(now.getTime() + ttlSeconds * 1000);
    const gitSha = this.getCurrentGitSha();
    const leaseId = `lease-${domain}-${Date.now().toString(36)}`;

    const newLease: DomainLease = {
      domain,
      leaseId,
      ownerWorkstationId: currentWs,
      ownerRole: role,
      acquiredAt: now.toISOString(),
      ttlSeconds,
      expiresAt: expires.toISOString(),
      gitCommitSha: gitSha,
    };

    const lockPath = this.getLockFilePath(domain);
    writeFileSync(lockPath, JSON.stringify(newLease, null, 2), "utf-8");
    const remoteSync = this.syncGitRemote("acquire", domain, lockPath);

    return {
      success: true,
      action: "acquire",
      domain,
      lease: newLease,
      message: `Successfully acquired exclusive lease for domain '${domain}' by '${currentWs}' (${role}) for ${ttlSeconds}s. ${remoteSync.message}`,
    };
  }

  /**
   * Releases domain lease.
   */
  public static releaseLock(domain: string, customWorkstationId?: string, force: boolean = false): LockOperationResult {
    const lockPath = this.getLockFilePath(domain);
    if (!existsSync(lockPath)) {
      return {
        success: true,
        action: "release",
        domain,
        message: `No active lease found for domain '${domain}'. Nothing to release.`,
      };
    }

    const currentWs = customWorkstationId || this.getWorkstationId();
    const existing = this.readLock(domain);

    if (existing && existing.ownerWorkstationId !== currentWs && !force) {
      return {
        success: false,
        action: "release",
        domain,
        lease: existing,
        message: `Permission denied: Lock for '${domain}' belongs to '${existing.ownerWorkstationId}'. Use force=true to override.`,
        error: "RELEASE_DENIED_NOT_OWNER",
      };
    }

    try {
      unlinkSync(lockPath);
      const remoteSync = this.syncGitRemote("release", domain, lockPath);
      return {
        success: true,
        action: "release",
        domain,
        message: `Lease for domain '${domain}' successfully released. ${remoteSync.message}`,
      };
    } catch (err: any) {
      return {
        success: false,
        action: "release",
        domain,
        message: `Failed to remove lock file: ${err.message}`,
        error: "IO_ERROR",
      };
    }
  }

  /**
   * Checks status of a domain lease.
   */
  public static getStatus(domain: string): LockOperationResult {
    const existing = this.readLock(domain);
    if (!existing) {
      return {
        success: true,
        action: "status",
        domain,
        message: `Domain '${domain}' is UNLOCKED and available for lease acquisition.`,
      };
    }

    const expired = this.isLeaseExpired(existing);
    return {
      success: true,
      action: "status",
      domain,
      lease: existing,
      message: expired
        ? `Domain '${domain}' lease expired at ${existing.expiresAt}. Eligible for reclaiming.`
        : `Domain '${domain}' is LOCKED by '${existing.ownerWorkstationId}' (${existing.ownerRole}) until ${existing.expiresAt}.`,
    };
  }

  /**
   * Automatically stages and commits lock changes to Git if --sync is requested.
   */
  public static syncGit(message: string): boolean {
    try {
      execSync("git add .agents/locks/", { encoding: "utf-8", stdio: ["ignore", "pipe", "ignore"] });
      const status = execSync("git status --porcelain .agents/locks/", { encoding: "utf-8" }).trim();
      if (status) {
        execSync(`git commit -m "${message}"`, { encoding: "utf-8", stdio: ["ignore", "pipe", "ignore"] });
      }
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Lists all currently registered domain locks.
   */
  public static listAllLocks(): DomainLease[] {
    if (!existsSync(this.LOCKS_DIR)) return [];

    const files = readdirSync(this.LOCKS_DIR).filter((f) => f.endsWith(".lock.json"));
    const leases: DomainLease[] = [];

    for (const file of files) {
      try {
        const content = readFileSync(join(this.LOCKS_DIR, file), "utf-8");
        leases.push(JSON.parse(content));
      } catch {}
    }

    return leases;
  }
}

// CLI Entrypoint
const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("git-lock-manager.ts") ||
  process.argv[1].endsWith("git-lock-manager.js")
);

if (isMain) {
  const args = process.argv.slice(2);
  const action = args[0] || "list";
  const domainIdx = args.indexOf("--domain");
  const domain = domainIdx !== -1 ? args[domainIdx + 1] : "core";
  const roleIdx = args.indexOf("--role");
  const role = (roleIdx !== -1 ? args[roleIdx + 1] : "alpha") as "alpha" | "beta";
  const shouldSync = args.includes("--sync");

  if (action === "acquire") {
    const res = GitLockManager.acquireLock(domain, role);
    if (res.success && shouldSync) {
      GitLockManager.syncGit(`chore(lock): acquire domain lease for '${domain}' [${role}]`);
    }
    console.log(JSON.stringify(res, null, 2));
    process.exit(res.success ? 0 : 1);
  } else if (action === "release") {
    const res = GitLockManager.releaseLock(domain);
    if (res.success && shouldSync) {
      GitLockManager.syncGit(`chore(lock): release domain lease for '${domain}'`);
    }
    console.log(JSON.stringify(res, null, 2));
    process.exit(res.success ? 0 : 1);
  } else if (action === "status") {
    const res = GitLockManager.getStatus(domain);
    console.log(JSON.stringify(res, null, 2));
    process.exit(0);
  } else {
    const locks = GitLockManager.listAllLocks();
    console.log(JSON.stringify({ active_workstation: GitLockManager.getWorkstationId(), domain_leases: locks }, null, 2));
    process.exit(0);
  }
}
