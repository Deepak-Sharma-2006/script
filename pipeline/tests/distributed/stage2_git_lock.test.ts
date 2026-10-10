import { test, describe, afterEach } from "node:test";
import assert from "node:assert/strict";
import { existsSync, unlinkSync } from "node:fs";
import { join } from "node:path";
import { GitLockManager } from "../../scripts/distributed/git-lock-manager.ts";
import { RoleHandoffEngine } from "../../scripts/distributed/role-handoff.ts";

describe("Stage 2: Mode 3 Git-Backed Collaborative Team Mesh (Workstation Alpha & Beta)", () => {
  const testDomain = "distributed_test_domain";

  afterEach(() => {
    // Clean up test lock
    GitLockManager.releaseLock(testDomain, "WORKSTATION_ALPHA", true);
    GitLockManager.releaseLock(testDomain, "WORKSTATION_BETA", true);
  });

  test("Gate 1: Workstation Alpha acquires exclusive domain lease", () => {
    const res = GitLockManager.acquireLock(testDomain, "alpha", 3600, "WORKSTATION_ALPHA");
    assert.equal(res.success, true, "Acquisition should succeed");
    assert.ok(res.lease, "Lease object must be returned");
    assert.equal(res.lease!.ownerWorkstationId, "WORKSTATION_ALPHA");
    assert.equal(res.lease!.ownerRole, "alpha");

    const lockFile = GitLockManager.getLockFilePath(testDomain);
    assert.ok(existsSync(lockFile), "Lock file must exist on disk");
  });

  test("Gate 2: Workstation Beta is blocked from acquiring active lease held by Alpha", () => {
    // Step 1: Workstation Alpha acquires
    GitLockManager.acquireLock(testDomain, "alpha", 3600, "WORKSTATION_ALPHA");

    // Step 2: Workstation Beta attempts acquisition on same domain
    const res = GitLockManager.acquireLock(testDomain, "beta", 3600, "WORKSTATION_BETA");
    assert.equal(res.success, false, "Workstation Beta acquisition must be denied");
    assert.equal(res.error, "LOCK_ACQUISITION_DENIED_ALREADY_HELD");
    assert.match(res.message, /Lease conflict/);
  });

  test("Gate 3: Status query accurately reflects lease owner and expiration", () => {
    GitLockManager.acquireLock(testDomain, "alpha", 1800, "WORKSTATION_ALPHA");
    const status = GitLockManager.getStatus(testDomain);

    assert.equal(status.success, true);
    assert.ok(status.lease);
    assert.equal(status.lease!.ownerWorkstationId, "WORKSTATION_ALPHA");
    assert.match(status.message, /LOCKED by 'WORKSTATION_ALPHA'/);
  });

  test("Gate 4: Lease release successfully clears domain lock", () => {
    GitLockManager.acquireLock(testDomain, "alpha", 3600, "WORKSTATION_ALPHA");
    const rel = GitLockManager.releaseLock(testDomain, "WORKSTATION_ALPHA");

    assert.equal(rel.success, true);
    const status = GitLockManager.getStatus(testDomain);
    assert.match(status.message, /UNLOCKED/);
  });

  test("Gate 5: Phase handoff creates structured manifest and inverts lead role", () => {
    RoleHandoffEngine.setActiveRole("alpha");
    const manifest = RoleHandoffEngine.executeHandoff(
      2,
      testDomain,
      "Phase 2 Core Complete, handing off for Adversarial hardening."
    );

    assert.equal(manifest.phaseNumber, 2);
    assert.equal(manifest.fromRole, "alpha");
    assert.equal(manifest.toRole, "beta");
    assert.match(manifest.sha256, /^[a-f0-9]{64}$/);

    const manifestPath = join(process.cwd(), ".agents", "handoffs", `phase-2-${testDomain}-handoff.json`);
    assert.ok(existsSync(manifestPath), "Handoff manifest JSON must exist");

    // Verify active role is now inverted
    assert.equal(RoleHandoffEngine.getActiveRole(), "beta");

    // Clean up handoff manifest
    try { unlinkSync(manifestPath); } catch {}
  });

  test("Gate 6: Reading latest handoff brief retrieves most recent transfer", () => {
    RoleHandoffEngine.setActiveRole("beta");
    RoleHandoffEngine.executeHandoff(3, testDomain, "Phase 3 Hardening Brief");

    const latest = RoleHandoffEngine.getLatestHandoff();
    assert.ok(latest, "Must retrieve latest handoff");
    assert.equal(latest!.phaseNumber, 3);
    assert.equal(latest!.domain, testDomain);

    // Clean up
    const manifestPath = join(process.cwd(), ".agents", "handoffs", `phase-3-${testDomain}-handoff.json`);
    try { unlinkSync(manifestPath); } catch {}
  });
});
