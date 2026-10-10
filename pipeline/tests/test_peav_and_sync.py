"""
Unit Tests for PlanExecutionVerifier (PEAV) and SpecSync
Validates Layer 2 of the 3-Dimensional Anti-Hallucination Shield.
"""

import os
import sys
import json
import unittest
import shutil

from scripts.orchestrator.plan_execution_verifier import PlanExecutionVerifier
from scripts.orchestrator.spec_sync import SpecSync


class TestPEAVAndSync(unittest.TestCase):
    def setUp(self):
        self.test_dir = "pipeline/specs/test_peav_artifacts" if os.path.exists("pipeline/specs") else "specs/test_peav_artifacts"
        os.makedirs(self.test_dir, exist_ok=True)

        self.spec_file = os.path.join(self.test_dir, "test_spec.json")
        self.contract_file = os.path.join(self.test_dir, "test_contract.json")
        self.impl_file = os.path.join(self.test_dir, "test_impl.py")
        self.test_file = os.path.join(self.test_dir, "test_suite.py")

        with open(self.spec_file, "w", encoding="utf-8") as f:
            json.dump({
                "feature_name": "vault_guard",
                "forbidden_states": ["Download certificate when uncertified"]
            }, f)

        with open(self.contract_file, "w", encoding="utf-8") as f:
            json.dump({
                "fsm_states": ["IDLE", "RUNNING", "COMPLETED", "CERTIFIED"]
            }, f)

        self.doc_artifacts = []

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)
        for p in getattr(self, "doc_artifacts", []):
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass

    def test_peav_catches_omission_defects(self):
        """Verifies PEAV rejects code missing required FSM states."""
        with open(self.impl_file, "w", encoding="utf-8") as f:
            f.write("""
class VaultGuard:
    def __init__(self):
        self.state = "IDLE"
        raise PermissionError("Guard")
""")
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("import unittest\n")

        res = PlanExecutionVerifier.verify_feature_alignment(
            self.spec_file, self.contract_file, self.impl_file, self.test_file
        )
        self.assertFalse(res["passed"], "PEAV must reject code with omitted FSM states.")
        self.assertTrue(any("missing FSM states" in err for err in res["errors"]))

    def test_peav_catches_lazy_stubs(self):
        """Verifies PEAV rejects TODO or pass stubs in implementation."""
        with open(self.impl_file, "w", encoding="utf-8") as f:
            f.write("""
class VaultGuard:
    def __init__(self):
        self.state = "IDLE"
        self.state = "RUNNING"
        self.state = "COMPLETED"
        self.state = "CERTIFIED"
    def execute(self):
        raise PermissionError("Guarded")
        # TODO: implement real logic later
""")
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("import unittest\n")

        res = PlanExecutionVerifier.verify_feature_alignment(
            self.spec_file, self.contract_file, self.impl_file, self.test_file
        )
        self.assertFalse(res["passed"], "PEAV must reject code with TODO stubs.")
        self.assertTrue(any("TODO" in err for err in res["errors"]))

    def test_peav_accepts_clean_aligned_code(self):
        """Verifies PEAV passes when all states, defensive guards, and logic are complete."""
        with open(self.impl_file, "w", encoding="utf-8") as f:
            f.write("""
class VaultGuard:
    def __init__(self):
        self.state = "IDLE"
    def start(self):
        self.state = "RUNNING"
    def complete(self):
        self.state = "COMPLETED"
    def certify(self):
        if self.state != "COMPLETED":
            raise PermissionError("Cannot certify before complete")
        self.state = "CERTIFIED"
        return {"certified": True}
""")
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("""
import unittest
class TestVaultGuard(unittest.TestCase):
    def test_flow(self):
        pass
""")

        res = PlanExecutionVerifier.verify_feature_alignment(
            self.spec_file, self.contract_file, self.impl_file, self.test_file
        )
        self.assertTrue(res["passed"], "PEAV must pass clean aligned code.")
        self.assertEqual(res["alignment_score"], 100.0)

    def test_spec_sync_persists_in_repo_docs(self):
        """Verifies SpecSync creates in-repo markdown files in docs/plans and docs/walkthroughs."""
        plan_path = SpecSync.persist_plan("Audit Trail", "# Plan for Audit Trail\nDetails here.")
        self.assertTrue(os.path.exists(plan_path))
        self.assertIn("docs", plan_path)
        self.assertIn("plans", plan_path)

        walkthrough_path = SpecSync.persist_walkthrough("Audit Trail", "# Walkthrough for Audit Trail\nExecuted cleanly.")
        self.assertTrue(os.path.exists(walkthrough_path))
        self.assertIn("docs", walkthrough_path)
        self.assertIn("walkthroughs", walkthrough_path)
        self.doc_artifacts.extend([plan_path, walkthrough_path])

        # Verify index exists
        index_path = os.path.join(os.getcwd(), "docs", "plans", "INDEX.md")
        self.assertTrue(os.path.exists(index_path))


if __name__ == "__main__":
    unittest.main()
