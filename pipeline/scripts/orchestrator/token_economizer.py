"""
Token Economizer & Output Compression Engine (INV-04 / Table A)

Enforces SWE-agent 35-line tool output bounds with automatic file spillover.
Prevents context window saturation from long command or test outputs while preserving
complete forensic traces on disk.
"""

import os
import sys
import hashlib
from typing import Tuple, Dict, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SPILLOVER_DIR = os.path.join(os.getcwd(), ".agents", "spillover")

class TokenEconomizer:
    """Compresses verbose terminal and tool outputs to preserve token budget."""

    MAX_DISPLAY_LINES = 35
    HEAD_LINES = 15
    TAIL_LINES = 15

    @classmethod
    def compress_output(cls, raw_output: str, source_tag: str = "tool_output") -> Tuple[str, Dict[str, Any]]:
        """
        Compresses output if it exceeds MAX_DISPLAY_LINES.
        Writes complete uncompressed output to .agents/spillover/ and returns truncated view.
        """
        if not raw_output:
            return "", {"compressed": False, "total_lines": 0, "spillover_path": None}

        lines = raw_output.splitlines()
        total_lines = len(lines)

        if total_lines <= cls.MAX_DISPLAY_LINES:
            return raw_output, {
                "compressed": False,
                "total_lines": total_lines,
                "displayed_lines": total_lines,
                "spillover_path": None
            }

        os.makedirs(SPILLOVER_DIR, exist_ok=True)
        content_hash = hashlib.sha256(raw_output.encode("utf-8")).hexdigest()[:12]
        spillover_file = os.path.join(SPILLOVER_DIR, f"{source_tag}_{content_hash}.log")

        with open(spillover_file, "w", encoding="utf-8") as f:
            f.write(raw_output)

        head = lines[:cls.HEAD_LINES]
        tail = lines[-cls.TAIL_LINES:]
        omitted = total_lines - (cls.HEAD_LINES + cls.TAIL_LINES)

        file_url = f"file:///{spillover_file.replace(os.sep, '/')}"
        summary_line = f"\n[... {omitted} lines omitted to preserve token economy. Full trace: {file_url} ...]\n"

        compressed = "\n".join(head) + summary_line + "\n".join(tail)

        return compressed, {
            "compressed": True,
            "total_lines": total_lines,
            "displayed_lines": cls.HEAD_LINES + cls.TAIL_LINES,
            "omitted_lines": omitted,
            "spillover_path": spillover_file
        }

def main():
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    compressed, stats = TokenEconomizer.compress_output(content)
    print(compressed)
    if stats["compressed"]:
        print(f"\nℹ️ Economizer: Compressed {stats['total_lines']} -> {stats['displayed_lines']} lines ({stats['spillover_path']})", file=sys.stderr)

if __name__ == "__main__":
    main()
