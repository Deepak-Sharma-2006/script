"""
Enterprise Agentic System — Orchestrator Package
"""
import os, sys
_CUR = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS = os.path.dirname(_CUR)
_PIPELINE = os.path.dirname(_SCRIPTS)
_WORKSPACE = os.path.dirname(_PIPELINE)
for _p in [_WORKSPACE, _PIPELINE, _SCRIPTS]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from scripts.orchestrator.doc_visualizer import DocVisualizer
from scripts.orchestrator.solution_council import SolutionCouncil
from scripts.orchestrator.coding_engine import CodingEngine
from scripts.orchestrator.task_dispatcher import TaskDispatcher
from scripts.orchestrator.sandbox_bridge import SandboxBridge
from scripts.orchestrator.cost_estimator import CostEstimator
from scripts.orchestrator.project_auditor import ProjectAuditor

__all__ = [
    "DocVisualizer",
    "SolutionCouncil",
    "CodingEngine",
    "TaskDispatcher",
    "SandboxBridge",
    "CostEstimator",
    "ProjectAuditor"
]
