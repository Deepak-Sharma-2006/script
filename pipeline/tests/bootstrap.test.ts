import test from "node:test";
import assert from "node:assert/strict";
import { createServer, defaultConfig } from "../../src/index.ts";

test("Bootstrap Server Test Suite", async (t) => {
  const server = createServer();

  await t.test("defaultConfig should have valid baseline properties", () => {
    assert.strictEqual(typeof defaultConfig.port, "number");
    assert.strictEqual(typeof defaultConfig.serviceName, "string");
    assert.strictEqual(typeof defaultConfig.version, "string");
    assert.ok(defaultConfig.port > 0);
  });

  await t.test("server instance should be created properly", () => {
    assert.ok(server !== null);
    assert.strictEqual(typeof server.listen, "function");
    assert.strictEqual(typeof server.close, "function");
  });

  await t.test("server endpoints and security shield verification", async () => {
    await new Promise<void>((resolve, reject) => {
      server.listen(0, async () => {
        try {
          const address = server.address();
          if (!address || typeof address === "string") {
            throw new Error("Invalid server address");
          }

          const base = `http://127.0.0.1:${address.port}`;

          // 1. Health check
          const healthRes = await fetch(`${base}/health`);
          assert.strictEqual(healthRes.status, 200);
          const healthData = await healthRes.json();
          assert.strictEqual(healthData.status, "healthy");
          assert.strictEqual(healthData.service, defaultConfig.serviceName);

          // 2. Info check
          const infoRes = await fetch(`${base}/api/info`);
          assert.strictEqual(infoRes.status, 200);
          const infoData = await infoRes.json();
          assert.strictEqual(infoData.service, defaultConfig.serviceName);
          assert.strictEqual(infoData.version, defaultConfig.version);

          // 3. Security check (path traversal & injection rejection)
          const badRes1 = await fetch(`${base}/../etc/passwd`);
          assert.strictEqual(badRes1.status, 400);

          const badRes2 = await fetch(`${base}/%3Cscript%3E`);
          assert.strictEqual(badRes2.status, 400);

          // 4. Not found route
          const notFoundRes = await fetch(`${base}/unmapped-route-xyz`);
          assert.strictEqual(notFoundRes.status, 404);

          server.close(() => resolve());
        } catch (err) {
          server.close(() => reject(err));
        }
      });
    });
  });
});
