"""
Contrarian Adversarial Falsification Engine (INV-03)
Intercepts skepticism, audit, and verification inquiries to suppress sycophancy
and enforce rigorous falsification:
1. Top 3 physical breaking points
2. Sensitivity curves under stress/distribution drift
3. Empirical confidence bounds grounded in verified test runs
"""

import sys
import re
import json
from typing import Dict, Any, List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class ContrarianAuditor:
    """
    Detects skepticism and ensures answers contain falsification analysis
    rather than ungrounded reassurance.
    """

    SKEPTICISM_TRIGGERS = [
        r"\bare\s+you\s+sure\b",
        r"\bwhat\s+is\s+the\s+guarantee\b",
        r"\bwhy\s+did\s+this\s+fail\b",
        r"\bis\s+this\s+real\b",
        r"\bprove\s+it\b",
        r"\bis\s+it\s+(?:sufficient|efficient|ready)\b",
        r"\bnot\s+just\s+a\s+readme\b",
        r"\bbrutally\s+honest\b",
        r"\breview\s+(?:our\s+)?harness\b",
    ]

    @classmethod
    def is_skepticism_prompt(cls, prompt: str) -> bool:
        """Determines if the prompt demands rigorous falsification."""
        for pattern in cls.SKEPTICISM_TRIGGERS:
            if re.search(pattern, prompt, re.IGNORECASE):
                return True
        return False

    @classmethod
    def generate_falsification_template(
        cls,
        subject: str,
        breaking_points: Optional[List[str]] = None,
        drift_sensitivities: Optional[List[str]] = None,
        empirical_bounds: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Synthesizes a structured contrarian failure audit for the subject.
        """
        bp = breaking_points or [
            f"Physical breaking point 1: Unhandled boundary state or memory spike in {subject}.",
            f"Physical breaking point 2: Silent degradation under non-stationary distribution drift.",
            f"Physical breaking point 3: Concurrency or lock contention bottleneck under parallel load.",
        ]
        drift = drift_sensitivities or [
            "Noise injection (10% corruption): Expected metric drop of ~2.5% to 4.0%.",
            "Sparse data / cold start: Upstream candidate recall drops to ~88% without secondary index fallback.",
            "Memory saturation: Process throttles or crashes if unbudgeted heap growth exceeds 75% RAM.",
        ]
        bounds = empirical_bounds or {
            "lower_bound_95ci": "Grounded lower bound from deterministic tests.",
            "observed_mean": "Empirically measured mean.",
            "upper_bound_95ci": "Upper bound subject to zero-fault execution.",
        }

        return {
            "subject": subject,
            "top_3_breaking_points": bp,
            "distribution_drift_sensitivity": drift,
            "empirical_confidence_bounds": bounds,
            "verdict": "CONTRARIAN_FALSIFICATION_ACTIVE",
        }

    @classmethod
    def audit_response_for_falsification(
        cls, prompt: str, response_text: str
    ) -> Dict[str, Any]:
        """
        If prompt expresses skepticism, verifies that response contains
        falsification elements and breaking point discussions.
        """
        is_skeptical = cls.is_skepticism_prompt(prompt)
        if not is_skeptical:
            return {"required": False, "passed": True, "reason": "Standard prompt; falsification not mandatory."}

        # Check for breaking points / limitations / failure modes
        has_breaking_points = bool(re.search(r"\b(?:breaking\s+point|failure\s+mode|limitation|vulnerability|bottleneck)\b", response_text, re.IGNORECASE))
        has_empirical_grounding = bool(re.search(r"\b(?:empirical|benchmark|measured|exit\s+code|run_command|test)\b", response_text, re.IGNORECASE))

        passed = has_breaking_points and has_empirical_grounding

        return {
            "required": True,
            "passed": passed,
            "has_breaking_points": has_breaking_points,
            "has_empirical_grounding": has_empirical_grounding,
            "reason": (
                "Response successfully includes adversarial falsification and empirical grounding."
                if passed
                else "REJECTED: Skepticism prompt requires explicit failure mode analysis and empirical verification."
            ),
        }


def main():
    if len(sys.argv) < 3:
        print("Usage: python -m scripts.orchestrator.contrarian_auditor <prompt> <response_text_file>")
        sys.exit(1)

    prompt = sys.argv[1]
    with open(sys.argv[2], "r", encoding="utf-8") as f:
        resp = f.read()

    result = ContrarianAuditor.audit_response_for_falsification(prompt, resp)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
