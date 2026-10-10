import test from "node:test";
import type { TestContext } from "node:test";
import assert from "node:assert/strict";
import { existsSync, unlinkSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { acquireLock, releaseLock, listLocks, getOperatingMode } from "../scripts/lock-manager.ts";
import { setOperatingMode, getActiveProfile } from "../scripts/role-switch.ts";

test("N-Person Team Mesh Test Suite", async (t: TestContext) => {
  const LOCKS_DIR = join(process.cwd(), ".agents/state/locks");

  await t.test("Operating mode switching should support True Pipeline modes (surge, portfolio, team)", () => {
    // 1. Team mode (Mode 3: Collaborative Team Mode)
    setOperatingMode("team");
    assert.strictEqual(getOperatingMode(), "team");
    const teamProf = getActiveProfile();
    assert.strictEqual(teamProf.mode, "team");

    // 2. Portfolio mode (Mode 2: Multi-Project / Portfolio Multiplexing)
    setOperatingMode("portfolio");
    assert.strictEqual(getOperatingMode(), "portfolio");
    const portProf = getActiveProfile();
    assert.strictEqual(portProf.mode, "portfolio");

    // 3. Deep Surge mode (Mode 1: All 4 Accounts on 1 Project)
    setOperatingMode("surge");
    assert.strictEqual(getOperatingMode(), "surge");
    const surgeProf = getActiveProfile();
    assert.strictEqual(surgeProf.mode, "surge");

    // 4. Backward compatibility aliases (solo and legacy dual map to surge)
    setOperatingMode("solo");
    assert.strictEqual(getOperatingMode(), "surge");
    setOperatingMode("dual");
    assert.strictEqual(getOperatingMode(), "surge");
  });

  await t.test("Concurrent parallel domain leasing across N team members", () => {
    // Activate team mode
    setOperatingMode("team");

    // Developer 1 (Alice) leases 'auth'
    const ok1 = acquireLock("auth", "Alice", "DomainLead", 3600);
    assert.strictEqual(ok1, true, "Alice should acquire 'auth'");

    // Developer 2 (Bob) leases 'billing' concurrently
    const ok2 = acquireLock("billing", "Bob", "DomainLead", 3600);
    assert.strictEqual(ok2, true, "Bob should acquire 'billing' concurrently");

    // Developer 3 (Charlie) leases 'frontend' concurrently
    const ok3 = acquireLock("frontend", "Charlie", "DomainLead", 3600);
    assert.strictEqual(ok3, true, "Charlie should acquire 'frontend' concurrently");

    // Conflict test: Developer 4 (Dana) tries to steal 'auth' while actively leased to Alice
    const conflict = acquireLock("auth", "Dana", "DomainLead", 3600);
    assert.strictEqual(conflict, false, "Dana should be blocked by active lease held by Alice");

    // Cleanup leases
    releaseLock("auth", "Alice");
    releaseLock("billing", "Bob");
    releaseLock("frontend", "Charlie");

    // Revert to Deep Surge mode
    setOperatingMode("surge");
  });
});
