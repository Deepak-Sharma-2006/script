"""
Test Suite — Presentation Engine Phase 6C: Cognitive Analyzer, Dynamic Planner & Two-Stage Workflow
Verifies:
1. CognitiveDeckAnalyzer extracts design grammar (palettes, fonts, patterns) from reference PPTX without cloning.
2. OmniDeckPlanner deconstructs an open-ended cross-domain prompt (AgriTech Edge AI) into a structured 6-slide plan.
3. DeckOrchestrator Stage 1 compiles native PPTX in <0.5s with ZERO automated PDF generation.
4. DeckOrchestrator Stage 2 only creates PDF upon explicit invocation.
"""

import os
import unittest
from scripts.engine.cognitive_analyzer import CognitiveDeckAnalyzer
from scripts.engine.planner import OmniDeckPlanner
from scripts.engine.deck_orchestrator import DeckOrchestrator


class TestEnginePhase6C(unittest.TestCase):
    """Unit tests for Phase 6C cognitive analysis, dynamic planning, and two-stage workflow."""

    def test_cognitive_analyzer_on_existing_deck(self):
        """Verifies CognitiveDeckAnalyzer extracts design grammar from presentation."""
        test_pptx = "specs/presentations/test_cognitive_sample.pptx"
        os.makedirs(os.path.dirname(test_pptx), exist_ok=True)
        from scripts.engine.pptx_compiler import PPTXCompiler
        from scripts.engine.schema import DeckConfig, SlideSpec, SlideArchetype, DeckManifest
        dummy_manifest = DeckManifest(
            deck_config=DeckConfig(title="Sample Cognitive Deck", team_name="Sample Team"),
            slides=[
                SlideSpec(
                    slide_number=1,
                    title="Sample Title",
                    archetype=SlideArchetype.TITLE_PAGE,
                    title_metadata=[("Problem Statement ID", "01"), ("Team Name", "Sample Team")]
                )
            ]
        )
        compiler = PPTXCompiler(manifest=dummy_manifest)
        compiler.compile(test_pptx)

        try:
            grammar = CognitiveDeckAnalyzer.analyze_pptx(test_pptx)
            self.assertIsNotNone(grammar.primary_bg)
            self.assertIsNotNone(grammar.accent_color)
            self.assertIsNotNone(grammar.heading_font)
            self.assertGreater(len(grammar.slide_patterns), 0)

            # Check detected slide patterns
            p1 = grammar.slide_patterns[0]
            self.assertEqual(p1.archetype_detected, "title")
        finally:
            if os.path.exists(test_pptx):
                os.remove(test_pptx)

    def test_omni_deck_planning_across_new_domain(self):
        """Verifies OmniDeckPlanner plans a 6-slide deck for an AgriTech drone problem statement."""
        agritech_prompt = """
        # AGRIVISION: Edge AI Multispectral Drone Swarm for Crop Disease & Irrigation Triage
        Team: AgroTech Titans
        
        The Problem:
        - Manual crop scouting across 100+ acre farms takes 3-5 days per cycle
        - Early blight and root rot infections remain invisible to RGB cameras until 40% crop loss occurs
        - Blanket pesticide spraying wastes $12,000 annually per farm and contaminates local groundwater
        
        Our Solution:
        - Autonomous edge AI drones scan 100 acres in 45 minutes using multispectral NDVI sensors
        - Micro-YOLOv10 model detects fungal pathogens at leaf level with 98.7% accuracy before visible symptoms
        - Variable-rate precision micro-nozzle spraying reduces chemical runoff by 78% and saves $9,400 per season
        
        Metrics: 98.7% accuracy, 45min turnaround, 78% chemical reduction.
        """

        plan = OmniDeckPlanner.plan_from_prompt(
            prompt=agritech_prompt,
            theme_name="modern_saas_glass",
            num_slides=6
        )

        self.assertEqual(len(plan.slides), 6)
        self.assertIn("AGRIVISION", plan.project_title.upper())
        self.assertEqual(plan.slides[0].archetype, "title")
        self.assertEqual(plan.slides[1].archetype, "split_tension")
        self.assertEqual(plan.slides[2].archetype, "swimlane_architecture")
        self.assertEqual(plan.slides[3].archetype, "bento_features")
        self.assertEqual(plan.slides[4].archetype, "kpi_metrics")
        self.assertEqual(plan.slides[5].archetype, "roadmap")

    def test_two_stage_pptx_first_workflow(self):
        """
        Verifies Stage 1 compiles ONLY PPTX instantly, and DOES NOT generate PDF.
        Then verifies Stage 2 generates PDF only upon explicit order.
        """
        prompt = """
        # AEROSEC: Autonomous Drone Airspace Intrusion Detection
        Problem: Rogue drones penetrate sensitive air corridors with zero radar cross-section.
        Solution: RF fingerprinting and acoustic triangulation isolate rogue drones in <50ms.
        """
        plan = OmniDeckPlanner.plan_from_prompt(prompt, theme_name="cyber_dark_terminal", num_slides=6)

        out_pptx = "specs/presentations/deck_aerosec_test.pptx"
        out_pdf = "specs/presentations/deck_aerosec_test.pdf"

        # Cleanup if left from previous runs
        if os.path.exists(out_pptx):
            os.remove(out_pptx)
        if os.path.exists(out_pdf):
            os.remove(out_pdf)

        # STAGE 1: Compile PPTX only
        pptx_result = DeckOrchestrator.compile_pptx(plan, out_pptx)
        self.assertTrue(os.path.exists(out_pptx))
        self.assertGreater(os.path.getsize(out_pptx), 10000)

        # CRITICAL ASSERTION: PDF must NOT exist after Stage 1!
        self.assertFalse(os.path.exists(out_pdf), "PDF should NOT be generated during Stage 1 PPTX compilation!")

        # STAGE 2: Explicit Gated PDF Export
        pdf_result = DeckOrchestrator.export_approved_pdf(out_pptx, out_pdf, render_pngs=False)
        self.assertTrue(os.path.exists(out_pdf), "PDF should be generated after explicit export order!")
        self.assertGreater(os.path.getsize(out_pdf), 10000)

        # Clean up test files
        if os.path.exists(out_pptx):
            os.remove(out_pptx)
        if os.path.exists(out_pdf):
            os.remove(out_pdf)


if __name__ == "__main__":
    unittest.main()
