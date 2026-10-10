import { test } from "node:test";
import assert from "node:assert";
import { Ledger } from "../src/ledger.ts";

test("Ledger records deposits and returns updated balance", () => {
  const l = new Ledger();
  assert.strictEqual(l.deposit(100), 100);
  assert.strictEqual(l.getBalance(), 100);
});
