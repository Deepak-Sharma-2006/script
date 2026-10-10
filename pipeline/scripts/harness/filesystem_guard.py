"""
Physical Stage-Gated Filesystem Guard
Enforces strict anti-cheating permission boundaries during autonomous loops:
- RED Stage (Testing Phase): Writes to src/ are blocked; writes to tests/ allowed.
- GREEN Stage (Implementation Phase): Writes to tests/ are physically locked to READ-ONLY via OS kernel attributes (attrib +r / chmod); writes to src/ allowed.
- AUDIT Stage: Both code and tests are locked read-only.
"""

import sys
import os
import stat
import subprocess
import argparse
from contextlib import contextmanager
from typing import Tuple, Optional, Generator

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class FilesystemGuard:
    """Interceps and physically gates file write operations based on the active pipeline lifecycle stage."""

    STAGES = ["RED", "GREEN", "AUDIT", "UNRESTRICTED"]

    @classmethod
    def evaluate_permission(cls, target_path: str, stage: str) -> Tuple[bool, str]:
        """
        Evaluates whether a target file path can be written to in the given stage.
        Returns: (allowed: bool, reason: str)
        """
        normalized_path = os.path.normpath(target_path).replace("\\", "/").lower()
        stage_upper = stage.upper()

        if stage_upper not in cls.STAGES:
            return False, f"Unknown lifecycle stage: '{stage}'. Valid stages: {cls.STAGES}"

        if stage_upper == "UNRESTRICTED":
            return True, "Unrestricted mode active."

        # RED PHASE: Authoring test contracts. src/ is strictly READ-ONLY.
        if stage_upper == "RED":
            if normalized_path.startswith("src/") or "/src/" in normalized_path:
                return False, (
                    f"PERMISSION_DENIED [ANTI-CHEATING]: Stage is RED (Test Specification Phase). "
                    f"Modifying implementation source '{target_path}' is forbidden. "
                    f"Write tests in tests/ only."
                )
            return True, "Write permitted for RED stage."

        # GREEN PHASE: Implementing code. tests/ is strictly READ-ONLY.
        if stage_upper == "GREEN":
            if normalized_path.startswith("tests/") or "/tests/" in normalized_path:
                return False, (
                    f"PERMISSION_DENIED [ANTI-CHEATING]: Stage is GREEN (Implementation Phase). "
                    f"Modifying test suite '{target_path}' is forbidden. "
                    f"You cannot alter tests to force green passes. Implement code in src/."
                )
            return True, "Write permitted for GREEN stage."

        # AUDIT PHASE: Code and tests are locked. Only docs and reports allowed.
        if stage_upper == "AUDIT":
            if (
                normalized_path.startswith("src/")
                or "/src/" in normalized_path
                or normalized_path.startswith("tests/")
                or "/tests/" in normalized_path
            ):
                return False, (
                    f"PERMISSION_DENIED [STAGE AUDIT]: Codebase is locked during AUDIT phase. "
                    f"Cannot modify code or tests. Write to docs/ or reports only."
                )
            return True, "Write permitted for AUDIT stage."

        return True, "Permitted."

    @classmethod
    def lock_path(cls, path: str) -> bool:
        """
        Physically locks a file or directory to READ-ONLY at the OS filesystem level.
        On Windows: invokes 'attrib +r <path>'
        On POSIX: removes write bits via os.chmod
        """
        if not os.path.exists(path):
            return False

        try:
            if sys.platform == "win32":
                target = os.path.normpath(path)
                subprocess.run(["attrib", "+r", target], check=True, capture_output=True)
            else:
                current_mode = os.stat(path).st_mode
                os.chmod(path, current_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
            return True
        except Exception as e:
            print(f"⚠️ [FilesystemGuard] Failed to lock '{path}': {e}", file=sys.stderr)
            return False

    @classmethod
    def unlock_path(cls, path: str) -> bool:
        """
        Physically unlocks a file or directory restoring write permissions at the OS level.
        On Windows: invokes 'attrib -r <path>'
        On POSIX: restores user write bit via os.chmod
        """
        if not os.path.exists(path):
            return False

        try:
            if sys.platform == "win32":
                target = os.path.normpath(path)
                subprocess.run(["attrib", "-r", target], check=True, capture_output=True)
            else:
                current_mode = os.stat(path).st_mode
                os.chmod(path, current_mode | stat.S_IWUSR)
            return True
        except Exception as e:
            print(f"⚠️ [FilesystemGuard] Failed to unlock '{path}': {e}", file=sys.stderr)
            return False

    @classmethod
    def lock_stage(cls, stage: str, test_path: Optional[str] = None, impl_path: Optional[str] = None) -> None:
        """
        Applies physical OS-level read-only locks according to pipeline stage invariants:
        - RED: Locks impl_path (preventing source cheating while testing red)
        - GREEN: Locks test_path (preventing modifying test assertions while passing green)
        - AUDIT: Locks both test_path and impl_path
        - UNRESTRICTED: Unlocks both
        """
        stage_upper = stage.upper()
        if stage_upper == "RED":
            if impl_path and os.path.exists(impl_path):
                cls.lock_path(impl_path)
            if test_path and os.path.exists(test_path):
                cls.unlock_path(test_path)
        elif stage_upper == "GREEN":
            if test_path and os.path.exists(test_path):
                cls.lock_path(test_path)
            if impl_path and os.path.exists(impl_path):
                cls.unlock_path(impl_path)
        elif stage_upper == "AUDIT":
            if test_path and os.path.exists(test_path):
                cls.lock_path(test_path)
            if impl_path and os.path.exists(impl_path):
                cls.lock_path(impl_path)
        elif stage_upper == "UNRESTRICTED":
            if test_path and os.path.exists(test_path):
                cls.unlock_path(test_path)
            if impl_path and os.path.exists(impl_path):
                cls.unlock_path(impl_path)

    @classmethod
    def unlock_stage(cls, stage: str, test_path: Optional[str] = None, impl_path: Optional[str] = None) -> None:
        """Safely unlocks all paths associated with the stage."""
        if test_path and os.path.exists(test_path):
            cls.unlock_path(test_path)
        if impl_path and os.path.exists(impl_path):
            cls.unlock_path(impl_path)

    @classmethod
    @contextmanager
    def physical_stage_guard(
        cls,
        stage: str,
        test_path: Optional[str] = None,
        impl_path: Optional[str] = None
    ) -> Generator[None, None, None]:
        """
        Context manager ensuring OS kernel physical locks are active during block execution
        and guaranteed to be released in finally.
        """
        cls.lock_stage(stage, test_path=test_path, impl_path=impl_path)
        try:
            yield
        finally:
            cls.unlock_stage(stage, test_path=test_path, impl_path=impl_path)


def main():
    parser = argparse.ArgumentParser(description="Stage-Gated Filesystem Guard")
    parser.add_argument("--path", required=True, help="Target file path to evaluate/lock")
    parser.add_argument("--stage", choices=["RED", "GREEN", "AUDIT", "UNRESTRICTED"], default="GREEN", help="Active lifecycle stage")
    parser.add_argument("--action", choices=["eval", "lock", "unlock"], default="eval", help="Guard action to perform")
    args = parser.parse_args()

    if args.action == "eval":
        allowed, reason = FilesystemGuard.evaluate_permission(args.path, args.stage)
        if allowed:
            print(f"✅ [FilesystemGuard] {reason}")
            sys.exit(0)
        else:
            print(f"🛑 [FilesystemGuard] {reason}", file=sys.stderr)
            sys.exit(1)
    elif args.action == "lock":
        success = FilesystemGuard.lock_path(args.path)
        sys.exit(0 if success else 1)
    elif args.action == "unlock":
        success = FilesystemGuard.unlock_path(args.path)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
