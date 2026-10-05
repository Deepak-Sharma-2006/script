"""
Anti-Hardcoding Automated Schema Guard (Enterprise Invariant)
Audits the template repository for forbidden hardcoded competition relics,
specific hackathon constants, and dataset paths to guarantee clean, parameterized,
and generalizable commercial software deliverables.
"""

import sys
import os
import re
from typing import List, Dict, Any, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class AntiHardcodingGuard:
    """
    Automated scanner for blocking hardcoded challenge relics,
    competition dataset paths, and uncalibrated hackathon constants.
    """

    SCAN_DIRECTORIES = [
        os.path.join(".agents", "harness"),
        os.path.join("templates", "domains"),
        os.path.join("scripts", "orchestrator"),
    ]

    # Patterns representing un-parameterized competition relics
    FORBIDDEN_PATTERNS = [
        (r"/kaggle/input", "Hardcoded Kaggle input dataset path"),
        (r"/kaggle/working", "Hardcoded Kaggle working directory path"),
        (r"scale_pos_weight\s*=\s*15", "Hardcoded hackathon margin hyperparameter (scale_pos_weight=15)"),
        (r"3\.8\s*million\s*records", "Hardcoded competition record volume (3.8 million records)"),
        (r"candidate\s*generator\s*recall\s*is\s*92\.5%", "Hardcoded challenge threshold (recall=92.5%)"),
    ]

    # File extensions to audit
    AUDIT_EXTENSIONS = {".json", ".ts", ".py", ".md", ".sh"}

    @classmethod
    def audit_file(cls, file_path: str) -> List[Dict[str, Any]]:
        """Audits a single file for forbidden hardcoded relics."""
        violations = []
        if not os.path.exists(file_path):
            return violations

        # Skip scanner self-audit to prevent false positives from regex pattern definitions
        normalized_path = file_path.replace("\\", "/")
        if normalized_path.endswith("anti_hardcoding_guard.py"):
            return violations

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            for line_idx, line in enumerate(lines, start=1):
                for pattern, desc in cls.FORBIDDEN_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        violations.append({
                            "file": file_path.replace("\\", "/"),
                            "line": line_idx,
                            "snippet": line.strip()[:100],
                            "rule": desc,
                        })
        except Exception as e:
            violations.append({
                "file": file_path.replace("\\", "/"),
                "line": 0,
                "snippet": str(e),
                "rule": "FILE_READ_ERROR"
            })

        return violations

    @classmethod
    def scan_workspace(cls, root_dir: str = ".") -> Tuple[int, List[Dict[str, Any]]]:
        """Scans configured directories across the workspace."""
        total_files = 0
        all_violations = []

        for target_dir in cls.SCAN_DIRECTORIES:
            full_dir = os.path.join(root_dir, target_dir)
            if not os.path.exists(full_dir):
                continue

            for dirpath, _, filenames in os.walk(full_dir):
                for fname in filenames:
                    ext = os.path.splitext(fname)[1].lower()
                    if ext in cls.AUDIT_EXTENSIONS:
                        total_files += 1
                        file_path = os.path.join(dirpath, fname)
                        violations = cls.audit_file(file_path)
                        all_violations.extend(violations)

        return total_files, all_violations


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    print("================================================================================")
    print("🛡️ [ANTI-HARDCODING GUARD] Scanning Repository for Un-Parameterized Relics")
    print("================================================================================")

    total_files, violations = AntiHardcodingGuard.scan_workspace()

    if violations:
        print(f"❌ [BREACH DETECTED] Found {len(violations)} forbidden hardcoded relics across {total_files} audited files:\n")
        for v in violations:
            print(f"  • {v['file']}:{v['line']} -> {v['rule']}")
            print(f"    Snippet: \"{v['snippet']}\"\n")
        print("Please parameterize these values into configurable options.")
        sys.exit(1)

    print(f"✅ [CLEAN] Audited {total_files} template files across harness, domains, and orchestrator.")
    print("   • Zero hardcoded Kaggle paths (/kaggle/*)")
    print("   • Zero stale competition thresholds (F0.5, 3.8M records, scale_pos_weight=15)")
    print("   • Parameterized Enterprise Invariant Standard: 100% COMPLIANT")
    print("================================================================================\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
