"""
Agent Consistency Gate (Pass^k vs. Mean@k)
Implements the AI Concept Atlas "Agent Consistency Gap" Resolution (IBM ALTK-Evolve).

Solves the Flaky Execution & False-Reliability Defect:
1. Executes a target test suite across k repeated independent trials.
2. Measures:
   - Mean@k       : Average pass rate across trials.
   - Pass^k       : Percentage of runs where 100% of trials succeeded with 0 failures.
   - Consistency Gap: (Mean@k - Pass^k) * 100%.
3. Enforces that critical enterprise pipelines must achieve Pass^k == 1.0 (Zero Consistency Gap).
"""

import os
import sys
import time
import subprocess
from typing import Dict, Any, List

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class ConsistencyChecker:
    """
    Evaluates multi-run repeatability to close the Agent Consistency Gap.
    """

    @classmethod
    def evaluate_consistency(
        cls,
        test_command: List[str],
        k_trials: int = 3,
        timeout_per_run: int = 30
    ) -> Dict[str, Any]:
        print(f"\n{'=' * 80}")
        print(f"[ConsistencyChecker] Launching Pass^{k_trials} Repeatability Probe")
        print(f"   Test Command : {' '.join(test_command)}")
        print(f"   Target Runs  : {k_trials} consecutive trials")
        print(f"   Metric Goal  : Zero Consistency Gap (Pass^{k_trials} == 1.0)")
        print(f"{'=' * 80}\n")

        run_results: List[Dict[str, Any]] = []
        passes = 0

        for i in range(1, k_trials + 1):
            t0 = time.time()
            res = subprocess.run(test_command, capture_output=True, text=True, timeout=timeout_per_run)
            duration = round(time.time() - t0, 3)
            passed = (res.returncode == 0)

            if passed:
                passes += 1
                status = "PASSED"
            else:
                status = f"FAILED (Code {res.returncode})"

            print(f"   Trial {i}/{k_trials}: [{status}] in {duration}s")
            run_results.append({
                "trial": i,
                "passed": passed,
                "exit_code": res.returncode,
                "duration_s": duration
            })

        mean_k = round(passes / k_trials, 3)
        pass_pow_k = 1.0 if passes == k_trials else 0.0
        consistency_gap = round((mean_k - pass_pow_k) * 100.0, 1)

        certified = (pass_pow_k == 1.0)

        print(f"\n{'=' * 80}")
        print(f"[CONSISTENCY REPORT] Result: {'[CONSISTENT - ZERO FLAKE]' if certified else '[FLAKY - CONSISTENCY GAP DETECTED]'}")
        print(f"   Mean@{k_trials}       : {round(mean_k * 100, 1)}%")
        print(f"   Pass^{k_trials}       : {round(pass_pow_k * 100, 1)}%")
        print(f"   Consistency Gap: {consistency_gap}%")
        print(f"{'=' * 80}\n")

        return {
            "k_trials": k_trials,
            "passes": passes,
            "mean_at_k": mean_k,
            "pass_pow_k": pass_pow_k,
            "consistency_gap_percent": consistency_gap,
            "certified_consistent": certified,
            "trial_logs": run_results
        }


if __name__ == "__main__":
    cmd = [sys.executable, "-m", "unittest", "tests/test_peav_and_sync.py"]
    res = ConsistencyChecker.evaluate_consistency(cmd, k_trials=3)
    sys.exit(0 if res["certified_consistent"] else 1)
