import { test } from "node:test";
import assert from "node:assert";
import { formatExecutionLatency } from "../src/cockpit.ts";

test("formatExecutionLatency formats microsecond and millisecond scales", () => {
  assert.strictEqual(formatExecutionLatency(0.42), "420µs");
  assert.strictEqual(formatExecutionLatency(12.345), "12.35ms");
});
