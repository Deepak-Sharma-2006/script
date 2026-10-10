"""
Unit Tests for AutonomousPipelineHarness (Stage 1 to 5 Mechanical Gates)
"""

import os
import sys
import shutil
import unittest

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from scripts.harness.autonomous_pipeline_harness import (
    AutonomousPipelineHarness,
    TautologicalTestDefect,
    CircuitBreakerTriggered,
    MutationHardeningFailure
)


class TestAutonomousPipelineHarness(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(WORKSPACE_ROOT, "specs", "temp_harness_test")
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_file = os.path.join(self.test_dir, "test_sample_module.py")
        self.impl_file = os.path.join(self.test_dir, "sample_module.py")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_catches_tautological_test_defect(self):
        """Verifies that a test passing without business logic is rejected."""
        tautological_test = """
import unittest
class TestSample(unittest.TestCase):
    def test_always_passes(self):
        self.assertTrue(True)
if __name__ == "__main__":
    unittest.main()
"""
        with self.assertRaises(TautologicalTestDefect):
            AutonomousPipelineHarness.execute_bounded_pipeline(
                feature_name="tautology_probe",
                test_file_path=self.test_file,
                test_code=tautological_test,
                impl_file_path=self.impl_file,
                impl_code_generator=lambda it, err: "class Sample: pass",
                run_mutation=False
            )

    def test_circuit_breaker_rolls_back_on_3_failures(self):
        """Verifies that failing 3 passes triggers rollback and raises CircuitBreakerTriggered."""
        failing_test = f"""
import unittest
import sys
sys.path.insert(0, r"{self.test_dir}")
from sample_module import calculate_tax

class TestTax(unittest.TestCase):
    def test_tax(self):
        self.assertEqual(calculate_tax(100), 15)

if __name__ == "__main__":
    unittest.main()
"""
        def buggy_generator(it, err):
            return "def calculate_tax(amount): return 0"

        with self.assertRaises(CircuitBreakerTriggered):
            AutonomousPipelineHarness.execute_bounded_pipeline(
                feature_name="circuit_breaker_probe",
                test_file_path=self.test_file,
                test_code=failing_test,
                impl_file_path=self.impl_file,
                impl_code_generator=buggy_generator,
                run_mutation=False
            )

        # Assert rollback: implementation file should be removed (since it didn't exist prior)
        self.assertFalse(os.path.exists(self.impl_file), "Implementation file must be rolled back on 3 failures.")

    def test_successful_harness_loop_with_mutation(self):
        """Verifies full loop succeeds and passes mutation gate when implementation is correct."""
        valid_test = f"""
import unittest
import sys
sys.path.insert(0, r"{self.test_dir}")
from sample_module import is_eligible

class TestEligible(unittest.TestCase):
    def test_boundary_gt(self):
        self.assertIs(is_eligible(18), True)
        self.assertIs(is_eligible(25), True)
    def test_boundary_lt(self):
        self.assertIs(is_eligible(17), False)
        self.assertIs(is_eligible(0), False)


if __name__ == "__main__":
    unittest.main()
"""
        def working_generator(it, err):
            if it == 1:
                # Intentionally fail pass 1 to test self-healing
                return "def is_eligible(age): return False"
            else:
                # Fix pass 2
                return "def is_eligible(age): return age >= 18"

        receipt = AutonomousPipelineHarness.execute_bounded_pipeline(
            feature_name="eligibility_engine",
            test_file_path=self.test_file,
            test_code=valid_test,
            impl_file_path=self.impl_file,
            impl_code_generator=working_generator,
            run_mutation=True
        )

        self.assertEqual(receipt.status, "VERIFIED_CERTIFIED")
        self.assertTrue(receipt.stage_2_red_verified)
        self.assertTrue(receipt.stage_3_green_verified)
        self.assertGreaterEqual(receipt.stage_4_mutation_kill_rate, 80.0)
        self.assertEqual(receipt.iterations_used, 2)

    def test_stage_gated_physical_kernel_locking(self):
        """Verifies OS-level read-only kernel locking blocks unauthorized file writes physically."""
        from scripts.harness.filesystem_guard import FilesystemGuard

        # Create target test file
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("# Original test suite")

        # 1. Lock stage GREEN (test file should become read-only at OS level)
        FilesystemGuard.lock_stage("GREEN", test_path=self.test_file)

        try:
            # Writing to test file must fail with PermissionError at the OS level
            with self.assertRaises(PermissionError):
                with open(self.test_file, "w", encoding="utf-8") as f:
                    f.write("# Tampered test suite")
        finally:
            # 2. Unlock and verify write succeeds
            FilesystemGuard.unlock_stage("UNRESTRICTED", test_path=self.test_file)

        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("# Clean rewrite after unlock")

        with open(self.test_file, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "# Clean rewrite after unlock")

        # 3. Test logical permission evaluation rules
        allowed, _ = FilesystemGuard.evaluate_permission("tests/test_foo.py", "RED")
        self.assertTrue(allowed)
        blocked, _ = FilesystemGuard.evaluate_permission("src/foo.py", "RED")
        self.assertFalse(blocked)

        allowed_g, _ = FilesystemGuard.evaluate_permission("src/foo.py", "GREEN")
        self.assertTrue(allowed_g)
        blocked_g, _ = FilesystemGuard.evaluate_permission("tests/test_foo.py", "GREEN")
        self.assertFalse(blocked_g)


if __name__ == "__main__":
    unittest.main()
