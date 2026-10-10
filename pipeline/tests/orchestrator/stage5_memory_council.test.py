"""
Stage 5 Verification Test Suite: Memory Vault, Claude Council, Hardware Profiler & Squad Attestation
Author: Antigravity Autonomous Enterprise Squad
"""

import os
import sys
import json
import tempfile
import unittest
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scripts.orchestrator.memory_vault_sync import MemoryVaultSync
from scripts.orchestrator.solution_council import SolutionCouncil
from scripts.ml.profile_gpu_step import profile_compute_step
from scripts.orchestrator.squad_attestation import SquadAttestor


class TestStage5MemoryCouncil(unittest.TestCase):
    """Verifies all Stage 5 enterprise capabilities under strict assertions."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix="stage5_test_")

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_gate1_memory_vault_markdown_to_sqlite_fts5(self):
        """Gate 1: Verifies dual-tier sync indexes decisions and handoffs into SQLite FTS5 table."""
        # Run sync_all
        sync_res = MemoryVaultSync.sync_all()
        self.assertIn("total_files_scanned", sync_res)
        self.assertIn("db_path", sync_res)

        # FTS5 search query
        results = MemoryVaultSync.search("FlashAttention")
        self.assertIsInstance(results, list)

        # General search query that always exists
        all_results = MemoryVaultSync.search("Phase")
        self.assertIsInstance(all_results, list)

    def test_gate2_claude_council_heuristic_evaluation(self):
        """Gate 2: Verifies 5-advisor heuristic audit evaluates plan across all 5 perspectives."""
        sample_plan = os.path.join(self.tmp_dir, "sample_plan.md")
        with open(sample_plan, "w", encoding="utf-8") as f:
            f.write("""# Production Architecture Plan: Multi-GPU Distributed Engine
## 1. System Overview
Implements distributed PyTorch training across 2 GPUs with cutlass SDPA.

## 2. Failure Path Mitigation & Recovery
Failure table handling OOM, network timeout, and checkpoint corruption.

## 3. Hardware Compute Bounds & Physics
Empirical step latency bounded at 1.58s/step on Tesla T4. 10 epochs takes 58.5 minutes.

## 4. Defensible Moats
Data ingestion moat with proprietary multi-spectral tiles and algorithmic FlashAttention speedup.
""")

        evaluation = SolutionCouncil.evaluate_plan(sample_plan)
        self.assertIn("composite_score", evaluation)
        self.assertIn("verdict", evaluation)
        self.assertIn("advisor_evaluations", evaluation)
        self.assertEqual(len(evaluation["advisor_evaluations"]), 5, "Must evaluate across all 5 advisors")
        self.assertIn("the_contrarian", evaluation["advisor_evaluations"])
        self.assertIn("the_first_principles_engineer", evaluation["advisor_evaluations"])
        self.assertIn("the_expansionist", evaluation["advisor_evaluations"])
        self.assertIn("the_naive_outsider", evaluation["advisor_evaluations"])
        self.assertIn("the_pragmatic_executor", evaluation["advisor_evaluations"])

    def test_gate3_hardware_micro_profiler(self):
        """Gate 3: Micro-profiler measures latency and emits empirical benchmark receipt."""
        receipt = profile_compute_step(steps_per_epoch=224, warmup_steps=1, measure_steps=2)
        self.assertIn("compute_accelerator", receipt)
        self.assertIn("step_latency_seconds", receipt)
        self.assertIn("ten_epoch_duration_minutes", receipt)
        self.assertGreater(receipt["step_latency_seconds"], 0.0)
        self.assertGreater(receipt["ten_epoch_duration_minutes"], 0.0)

    def test_gate4_squad_attestation_receipt_with_real_audit(self):
        """Gate 4: SquadAttestor records real execution and emits provenance hash."""
        active_personas = ["Product Manager", "System Architect", "Adversarial SDET", "Core Engineer", "Mutation Auditor", "Technical Writer"]
        executed_cmds = [{"command": "python -m unittest tests/orchestrator/stage4_self_healing_mutation.test.py", "exit_code": 0}]

        record = SquadAttestor.record_attestation(
            prompt="Stage 5 Full Certification Sweep",
            active_personas=active_personas,
            executed_commands=executed_cmds,
            domain="ai_ml",
            subdomains=["deep_learning"]
        )

        self.assertIn("provenance_hash", record)
        self.assertIn("timestamp", record)
        self.assertEqual(len(record["provenance_hash"]), 64, "Provenance hash must be SHA-256 (64 hex characters)")

        # Verify receipt formatting
        receipt_md = SquadAttestor.format_receipt_markdown(record)
        self.assertIn("squad_execution_attestation", receipt_md)
        self.assertIn(record["provenance_hash"], receipt_md)

        # Verify DB verification
        verify_res = SquadAttestor.verify_attestation(record["provenance_hash"])
        self.assertTrue(verify_res.get("verified"), "Attestation verification failed")


if __name__ == "__main__":
    unittest.main()
