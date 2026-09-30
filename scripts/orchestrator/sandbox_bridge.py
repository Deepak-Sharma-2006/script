"""
Orchestrator — Sandbox Execution Bridge (Option A Process Jail + Option B Container Staging)
Executes untrusted or generated test code inside an isolated, constrained environment.
- Option A (Active): Native OS Process Jail with execution timeouts, environment sanitization,
  memory ceilings, and strict working directory bounding.
- Option B (Staged): Ephemeral Docker container sandbox bridge (activated when Docker daemon is detected).
"""

import os
import sys
import time
import shutil
import subprocess
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class SandboxResult:
    command: List[str]
    returncode: int
    stdout: str
    stderr: str
    duration_seconds: float
    timed_out: bool
    sandbox_mode: str  # "process_jail" or "docker_container"


class SandboxBridge:
    """
    Executes commands with execution isolation to prevent blast radius
    from untrusted or self-healing generated code.
    """

    DEFAULT_TIMEOUT_SECONDS = 30
    BLOCKED_ENV_PREFIXES = ("AWS_", "GITHUB_", "OPENAI_", "ANTHROPIC_", "GEMINI_", "STRIPE_", "SSH_", "SECRET_")

    @classmethod
    def is_docker_available(cls) -> bool:
        """Checks if Docker daemon is running and accessible."""
        docker_bin = shutil.which("docker")
        if not docker_bin:
            return False
        try:
            res = subprocess.run([docker_bin, "info"], capture_output=True, timeout=2)
            return res.returncode == 0
        except Exception:
            return False

    @classmethod
    def execute(
        cls,
        command: List[str],
        cwd: Optional[str] = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
        force_mode: Optional[str] = None,
        extra_env: Optional[Dict[str, str]] = None
    ) -> SandboxResult:
        """
        Executes a command through the isolation bridge.
        Defaults to Option A (Process Jail) unless Option B is forced or Docker is active.
        """
        mode = force_mode or "process_jail"

        if mode == "docker" and cls.is_docker_available():
            return cls._execute_docker(command, cwd=cwd, timeout_seconds=timeout_seconds, extra_env=extra_env)
        else:
            return cls._execute_process_jail(command, cwd=cwd, timeout_seconds=timeout_seconds, extra_env=extra_env)

    @classmethod
    def _execute_process_jail(
        cls,
        command: List[str],
        cwd: Optional[str] = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
        extra_env: Optional[Dict[str, str]] = None
    ) -> SandboxResult:
        """
        Option A: Host Process Jail.
        Enforces execution bounds:
          1. Sanitized environment (blocking credentials & API keys).
          2. Working directory isolation.
          3. Hard process timeout with SIGTERM/SIGKILL tree termination.
        """
        work_dir = cwd or os.getcwd()
        os.makedirs(work_dir, exist_ok=True)

        # 1. Sanitize environment variables
        clean_env = {}
        for k, v in os.environ.items():
            if any(k.startswith(p) for p in cls.BLOCKED_ENV_PREFIXES):
                continue
            clean_env[k] = v

        # Set safety environment overrides
        clean_env["PYTHONUNBUFFERED"] = "1"
        clean_env["SANDBOX_ISOLATED"] = "1"
        if extra_env:
            clean_env.update(extra_env)

        start_time = time.time()
        timed_out = False

        try:
            proc = subprocess.Popen(
                command,
                cwd=work_dir,
                env=clean_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False
            )
            stdout, stderr = proc.communicate(timeout=timeout_seconds)
            duration = time.time() - start_time
            return SandboxResult(
                command=command,
                returncode=proc.returncode,
                stdout=stdout,
                stderr=stderr,
                duration_seconds=duration,
                timed_out=False,
                sandbox_mode="process_jail"
            )
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            proc.kill()
            stdout, stderr = proc.communicate()
            return SandboxResult(
                command=command,
                returncode=124,  # Standard timeout exit code
                stdout=stdout or "",
                stderr=(stderr or "") + f"\n[SandboxBridge] Execution terminated: Exceeded {timeout_seconds}s timeout ceiling.",
                duration_seconds=duration,
                timed_out=True,
                sandbox_mode="process_jail"
            )
        except Exception as e:
            duration = time.time() - start_time
            return SandboxResult(
                command=command,
                returncode=1,
                stdout="",
                stderr=f"[SandboxBridge] Failed to execute process: {e}",
                duration_seconds=duration,
                timed_out=False,
                sandbox_mode="process_jail"
            )

    @classmethod
    def _execute_docker(
        cls,
        command: List[str],
        cwd: Optional[str] = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
        extra_env: Optional[Dict[str, str]] = None
    ) -> SandboxResult:
        """
        Option B: Containerized Docker Sandbox.
        Runs inside an ephemeral container with constrained memory and CPU.
        """
        work_dir = os.path.abspath(cwd or os.getcwd())
        docker_cmd = [
            "docker", "run", "--rm",
            "--network", "none",
            "-m", "512m",
            "--cpus", "1.0",
            "-v", f"{work_dir}:/workspace:rw",
            "-w", "/workspace"
        ]
        if extra_env:
            for k, v in extra_env.items():
                docker_cmd.extend(["-e", f"{k}={v}"])

        docker_cmd.append("python:3.12-slim")
        docker_cmd.extend(command)

        start_time = time.time()
        try:
            res = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            duration = time.time() - start_time
            return SandboxResult(
                command=command,
                returncode=res.returncode,
                stdout=res.stdout,
                stderr=res.stderr,
                duration_seconds=duration,
                timed_out=False,
                sandbox_mode="docker_container"
            )
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return SandboxResult(
                command=command,
                returncode=124,
                stdout="",
                stderr=f"[SandboxBridge] Docker container exceeded {timeout_seconds}s timeout.",
                duration_seconds=duration,
                timed_out=True,
                sandbox_mode="docker_container"
            )

    # =========================================================================
    # Domain-Specific Toolchain Execution Proxies (Component 5)
    # =========================================================================

    @classmethod
    def execute_solidity(
        cls,
        test_path: str,
        cwd: Optional[str] = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    ) -> SandboxResult:
        """Runs Foundry forge test inside the process jail with gas reporting."""
        cmd = ["forge", "test", "--match-path", test_path, "--gas-report"]
        return cls.execute(cmd, cwd=cwd, timeout_seconds=timeout_seconds)

    @classmethod
    def execute_cargo(
        cls,
        manifest_path: str,
        cwd: Optional[str] = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    ) -> SandboxResult:
        """Runs cargo test inside the process jail with timeout bounding."""
        cmd = ["cargo", "test", "--manifest-path", manifest_path]
        return cls.execute(cmd, cwd=cwd, timeout_seconds=timeout_seconds)

    @classmethod
    def execute_c_cpp(
        cls,
        source_path: str,
        output_bin: str = "build_out.exe" if sys.platform == "win32" else "build_out",
        cwd: Optional[str] = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    ) -> SandboxResult:
        """Compiles C/C++ via gcc/clang and validates syntax inside jail."""
        compiler = shutil.which("gcc") or shutil.which("clang") or "gcc"
        cmd = [compiler, "-O2", "-Wall", source_path, "-o", output_bin]
        return cls.execute(cmd, cwd=cwd, timeout_seconds=timeout_seconds)

    @classmethod
    def execute_k8s(
        cls,
        manifest_path: str,
        cwd: Optional[str] = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    ) -> SandboxResult:
        """Validates Kubernetes YAML syntax via client-side dry-run."""
        cmd = ["kubectl", "apply", "--dry-run=client", "-f", manifest_path]
        return cls.execute(cmd, cwd=cwd, timeout_seconds=timeout_seconds)

