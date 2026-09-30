"""
Programmatic GateGuard Fact-Forcing Middleware (INV-01)
Intercepts plans, architectures, and responses to block ungrounded empirical
assertions (metrics, dataset distributions, test scores) that lack physical
tool execution proof in the session transcript or audit trail.
"""

import sys
import os
import re
import json
from typing import Dict, Any, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class GateGuard:
    """
    Enforces that empirical claims are grounded in verifiable tool executions.
    Rejects plans that hallucinate dataset shapes, distributions, or metrics.
    """

    EMPIRICAL_ASSERTION_PATTERNS = [
        (r"\b\d+(?:\.\d+)?%\s+(?:singletons?|nulls?|matches?|match\s+rate|accuracy|f1|f0\.5|coverage)\b", "Percentage metric assertion"),
        (r"\b(?:f0\.5|f1|accuracy|recall|precision)\s*[=≥≤≈]\s*0\.\d+\b", "Numeric metric bound assertion"),
        (r"\b\d+(?:\.\d+)?\s*(?:M|K|k|million|thousand)\s*(?:records|rows|entities|tokens|pairs)\b", "Dataset scale assertion"),
        (r"\b(?:zero|0)\s+(?:nulls?|missing|ghost|hallucination)\b", "Zero-fault empirical assertion"),
    ]

    AUDIT_TRAIL_PATH = os.path.join(".agents", "audit_trail.log")

    @classmethod
    def extract_empirical_claims(cls, text: str) -> List[Dict[str, str]]:
        """Finds all empirical claims in the text."""
        claims = []
        for pattern, claim_type in cls.EMPIRICAL_ASSERTION_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for m in matches:
                claims.append({
                    "matched_text": m.group(0),
                    "claim_type": claim_type,
                    "position": m.start(),
                })
        return claims

    @classmethod
    def check_execution_evidence(
        cls,
        claims: List[Dict[str, str]],
        executed_commands: Optional[List[str]] = None,
        max_lookback_lines: int = 50,
        inspect_audit_log: bool = True,
    ) -> Dict[str, Any]:
        """
        Validates if tool execution history contains evidence (file inspections, test runs, data reads).
        """
        recent_commands = list(executed_commands) if executed_commands is not None else []

        # Also inspect .agents/audit_trail.log if requested and executed_commands wasn't explicitly supplied as empty
        if inspect_audit_log and executed_commands is None and os.path.exists(cls.AUDIT_TRAIL_PATH):
            try:
                with open(cls.AUDIT_TRAIL_PATH, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    recent_lines = [l.strip() for l in lines[-max_lookback_lines:] if l.strip()]
                    recent_commands.extend(recent_lines)
            except Exception:
                pass

        has_data_inspection = any(
            any(k in cmd.lower() for k in ["head", "tail", "wc", "python", "pytest", "npm", "cat", "view", "grep"])
            for cmd in recent_commands
        )

        violations = []
        if claims and not has_data_inspection:
            for c in claims:
                violations.append(
                    f"GATEGUARD REJECTION: Empirical claim '{c['matched_text']}' ({c['claim_type']}) "
                    f"asserted without raw file tool execution proof."
                )

        return {
            "passed": len(violations) == 0,
            "claims_count": len(claims),
            "claims": claims,
            "evidence_commands_count": len(recent_commands),
            "violations": violations,
        }

    @classmethod
    def audit_text(
        cls,
        text: str,
        executed_commands: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Audits text and returns pass/fail and required actions."""
        claims = cls.extract_empirical_claims(text)
        evidence = cls.check_execution_evidence(claims, executed_commands)
        return evidence


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.orchestrator.gate_guard <path_to_text_or_plan>")
        sys.exit(1)

    filepath = sys.argv[1]
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    result = GateGuard.audit_text(content)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
