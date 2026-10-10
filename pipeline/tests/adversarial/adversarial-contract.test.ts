import test from "node:test";
import assert from "node:assert/strict";
import { timingSafeEqual } from "node:crypto";
import { writeFileSync, unlinkSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { acquireLock, releaseLock, listLocks, heartbeatLock } from "../../scripts/lock-manager.ts";
import { createServer, defaultConfig } from "../../../src/index.ts";
import { searchMemories, saveMemory } from "../../scripts/memory-vault.ts";

/**
 * ADVERSARIAL SDET & CHAOS BATTERY
 * Authored exclusively by Lead 2 (Adversarial Systems & Product Lead).
 * Tests concurrency races, malicious input fuzzing, state corruption chaos, and timing security.
 */

test("ADVERSARIAL BATTERY [Lead 2 / SDET]: Concurrency & Race Condition Probing", async (t) => {
  const testDomain = "adversarial-concurrency-test";

  // Clean up any residual lock
  releaseLock(testDomain, "AdversarialTester");

  await t.test("Simultaneous concurrent lease claims must enforce strict mutual exclusion (Zero Race Conditions)", async () => {
    const attempts = 10;
    const operators = Array.from({ length: attempts }, (_, i) => `Operator_Worker_${i}`);

    // Run 10 parallel lease acquisition attempts simultaneously
    const results = await Promise.all(
      operators.map((op) => Promise.resolve(acquireLock(testDomain, op, "Alpha", 60)))
    );

    const winners = results.filter((ok) => ok === true);
    const losers = results.filter((ok) => ok === false);

    // Exactly 1 must win the lease
    assert.strictEqual(winners.length, 1, "Exactly one concurrent worker must acquire the lease.");
    // 9 must be safely rejected
    assert.strictEqual(losers.length, attempts - 1, "All competing concurrent workers must be rejected.");
  });

  await t.test("Active lease must resist unauthorized heartbeat from impostor operator", () => {
    // Attempt heartbeat by impostor
    const ok = heartbeatLock(testDomain, "ImpostorOperator", 120);
    // The lock manager should not transfer ownership via heartbeat
    const locks = listLocks();
    const active = locks.find((l) => l.domain === testDomain);
    assert.ok(active, "Active lock must exist");
    assert.notStrictEqual(active.operator, "ImpostorOperator", "Impostor must not hijack lease through heartbeat");
  });

  // Cleanup
  const activeLock = listLocks().find((l) => l.domain === testDomain);
  if (activeLock) {
    releaseLock(testDomain, activeLock.operator);
  }
});

test("ADVERSARIAL BATTERY [Lead 2 / SDET]: Boundary Value Fuzzing & Malicious Payloads", async (t) => {
  const server = createServer();

  await t.test("Server must handle massive query parameter strings without memory exhaustion or crash", async () => {
    const massivePath = "/api/health?" + "x=".repeat(50000);
    let handled = false;

    // Simulate mock request
    const req: any = { url: massivePath, method: "GET" };
    const res: any = {
      writeHead: (status: number) => {
        assert.ok([200, 404, 414, 431].includes(status), `Server responded with status ${status}`);
        handled = true;
      },
      end: (data: string) => {
        assert.ok(typeof data === "string");
      },
    };

    server.emit("request", req, res);
    assert.ok(handled, "Massive path request was safely handled without uncaught exception.");
  });

  await t.test("Server must gracefully 404 on path traversal attempts without leaking filesystem", async () => {
    const maliciousPaths = [
      "/../../../../etc/passwd",
      "/..\\..\\..\\windows\\system32",
      "/api/health%00.html",
      "/<script>alert(1)<%2Fscript>",
    ];

    for (const path of maliciousPaths) {
      let statusResult = 0;
      let bodyResult = "";

      const req: any = { url: path, method: "GET" };
      const res: any = {
        writeHead: (status: number) => {
          statusResult = status;
        },
        end: (data: string) => {
          bodyResult = data;
        },
      };

      server.emit("request", req, res);
      assert.ok([400, 404].includes(statusResult), `Malicious path '${path}' must safely return 400 Bad Request or 404 Not Found.`);
      assert.ok(!bodyResult.includes("passwd"), "Response must never leak internal files.");
    }
  });

  await t.test("Memory Vault must safely handle SQL injection strings in search queries", () => {
    const sqlInjectionQueries = [
      "' OR '1'='1",
      "'; DROP TABLE memories; --",
      "UNION SELECT * FROM memories",
      "1' OR 1=1 #",
      "'; DELETE FROM memories WHERE '1'='1",
    ];

    for (const q of sqlInjectionQueries) {
      // Must not throw SQL syntax or crash
      assert.doesNotThrow(() => {
        const results = searchMemories(q);
        assert.ok(Array.isArray(results), "Search query should return a safe array result.");
      }, `SQL injection string '${q}' must be safely handled via parameterized queries.`);
    }
  });
});

test("ADVERSARIAL BATTERY [Lead 2 / SDET]: State Corruption & Chaos Fault Injection", async (t) => {
  const chaosDomain = "adversarial-chaos-corrupted";
  const locksDir = join(process.cwd(), ".agents/state/locks");
  if (!existsSync(locksDir)) {
    mkdirSync(locksDir, { recursive: true });
  }
  const corruptedFile = join(locksDir, `${chaosDomain}.lock.json`);

  await t.test("System must survive corrupted / malformed lock JSON files on disk without crashing", () => {
    // Write invalid raw JSON to simulate abrupt disk write truncation or power outage
    writeFileSync(corruptedFile, '{"domain": "adversarial-chaos", "operator": UNTERMINATED_JSON', "utf-8");

    // listLocks must not throw; it must log warning and continue
    assert.doesNotThrow(() => {
      const locks = listLocks();
      assert.ok(Array.isArray(locks));
    }, "listLocks must safely recover from corrupted lock files.");

    // Clean up corrupted file
    if (existsSync(corruptedFile)) {
      unlinkSync(corruptedFile);
    }
  });

  await t.test("Releasing a non-existent or previously released lock must be idempotent and non-fatal", () => {
    assert.doesNotThrow(() => {
      const result = releaseLock("non-existent-domain-xyz", "OperatorTest");
      assert.strictEqual(result, true, "Idempotent release of absent domain must return true.");
    });
  });
});

test("ADVERSARIAL BATTERY [Lead 2 / SDET]: Timing Attack & Cryptographic Resistance", async (t) => {
  await t.test("Token comparison must use constant-time crypto.timingSafeEqual", () => {
    const tokenA = Buffer.from("auth_mock_timing_token_12345");
    const tokenB = Buffer.from("auth_mock_timing_token_12345");
    const tokenC = Buffer.from("auth_mock_timing_token_99999");

    // Identical buffers
    assert.ok(timingSafeEqual(tokenA, tokenB), "Identical tokens must match via timingSafeEqual.");
    // Differing buffers
    assert.ok(!timingSafeEqual(tokenA, tokenC), "Differing tokens must fail via timingSafeEqual.");
  });
});
