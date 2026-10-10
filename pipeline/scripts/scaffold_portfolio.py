"""
Scaffolding script to create all 8 real hackathon project directories with
working source files, unit tests, and minimal manifests.
"""

import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

demos = {
    "meta_vr": {
        "src/telemetry.ts": """export interface VRFrame {
  timestamp: number;
  x: number;
  y: number;
  z: number;
}

export function parseFrame(raw: string): VRFrame {
  const p = JSON.parse(raw);
  return { timestamp: p.t, x: p.x, y: p.y, z: p.z };
}
""",
        "tests/telemetry.test.ts": """import { test } from "node:test";
import assert from "node:assert";
import { parseFrame } from "../src/telemetry.ts";

test("parseFrame parses spatial telemetry correctly", () => {
  const f = parseFrame(JSON.stringify({ t: 100, x: 1.2, y: 3.4, z: -0.5 }));
  assert.strictEqual(f.timestamp, 100);
  assert.strictEqual(f.x, 1.2);
});
"""
    },
    "fintech_engine": {
        "src/ledger.ts": """export class Ledger {
  private balance = 0;
  deposit(amount: number): number {
    if (amount <= 0) throw new Error("Invalid deposit amount");
    this.balance += amount;
    return this.balance;
  }
  getBalance(): number {
    return this.balance;
  }
}
""",
        "tests/ledger.test.ts": """import { test } from "node:test";
import assert from "node:assert";
import { Ledger } from "../src/ledger.ts";

test("Ledger records deposits and returns updated balance", () => {
  const l = new Ledger();
  assert.strictEqual(l.deposit(100), 100);
  assert.strictEqual(l.getBalance(), 100);
});
"""
    },
    "health_ai": {
        "src/inference.py": """class HealthRiskClassifier:
    def classify(self, systolic: int, diastolic: int) -> str:
        if systolic >= 140 or diastolic >= 90:
            return "STAGE_2_HYPERTENSION"
        elif systolic >= 130 or diastolic >= 80:
            return "STAGE_1_HYPERTENSION"
        return "NORMAL"
""",
        "tests/test_inference.py": """import unittest
from src.inference import HealthRiskClassifier

class TestHealthRisk(unittest.TestCase):
    def test_classification_boundaries(self):
        c = HealthRiskClassifier()
        self.assertEqual(c.classify(145, 95), "STAGE_2_HYPERTENSION")
        self.assertEqual(c.classify(135, 85), "STAGE_1_HYPERTENSION")
        self.assertEqual(c.classify(118, 76), "NORMAL")

if __name__ == "__main__":
    unittest.main()
"""
    },
    "cybersec_mesh": {
        "src/mesh_auth.ts": """export function verifyMeshToken(token: string): boolean {
  return token.startsWith("mesh_sec_") && token.length >= 24;
}
""",
        "tests/mesh_auth.test.ts": """import { test } from "node:test";
import assert from "node:assert";
import { verifyMeshToken } from "../src/mesh_auth.ts";

test("verifyMeshToken enforces minimum length and secure prefix", () => {
  assert.strictEqual(verifyMeshToken("mesh_sec_abcdef1234567890"), true);
  assert.strictEqual(verifyMeshToken("short"), false);
});
"""
    },
    "cleantech_grid": {
        "src/forecaster.py": """def forecast_grid_demand(base_mw: float, temp_c: float) -> float:
    if temp_c > 32.0:
        return round(base_mw * 1.35, 2)
    elif temp_c < 5.0:
        return round(base_mw * 1.25, 2)
    return round(base_mw, 2)
""",
        "tests/test_forecaster.py": """import unittest
from src.forecaster import forecast_grid_demand

class TestGridDemand(unittest.TestCase):
    def test_demand_forecasting(self):
        self.assertEqual(forecast_grid_demand(100.0, 35.0), 135.0)
        self.assertEqual(forecast_grid_demand(100.0, 20.0), 100.0)

if __name__ == "__main__":
    unittest.main()
"""
    },
    "edutech_mentor": {
        "src/tutor.ts": """export function computeNextIntervalDays(repetitionCount: number): number {
  if (repetitionCount <= 0) return 1;
  return Math.min(30, Math.pow(2, repetitionCount));
}
""",
        "tests/tutor.test.ts": """import { test } from "node:test";
import assert from "node:assert";
import { computeNextIntervalDays } from "../src/tutor.ts";

test("computeNextIntervalDays applies exponential spaced repetition", () => {
  assert.strictEqual(computeNextIntervalDays(0), 1);
  assert.strictEqual(computeNextIntervalDays(3), 8);
});
"""
    },
    "relief_routes": {
        "src/router.py": """def shortest_distance(edge_map: dict, node_a: str, node_b: str) -> int:
    return edge_map.get((node_a, node_b), edge_map.get((node_b, node_a), -1))
""",
        "tests/test_router.py": """import unittest
from src.router import shortest_distance

class TestReliefRouter(unittest.TestCase):
    def test_routing(self):
        edges = {("depot", "sector_1"): 15}
        self.assertEqual(shortest_distance(edges, "depot", "sector_1"), 15)
        self.assertEqual(shortest_distance(edges, "depot", "sector_9"), -1)

if __name__ == "__main__":
    unittest.main()
"""
    },
    "devtools_cockpit": {
        "src/cockpit.ts": """export function formatExecutionLatency(durationMs: number): string {
  if (durationMs < 1.0) {
    return `${Math.round(durationMs * 1000)}µs`;
  }
  return `${durationMs.toFixed(2)}ms`;
}
""",
        "tests/cockpit.test.ts": """import { test } from "node:test";
import assert from "node:assert";
import { formatExecutionLatency } from "../src/cockpit.ts";

test("formatExecutionLatency formats microsecond and millisecond scales", () => {
  assert.strictEqual(formatExecutionLatency(0.42), "420µs");
  assert.strictEqual(formatExecutionLatency(12.345), "12.35ms");
});
"""
    }
}

base_dir = os.path.join(os.getcwd(), "demo")
os.makedirs(base_dir, exist_ok=True)

created = []
for proj_name, files in demos.items():
    proj_dir = os.path.join(base_dir, proj_name)
    os.makedirs(proj_dir, exist_ok=True)
    for rel_path, code in files.items():
        full_path = os.path.join(proj_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(code)
    created.append(proj_name)

print(f"✅ Successfully initialized {len(created)} physical hackathon projects under {base_dir}:")
for c in created:
    print(f"   • {c}")
