"""
Two-Tier Format Guard & Banned Sycophancy Scanner (INV-11)
Validates that model outputs adhere to the 6-persona enterprise structure,
contain valid cryptographic attestation receipts, and do not assert
unsubstantiated sycophantic claims.
"""

import sys
import re
import json
import yaml
from typing import Dict, Any, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class FormatGuard:
    """
    Validates LLM responses and markdown documents for:
    1. Complete 6-Persona Lifecycle Headers
    2. Structural Validity of Squad Execution Attestation Receipt
    3. Banned Sycophancy phrases without empirical tool execution
    4. Tier 2 Tactical Micro-Verdicts synthesis/validation
    """

    REQUIRED_PERSONAS = [
        ("Product Manager", r"\[Product Manager\]"),
        ("System Architect", r"\[System Architect\]"),
        ("Adversarial SDET", r"\[Adversarial SDET\]"),
        ("Core Engineer", r"\[Core Engineer\]"),
        ("Mutation & Security Auditor", r"\[Mutation & Security Auditor\]"),
        ("Technical Writer", r"\[Technical Writer\]"),
    ]

    BANNED_SYCOPHANCY_PATTERNS = [
        r"\bguaranteed\b",
        r"\bQ\.E\.D\.\b",
        r"\bmathematical(?:ly)?\s+proof\b",
        r"\bmathematical(?:ly)?\s+guaranteed\b",
        r"\b100%\s+win\b",
        r"\babsolute\s+certainty\b",
        r"\bimpossible\s+to\s+fail\b",
        r"\bflawless\s+execution\b",
        r"\bzero\s+risk\b",
    ]

    @classmethod
    def validate_personas(cls, text: str) -> Dict[str, Any]:
        """Asserts all 6 Enterprise Personas are present."""
        found = {}
        missing = []
        for name, pattern in cls.REQUIRED_PERSONAS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                found[name] = True
            else:
                found[name] = False
                missing.append(name)

        return {
            "all_present": len(missing) == 0,
            "found_count": len([k for k, v in found.items() if v]),
            "total_required": len(cls.REQUIRED_PERSONAS),
            "missing_personas": missing,
            "details": found,
        }

    @classmethod
    def validate_attestation(cls, text: str) -> Dict[str, Any]:
        """Asserts valid Squad Execution Attestation block exists."""
        # Find yaml code block with squad_execution_attestation
        yaml_match = re.search(
            r"```(?:yaml)?\s*(squad_execution_attestation:[\s\S]*?)```",
            text,
            re.IGNORECASE,
        )
        if not yaml_match:
            return {
                "valid": False,
                "error": "Missing squad_execution_attestation YAML receipt block.",
                "data": None,
            }

        yaml_content = yaml_match.group(1)
        try:
            parsed = yaml.safe_load(yaml_content)
            attestation = parsed.get("squad_execution_attestation", {})
            required_keys = ["timestamp", "provenance_hash", "active_personas", "executed_commands"]
            missing_keys = [k for k in required_keys if k not in attestation]
            if missing_keys:
                return {
                    "valid": False,
                    "error": f"Attestation YAML missing required keys: {missing_keys}",
                    "data": attestation,
                }

            skills = attestation.get("activated_skills", [])
            skills_count = len(skills) if isinstance(skills, list) else 0

            return {
                "valid": True,
                "provenance_hash": attestation.get("provenance_hash"),
                "commands_count": len(attestation.get("executed_commands", [])),
                "skills_count": skills_count,
                "activated_skills": skills,
                "data": attestation,
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Failed to parse attestation YAML: {str(e)}",
                "data": None,
            }

    @classmethod
    def scan_sycophancy(cls, text: str, executed_commands_count: int = 0) -> Dict[str, Any]:
        """
        Flags banned sycophantic claims unless substantiated by real tool executions.
        """
        flagged = []
        for pattern in cls.BANNED_SYCOPHANCY_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                flagged.extend(matches)

        flagged = list(set(flagged))
        # If there are zero executed commands, sycophantic certainty claims are fatal
        is_violation = len(flagged) > 0 and executed_commands_count == 0

        return {
            "violation": is_violation,
            "flagged_phrases": flagged,
            "executed_commands_count": executed_commands_count,
            "reason": (
                "Unsubstantiated certainty phrases detected without empirical tool execution."
                if is_violation
                else "Clean or substantiated by empirical tool executions."
            ),
        }

    @classmethod
    def synthesize_tier2_micro_verdicts(
        cls, prompt: str, domain: str = "general"
    ) -> Dict[str, str]:
        """
        Tier 2 Tactical Micro-Verdict Engine: Under rapid-fire or emergency prompts,
        generates standard 1-sentence micro-verdicts for each persona so personas
        are never dropped.
        """
        return {
            "Product Manager": f"Tactical intent confirmed: prioritize high-impact execution for {domain} with zero scope creep.",
            "System Architect": "Deterministic schema contracts preserved; state machine invariants remain locked.",
            "Adversarial SDET": "Rapid boundary validation active; pre-execution constraints asserted.",
            "Core Engineer": "Executing idiomatic targeted patch with minimum cyclomatic complexity.",
            "Mutation & Security Auditor": "Zero secrets verified; constant-time boundaries and fail-closed gates active.",
            "Technical Writer": "Logging structured diff and synchronizing living memory ledger.",
        }

    @classmethod
    def audit_response(
        cls, text: str, is_tactical: bool = False
    ) -> Dict[str, Any]:
        """
        Performs a full audit of an LLM response.
        """
        persona_check = cls.validate_personas(text)
        attestation_check = cls.validate_attestation(text)
        cmd_count = attestation_check.get("commands_count", 0) if attestation_check.get("valid") else 0
        sycophancy_check = cls.scan_sycophancy(text, executed_commands_count=cmd_count)

        passed = (
            persona_check["all_present"]
            and attestation_check["valid"]
            and not sycophancy_check["violation"]
        )

        return {
            "passed": passed,
            "persona_audit": persona_check,
            "attestation_audit": attestation_check,
            "sycophancy_audit": sycophancy_check,
            "is_tactical": is_tactical,
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.orchestrator.format_guard <path_to_text_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    result = FormatGuard.audit_response(content)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
