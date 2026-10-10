"""
Presentation Engine Facade (INV-08 / Table A)

Provides unified presentation deck orchestration by delegating directly to
the OmniDeck engine (scripts/engine/deck_orchestrator.py).
Wires real benchmark metrics output from ML runs into championship pitch decks.
"""

import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scripts.engine.deck_orchestrator import DeckOrchestrator
from scripts.engine.planner import OmniDeckPlan, OmniSlidePlan

class PresentationEngine(DeckOrchestrator):
    """Orchestrates championship pitch presentations with Stage 1 PPTX and gated Stage 2 PDF."""
    pass

if __name__ == "__main__":
    print("OmniDeck Presentation Engine operational. Run python -m scripts.orchestrator.task_dispatcher --task presentation for execution.")
