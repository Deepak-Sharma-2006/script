"""
Active Interception Kernel & Dynamic Multi-Domain Harness
Enforces pre-execution, in-flight, and post-execution gates across all 8 Master Domains and 46 Subdomains.
Implements the 7 Enterprise Harness Pillars:
  1. Safety & Governance (Microsoft Agent Governance: PERMIT, BLOCK, MODIFY, ESCALATE)
  2. Telemetry & Observability (AWS Dogwood continuous runtime verification)
  3. Context Steering & Reshaping (Stripe positive prompt guidance & output truncation)
  4. In-Flight Verification Loop (DeepCode AST and invariant checks)
  5. Continual Self-Evolution (Trajectory signal aggregation & staged patches)
  6. Cognitive Memory Recall (Hermes Agent SQLite Vault injection)
  7. Multi-Agent Personas & Domain Contracts (Omnigent 6+1 squad)
"""

import sys
import os
import re
import json
import ast
from enum import Enum
from datetime import datetime, timezone
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
from scripts.orchestrator.continual_evolution import EvolutionEngine


class DecisionOutcome(str, Enum):
    """
    Microsoft Agent Governance Toolkit Join Point Outcomes
    """
    PERMIT = "PERMIT"
    BLOCK = "BLOCK"
    MODIFY = "MODIFY"
    ESCALATE = "ESCALATE"


class ActiveKernel:
    """
    Unified active execution kernel wrapping tool invocations, shell commands,
    and output validation with dynamic 8-domain and 46-subdomain contracts.
    """

    STATE_FILE = os.path.join(WORKSPACE_ROOT, ".agents", "state", "active-domain.json")
    AUDIT_LOG_FILE = os.path.join(WORKSPACE_ROOT, ".agents", "audit_trail.log")
    STREAM_LOG_FILE = os.path.join(WORKSPACE_ROOT, ".agents", "state", "telemetry_stream.jsonl")

    # Layer 1: High-impact destructive command patterns mandating Operator Escalation
    DESTRUCTIVE_COMMAND_PATTERNS = [
        (r"\brm\s+-[rRfF]{1,3}\b", "Recursive deletion (rm -rf)"),
        (r"\brmdir\s+/[sSqQ]\b", "Recursive Windows directory wipe (rmdir /s /q)"),
        (r"\bDROP\s+(?:DATABASE|TABLE|SCHEMA)\b", "Database object destruction (DROP TABLE/DATABASE)"),
        (r"\bTRUNCATE\s+TABLE\b", "Database table wipe (TRUNCATE TABLE)"),
        (r"\bterraform\s+destroy\b", "Infrastructure teardown (terraform destroy)"),
        (r"\bkubectl\s+delete\s+(?:all|namespace|ns)\b", "Cluster resource wipe (kubectl delete all/ns)"),
        (r"\baws\s+s3\s+rb\b", "S3 bucket destruction (aws s3 rb)"),
        (r"\baws\s+s3\s+rm\s+.*--recursive\b", "Recursive S3 deletion (aws s3 rm --recursive)"),
        (r"\bgit\s+push\s+.*--force\b.*(?:main|master)", "Force push to protected trunk branch"),
        (r"\bmkfs(?:\.[a-z0-9]+)?\b", "Filesystem format (mkfs)"),
        (r"\bfdisk\b", "Disk partition modification (fdisk)"),
    ]

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
    def emit_telemetry(cls, event_type: str, details: Dict[str, Any]):
        """
        Layer 2 Telemetry & Observability (AWS Dogwood Runtime Verification):
        Continuous, non-blocking telemetry emitter streaming runtime events
        to .agents/audit_trail.log and .agents/state/telemetry_stream.jsonl.
        """
        try:
            now_iso = datetime.now(timezone.utc).isoformat()
            active_domain, _ = cls.get_active_domain()
            record = {
                "timestamp": now_iso,
                "event_type": event_type,
                "domain": active_domain,
                "details": details,
            }
            # Append JSONL stream
            os.makedirs(os.path.dirname(cls.STREAM_LOG_FILE), exist_ok=True)
            with open(cls.STREAM_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")

            # Append human-readable audit trail
            os.makedirs(os.path.dirname(cls.AUDIT_LOG_FILE), exist_ok=True)
            with open(cls.AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{now_iso}] [{event_type}] Domain: {active_domain} | Status: {details.get('status', 'OK')}\n")
        except Exception:
            # Non-blocking: logging failure must never abort execution
            pass

    @classmethod
    def transform_output(cls, output_text: str, exit_code: int = 0, max_lines: int = 35) -> str:
        """
        Layer 3 Context Steering & Reshaping (Stripe Positive Injection & Deep Agents Summarization):
        Truncates verbose stdout/stderr beyond max_lines, preserving head and tail lines.
        Injects positive diagnostic guidance on failure to break ungrounded retry loops.
        """
        lines = output_text.splitlines()
        transformed = output_text

        # 1. Truncate if exceeding max_lines
        if len(lines) > max_lines:
            head = lines[:5]
            tail = lines[-30:]
            skipped = len(lines) - 35
            transformed = (
                "\n".join(head)
                + f"\n\n[... TRUNCATED {skipped} LINES OF VERBOSE HARNESS LOGS ...]\n\n"
                + "\n".join(tail)
            )

        # 2. Positive error prompt injection if exit_code != 0
        if exit_code != 0:
            diagnosis = "Execution command terminated with non-zero exit code."
            action = "Inspect error stack trace and resolve missing symbols or configuration."

            lower_text = output_text.lower()
            if "syntaxerror" in lower_text:
                diagnosis = "Source code contains an invalid syntax token or unclosed delimiter."
                action = "Run AST parse check or linter to pinpoint line number before re-executing."
            elif "modulenotfounderror" in lower_text or "cannot find module" in lower_text:
                diagnosis = "Required module or dependency is not available in the active environment."
                action = "Check package.json or dependencies. Adhere to zero-ghost package invariant."
            elif "assertionerror" in lower_text or "failed" in lower_text:
                diagnosis = "Test assertion contract breached; actual output diverged from expected."
                action = "Inspect failing assertion and update business logic to satisfy contract."
            elif "memory" in lower_text or "ram" in lower_text:
                diagnosis = "Process exceeded physical memory allocation limits."
                action = "Implement chunking, stream processing, or scale profiling."

            guidance = (
                f"\n\n[HARNESS POSITIVE DIAGNOSTIC GUIDANCE]\n"
                f"- Execution Status : FAILED (Exit Code {exit_code})\n"
                f"- Diagnosis        : {diagnosis}\n"
                f"- Recommended Step : {action}\n"
                f"- Safety Invariant : Fail-closed contract enforced. Do not repeat failed invocation without remediation."
            )
            transformed += guidance

        return transformed

    # Research Trigger Heuristics for Autonomous Phase 0 Activation
    RESEARCH_TRIGGER_PATTERNS = [
        r"\b(?:arxiv|nature|cvpr|neurips|icml|iclr|doi\.org)\b",
        r"\b(?:sota|state[- ]of[- ]the[- ]art|benchmark|prior[- ]art|baseline)\b",
        r"\b(?:novel architecture|research paper|literature review)\b",
        r"\b(?:aquavplant|hmt[- ]net|farseg|mask2former|dinov2)\b",
    ]

    @classmethod
    def check_research_intent(cls, prompt: str) -> Dict[str, Any]:
        """
        Pre-Flight Research Interceptor (Phase 0 Trigger):
        Detects whether incoming prompt references specialized academic research,
        papers, or SOTA benchmarks, mandating live search tool dispatch before architectural synthesis.
        """
        matched = []
        for pat in cls.RESEARCH_TRIGGER_PATTERNS:
            matches = re.findall(pat, prompt, re.IGNORECASE)
            if matches:
                matched.extend([m.lower() for m in matches])

        requires_research = len(matched) > 0
        return {
            "requires_research": requires_research,
            "triggers_detected": list(set(matched)),
            "persona_to_activate": "Deep Research Specialist",
            "mandated_action": (
                "Execute search_web or python -m scripts.orchestrator.task_dispatcher --task research "
                "before formulating implementation plans."
                if requires_research
                else "Standard exploration permitted."
            ),
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
    def pre_invocation_memory_recall(cls, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Layer 6 Cognitive Memory Injection (Hermes Agent Vault Recall):
        Retrieves relevant architectural decisions and lessons learned prior to execution.
        """
        vault_db = os.path.join(WORKSPACE_ROOT, ".agents", "memory", "vault.sqlite")
        results = []
        if os.path.exists(vault_db):
            try:
                import sqlite3
                conn = sqlite3.connect(vault_db)
                c = conn.cursor()
                keywords = [k.strip() for k in query.split() if len(k.strip()) > 3]
                if keywords:
                    like_clauses = " OR ".join(["body LIKE ?" for _ in keywords[:3]])
                    sql = f"SELECT id, title, kind, body, file_path FROM memories WHERE {like_clauses} LIMIT ?"
                    params = [f"%{k}%" for k in keywords[:3]] + [limit]
                    c.execute(sql, params)
                    rows = c.fetchall()
                    for r in rows:
                        results.append({
                            "id": r[0],
                            "title": r[1],
                            "kind": r[2],
                            "body": r[3][:150] + "..." if len(r[3]) > 150 else r[3],
                            "file_path": r[4],
                        })
                conn.close()
            except Exception:
                pass
        return results

    @classmethod
    def verify_in_flight(
        cls,
        target_file: str,
        file_content: str,
        domain: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Layer 4 Verification Loop (DeepCode In-Flight Verification):
        Validates syntax, zero-raw-LaTeX invariants, and domain contracts before write commits.
        """
        active_domain, _ = cls.get_active_domain()
        if domain:
            active_domain = domain

        violations = []

        # 1. Python AST syntax validation
        if target_file.endswith(".py"):
            try:
                ast.parse(file_content)
            except SyntaxError as e:
                violations.append({
                    "type": "PYTHON_SYNTAX_ERROR",
                    "details": f"SyntaxError at line {e.lineno}: {e.msg}",
                })

        # 2. Zero-Raw-LaTeX Invariant validation
        if target_file.endswith((".md", ".txt", ".json")):
            latex_res = FormatGuard.scan_latex(file_content)
            if latex_res.get("violation"):
                violations.append({
                    "type": "RawLaTeXDelimiter",
                    "details": f"{latex_res.get('count')} raw LaTeX delimiter instances detected.",
                })

        # 3. Domain invariant validation
        domain_cfg = cls.DOMAIN_INVARIANTS.get(active_domain)
        if domain_cfg:
            for pattern in domain_cfg.get("forbidden_patterns", []):
                if re.search(pattern, file_content, re.IGNORECASE):
                    violations.append({
                        "type": "DomainInvariantBreach",
                        "pattern": pattern,
                        "guidance": domain_cfg.get("guidance", ""),
                    })

        passed = len(violations) == 0
        res = {
            "passed": passed,
            "target_file": target_file,
            "violations_count": len(violations),
            "violations": violations,
        }

        if not passed:
            # Layer 5: Self-Evolution Signal Recording
            first_v = violations[0]
            sig_res = EvolutionEngine.record_failure_signal(
                signature=f"in_flight:{target_file}:{first_v['type']}",
                category=first_v["type"],
                description=f"In-flight verification failed on {target_file}",
                remediation="Ensure syntax correctness and zero invariant violations before committing.",
                domain=active_domain,
                target_file=target_file,
            )
            if sig_res.get("staged"):
                res["staged_evolution_patch"] = sig_res.get("patch_id")
                res["operator_verification_request"] = sig_res.get("operator_notification")

        cls.emit_telemetry("IN_FLIGHT_VERIFY", res)
        return res

    @classmethod
    def pre_execute_gate(
        cls,
        command_line: str,
        target_file: Optional[str] = None,
        file_content: Optional[str] = None,
        item_count: Optional[int] = None,
        domain: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Active Pre-Execution Gate:
        Evaluates safety/governance (PERMIT, BLOCK, MODIFY, ESCALATE),
        deadline lockdown, scale profiler, large-batch memory limits, and domain invariants
        BEFORE any shell command or file write is executed.
        """
        active_domain, active_subs = cls.get_active_domain()
        if domain is not None:
            active_domain = domain

        # 1. Layer 1 Safety & Governance: Destructive Shell Command Gate (Operator Approval Escalation)
        for pattern, desc in cls.DESTRUCTIVE_COMMAND_PATTERNS:
            if re.search(pattern, command_line, re.IGNORECASE):
                is_approved = (
                    "--operator-approved" in command_line
                    or os.environ.get("OPERATOR_APPROVED") == "1"
                )
                if not is_approved:
                    escalate_res = {
                        "permitted": False,
                        "action": DecisionOutcome.ESCALATE.value,
                        "gate": "SafetyGovernance:DestructiveCommandGate",
                        "status": "REJECTED_REQUIRES_OPERATOR_APPROVAL",
                        "destructive_action": desc,
                        "command": command_line,
                        "reason": f"Destructive shell operation detected ({desc}). Mandates explicit operator approval prompt.",
                        "escalation_prompt": f"OPERATOR APPROVAL REQUIRED: Shell action '{command_line}' is destructive ({desc}). Confirm or append '--operator-approved'.",
                        "remediation_guidance": "Execute safe alternative (e.g. non-destructive inspection or dry-run) or request operator approval token.",
                    }
                    cls.emit_telemetry("ESCALATE_DESTRUCTIVE_COMMAND", escalate_res)
                    return escalate_res

        # 2. Scale Profiler & Heavy Batch Resource Guard (Only for large datasets / heavy compute jobs)
        is_large_batch = (
            (item_count is not None and item_count > 10000)
            or bool(re.search(r"(?:3\.8M|1M|100k|500k|large|pairwise|full_dataset)", command_line, re.IGNORECASE))
            or "--guard-memory" in command_line
        )

        if is_large_batch:
            # 2a. Scale Profiler check
            if "scale_profiler" not in command_line:
                block_res = {
                    "permitted": False,
                    "action": DecisionOutcome.BLOCK.value,
                    "gate": "ScaleProfiler",
                    "status": "REJECTED_UNPROFILED_LARGE_SCALE",
                    "reason": f"Execution operates on >10,000 items without mandatory 500-item micro-batch profiling.",
                    "remediation_guidance": "Run `python -m scripts.orchestrator.scale_profiler 500 <elapsed> <total>` before full execution.",
                }
                cls.emit_telemetry("PRE_EXECUTE_BLOCKED", block_res)
                return block_res

            # 2b. Memory Guard for heavy batch pipelines (prevents uncatchable kernel SIGKILL)
            mem_check = MemoryGuard.check_memory(max_pct=75.0)
            if not mem_check["within_budget"]:
                block_res = {
                    "permitted": False,
                    "action": DecisionOutcome.BLOCK.value,
                    "gate": "MemoryGuard",
                    "status": "REJECTED_MEMORY_BREACH",
                    "reason": (
                        f"Physical RAM allocation {mem_check['used_percent']}% exceeds 75% ceiling "
                        f"({mem_check['available_gb']} GB available). Large batch compute halted to prevent SIGKILL."
                    ),
                    "remediation_guidance": "Chunk in-memory data, stream via Polars/generator, or free unused references.",
                }
                # Record Layer 5 failure signal for critical memory breach
                sig_res = EvolutionEngine.record_failure_signal(
                    signature=f"MemoryGuard:CeilingBreach:{mem_check['used_percent']}",
                    category="HardwareRAMBreach",
                    description=f"RAM allocation {mem_check['used_percent']}% exceeded 75% ceiling",
                    remediation="Stream via Polars or generator.",
                    domain=active_domain,
                )
                if sig_res.get("staged"):
                    block_res["staged_evolution_patch"] = sig_res.get("patch_id")
                    block_res["operator_verification_request"] = sig_res.get("operator_notification")

                cls.emit_telemetry("PRE_EXECUTE_BLOCKED", block_res)
                return block_res

        # 3. Deadline Lockdown (Universal Gate)
        lock_check = DeadlineLockdown.validate_action(command_line)
        if not lock_check["permitted"]:
            block_res = {
                "permitted": False,
                "action": DecisionOutcome.BLOCK.value,
                "gate": "DeadlineLockdown",
                "status": "REJECTED_T4H_LOCKDOWN",
                "reason": lock_check["reason"],
                "remediation_guidance": "Switch strictly to submission packaging, schema linting, and smoke testing.",
            }
            cls.emit_telemetry("PRE_EXECUTE_BLOCKED", block_res)
            return block_res

        # 4. Domain-Specific Invariant Checks
        domain_cfg = cls.DOMAIN_INVARIANTS.get(active_domain)
        if domain_cfg and file_content:
            for pattern in domain_cfg.get("forbidden_patterns", []):
                if re.search(pattern, file_content, re.IGNORECASE):
                    # Record failure signal in Layer 5 Continual Evolution Engine
                    sig_res = EvolutionEngine.record_failure_signal(
                        signature=f"{active_domain}:{pattern}",
                        category="DomainInvariantBreach",
                        description=f"Code violates domain invariant pattern: {pattern}",
                        remediation=domain_cfg.get("guidance", "Adhere to domain security specifications."),
                        domain=active_domain,
                        target_file=target_file,
                    )
                    block_res = {
                        "permitted": False,
                        "action": DecisionOutcome.BLOCK.value,
                        "gate": f"DomainGate:{active_domain}",
                        "status": "REJECTED_DOMAIN_INVARIANT_VIOLATION",
                        "reason": f"Code violates domain invariant pattern: {pattern}",
                        "remediation_guidance": domain_cfg.get("guidance", "Adhere to domain security specifications."),
                    }
                    if sig_res.get("staged"):
                        block_res["staged_evolution_patch"] = sig_res.get("patch_id")
                        block_res["operator_verification_request"] = sig_res.get("operator_notification")

                    cls.emit_telemetry("PRE_EXECUTE_BLOCKED", block_res)
                    return block_res

        # Resolve matching skills automatically
        skills_info = SkillResolver.resolve_skills(command_line, domain_id=active_domain, subdomains=active_subs)

        permit_res = {
            "permitted": True,
            "action": DecisionOutcome.PERMIT.value,
            "domain": active_domain,
            "subdomains": active_subs,
            "activated_skills": skills_info.get("activated_skills", []),
            "status": "APPROVED",
        }
        cls.emit_telemetry("PRE_EXECUTE_PERMITTED", permit_res)
        return permit_res

    @classmethod
    def post_execute_gate(
        cls,
        output_text: str,
        executed_commands: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Active Post-Execution Gate:
        Evaluates Fact-Forcing (GateGuard), Personas & Receipt Validity (FormatGuard),
        Zero-Raw-LaTeX Invariant, and Skill Attestation.
        """
        # 1. Fact-Forcing GateGuard Check
        gate_res = GateGuard.audit_text(output_text, executed_commands=executed_commands)
        if not gate_res["passed"]:
            fail_res = {
                "passed": False,
                "gate": "GateGuard",
                "status": "REJECTED_UNGROUNDED_ASSERTION",
                "violations": gate_res.get("violations", []),
                "remediation_guidance": "Physically inspect raw files or execute real tests before asserting metrics.",
            }
            # Record Layer 5 failure signal
            sig_res = EvolutionEngine.record_failure_signal(
                signature="GateGuard:UngroundedClaim",
                category="UngroundedAssertion",
                description="GateGuard flagged assertion made without executed command evidence.",
                remediation="Execute empirical commands before asserting test passes or performance numbers.",
                domain="general",
            )
            if sig_res.get("staged"):
                fail_res["staged_evolution_patch"] = sig_res.get("patch_id")
                fail_res["operator_verification_request"] = sig_res.get("operator_notification")

            cls.emit_telemetry("POST_EXECUTE_REJECTED", fail_res)
            return fail_res

        # 2. FormatGuard 6-Persona and Attestation Check
        format_res = FormatGuard.audit_response(output_text)
        if not format_res["passed"]:
            fail_res = {
                "passed": False,
                "gate": "FormatGuard",
                "status": "REJECTED_FORMAT_VIOLATION",
                "details": format_res,
                "remediation_guidance": "Include all 6 personas and valid squad_execution_attestation YAML receipt.",
            }
            # Detect whether failure was due to raw LaTeX or missing personas
            has_latex = format_res.get("latex_audit", {}).get("violation", False)
            sig_res = EvolutionEngine.record_failure_signal(
                signature="FormatGuard:RawLaTeX" if has_latex else "FormatGuard:MissingPersonas",
                category="RawLaTeXDelimiter" if has_latex else "FormatViolation",
                description="FormatGuard audit rejected output format.",
                remediation="Enforce clean Unicode typography and 6-persona execution hierarchy.",
                domain="general",
            )
            if sig_res.get("staged"):
                fail_res["staged_evolution_patch"] = sig_res.get("patch_id")
                fail_res["operator_verification_request"] = sig_res.get("operator_notification")

            cls.emit_telemetry("POST_EXECUTE_REJECTED", fail_res)
            return fail_res

        pass_res = {
            "passed": True,
            "status": "POST_EXECUTION_VERIFIED",
            "skills_count": format_res.get("attestation_audit", {}).get("skills_count", 0),
        }
        cls.emit_telemetry("POST_EXECUTE_VERIFIED", pass_res)
        return pass_res


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
            "harness_pillars": [
                "Layer 1: Safety & Governance (Microsoft Join Points: PERMIT, BLOCK, MODIFY, ESCALATE)",
                "Layer 2: Telemetry & Observability (AWS Dogwood Runtime Verification)",
                "Layer 3: Context Steering & Output Reshaping (Stripe Positive Injection)",
                "Layer 4: In-Flight Verification Loop (DeepCode AST and Invariant Checks)",
                "Layer 5: Continual Self-Evolution (Trajectory Diffing & Staged Patches)",
                "Layer 6: Cognitive Memory Recall (Hermes Agent SQLite Vault Injection)",
                "Layer 7: Multi-Agent Personas & Domain Contracts (Omnigent 6+1 Squad)",
            ],
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
    elif arg == "--transform" and len(sys.argv) > 2:
        sample = sys.argv[2]
        res = ActiveKernel.transform_output(sample, exit_code=1)
        print(res)
        sys.exit(0)
    elif arg == "--research-check" and len(sys.argv) > 2:
        prompt_str = " ".join(sys.argv[2:])
        res = ActiveKernel.check_research_intent(prompt_str)
        print(json.dumps(res, indent=2))
        sys.exit(0)


if __name__ == "__main__":
    main()
