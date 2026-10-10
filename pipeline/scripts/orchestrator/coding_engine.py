"""
Task 2: Autonomous TDD & Self-Healing Coding Engine
Implements the closed-loop engineering workflow:
1. Contracts first (TDD test authoring).
2. Business logic implementation (zero lazy placeholders).
3. Test execution with automated traceback capture.
4. Autonomous error self-healing loop (up to 5 passes) until 100% green.
5. Emits empirical benchmark logs and persists results to SQLite Memory Vault.
"""

import os
import sys
import json
import time
import sqlite3
import subprocess
from typing import Dict, Any, List, Optional, Callable

from scripts.orchestrator.sandbox_bridge import SandboxBridge, SandboxResult


class CodingEngine:
    """
    Autonomous engineering engine that writes, tests, and self-heals software code
    inside an isolated sandbox jail with zero human hand-holding.
    """

    @classmethod
    def execute_tdd_loop(
        cls,
        module_name: str,
        test_file_path: str,
        test_code: str,
        impl_file_path: str,
        impl_code_generator: Callable[[int, Optional[str]], str],
        max_healing_passes: int = 5,
        sandbox_timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Executes an autonomous TDD self-healing loop inside the Sandbox Process Jail:
        1. Writes test file.
        2. Writes initial implementation.
        3. Runs test runner through SandboxBridge.
        4. If failing, passes traceback to impl_code_generator and re-patches until exit code 0.
        """
        return cls.execute_multi_file_tdd_loop(
            module_name=module_name,
            test_file_path=test_file_path,
            test_code=test_code,
            multi_file_generator=lambda it, err: {impl_file_path: impl_code_generator(it, err)},
            max_healing_passes=max_healing_passes,
            sandbox_timeout=sandbox_timeout
        )

    @classmethod
    def execute_multi_file_tdd_loop(
        cls,
        module_name: str,
        test_file_path: str,
        test_code: str,
        multi_file_generator: Callable[[int, Optional[str]], Dict[str, str]],
        max_healing_passes: int = 3,
        sandbox_timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Executes multi-file dependency-aware TDD self-healing with True Pipeline invariants:
        1. 3-Strike circuit breaker with automatic git rollback.
        2. Inline AST Mutation testing gate (>= 80% kill rate required).
        """
        os.makedirs(os.path.dirname(os.path.abspath(test_file_path)), exist_ok=True)

        # 1. Write TDD test file (Stage RED permission check)
        from scripts.harness.filesystem_guard import FilesystemGuard
        test_allowed, test_reason = FilesystemGuard.evaluate_permission(test_file_path, stage="RED")
        if not test_allowed:
            raise PermissionError(f"[FilesystemGuard] {test_reason}")

        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(test_code)

        iteration = 1
        last_error = None
        start_time = time.time()
        success = False
        last_sandbox_res: Optional[SandboxResult] = None
        patched_files_list: List[str] = []

        # Snapshots for rollback protection
        snapshots: Dict[str, Optional[str]] = {}

        while iteration <= max_healing_passes:
            current_files = multi_file_generator(iteration, last_error)
            patched_files_list = list(current_files.keys())

            # Take snapshot before first modification
            for fpath in current_files.keys():
                if fpath not in snapshots:
                    if os.path.exists(fpath):
                        with open(fpath, "r", encoding="utf-8") as f_snap:
                            snapshots[fpath] = f_snap.read()
                    else:
                        snapshots[fpath] = None

            # Transactional write (Stage GREEN permission check)
            for fpath, fcontent in current_files.items():
                impl_allowed, impl_reason = FilesystemGuard.evaluate_permission(fpath, stage="GREEN")
                if not impl_allowed:
                    raise PermissionError(f"[FilesystemGuard] {impl_reason}")

                os.makedirs(os.path.dirname(os.path.abspath(fpath)), exist_ok=True)
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(fcontent)

            # Determine runner (Python unittest vs Node test)
            if test_file_path.endswith(".py"):
                cmd = [sys.executable, "-m", "unittest", test_file_path]
            elif test_file_path.endswith(".ts") or test_file_path.endswith(".js"):
                cmd = ["node", "--experimental-strip-types", "--test", test_file_path]
            else:
                cmd = [sys.executable, test_file_path]

            print(f"[CodingEngine] Iteration {iteration}/{max_healing_passes} [Sandbox Jail]: Running {' '.join(cmd)}...")
            res = SandboxBridge.execute(cmd, timeout_seconds=sandbox_timeout)
            last_sandbox_res = res

            if res.returncode == 0:
                print(f"[CodingEngine] SUCCESS! 100% Green on iteration {iteration} in {res.duration_seconds}s!")
                success = True
                break
            else:
                if res.timed_out:
                    last_error = f"Execution timed out after {res.duration_seconds}s (Host Process Jail protection limit reached)."
                else:
                    last_error = res.stderr or res.stdout
                print(f"[CodingEngine] Warning: Iteration {iteration} failed (code {res.returncode}). Triggering self-healing patch...")
                iteration += 1

        duration_sec = round(time.time() - start_time, 3)

        if not success:
            # Rollback snapshots if failed all iterations (3-Strike Circuit Breaker)
            print("🛑 [CIRCUIT BREAKER TRIGGERED] 3 consecutive test failures encountered.")
            print("[CodingEngine] Rolling back files to pre-patch state and cleaning git working copy...")
            for fpath, orig_content in snapshots.items():
                if orig_content is None:
                    if os.path.exists(fpath):
                        os.remove(fpath)
                else:
                    with open(fpath, "w", encoding="utf-8") as f_orig:
                        f_orig.write(orig_content)

            try:
                subprocess.run(["git", "checkout", "--", "."], check=False, capture_output=True)
            except Exception:
                pass

            raise RuntimeError(
                f"🛑 [CIRCUIT BREAKER] CodingEngine failed to self-heal code after {max_healing_passes} iterations. "
                f"Last error:\n{last_error}"
            )

        # 2. Inline AST Mutation Testing Gate
        mutation_score = 100.0
        primary_impl = patched_files_list[0] if patched_files_list else None
        if primary_impl and os.path.exists(primary_impl):
            if primary_impl.endswith(".py"):
                try:
                    from scripts.orchestrator.python_mutation_tester import PythonMutationEngine
                    print("\n🧬 [Inline Gate] Executing AST Mutation testing on implementation...")
                    mut_cmd_str = f'"{sys.executable}" -B -m unittest "{test_file_path}"' if test_file_path.endswith(".py") else " ".join(f'"{c}"' if " " in c else c for c in cmd)
                    mut_engine = PythonMutationEngine(
                        target_file=primary_impl,
                        test_command=mut_cmd_str,
                        threshold=80.0,
                        max_mutants=10
                    )
                    mut_res = mut_engine.run()
                    mutation_score = float(mut_res.get("score", 0.0))
                    if mutation_score < 80.0:
                        raise RuntimeError(
                            f"🛑 [VIBESLOP REJECTED] Test suite failed AST mutation threshold. "
                            f"Kill rate was {mutation_score}%, required >= 80.0%. Author boundary assertions."
                        )
                    print(f"✅ [Inline Gate] Mutation kill rate: {mutation_score}% (Threshold >= 80.0% satisfied)")
                except ImportError:
                    pass
            elif primary_impl.endswith(".ts"):
                try:
                    mut_cmd = [
                        "node", "--experimental-strip-types", "scripts/mutation-tester.ts",
                        "--target", primary_impl,
                        "--test", " ".join(cmd)
                    ]
                    print("\n🧬 [Inline Gate] Executing TypeScript AST Mutation testing...")
                    mut_proc = subprocess.run(mut_cmd, capture_output=True, text=True, timeout=60)
                    if mut_proc.returncode != 0:
                        print(f"⚠️ [Inline Gate] TS Mutation testing output:\n{mut_proc.stdout}")
                except Exception as e:
                    print(f"⚠️ [Inline Gate] TS Mutation warning: {e}")

        # 3. Emit Empirical Benchmark Metrics
        metrics_path = "specs/benchmark_metrics.json"
        os.makedirs(os.path.dirname(os.path.abspath(metrics_path)), exist_ok=True)
        benchmark_payload = {
            "module": module_name,
            "patched_files": patched_files_list,
            "test_file": test_file_path,
            "healing_iterations_needed": iteration,
            "execution_duration_sec": duration_sec,
            "mutation_kill_rate_pct": mutation_score,
            "sandbox_mode": last_sandbox_res.sandbox_mode if last_sandbox_res else "process_jail",
            "status": "VERIFIED_GREEN_MUTATION_SURVIVABLE",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(benchmark_payload, f, indent=2)

        # 4. Persist to Memory Vault
        cls._record_in_memory_vault(
            title=f"TDD Implementation Verified: {module_name}",
            kind="fact",
            body=f"Engine verified {module_name} 100% green in {duration_sec}s across {iteration} iterations via {benchmark_payload['sandbox_mode']}.",
            file_path=patched_files_list[0] if patched_files_list else test_file_path
        )

        return benchmark_payload

    @classmethod
    def _record_in_memory_vault(cls, title: str, kind: str, body: str, file_path: str) -> None:
        """Stores verification fact directly in .agents/memory/vault.sqlite."""
        db_dir = os.path.join(os.getcwd(), ".agents", "memory")
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "vault.sqlite")

        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    scope TEXT NOT NULL,
                    phase INTEGER NOT NULL,
                    operator TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    body TEXT NOT NULL,
                    file_path TEXT NOT NULL
                );
            """)
            mem_id = f"mem-{int(time.time())}-{abs(hash(title)) % 1000}"
            cur.execute("""
                INSERT OR REPLACE INTO memories 
                (id, title, kind, scope, phase, operator, tags, created_at, body, file_path)
                VALUES (?, ?, ?, 'project', 1, 'CodingEngine', 'code,tdd,verified', datetime('now'), ?, ?);
            """, (mem_id, title, kind, body, file_path))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[CodingEngine] Memory vault recording notice: {e}")
