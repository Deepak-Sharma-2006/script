import { test } from "node:test";
import assert from "node:assert";
import { computeNextIntervalDays } from "../src/tutor.ts";

test("computeNextIntervalDays applies exponential spaced repetition", () => {
  assert.strictEqual(computeNextIntervalDays(0), 1);
  assert.strictEqual(computeNextIntervalDays(3), 8);
});
