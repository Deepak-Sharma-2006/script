# OmniDeck Presentation Synthesis Engine

This directory contains the core Python modules for OmniDeck, the presentation generation engine powering Task 3 of the Universal Task Dispatcher.

## Key Subsystems
- `pptx_compiler.py`: Compiles native `.pptx` presentations (<0.2s) with 2D Flex/Grid coordinate math.
- `flex_grid_solver.py` & `layout_solver.py`: Deterministic non-overlapping layout solvers.
- `themes.py` & `theme_registry.py`: Modern color themes (dark, light, cyber terminal, modern SaaS).
- `primitives/`: 7 foundational visual primitives (cards, callouts, stat blocks, badges, tables, node graphs).
- `vision_qa_gate.py`: Computer-vision QA gate checking WCAG contrast and boundary overlap.
- `cognitive_analyzer.py`: Reverse-engineers design grammar and typography from reference decks.
- `planner.py` & `deck_orchestrator.py`: Two-stage presentation orchestrator.
