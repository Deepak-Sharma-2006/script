"""
OmniDeck Compiler Facade (INV-08 / Table A)

Delegates directly to scripts/engine/pptx_compiler.py and deck_orchestrator.py
for sub-0.2s native PowerPoint generation.
"""

import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scripts.engine.pptx_compiler import OmniDeckCompiler

if __name__ == "__main__":
    print("OmniDeck Compiler operational.")
