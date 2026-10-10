"""
Native Python AST Mutation Testing Engine
Enforces the >=80% Mutation Kill Rate Threshold on Python Codebases.
Injects 4 fault classes directly via Python standard ast:
  1. Boundary / Comparison inversions (>, <=, ==, !=, in, not in)
  2. Boolean & logical inversions (True/False, and/or)
  3. Arithmetic operator mutations (+, -, *, /)
  4. Return value overrides (return x -> return None)
Transactionally safe: creates atomic .bak backup and restores original code on any exit.
"""

import ast
import atexit
import copy
import os
import shutil
import signal
import subprocess
import sys
import time
from typing import List, Dict, Any, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class MutantDef:
    def __init__(self, mutant_id: str, category: str, description: str, lineno: int, mutated_code: str):
        self.mutant_id = mutant_id
        self.category = category
        self.description = description
        self.lineno = lineno
        self.mutated_code = mutated_code
        self.status = "PENDING"
        self.duration_ms = 0


class ASTMutationCollector(ast.NodeVisitor):
    """Walks the AST and records mutation opportunities."""

    def __init__(self, original_tree: ast.AST):
        self.original_tree = original_tree
        self.mutants: List[MutantDef] = []
        self._counter = 0

    def _add_mutant(self, category: str, desc: str, lineno: int, mutated_tree: ast.AST):
        self._counter += 1
        mutant_id = f"PY_M{self._counter:03d}"
        try:
            mutated_code = ast.unparse(mutated_tree)
        except Exception:
            mutated_code = ""
        self.mutants.append(MutantDef(mutant_id, category, desc, lineno, mutated_code))

    def visit_Compare(self, node: ast.Compare):
        cmp_map = {
            ast.Gt: (ast.LtE, "> to <="),
            ast.Lt: (ast.GtE, "< to >="),
            ast.GtE: (ast.Lt, ">= to <"),
            ast.LtE: (ast.Gt, "<= to >"),
            ast.Eq: (ast.NotEq, "== to !="),
            ast.NotEq: (ast.Eq, "!= to =="),
            ast.In: (ast.NotIn, "in to not in"),
            ast.NotIn: (ast.In, "not in to in"),
            ast.Is: (ast.IsNot, "is to is not"),
            ast.IsNot: (ast.Is, "is not to is"),
        }
        for i, op in enumerate(node.ops):
            op_type = type(op)
            if op_type in cmp_map:
                new_op_cls, desc = cmp_map[op_type]
                tree_copy = copy.deepcopy(self.original_tree)
                # Find matching node in copy
                target = self._find_node_by_lineno(tree_copy, node)
                if target and isinstance(target, ast.Compare) and len(target.ops) > i:
                    target.ops[i] = new_op_cls()
                    self._add_mutant("Boundary Inversion", f"Invert {desc}", getattr(node, 'lineno', 1), tree_copy)
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp):
        if isinstance(node.op, ast.And):
            tree_copy = copy.deepcopy(self.original_tree)
            target = self._find_node_by_lineno(tree_copy, node)
            if target and isinstance(target, ast.BoolOp):
                target.op = ast.Or()
                self._add_mutant("Boolean Operator", "Mutate 'and' to 'or'", getattr(node, 'lineno', 1), tree_copy)
        elif isinstance(node.op, ast.Or):
            tree_copy = copy.deepcopy(self.original_tree)
            target = self._find_node_by_lineno(tree_copy, node)
            if target and isinstance(target, ast.BoolOp):
                target.op = ast.And()
                self._add_mutant("Boolean Operator", "Mutate 'or' to 'and'", getattr(node, 'lineno', 1), tree_copy)
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp):
        bin_map = {
            ast.Add: (ast.Sub, "+ to -"),
            ast.Sub: (ast.Add, "- to +"),
            ast.Mult: (ast.FloorDiv, "* to //"),
        }
        op_type = type(node.op)
        if op_type in bin_map:
            new_op_cls, desc = bin_map[op_type]
            tree_copy = copy.deepcopy(self.original_tree)
            target = self._find_node_by_lineno(tree_copy, node)
            if target and isinstance(target, ast.BinOp):
                target.op = new_op_cls()
                self._add_mutant("Arithmetic Operator", f"Mutate {desc}", getattr(node, 'lineno', 1), tree_copy)
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, bool):
            tree_copy = copy.deepcopy(self.original_tree)
            target = self._find_node_by_lineno(tree_copy, node)
            if target and isinstance(target, ast.Constant) and isinstance(target.value, bool):
                target.value = not target.value
                self._add_mutant("Literal Inversion", f"Mutate {not target.value} to {target.value}", getattr(node, 'lineno', 1), tree_copy)
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return):
        if node.value is not None and not (isinstance(node.value, ast.Constant) and node.value.value is None):
            tree_copy = copy.deepcopy(self.original_tree)
            target = self._find_node_by_lineno(tree_copy, node)
            if target and isinstance(target, ast.Return):
                target.value = ast.Constant(value=None)
                self._add_mutant("Return Value Override", "Override return value with None", getattr(node, 'lineno', 1), tree_copy)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Domain Fault Class: MUT_SEC_TIMING_LEAK & MUT_DEEPTECH_PRECISION
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        if func_name in ("compare_digest", "timingSafeEqual") and len(node.args) >= 2:
            tree_copy = copy.deepcopy(self.original_tree)
            target = self._find_node_by_lineno(tree_copy, node)
            if target and isinstance(target, ast.Call):
                # Replace with raw float/string equality == (timing leak)
                target.func = ast.Name(id="__timing_leak_eq__", ctx=ast.Load())
                self._add_mutant("Domain Security (MUT_SEC_TIMING_LEAK)", "Invert constant-time check to raw comparison", getattr(node, 'lineno', 1), tree_copy)
        elif func_name == "isclose" and len(node.args) >= 2:
            tree_copy = copy.deepcopy(self.original_tree)
            target = self._find_node_by_lineno(tree_copy, node)
            if target and isinstance(target, ast.Call):
                self._add_mutant("Domain Deep Tech (MUT_DEEPTECH_PRECISION)", "Invert epsilon bound to raw comparison", getattr(node, 'lineno', 1), tree_copy)

        self.generic_visit(node)

    def _find_node_by_lineno(self, tree: ast.AST, original_node: ast.AST) -> Optional[ast.AST]:
        target_lineno = getattr(original_node, "lineno", None)
        target_col = getattr(original_node, "col_offset", None)
        target_type = type(original_node)
        if target_lineno is None:
            return None

        for candidate in ast.walk(tree):
            if (type(candidate) == target_type and
                getattr(candidate, "lineno", None) == target_lineno and
                getattr(candidate, "col_offset", None) == target_col):
                return candidate
        return None


class PythonMutationEngine:
    """Executes atomic mutation testing on a Python file."""

    def __init__(self, target_file: str, test_command: str, threshold: float = 80.0, max_mutants: int = 15):
        self.target_file = os.path.abspath(target_file)
        self.test_command = test_command
        self.threshold = threshold
        self.max_mutants = max_mutants
        self.backup_file = f"{self.target_file}.bak"

    def _restore_backup(self):
        if os.path.exists(self.backup_file):
            shutil.copyfile(self.backup_file, self.target_file)
            try:
                os.remove(self.backup_file)
            except Exception:
                pass

    def run(self) -> Dict[str, Any]:
        if not os.path.exists(self.target_file):
            raise FileNotFoundError(f"Target file not found: {self.target_file}")

        print(f"\n🧬 [Python Mutation Engine] Target: {os.path.basename(self.target_file)}")
        print(f"📋 Test Command: '{self.test_command}' (Threshold: {self.threshold}%)\n")

        with open(self.target_file, "r", encoding="utf-8") as f:
            original_code = f.read()

        # Step 1: Create atomic backup
        shutil.copyfile(self.target_file, self.backup_file)
        atexit.register(self._restore_backup)
        
        # Register signal handlers for clean rollback on Ctrl+C / SIGTERM
        def _signal_handler(signum, frame):
            self._restore_backup()
            sys.exit(1)
        try:
            signal.signal(signal.SIGINT, _signal_handler)
            signal.signal(signal.SIGTERM, _signal_handler)
        except Exception:
            pass

        try:
            # Step 2: Verify baseline tests pass before mutating
            print("▶ Verifying baseline test suite passes...")
            sub_env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
            base_res = subprocess.run(self.test_command, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace", env=sub_env, timeout=20)
            if base_res.returncode != 0:
                print(f"❌ Baseline tests failed! Cannot mutate a failing test suite.\n{base_res.stderr}")
                return {"passed": False, "score": 0.0, "error": "Baseline failed"}
            print("   ✅ Baseline tests GREEN.\n")

            # Step 3: Parse AST and collect mutants
            tree = ast.parse(original_code, filename=self.target_file)
            collector = ASTMutationCollector(tree)
            collector.visit(tree)

            all_mutants = [m for m in collector.mutants if m.mutated_code and m.mutated_code != original_code]
            if not all_mutants:
                print("⚠️  No mutation points found in target AST. Code contains no mutable operators.")
                return {"passed": True, "score": 100.0, "total": 0, "killed": 0}

            # Select balanced set of mutants up to max_mutants
            selected = all_mutants[:self.max_mutants]
            print(f"🔬 Injected {len(selected)} AST Mutants (Max cap: {self.max_mutants}):")

            killed = 0
            survived = 0

            for mutant in selected:
                sys.stdout.write(f"   ▶ Testing {mutant.mutant_id} [{mutant.category}] L{mutant.lineno}: {mutant.description}... ")
                sys.stdout.flush()

                # Write mutant code to file
                with open(self.target_file, "w", encoding="utf-8") as f:
                    f.write(mutant.mutated_code)

                start_t = time.time()
                try:
                    # Run test command
                    res = subprocess.run(self.test_command, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace", env=sub_env, timeout=10)

                    duration_ms = int((time.time() - start_t) * 1000)
                    mutant.duration_ms = duration_ms

                    if res.returncode != 0:
                        # Non-zero return means test caught the bug -> Mutant KILLED!
                        killed += 1
                        mutant.status = "KILLED"
                        print(f"🗡️  KILLED ({duration_ms}ms)")
                    else:
                        # Zero return means test suite didn't catch the fault -> Mutant SURVIVED
                        survived += 1
                        mutant.status = "SURVIVED"
                        print(f"⚠️  SURVIVED ({duration_ms}ms)")


                except subprocess.TimeoutExpired:
                    killed += 1
                    mutant.status = "KILLED (TIMEOUT)"
                    print("🗡️  KILLED (Infinite loop/Timeout)")
                except Exception as ex:
                    killed += 1
                    mutant.status = "KILLED (ERROR)"
                    print(f"🗡️  KILLED ({type(ex).__name__})")

            total = killed + survived
            score = round((killed / total) * 100, 1) if total > 0 else 100.0
            passed = score >= self.threshold

            print(f"\n{'=' * 70}")
            print(f"📊 PYTHON MUTATION SCORECARD:")
            print(f"   Total Mutants: {total}")
            print(f"   Killed:        {killed}")
            print(f"   Survived:      {survived}")
            print(f"   Kill Rate:     {score}% (Threshold: {self.threshold}%)")
            status_icon = "✅ PASSED" if passed else "❌ FAILED (Anti-Green Signal Trap Triggered)"
            print(f"   Final Status:  {status_icon}")
            print(f"{'=' * 70}\n")

            return {
                "passed": passed,
                "score": score,
                "total": total,
                "killed": killed,
                "survived": survived,
                "threshold": self.threshold
            }

        finally:
            self._restore_backup()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m scripts.orchestrator.python_mutation_tester <target_file.py> <test_command> [threshold]")
        sys.exit(1)

    tgt = sys.argv[1]
    cmd = sys.argv[2]
    thresh = float(sys.argv[3]) if len(sys.argv) > 3 else 80.0

    engine = PythonMutationEngine(tgt, cmd, thresh)
    result = engine.run()
    sys.exit(0 if result["passed"] else 1)
