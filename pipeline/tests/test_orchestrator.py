"""
Test Suite — Enterprise Agentic System Orchestrator
Verifies:
1. DocVisualizer renders high-resolution PNG graphics (flowchart, topology, KPI dashboard).
2. SolutionCouncil formulates solution, renders diagrams, writes dossier, and persists to SQLite.
3. CodingEngine executes autonomous TDD loop with automated self-healing.
4. TaskDispatcher correctly routes individual tasks (solution, code, presentation, memory).
"""

import os
import shutil
import unittest
from PIL import Image

from scripts.orchestrator.doc_visualizer import DocVisualizer
from scripts.orchestrator.solution_council import SolutionCouncil
from scripts.orchestrator.coding_engine import CodingEngine
from scripts.orchestrator.task_dispatcher import TaskDispatcher


class TestEnterpriseOrchestrator(unittest.TestCase):
    """Unit tests for the orchestrator, doc visualizer, solution council, and coding engine."""

    def test_doc_visualizer_rendering(self):
        """Verifies DocVisualizer renders clean PNG visual diagrams."""
        out_dir = "pipeline/specs/test_assets" if os.path.exists("pipeline/specs") else "specs/test_assets"
        os.makedirs(out_dir, exist_ok=True)

        flow_path = os.path.join(out_dir, "test_flow.png")
        topo_path = os.path.join(out_dir, "test_topo.png")
        kpi_path = os.path.join(out_dir, "test_kpi.png")

        # 1. Flowchart
        DocVisualizer.render_flowchart([
            ("Stage 1: Probe", "Passive packet sniffing"),
            ("Stage 2: Correlate", "Graph attention neural net"),
            ("Stage 3: Export", "Cryptographic proof bundle")
        ], flow_path, title="TEST PIPELINE FLOW")
        self.assertTrue(os.path.exists(flow_path))
        with Image.open(flow_path) as im:
            self.assertEqual(im.size, (1600, 420))

        # 2. Topology
        DocVisualizer.render_architecture_topology([
            {"name": "Tier 1: Ingestion", "nodes": ["Tor Feed", "Kafka"]},
            {"name": "Tier 2: AI Core", "nodes": ["PyTorch GNN", "ChromaDB"]}
        ], topo_path, title="TEST TOPOLOGY")
        self.assertTrue(os.path.exists(topo_path))

        # 3. KPI Dashboard
        DocVisualizer.render_kpi_dashboard([
            {"number": "99.4%", "label": "Precision", "delta": "+5.2%"},
            {"number": "42ms", "label": "Latency", "delta": "Sub-50ms"}
        ], kpi_path, title="TEST METRICS")
        self.assertTrue(os.path.exists(kpi_path))

        # Cleanup test images and directory
        for p in [flow_path, topo_path, kpi_path]:
            if os.path.exists(p):
                os.remove(p)
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir, ignore_errors=True)

    def test_solution_council_dossier_and_memory(self):
        """Verifies SolutionCouncil formulates solution, renders visuals, and records to Memory Vault."""
        out_dir = "docs/dossiers/test_council"
        res = SolutionCouncil.formulate_solution(
            problem_title="SIH-2026: Satellite Fire Early Warning",
            problem_text="High altitude thermal imaging for forest wildfire triage.",
            domain="Clean Energy & Space",
            output_dir=out_dir,
            persist_to_docs=False
        )

        dossier_path = res["dossier_path"]
        self.assertTrue(os.path.exists(dossier_path))
        with open(dossier_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check visual diagrams embedded natively
        self.assertIn("System Architecture Topology", content)
        self.assertIn("Forensic Workflow Pipeline", content)
        self.assertIn("Empirical Performance Dashboard", content)

        # Check Memory Vault was updated
        mem_res = TaskDispatcher.dispatch("memory", query="Satellite")
        self.assertGreater(len(mem_res["matches"]), 0)

        # Cleanup dossier
        import shutil
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir, ignore_errors=True)

    def test_coding_engine_tdd_self_healing_loop(self):
        """Simulates an autonomous TDD loop where iteration 1 fails and iteration 2 self-heals to green."""
        test_file = "pipeline/tests/scratch_tdd_test.py" if os.path.exists("pipeline/tests") else "tests/scratch_tdd_test.py"
        impl_file = "src/scratch_math.py"

        test_code = """import unittest
from src.scratch_math import calculate_risk_score

class TestScratchMath(unittest.TestCase):
    def test_risk_score(self):
        self.assertEqual(calculate_risk_score(10, 5), 50)
        self.assertEqual(calculate_risk_score(0, 5), 0)
        self.assertEqual(calculate_risk_score(-2, 4), -8)
"""

        # Generator returns buggy code on iter 1, fixed code on iter 2
        def dynamic_code_generator(iteration: int, error_msg: str):
            if iteration == 1:
                return "def calculate_risk_score(a, b):\n    return a + b  # Bug: returns 15 instead of 50\n"
            else:
                return "def calculate_risk_score(a, b):\n    return a * b  # Fixed: returns 50\n"

        metrics = CodingEngine.execute_tdd_loop(
            module_name="scratch_math",
            test_file_path=test_file,
            test_code=test_code,
            impl_file_path=impl_file,
            impl_code_generator=dynamic_code_generator,
            max_healing_passes=3
        )

        self.assertIn(metrics["status"], ["VERIFIED_GREEN", "VERIFIED_GREEN_MUTATION_SURVIVABLE"])
        self.assertEqual(metrics["healing_iterations_needed"], 2)

        # Cleanup scratch files
        for p in [test_file, impl_file, "pipeline/specs/benchmark_metrics.json", "specs/benchmark_metrics.json"]:
            if os.path.exists(p):
                os.remove(p)

    def test_task_dispatcher_individual_routes(self):
        """Verifies TaskDispatcher executes individual tasks cleanly."""
        # Task 3: Presentation route (PPTX first)
        res = TaskDispatcher.dispatch(
            task="presentation",
            prompt="Autonomous Medical Diagnostics Platform",
            theme="modern_saas_glass",
            slides=4,
            output_pptx="pipeline/specs/presentations/test_dispatcher_deck.pptx" if os.path.exists("pipeline/specs") else "specs/presentations/test_dispatcher_deck.pptx",
            export_pdf=False
        )
        self.assertEqual(res["slides_count"], 4)
        self.assertTrue(os.path.exists(res["pptx_path"]))
        self.assertIsNone(res["pdf_path"])  # PDF must NOT be created!

        # Cleanup
        if os.path.exists(res["pptx_path"]):
            os.remove(res["pptx_path"])


if __name__ == "__main__":
    unittest.main()
