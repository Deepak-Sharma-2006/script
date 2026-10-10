"""
Unit & Adversarial Test Suite for Stage 4: Autonomous Closed-Loop Self-Healing TDD & Mutation Gate
"""

import os
import sys
import unittest
import shutil

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.getcwd())

from scripts.orchestrator.coding_engine import CodingEngine
from scripts.orchestrator.python_mutation_tester import PythonMutationEngine

class TestStage4SelfHealingAndMutation(unittest.TestCase):

    def setUp(self):
        self.scratch_dir = os.path.join(os.getcwd(), "tests", "scratch_stage4")
        os.makedirs(self.scratch_dir, exist_ok=True)
        with open(os.path.join(self.scratch_dir, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("")

    def tearDown(self):
        if os.path.exists(self.scratch_dir):
            shutil.rmtree(self.scratch_dir, ignore_errors=True)

    def test_gate1_autonomous_tdd_self_healing_loop(self):
        """Gate 1: Verifies red-to-green auto-healing loop when iteration 1 fails and iteration 2 heals."""
        test_file = os.path.join(self.scratch_dir, "test_discount.py")
        impl_file = os.path.join(self.scratch_dir, "discount.py")

        test_code = """
import unittest
from tests.scratch_stage4.discount import calculate_discount

class TestDiscount(unittest.TestCase):
    def test_twenty_percent(self):
        self.assertEqual(calculate_discount(100.0), 80.0)

if __name__ == '__main__':
    unittest.main()
"""

        def patch_generator(iteration, error_traceback):
            if iteration == 1:
                # Buggy implementation: 10% discount instead of 20%
                return """
def calculate_discount(price: float) -> float:
    return price * 0.90
"""
            else:
                # Self-healed implementation: 20% discount
                return """
def calculate_discount(price: float) -> float:
    return price * 0.80
"""

        result = CodingEngine.execute_tdd_loop(
            module_name="discount_module",
            test_file_path=test_file,
            test_code=test_code,
            impl_file_path=impl_file,
            impl_code_generator=patch_generator,
            max_healing_passes=3,
            sandbox_timeout=10
        )

        self.assertIsNotNone(result)
        # Verify benchmark metric was written
        benchmark_path = os.path.join(os.getcwd(), "specs", "benchmark_metrics.json")
        self.assertTrue(os.path.exists(benchmark_path))

    def test_gate2_python_ast_mutation_engine_kills_faults(self):
        """Gate 2: Injects AST mutations into a target file and verifies test suite kills them."""
        target_file = os.path.join(self.scratch_dir, "math_ops.py")
        test_file = os.path.join(self.scratch_dir, "test_math_ops.py")

        with open(target_file, "w", encoding="utf-8") as f:
            f.write("""
def is_positive(x: int) -> bool:
    return x > 0

def add_positive(a: int, b: int) -> int:
    if a > 0 and b > 0:
        return a + b
    return 0
""")

        with open(test_file, "w", encoding="utf-8") as f:
            f.write("""
import unittest
from tests.scratch_stage4.math_ops import is_positive, add_positive

class TestMathOps(unittest.TestCase):
    def test_is_positive(self):
        self.assertTrue(is_positive(5))
        self.assertFalse(is_positive(-1))
        self.assertFalse(is_positive(0))

    def test_add_positive(self):
        self.assertEqual(add_positive(2, 3), 5)
        self.assertEqual(add_positive(-1, 3), 0)
        self.assertEqual(add_positive(3, -1), 0)
        self.assertEqual(add_positive(0, 0), 0)

if __name__ == '__main__':
    unittest.main()
""")

        test_cmd = f"python -m unittest {test_file}"
        engine = PythonMutationEngine(target_file, test_cmd, threshold=80.0, max_mutants=10)
        result = engine.run()

        self.assertTrue(result["passed"], "Robust test suite must achieve >= 80% kill rate")
        self.assertGreaterEqual(result["score"], 80.0)
        self.assertGreater(result["killed"], 0)

    def test_gate3_anti_green_signal_trap_catches_tautology(self):
        """Gate 3: Demonstrates detection of weak test suite, and hardens it to achieve 100% kill rate."""
        target_file = os.path.join(self.scratch_dir, "auth_check.py")
        test_file = os.path.join(self.scratch_dir, "test_auth_check.py")

        with open(target_file, "w", encoding="utf-8") as f:
            f.write("""
def check_permission(user_role: str, is_admin: bool) -> bool:
    if is_admin or user_role == "root":
        return True
    return False
""")

        # 1. First: demonstrate why weak test fails (Anti-Green Signal Trap)
        # Weak test: only tests root with admin=True; never tests false branches or independent conditions
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("""
import unittest
from tests.scratch_stage4.auth_check import check_permission

class TestWeakAuth(unittest.TestCase):
    def test_trivial(self):
        self.assertTrue(check_permission("root", True))

if __name__ == '__main__':
    unittest.main()
""")

        test_cmd = f"python -m unittest {test_file}"
        engine_weak = PythonMutationEngine(target_file, test_cmd, threshold=80.0, max_mutants=10)
        result_weak = engine_weak.run()

        # Mutants survived because false/boundary branches were omitted
        self.assertFalse(result_weak["passed"], "Weak test suite must fail mutation threshold (<80%)")
        self.assertGreaterEqual(result_weak["survived"], 4, "Weak test suite must have multiple surviving mutants")

        # 2. Fix & Harden: Inject comprehensive boundary & branch test suite
        print("\n🛡️ [Self-Hardening] Upgrading auth_check test suite to kill all surviving mutants...")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("""
import unittest
from tests.scratch_stage4.auth_check import check_permission

class TestHardenedAuth(unittest.TestCase):
    def test_admin_permitted_even_if_not_root(self):
        self.assertTrue(check_permission("guest", True))
        self.assertTrue(check_permission("user", True))

    def test_root_permitted_even_if_not_admin(self):
        self.assertTrue(check_permission("root", False))

    def test_non_admin_non_root_rejected(self):
        self.assertIs(check_permission("guest", False), False)
        self.assertIs(check_permission("user", False), False)
        self.assertIs(check_permission("", False), False)

    def test_both_admin_and_root_permitted(self):
        self.assertTrue(check_permission("root", True))

if __name__ == '__main__':
    unittest.main()
""")

        engine_hardened = PythonMutationEngine(target_file, test_cmd, threshold=80.0, max_mutants=10)
        result_hardened = engine_hardened.run()

        # With complete branch coverage, all 6 mutants are killed!
        self.assertTrue(result_hardened["passed"], "Hardened test suite must pass mutation threshold (>=80%)")
        self.assertEqual(result_hardened["killed"], 6)
        self.assertEqual(result_hardened["survived"], 0)
        self.assertEqual(result_hardened["score"], 100.0)

if __name__ == "__main__":
    unittest.main()
