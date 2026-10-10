"""
True Pipeline Unified Engine Package
Encapsulates all orchestrators, engines, harness guards, and distributed collaboration subsystems.
"""
import os
import sys

_PIPELINE_ROOT = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.join(_PIPELINE_ROOT, "scripts")
_WORKSPACE_ROOT = os.path.dirname(_PIPELINE_ROOT)

for _p in [_WORKSPACE_ROOT, _PIPELINE_ROOT, _SCRIPTS_ROOT]:
    if _p not in sys.path:
        sys.path.insert(0, _p)
