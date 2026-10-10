import { test } from "node:test";
import assert from "node:assert";
import { verifyMeshToken } from "../src/mesh_auth.ts";

test("verifyMeshToken enforces minimum length and secure prefix", () => {
  assert.strictEqual(verifyMeshToken("mesh_sec_abcdef1234567890"), true);
  assert.strictEqual(verifyMeshToken("short"), false);
});
