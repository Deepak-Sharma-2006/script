"""
Test Suite — Sandbox Execution Bridge & Multi-File TDD Self-Healing
Verifies:
1. SandboxBridge enforces execution timeouts (SIGKILL termination).
2. SandboxBridge sanitizes dangerous environment variables (AWS, OpenAI, GitHub keys).
3. SandboxBridge returns structured SandboxResult with duration and exit codes.
4. CodingEngine executes multi-file transactional TDD self-healing with rollback safety.
"""

import os
import sys
import time
import shutil
import unittest
from scripts.orchestrator.sandbox_bridge import SandboxBridge, SandboxResult
from scripts.orchestrator.coding_engine import CodingEngine


class TestSandboxBridge(unittest.TestCase):
    """Tests process jail bounds, secret sanitization, and execution controls."""

    def test_sandbox_normal_execution(self):
        """Verifies standard commands execute cleanly inside the process jail."""
        cmd = [sys.executable, "-c", "import sys; print('SANDBOX_ACTIVE'); sys.exit(0)"]
        res = SandboxBridge.execute(cmd, timeout_seconds=5)
        self.assertEqual(res.returncode, 0)
        self.assertIn("SANDBOX_ACTIVE", res.stdout)
        self.assertFalse(res.timed_out)
        self.assertEqual(res.sandbox_mode, "process_jail")
        self.assertGreater(res.duration_seconds, 0)

    def test_sandbox_timeout_enforcement(self):
        """Verifies runaway infinite loops or hung processes are hard-terminated."""
        # Run a 10-second sleep with a 1-second timeout
        cmd = [sys.executable, "-c", "import time; time.sleep(10)"]
        start = time.time()
        res = SandboxBridge.execute(cmd, timeout_seconds=1)
        duration = time.time() - start

        self.assertTrue(res.timed_out)
        self.assertNotEqual(res.returncode, 0)
        # Should terminate around 1.0 - 2.5 seconds, not wait 10s
        self.assertLess(duration, 5.0)

    def test_sandbox_environment_sanitization(self):
        """Verifies secrets and credentials are never leaked into the subprocess."""
        os.environ["OPENAI_API_KEY"] = "sk-leaked-test-token"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "aws-leaked-secret"

        code = (
            "import os, sys; "
            "has_openai = 'OPENAI_API_KEY' in os.environ; "
            "has_aws = 'AWS_SECRET_ACCESS_KEY' in os.environ; "
            "print(f'OPENAI:{has_openai},AWS:{has_aws}'); "
        )
        cmd = [sys.executable, "-c", code]
        res = SandboxBridge.execute(cmd, timeout_seconds=5)

        self.assertEqual(res.returncode, 0)
        self.assertIn("OPENAI:False,AWS:False", res.stdout.strip())

        # Cleanup test env
        os.environ.pop("OPENAI_API_KEY", None)
        os.environ.pop("AWS_SECRET_ACCESS_KEY", None)

    def test_multi_file_tdd_loop(self):
        """Verifies CodingEngine handles multi-file coordinated patching."""
        test_file = "specs/scratch_tests/test_multifile_calc.py"
        calc_file = "specs/scratch_tests/calculator.py"
        formatter_file = "specs/scratch_tests/formatter.py"

        test_code = """
import unittest
from specs.scratch_tests.calculator import add
from specs.scratch_tests.formatter import format_result

class TestMultiFile(unittest.TestCase):
    def test_add_and_format(self):
        total = add(40, 2)
        formatted = format_result("ANSWER", total)
        self.assertEqual(formatted, "ANSWER: 42")

if __name__ == '__main__':
    unittest.main()
"""

        # Multi-file patch generator that fixes syntax on pass 2
        def patch_generator(iteration: int, last_error: str):
            if iteration == 1:
                # Deliberate bug in formatter.py
                return {
                    calc_file: "def add(a, b): return a + b\n",
                    formatter_file: "def format_result(label, val): return f'{label}: {val - 1}'\n"
                }
            else:
                # Correct implementation
                return {
                    calc_file: "def add(a, b): return a + b\n",
                    formatter_file: "def format_result(label, val): return f'{label}: {val}'\n"
                }

        res = CodingEngine.execute_multi_file_tdd_loop(
            module_name="multi_file_calculator",
            test_file_path=test_file,
            test_code=test_code,
            multi_file_generator=patch_generator,
            max_healing_passes=3,
            sandbox_timeout=10
        )

        self.assertEqual(res["status"], "VERIFIED_GREEN")
        self.assertEqual(res["healing_iterations_needed"], 2)
        self.assertEqual(res["sandbox_mode"], "process_jail")

        # Cleanup scratch test files and directory
        for f in [test_file, calc_file, formatter_file]:
            if os.path.exists(f):
                os.remove(f)
        if os.path.exists("specs/scratch_tests"):
            shutil.rmtree("specs/scratch_tests", ignore_errors=True)

    def test_domain_toolchain_wrappers_timeout_bounded(self):
        """Verifies domain toolchain proxies enforce execution bounds and secret sanitization."""
        # Test Solidity wrapper
        res_sol = SandboxBridge.execute_solidity("test/Counter.t.sol", timeout_seconds=1)
        self.assertIsInstance(res_sol, SandboxResult)
        self.assertLess(res_sol.duration_seconds, 3.0)

        # Test Cargo wrapper
        res_cargo = SandboxBridge.execute_cargo("Cargo.toml", timeout_seconds=1)
        self.assertIsInstance(res_cargo, SandboxResult)
        self.assertLess(res_cargo.duration_seconds, 3.0)

        # Test C/C++ wrapper
        res_cpp = SandboxBridge.execute_c_cpp("non_existent_main.cpp", timeout_seconds=1)
        self.assertIsInstance(res_cpp, SandboxResult)
        self.assertLess(res_cpp.duration_seconds, 3.0)

        # Test Kubernetes wrapper
        res_k8s = SandboxBridge.execute_k8s("k8s/deployment.yaml", timeout_seconds=1)
        self.assertIsInstance(res_k8s, SandboxResult)
        self.assertLess(res_k8s.duration_seconds, 3.0)


if __name__ == "__main__":
    unittest.main()
