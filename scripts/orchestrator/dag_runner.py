"""
Headless Idempotent DAG Pipeline Runner (INV-04)
Executes reproducible, step-cached multi-stage data and engineering pipelines.
Caches stage outputs by hashing code + inputs, skipping redundant executions
and eliminating the fragile interactive notebook execution pattern.
"""

import sys
import os
import json
import hashlib
import subprocess
import time
from typing import Dict, Any, List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class DAGRunner:
    """
    Orchestrates DAG pipelines with SHA-256 step caching and idempotency.
    """

    CACHE_FILE = os.path.join(".agents", "cache", "dag_cache.json")

    @classmethod
    def _hash_file(cls, path: str) -> str:
        """Returns SHA-256 of file contents, or empty string if file doesn't exist."""
        if not os.path.exists(path):
            return ""
        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    @classmethod
    def _compute_stage_fingerprint(cls, stage: Dict[str, Any]) -> str:
        """
        Combines hashes of:
        1. Script file / command
        2. Input files
        3. Parameters
        """
        hasher = hashlib.sha256()

        # Script or command
        script_path = stage.get("script")
        if script_path and os.path.exists(script_path):
            hasher.update(cls._hash_file(script_path).encode("utf-8"))
        else:
            hasher.update(str(stage.get("command", "")).encode("utf-8"))

        # Inputs
        for inp in stage.get("inputs", []):
            if os.path.exists(inp):
                hasher.update(cls._hash_file(inp).encode("utf-8"))
            else:
                hasher.update(f"missing:{inp}".encode("utf-8"))

        # Params
        params = json.dumps(stage.get("params", {}), sort_keys=True)
        hasher.update(params.encode("utf-8"))

        return hasher.hexdigest()

    @classmethod
    def _load_cache(cls) -> Dict[str, Any]:
        if os.path.exists(cls.CACHE_FILE):
            try:
                with open(cls.CACHE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    @classmethod
    def _save_cache(cls, cache: Dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(cls.CACHE_FILE), exist_ok=True)
        with open(cls.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)

    @classmethod
    def run_stage(
        cls, stage: Dict[str, Any], force: bool = False
    ) -> Dict[str, Any]:
        """
        Runs a single stage with caching.
        """
        stage_name = stage.get("name", "unnamed_stage")
        fingerprint = cls._compute_stage_fingerprint(stage)
        cache = cls._load_cache()

        # Check if outputs exist and fingerprint matches
        outputs = stage.get("outputs", [])
        all_outputs_exist = all(os.path.exists(out) for out in outputs) if outputs else True

        if not force and all_outputs_exist and cache.get(stage_name, {}).get("fingerprint") == fingerprint:
            return {
                "stage": stage_name,
                "status": "CACHED_SKIP",
                "fingerprint": fingerprint,
                "message": "Stage inputs and code unchanged; using cached outputs.",
            }

        cmd = stage.get("command")
        if not cmd:
            script = stage.get("script")
            if script:
                cmd = f'"{sys.executable}" "{script}"'
            else:
                return {
                    "stage": stage_name,
                    "status": "FAILED",
                    "error": "No command or script specified for stage.",
                }

        start_time = time.perf_counter()
        try:
            res = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            elapsed = time.perf_counter() - start_time
            if res.returncode == 0:
                cache[stage_name] = {
                    "fingerprint": fingerprint,
                    "timestamp": time.time(),
                    "elapsed_sec": round(elapsed, 3),
                }
                cls._save_cache(cache)
                return {
                    "stage": stage_name,
                    "status": "SUCCESS",
                    "exit_code": 0,
                    "elapsed_sec": round(elapsed, 3),
                    "fingerprint": fingerprint,
                }
            else:
                return {
                    "stage": stage_name,
                    "status": "FAILED",
                    "exit_code": res.returncode,
                    "stderr": res.stderr[:1000],
                    "elapsed_sec": round(elapsed, 3),
                }
        except Exception as e:
            return {
                "stage": stage_name,
                "status": "ERROR",
                "error": str(e),
            }

    @classmethod
    def run_pipeline(
        cls, pipeline: List[Dict[str, Any]], force: bool = False
    ) -> Dict[str, Any]:
        """
        Executes a sequence of stages in order, stopping on first failure.
        """
        results = []
        pipeline_start = time.perf_counter()

        for idx, stage in enumerate(pipeline):
            res = cls.run_stage(stage, force=force)
            results.append(res)
            if res["status"] in ("FAILED", "ERROR"):
                return {
                    "pipeline_status": "ABORTED",
                    "failed_at_stage": stage.get("name", f"stage_{idx}"),
                    "stages": results,
                    "total_elapsed_sec": round(time.perf_counter() - pipeline_start, 3),
                }

        return {
            "pipeline_status": "SUCCESS",
            "stages": results,
            "total_elapsed_sec": round(time.perf_counter() - pipeline_start, 3),
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.orchestrator.dag_runner --pipeline <file.json> [--run|--force]")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description="Headless Idempotent DAG Runner")
    parser.add_argument("--pipeline", required=True, help="Path to pipeline JSON")
    parser.add_argument("--run", action="store_true", help="Execute pipeline")
    parser.add_argument("--force", action="store_true", help="Bypass cache")
    args = parser.parse_args()

    with open(args.pipeline, "r", encoding="utf-8") as f:
        pipe_def = json.load(f)

    stages = pipe_def if isinstance(pipe_def, list) else pipe_def.get("stages", [])
    if args.run or args.force:
        res = DAGRunner.run_pipeline(stages, force=args.force)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["pipeline_status"] == "SUCCESS" else 1)
    else:
        print(f"Pipeline definition loaded: {len(stages)} stages ready. Pass --run to execute.")
        sys.exit(0)


if __name__ == "__main__":
    main()
