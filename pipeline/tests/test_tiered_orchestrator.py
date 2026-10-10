"""
Automated Comprehensive Test Suite for Tiered 10+1 Architecture
Covers:
- Tier A: 9 Core Universal Modules (INV-01, INV-02, INV-03, INV-04, INV-05, INV-07, INV-10, INV-11, INV-12)
- Tier B: Generalized Pipeline Gate (INV-06, INV-09)
- Tier C: AI/ML Domain Plugin (INV-08)
"""

import os
import sys
import json
import time
import pytest
from datetime import datetime, timezone, timedelta

# Ensure workspace root is in python path
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from scripts.orchestrator.format_guard import FormatGuard
from scripts.orchestrator.squad_attestation import SquadAttestor
from scripts.orchestrator.gate_guard import GateGuard
from scripts.orchestrator.scale_profiler import ScaleProfiler
from scripts.orchestrator.contrarian_auditor import ContrarianAuditor
from scripts.orchestrator.dag_runner import DAGRunner
from scripts.orchestrator.memory_guard import MemoryGuard, enforce_memory_limit, MemoryBudgetExceededException
from scripts.orchestrator.deadline_lockdown import DeadlineLockdown
from scripts.orchestrator.prompt_hygiene import PromptHygieneEngine
from scripts.orchestrator.pipeline_gate import PipelineGate
from scripts.orchestrator.calibration_auditor import CalibrationAuditor


# ==============================================================================
# Tier A: Module 1 & 2 Tests (FormatGuard & SquadAttestor - INV-11, INV-12)
# ==============================================================================

def test_format_guard_personas_detection():
    complete_text = """
    [Product Manager] Scope defined.
    [System Architect] Contract verified.
    [Adversarial SDET] Tests written first.
    [Core Engineer] Business logic implemented.
    [Mutation & Security Auditor] Zero secrets verified.
    [Technical Writer] Docs synchronized.
    """
    res = FormatGuard.validate_personas(complete_text)
    assert res["all_present"] is True
    assert res["found_count"] == 6

    incomplete_text = """
    [Product Manager] Scope defined.
    [Core Engineer] Code written.
    """
    res_inc = FormatGuard.validate_personas(incomplete_text)
    assert res_inc["all_present"] is False
    assert "System Architect" in res_inc["missing_personas"]
    assert "Adversarial SDET" in res_inc["missing_personas"]


def test_format_guard_sycophancy_scanner():
    clean_text = "Empirical benchmark measured 1,200 qps on 500-sample test."
    res_clean = FormatGuard.scan_sycophancy(clean_text, executed_commands_count=1)
    assert res_clean["violation"] is False

    sycophantic_text = "This solution is mathematically guaranteed to achieve 100% win with zero risk."
    res_bad = FormatGuard.scan_sycophancy(sycophantic_text, executed_commands_count=0)
    assert res_bad["violation"] is True
    assert len(res_bad["flagged_phrases"]) > 0


def test_format_guard_latex_scanner():
    # 1. Prohibited block LaTeX
    bad_block = "The joint loss is $$L_{total} = L_{focal} + 0.5 L_{dice}$$ across batches."
    res_block = FormatGuard.scan_latex(bad_block)
    assert res_block["violation"] is True
    assert any(v["type"] == "RAW_LATEX_BLOCK" for v in res_block["violations"])

    # 2. Prohibited inline LaTeX
    bad_inline = "Weights are calculated with $\\beta = 0.9999$ for effective samples."
    res_inline = FormatGuard.scan_latex(bad_inline)
    assert res_inline["violation"] is True
    assert any(v["type"] == "RAW_LATEX_INLINE" for v in res_inline["violations"])

    # 3. Prohibited LaTeX commands
    bad_cmd = "Using \\mathcal{L} and \\frac{1}{2} in prose."
    res_cmd = FormatGuard.scan_latex(bad_cmd)
    assert res_cmd["violation"] is True

    # 4. Valid clean Unicode math
    clean_unicode = "The joint loss is L_total = L_CB-Focal + 0.5 × L_SoftDice, where β = 0.9999 and WCAER ≤ 15.0%."
    res_clean = FormatGuard.scan_latex(clean_unicode)
    assert res_clean["violation"] is False
    assert len(res_clean["violations"]) == 0

    # 5. Currency must NOT be flagged
    currency_text = "Instance costs $0.736 per hour, total cost is $50 to $100."
    res_curr = FormatGuard.scan_latex(currency_text)
    assert res_curr["violation"] is False

    # 6. Fenced code blocks containing LaTeX/math must NOT be flagged
    code_block = "Here is an example:\n```latex\n\\mathcal{L} = \\frac{1}{2}\n```\n"
    res_code = FormatGuard.scan_latex(code_block)
    assert res_code["violation"] is False


def test_squad_attestation_lifecycle(tmp_path):
    receipt = SquadAttestor.record_attestation(
        prompt="Test prompt for tiered architecture verification",
        active_personas=["Product Manager", "Core Engineer"],
        executed_commands=[{"cmd": "pytest tests/", "exit_code": 0}],
        git_head="test_commit_sha"
    )
    assert "provenance_hash" in receipt
    assert len(receipt["provenance_hash"]) == 64
    assert receipt["commands_count"] == 1

    # Verify retrieval
    verified = SquadAttestor.verify_attestation(receipt["provenance_hash"])
    assert verified["verified"] is True
    assert verified["data"]["prompt"] == "Test prompt for tiered architecture verification"


# ==============================================================================
# Tier A: Module 3 Tests (GateGuard - INV-01)
# ==============================================================================

def test_gate_guard_empirical_claim_extraction():
    text = "Our pipeline achieves 94.4% match rate and processes 3.8M records with 0 nulls."
    claims = GateGuard.extract_empirical_claims(text)
    assert len(claims) >= 3
    claim_types = [c["claim_type"] for c in claims]
    assert any("Percentage" in ct for ct in claim_types)
    assert any("Dataset scale" in ct for ct in claim_types)
    assert any("Zero-fault" in ct for ct in claim_types)


def test_gate_guard_rejection_without_evidence():
    text = "We observe 80% singletons across the entire corpus."
    # With no command evidence
    res = GateGuard.check_execution_evidence(GateGuard.extract_empirical_claims(text), executed_commands=[])
    assert res["passed"] is False
    assert len(res["violations"]) > 0

    # With command evidence
    res_valid = GateGuard.check_execution_evidence(
        GateGuard.extract_empirical_claims(text),
        executed_commands=["python -m scripts.check_singletons --corpus data/raw.csv"]
    )
    assert res_valid["passed"] is True
    assert len(res_valid["violations"]) == 0


# ==============================================================================
# Tier A: Module 4 Tests (ScaleProfiler - INV-02)
# ==============================================================================

def test_scale_profiler_micro_benchmark():
    def dummy_processor(items):
        time.sleep(0.01)
        return len(items)

    sample = list(range(500))
    res = ScaleProfiler.benchmark_callable(dummy_processor, sample, total_dataset_size=10000, max_allowed_hours=1.0)
    assert res["batch_size"] == 500
    assert res["throughput_items_per_sec"] > 0
    assert res["within_budget"] is True
    assert res["status"] == "APPROVED"


def test_scale_profiler_quadratic_complexity_detection():
    # Simulate quadratic explosion: 100 items -> 0.01s, 200 items -> 0.04s (2x size = 4x time)
    res = ScaleProfiler.estimate_complexity(
        batch_sizes=[100, 200],
        elapsed_times=[0.01, 0.04],
        total_dataset_size=1_000_000,
        max_allowed_hours=0.5
    )
    assert res["estimated_exponent_alpha"] >= 1.8
    assert "Quadratic Explosion" in res["complexity_class"]
    assert res["status"] == "REJECTED_SCALE_BOTTLENECK"


# ==============================================================================
# Tier A: Module 5 Tests (ContrarianAuditor - INV-03)
# ==============================================================================

def test_contrarian_auditor_skepticism_trigger():
    assert ContrarianAuditor.is_skepticism_prompt("Are you sure this pipeline will work?") is True
    assert ContrarianAuditor.is_skepticism_prompt("Review our harness and prove it is not just a readme") is True
    assert ContrarianAuditor.is_skepticism_prompt("What is the guarantee against OOM?") is True
    assert ContrarianAuditor.is_skepticism_prompt("Create an auth component for login") is False


def test_contrarian_falsification_template_generation():
    template = ContrarianAuditor.generate_falsification_template("Entity Resolution Cascade")
    assert "top_3_breaking_points" in template
    assert len(template["top_3_breaking_points"]) == 3
    assert "distribution_drift_sensitivity" in template
    assert "empirical_confidence_bounds" in template


# ==============================================================================
# Tier A: Module 6 Tests (DAGRunner - INV-04)
# ==============================================================================

def test_dag_runner_idempotent_caching(tmp_path):
    stage_file = tmp_path / "stage_test.py"
    output_file = tmp_path / "output.txt"
    stage_file.write_text(f"""
with open(r"{output_file}", "w") as f:
    f.write("stage 1 complete")
""")

    stage_def = {
        "name": "test_stage_1",
        "script": str(stage_file),
        "inputs": [],
        "outputs": [str(output_file)],
        "params": {"batch": 100}
    }

    # First run: should execute successfully
    res1 = DAGRunner.run_stage(stage_def, force=True)
    assert res1["status"] == "SUCCESS"
    assert output_file.exists()

    # Second run without force: should hit CACHED_SKIP
    res2 = DAGRunner.run_stage(stage_def, force=False)
    assert res2["status"] == "CACHED_SKIP"


# ==============================================================================
# Tier A: Module 7 Tests (MemoryGuard - INV-05)
# ==============================================================================

def test_memory_guard_system_detection():
    info = MemoryGuard.get_system_memory_info()
    assert info["total_gb"] > 0
    assert info["available_gb"] >= 0
    assert 0.0 <= info["used_percent"] <= 100.0

    verdict = MemoryGuard.check_memory(max_pct=99.9)
    assert verdict["within_budget"] is True


def test_memory_guard_exception_on_low_ceiling():
    # Forcing max_pct=0.001 to simulate breach
    with pytest.raises(MemoryBudgetExceededException):
        @enforce_memory_limit(max_pct=0.001)
        def heavy_function():
            return "should fail"
        heavy_function()


# ==============================================================================
# Tier A: Module 8 Tests (DeadlineLockdown - INV-07)
# ==============================================================================

def test_deadline_lockdown_modes():
    # Set future deadline 10 hours away
    far_future = (datetime.now(timezone.utc) + timedelta(hours=10)).isoformat()
    status_far = DeadlineLockdown.set_deadline(far_future, lockdown_hours=4.0)
    assert status_far["status"] == "NORMAL_EXPLORATION"

    # Action check during normal exploration
    assert DeadlineLockdown.validate_action("train_new_model")["permitted"] is True

    # Set imminent deadline 2 hours away (< 4h)
    imminent = (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()
    status_imm = DeadlineLockdown.set_deadline(imminent, lockdown_hours=4.0)
    assert status_imm["status"] == "SAFE_SUBMISSION_LOCKDOWN"

    # Prohibited action during lockdown
    val_proh = DeadlineLockdown.validate_action("train_new_model")
    assert val_proh["permitted"] is False

    # Permitted action during lockdown
    val_perm = DeadlineLockdown.validate_action("generate_submission")
    assert val_perm["permitted"] is True


# ==============================================================================
# Tier A: Module 9 Tests (PromptHygieneEngine - INV-10)
# ==============================================================================

def test_prompt_hygiene_assembly():
    res = PromptHygieneEngine.assemble_compact_prompt(domain="ai_ml")
    assert res["category"] == "ai_ml"
    assert "Enterprise Autonomous Agentic Core Kernel" in res["prompt_text"]
    assert "Asymptotic Scale Profiler" in res["prompt_text"]
    # Check compression: compact prompt should be <= 6000 characters
    assert res["char_count"] < 6000
    assert res["compression_ratio_vs_25kb"] >= 4.0


# ==============================================================================
# Tier B: Module 10 Tests (PipelineGate - Tier B: INV-06, INV-09)
# ==============================================================================

def test_pipeline_gate_upstream_recall():
    # If candidate recall is 0.933 and target is 0.990 (required >= 1.0 or 0.99 + 0.05 = 1.04 capped at 1.0)
    res_fail = PipelineGate.evaluate_upstream_recall(upstream_recall=0.933, target_score=0.990)
    assert res_fail["gate_passed"] is False
    assert res_fail["status"] == "GATE_REJECTED_INSUFFICIENT_UPSTREAM_RECALL"

    # If candidate recall is 0.995 and target is 0.920 (required >= 0.970)
    res_pass = PipelineGate.evaluate_upstream_recall(upstream_recall=0.995, target_score=0.920)
    assert res_pass["gate_passed"] is True
    assert res_pass["status"] == "APPROVED"


def test_pipeline_gate_distractor_parity():
    # Production: 100,000 negatives to 1,000 positives (100:1 ratio)
    # Validation toy: 50 negatives to 100 positives (0.5:1 ratio) -> Should fail
    res_toy = PipelineGate.evaluate_distractor_parity(
        val_negatives=50, val_positives=100,
        prod_negatives=100000, prod_positives=1000
    )
    assert res_toy["parity_passed"] is False
    assert res_toy["status"] == "TOY_MIRAGE_DETECTED"

    # Validation parity: 9,000 negatives to 100 positives (90:1 ratio vs 100:1) -> Within 35% tolerance
    res_valid = PipelineGate.evaluate_distractor_parity(
        val_negatives=9000, val_positives=100,
        prod_negatives=100000, prod_positives=1000
    )
    assert res_valid["parity_passed"] is True
    assert res_valid["status"] == "APPROVED"


# ==============================================================================
# Tier C: Module 11 Tests (CalibrationAuditor - Tier C: INV-08)
# ==============================================================================

def test_calibration_auditor_ece_and_brier():
    # Perfectly calibrated synthetic data
    probs = [0.1] * 90 + [0.9] * 10
    labels = [0] * 81 + [1] * 9 + [0] * 1 + [1] * 9
    res = CalibrationAuditor.calculate_ece(probs, labels, num_bins=5)
    assert "expected_calibration_error" in res
    assert "brier_score" in res
    assert res["expected_calibration_error"] < 0.15
    assert res["is_well_calibrated"] is True
    assert res["status"] == "APPROVED"

    # Distorted probabilities: high confidence (0.95) but all labels are 0
    distorted_probs = [0.95] * 50
    distorted_labels = [0] * 50
    res_bad = CalibrationAuditor.calculate_ece(distorted_probs, distorted_labels, num_bins=5)
    assert res_bad["expected_calibration_error"] > 0.50
    assert res_bad["is_well_calibrated"] is False
    assert res_bad["status"] == "DISTORTED_PROBABILITIES_DETECTED"


# ==============================================================================
# Automatic Skill Resolution & Active Interception Kernel Tests
# ==============================================================================

import importlib.util
from scripts.orchestrator.skill_resolver import SkillResolver

_harness_kernel_path = os.path.join(WORKSPACE_ROOT, ".agents", "harness", "active_kernel.py")
_spec = importlib.util.spec_from_file_location("active_kernel", _harness_kernel_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
ActiveKernel = _mod.ActiveKernel


def test_skill_resolver_resolution():
    res = SkillResolver.resolve_skills("build high performance api with redis", domain_id="software", subdomains=["backend_systems"])
    assert res["domain"] == "software"
    assert "backend_systems" in res["subdomains"]
    assert res["resolved_count"] > 0
    assert len(res["activated_skills"]) > 0

    # Ensure every returned skill physically exists on disk
    for s in res["activated_skills"]:
        assert os.path.exists(s["path"])
        assert s["path"].endswith("SKILL.md")
        assert "match_reason" in s


def test_active_kernel_pre_and_post_gates():
    # Reset deadline to far future so normal exploration is active
    far_future = (datetime.now(timezone.utc) + timedelta(hours=10)).isoformat()
    DeadlineLockdown.set_deadline(far_future, lockdown_hours=4.0)

    # 1. Test large dataset unprofiled rejection
    res_large = ActiveKernel.pre_execute_gate("python match.py --dataset 3.8M_full_dataset")
    assert res_large["permitted"] is False
    assert res_large["gate"] == "ScaleProfiler"
    assert "remediation_guidance" in res_large

    # 2. Test domain invariant code violation
    violation_code = 'msg.sender.call{value: 100}(""); balances[msg.sender] = 0;'
    res_domain = ActiveKernel.pre_execute_gate("execute_swap", file_content=violation_code, domain="blockchain")
    # Active domain is blockchain
    assert res_domain["permitted"] is False
    assert "DomainGate" in res_domain["gate"]
    assert "remediation_guidance" in res_domain

    # 3. Test permitted execution with automatic skill resolution
    res_ok = ActiveKernel.pre_execute_gate("echo test")
    # If not in lockdown or if action is allowed
    assert "activated_skills" in res_ok


def test_active_kernel_destructive_command_escalation():
    """Asserts that destructive shell commands mandate operator approval (ESCALATE)."""
    # 1. rm -rf
    res_rm = ActiveKernel.pre_execute_gate("rm -rf /var/data/models")
    assert res_rm["permitted"] is False
    assert res_rm["action"] == "ESCALATE"
    assert res_rm["status"] == "REJECTED_REQUIRES_OPERATOR_APPROVAL"
    assert "destructive_action" in res_rm
    assert "escalation_prompt" in res_rm

    # 2. DROP TABLE
    res_drop = ActiveKernel.pre_execute_gate("psql -c 'DROP TABLE production_users;'")
    assert res_drop["permitted"] is False
    assert res_drop["action"] == "ESCALATE"
    assert res_drop["status"] == "REJECTED_REQUIRES_OPERATOR_APPROVAL"

    # 3. terraform destroy
    res_tf = ActiveKernel.pre_execute_gate("terraform destroy --auto-approve")
    assert res_tf["permitted"] is False
    assert res_tf["action"] == "ESCALATE"

    # 4. Explicit operator approval bypasses escalation
    res_approved = ActiveKernel.pre_execute_gate("rm -rf /var/data/models --operator-approved")
    assert res_approved["permitted"] is True
    assert res_approved["action"] == "PERMIT"
    assert res_approved["status"] == "APPROVED"


def test_active_kernel_output_transformation_and_diagnostic_guidance():
    """Asserts Layer 3 Context Steering truncates verbose logs and injects positive hints."""
    # 1. Output truncation on > 35 lines
    long_output = "\n".join([f"Processing log chunk #{i}..." for i in range(60)])
    transformed = ActiveKernel.transform_output(long_output, exit_code=0, max_lines=35)
    assert "[... TRUNCATED" in transformed
    assert "LINES OF VERBOSE HARNESS LOGS ...]" in transformed
    assert "Processing log chunk #0..." in transformed
    assert "Processing log chunk #59..." in transformed

    # 2. Positive prompt injection on non-zero exit code
    failing_output = "ModuleNotFoundError: No module named 'scipy'"
    with_hints = ActiveKernel.transform_output(failing_output, exit_code=1)
    assert "[HARNESS POSITIVE DIAGNOSTIC GUIDANCE]" in with_hints
    assert "FAILED (Exit Code 1)" in with_hints
    assert "zero-ghost package invariant" in with_hints


def test_active_kernel_in_flight_verification():
    """Asserts Layer 4 DeepCode In-Flight Verification."""
    # 1. Python syntax error detection
    bad_py = "def broken_func(\n    return 42"
    res_py = ActiveKernel.verify_in_flight("test_script.py", bad_py)
    assert res_py["passed"] is False
    assert res_py["violations_count"] > 0
    assert res_py["violations"][0]["type"] == "PYTHON_SYNTAX_ERROR"

    # 2. Clean Python syntax passes
    clean_py = "def clean_func():\n    return 42\n"
    res_clean = ActiveKernel.verify_in_flight("clean_script.py", clean_py)
    assert res_clean["passed"] is True

    # 3. Raw LaTeX delimiter detection in markdown
    bad_md = r"The loss function is $$\mathcal{L}_{total}$$."
    res_md = ActiveKernel.verify_in_flight("design_doc.md", bad_md)
    assert res_md["passed"] is False
    assert any(v["type"] == "RawLaTeXDelimiter" for v in res_md["violations"])


def test_continual_evolution_staging_and_operator_notification():
    """Asserts Layer 5 Continual Evolution recurrence gating and staged patch creation."""
    from scripts.orchestrator.continual_evolution import EvolutionEngine

    test_sig = f"test_sig_{int(time.time())}"
    
    # First occurrence of non-critical signal: should NOT stage immediately
    res1 = EvolutionEngine.record_failure_signal(
        signature=test_sig,
        category="NonCriticalFlake",
        description="Minor transient latency spike",
        remediation="Optimize query",
        domain="ai_ml",
    )
    assert res1["occurrences"] == 1
    assert res1["staged"] is False

    # Second occurrence: meets recurrence threshold (count >= 2) -> STAGES patch
    res2 = EvolutionEngine.record_failure_signal(
        signature=test_sig,
        category="NonCriticalFlake",
        description="Minor transient latency spike",
        remediation="Optimize query",
        domain="ai_ml",
    )
    assert res2["occurrences"] == 2
    assert res2["staged"] is True
    assert "patch_id" in res2
    assert "operator_notification" in res2
    assert "AUTOMATED STAGED EVOLUTION VERIFICATION REQUEST" in res2["operator_notification"]

    # Reject/Dismiss patch
    dismiss_res = EvolutionEngine.reject_patch(res2["patch_id"], reason="Test assertion cleanup")
    assert dismiss_res["success"] is True
    assert dismiss_res["status"] == "DISMISSED"


def test_active_kernel_research_intent_check():
    """Asserts Pre-Flight Research Interceptor triggers on specialized literature/benchmarks."""
    # 1. Triggers detected
    res_trigger = ActiveKernel.check_research_intent("Review SOTA papers on CVPR and Nature for AqUavplant benchmark")
    assert res_trigger["requires_research"] is True
    assert res_trigger["persona_to_activate"] == "Deep Research Specialist"
    assert "cvpr" in res_trigger["triggers_detected"]
    assert "aquavplant" in res_trigger["triggers_detected"]

    # 2. Ordinary execution prompt does not trigger
    res_normal = ActiveKernel.check_research_intent("format this string and print to stdout")
    assert res_normal["requires_research"] is False

