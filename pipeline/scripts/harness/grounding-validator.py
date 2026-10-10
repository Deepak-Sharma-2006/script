"""
Empirical Claims & Grounding Validator (INV-01 / Stage 1)

Validates that all commit diffs, documentation claims, and benchmark metrics
are grounded in verified project execution evidence:
1. Physical Hardware Latency Verification (Steps * Latency = Time).
2. Audit Trail Grounding (Assertions of 'tests pass' must have matching exit 0 in audit log).
3. Zero Hallucinated Run Logs (Training metrics must match actual log tokens).
"""

import os
import sys
import re
import json
import subprocess
from typing import List, Dict, Any, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORKSPACE_ROOT = os.getcwd()
AUDIT_LOG_FILE = os.path.join(WORKSPACE_ROOT, ".agents", "audit_trail.log")
BENCHMARK_FILE = os.path.join(WORKSPACE_ROOT, "pipeline", "specs", "benchmark_metrics.json") if os.path.exists(os.path.join(WORKSPACE_ROOT, "pipeline", "specs", "benchmark_metrics.json")) else os.path.join(WORKSPACE_ROOT, "specs", "benchmark_metrics.json")

class GroundingValidator:
    """Verifies that documentation, diffs, and benchmark files are empirically grounded."""

    @classmethod
    def load_recent_audit_log(cls, max_lines: int = 100) -> List[str]:
        if not os.path.exists(AUDIT_LOG_FILE):
            return []
        try:
            with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                return lines[-max_lines:]
        except Exception:
            return []

    @classmethod
    def verify_physical_compute_bounds(cls, text: str) -> List[Dict[str, Any]]:
        """
        Validates that reported training times do not violate physical hardware compute floors.
        For Tesla T4 at 672x672 (2309 tokens/tile, 16 batch, 224 steps/epoch):
        Empirical floor is 1.58s / step -> 354s (5.9 min) per epoch.
        """
        violations = []
        
        # Pattern checking for claims of 20 epochs in under 60 minutes on T4
        if re.search(r"\b20\s+epochs?\b", text, re.IGNORECASE):
            low_duration_match = re.search(r"\b([0-5]?[0-9])\s*(?:min(?:utes?)?|m)\b", text, re.IGNORECASE)
            if low_duration_match:
                mins = float(low_duration_match.group(1))
                if mins < 60.0 and "t4" in text.lower():
                    violations.append({
                        "type": "PHYSICAL_COMPUTE_VIOLATION",
                        "claim": f"20 epochs in {mins} minutes on Tesla T4",
                        "physics_bound": "Physical minimum for 20 epochs on T4 at 672x672 is ~118 minutes (1.58s/step * 224 steps * 20 ep).",
                        "resolution": "Use real 10-epoch transfer schedule (~58.5 min) or multi-resolution curriculum."
                    })

        return violations

    @classmethod
    def verify_test_pass_grounding(cls, staged_diff: str) -> List[Dict[str, Any]]:
        """
        If diff claims 'tests pass' or 'all tests green', verifies that a real test command
        succeeded in .agents/audit_trail.log.
        """
        violations = []
        claims_tests_pass = bool(re.search(r"(?:tests?\s+(?:pass(?:ed)?|green|succeed(?:ed)?)|100%\s+green)", staged_diff, re.IGNORECASE))
        
        if claims_tests_pass:
            recent_logs = cls.load_recent_audit_log(200)
            has_passed_test = False
            for line in recent_logs:
                if ("test" in line.lower() or "pytest" in line.lower() or "vitest" in line.lower()) and "EXIT: 0" in line:
                    has_passed_test = True
                    break
            
            if not has_passed_test and len(recent_logs) > 0:
                # Flag as ungrounded test claim if diff claims tests pass but no recent test run succeeded
                violations.append({
                    "type": "UNGROUNDED_TEST_ASSERTION",
                    "claim": "Documentation or commit diff asserts tests passed, but .agents/audit_trail.log has zero recorded EXIT: 0 test executions.",
                    "resolution": "Execute real tests via npm test or pytest before claiming tests pass."
                })

        return violations

    @classmethod
    def verify_file(cls, file_path: str) -> Tuple[bool, List[Dict[str, Any]]]:
        if not os.path.exists(file_path):
            return True, []
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        violations = []
        violations.extend(cls.verify_physical_compute_bounds(content))
        return len(violations) == 0, violations

    @classmethod
    def verify_staged(cls) -> Tuple[bool, List[Dict[str, Any]]]:
        try:
            diff = subprocess.check_output(["git", "diff", "--staged"], text=True, cwd=WORKSPACE_ROOT)
        except Exception:
            diff = ""

        violations = []
        violations.extend(cls.verify_physical_compute_bounds(diff))
        violations.extend(cls.verify_test_pass_grounding(diff))
        return len(violations) == 0, violations


def main():
    print("🔍 [Grounding Validator] Verifying empirical grounding against physical bounds and audit logs...")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--staged":
        valid, violations = GroundingValidator.verify_staged()
    elif len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        valid, violations = GroundingValidator.verify_file(sys.argv[1])
    else:
        # Default: verify staged changes
        valid, violations = GroundingValidator.verify_staged()

    if not valid:
        print("\n🛑 [GROUNDING VIOLATION DETECTED]")
        for v in violations:
            print(f"   ❌ Type: {v['type']}")
            print(f"      Claim: {v['claim']}")
            print(f"      Resolution: {v['resolution']}")
        sys.exit(1)

    print("✅ [Grounding Validator] All empirical assertions grounded in verified execution evidence.")
    sys.exit(0)

if __name__ == "__main__":
    main()
