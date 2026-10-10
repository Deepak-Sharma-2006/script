import { test } from "node:test";
import assert from "node:assert";
import { parseFrame } from "../src/telemetry.ts";

test("parseFrame parses spatial telemetry correctly", () => {
  const f = parseFrame(JSON.stringify({ t: 100, x: 1.2, y: 3.4, z: -0.5 }));
  assert.strictEqual(f.timestamp, 100);
  assert.strictEqual(f.x, 1.2);
});
