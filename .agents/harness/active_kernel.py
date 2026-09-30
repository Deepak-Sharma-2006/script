"""
Active Interception Kernel & Dynamic Multi-Domain Harness
Enforces pre-execution and post-execution gates across all 8 Master Domains and 46 Subdomains.
Provides active interception, cognitive Memory Vault tracking, and structured self-healing feedback.
"""

import sys
import os
import re
import json
from typing import Dict, Any, List, Optional, Tuple

# Ensure workspace root is in python path
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scripts.orchestrator.memory_guard import MemoryGuard, MemoryBudgetExceededException
from scripts.orchestrator.deadline_lockdown import DeadlineLockdown
from scripts.orchestrator.scale_profiler import ScaleProfiler
from scripts.orchestrator.gate_guard import GateGuard
from scripts.orchestrator.format_guard import FormatGuard
from scripts.orchestrator.skill_resolver import SkillResolver
from scripts.orchestrator.pipeline_gate import PipelineGate
from scripts.orchestrator.calibration_auditor import CalibrationAuditor


class ActiveKernel:
    """
    Unified active execution kernel wrapping tool invocations, bash execution,
    and output validation with dynamic 8-domain and 46-subdomain contracts.
    """

    STATE_FILE = os.path.join(".agents", "state", "active-domain.json")

    DOMAIN_INVARIANTS = {
        "blockchain": {
            "name": "Blockchain & Smart Contracts",
            "forbidden_patterns": [
                r"msg\.sender\.call\{value:\s*[^}]+\}\(\"\"\);\s*balances\[msg\.sender\]\s*=",
                r"reserves\[0\]\s*/\s*reserves\[1\](?!.*TWAP)",
            ],
            "required_patterns": ["ReentrancyGuard", "SafeERC20"],
            "guidance": "Enforce Checks-Effects-Interactions (CEI) and TWAP oracle price feeds.",
        },
        "ai_ml": {
            "name": "AI, ML & Data Engineering",
            "forbidden_patterns": [
                r"pd\.read_csv\([^)]+\)(?!.*chunksize)",
                r"scale_pos_weight\s*=\s*\d+(?!.*calibrat)",
            ],
            "required_patterns": ["ScaleProfiler", "MemoryGuard"],
            "guidance": "Enforce 500-item micro-benchmarks, 75% RAM limit, and probability calibration.",
        },
        "cybersecurity": {
            "name": "Cybersecurity & Zero Trust",
            "forbidden_patterns": [
                r"==\s*['\"][a-zA-Z0-9_\-]{16,}['\"]",  # Plain equality on tokens
                r"password\s*=\s*['\"][^'\"]+['\"]",     # Hardcoded password
            ],
            "required_patterns": ["timingSafeEqual", "hash"],
            "guidance": "Enforce constant-time timingSafeEqual comparisons and zero plaintext credentials.",
        },
        "software": {
            "name": "Software & Web Systems",
            "forbidden_patterns": [
                r":\s*any\b",
                r"res\.status\(500\)\.send\(['\"][^'\"]+['\"]\)",
            ],
            "required_patterns": ["ProblemDetails", "interface"],
            "guidance": "Enforce strict TypeScript (zero any) and RFC 7807 structured Problem Details.",
        },
        "cloud_infra": {
            "name": "Cloud Infrastructure & SRE",
            "forbidden_patterns": [
                r"USER\s+root",
                r"--privileged",
            ],
            "required_patterns": ["resources", "limits"],
            "guidance": "Enforce non-root container execution and explicit cgroup memory/CPU limits.",
        },
        "data_engineering": {
            "name": "Data Engineering & Lakehouses",
            "forbidden_patterns": [
                r"\.to_csv\([^)]+\)(?!.*chunk)",
            ],
            "required_patterns": ["parquet", "feather"],
            "guidance": "Enforce zero-copy columnar storage formats and stream buffer limits.",
        },
        "deep_tech": {
            "name": "Deep Tech & Scientific Computing",
            "forbidden_patterns": [
                r"random\.seed\(None\)",
            ],
            "required_patterns": ["float64", "seed"],
            "guidance": "Enforce deterministic seed initialization and IEEE 754 precision compliance.",
        },
        "vertical_applied": {
            "name": "Vertical Applied & Regulated IT",
            "forbidden_patterns": [
                r"console\.log\(.*ssn.*\)",
                r"print\(.*patient_id.*\)",
            ],
            "required_patterns": ["audit_trail", "sanitize"],
            "guidance": "Enforce HIPAA/GDPR statutory audit logging and zero PII leakage.",
        },
    }

    @classmethod
    def get_active_domain(cls) -> Tuple[str, List[str]]:
        """Resolves active domain and subdomains."""
        if os.path.exists(cls.STATE_FILE):
            try:
                with open(cls.STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    dom = data.get("domain_id", data.get("domain", "software"))
                    subs = data.get("subdomains", [])
                    return dom, subs
            except Exception:
                pass
        return "software", []

    @classmethod
    def get_vault_status(cls) -> Dict[str, Any]:
        """Resolves the cognitive/semantic Memory Vault state from SQLite."""
        vault_db = os.path.join(WORKSPACE_ROOT, ".agents", "memory", "vault.sqlite")
        total_memories = 0
        total_attestations = 0
        is_connected = False
        if os.path.exists(vault_db):
            try:
                import sqlite3
                conn = sqlite3.connect(vault_db)
                c = conn.cursor()
                c.execute("SELECT count(*) FROM memories")
                total_memories = c.fetchone()[0]
                c.execute("SELECT count(*) FROM squad_attestations")
                total_attestations = c.fetchone()[0]
                conn.close()
                is_connected = True
            except Exception:
                pass

        vault_docs_dir = os.path.join(WORKSPACE_ROOT, ".agents", "memory")
        doc_count = 0
        if os.path.exists(vault_docs_dir):
            for root, _, files in os.walk(vault_docs_dir):
                doc_count += sum(1 for f in files if f.endswith(".md"))

        return {
            "status": "CONNECTED" if is_connected else "INITIALIZING",
            "backend": "SQLite (.agents/memory/vault.sqlite)",
            "indexed_memories": total_memories,
            "attestations_sealed": total_attestations,
            "vault_documents": doc_count,
        }

    @classmethod
    def pre_execute_gate(
        cls,
        command_line: str,
        target_file: Optional[str] = None,
        file_content: Optional[str] = None,
        item_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Active Pre-Execution Gate:
        Evaluates deadline lockdown, scale profiler, large-batch memory limits, and domain invariants
        BEFORE any shell command or file write is executed.
        """
        active_domain, active_subs = cls.get_active_domain()

        # 1. Scale Profiler & Heavy Batch Resource Guard (Only for large datasets / heavy compute jobs)
        is_large_batch = (
            (item_count is not None and item_count > 10000)
            or bool(re.search(r"(?:3\.8M|1M|100k|500k|large|pairwise|full_dataset)", command_line, re.IGNORECASE))
            or "--guard-memory" in command_line
        )

        if is_large_batch:
            # 1a. Scale Profiler check
            if "scale_profiler" not in command_line:
                return {
                    "permitted": False,
                    "gate": "ScaleProfiler",
                    "status": "REJECTED_UNPROFILED_LARGE_SCALE",
                    "reason": f"Execution operates on >10,000 items without mandatory 500-item micro-batch profiling.",
                    "remediation_guidance": "Run `python -m scripts.orchestrator.scale_profiler 500 <elapsed> <total>` before full execution.",
                }

            # 1b. Memory Guard for heavy batch pipelines (prevents uncatchable kernel SIGKILL)
            mem_check = MemoryGuard.check_memory(max_pct=75.0)
            if not mem_check["within_budget"]:
                return {
                    "permitted": False,
                    "gate": "MemoryGuard",
                    "status": "REJECTED_MEMORY_BREACH",
                    "reason": (
                        f"Physical RAM allocation {mem_check['used_percent']}% exceeds 75% ceiling "
                        f"({mem_check['available_gb']} GB available). Large batch compute halted to prevent SIGKILL."
                    ),
                    "remediation_guidance": "Chunk in-memory data, stream via Polars/generator, or free unused references.",
                }

        # 2. Deadline Lockdown (Universal Gate)
        lock_check = DeadlineLockdown.validate_action(command_line)
        if not lock_check["permitted"]:
            return {
                "permitted": False,
                "gate": "DeadlineLockdown",
                "status": "REJECTED_T4H_LOCKDOWN",
                "reason": lock_check["reason"],
                "remediation_guidance": "Switch strictly to submission packaging, schema linting, and smoke testing.",
            }

        # 3. Domain-Specific Invariant Checks
        domain_cfg = cls.DOMAIN_INVARIANTS.get(active_domain)
        if domain_cfg and file_content:
            for pattern in domain_cfg.get("forbidden_patterns", []):
                if re.search(pattern, file_content, re.IGNORECASE):
                    return {
                        "permitted": False,
                        "gate": f"DomainGate:{active_domain}",
                        "status": "REJECTED_DOMAIN_INVARIANT_VIOLATION",
                        "reason": f"Code violates domain invariant pattern: {pattern}",
                        "remediation_guidance": domain_cfg.get("guidance", "Adhere to domain security specifications."),
                    }

        # Resolve matching skills automatically
        skills_info = SkillResolver.resolve_skills(command_line, domain_id=active_domain, subdomains=active_subs)

        return {
            "permitted": True,
            "domain": active_domain,
            "subdomains": active_subs,
            "activated_skills": skills_info.get("activated_skills", []),
            "status": "APPROVED",
        }

    @classmethod
    def post_execute_gate(
        cls,
        output_text: str,
        executed_commands: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Active Post-Execution Gate:
        Evaluates Fact-Forcing (GateGuard), Personas & Receipt Validity (FormatGuard),
        and Skill Attestation.
        """
        # 1. Fact-Forcing GateGuard Check
        gate_res = GateGuard.audit_text(output_text, executed_commands=executed_commands)
        if not gate_res["passed"]:
            return {
                "passed": False,
                "gate": "GateGuard",
                "status": "REJECTED_UNGROUNDED_ASSERTION",
                "violations": gate_res.get("violations", []),
                "remediation_guidance": "Physically inspect raw files or execute real tests before asserting metrics.",
            }

        # 2. FormatGuard 6-Persona and Attestation Check
        format_res = FormatGuard.audit_response(output_text)
        if not format_res["passed"]:
            return {
                "passed": False,
                "gate": "FormatGuard",
                "status": "REJECTED_FORMAT_VIOLATION",
                "details": format_res,
                "remediation_guidance": "Include all 6 personas and valid squad_execution_attestation YAML receipt.",
            }

        return {
            "passed": True,
            "status": "POST_EXECUTION_VERIFIED",
            "skills_count": format_res.get("attestation_audit", {}).get("skills_count", 0),
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python .agents/harness/active_kernel.py [--status|--check|--intercept <command>]")
        sys.exit(0)

    arg = sys.argv[1]
    if arg in ("--check", "--status"):
        dom, subs = ActiveKernel.get_active_domain()
        vault = ActiveKernel.get_vault_status()
        lock = DeadlineLockdown.get_status()
        payload = {
            "active_kernel": "ONLINE",
            "domain": dom,
            "subdomains": subs,
            "agent_memory_vault": vault,
            "deadline": lock,
        }
        if "--hardware" in sys.argv:
            payload["host_hardware_ram"] = MemoryGuard.check_memory()

        print(json.dumps(payload, indent=2))
        sys.exit(0)
    elif arg == "--intercept" and len(sys.argv) > 2:
        cmd = " ".join(sys.argv[2:])
        res = ActiveKernel.pre_execute_gate(cmd)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["permitted"] else 1)


if __name__ == "__main__":
    main()
