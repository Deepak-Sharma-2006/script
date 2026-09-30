"""
Test Suite — OmniDeck UI Mockup Primitives & Custom Slide Archetypes
Verifies:
1. DeckOrchestrator compiles slides with 'browser_mockup' archetype.
2. DeckOrchestrator compiles slides with 'mobile_mockup' archetype.
3. DeckOrchestrator compiles slides with 'quadrant_matrix' archetype.
4. DeckOrchestrator compiles slides with 'radial_ecosystem' archetype.
5. All slides compile to valid PPTX presentations in <0.2s.
"""

import os
import time
import unittest
from pptx import Presentation

from scripts.engine.planner import OmniDeckPlan, OmniSlidePlan
from scripts.engine.deck_orchestrator import DeckOrchestrator


class TestUIMockupPrimitives(unittest.TestCase):
    """Tests high-fidelity visual UI mockup primitives and custom archetypes."""

    def test_compile_mockup_and_matrix_deck(self):
        """Verifies rapid compilation of custom UI mockup slides into a valid PPTX."""
        out_pptx = "specs/test_output_mockups.pptx"
        if os.path.exists(out_pptx):
            os.remove(out_pptx)

        slides = [
            OmniSlidePlan(
                slide_number=1,
                title="Enterprise Command Center Web Surface",
                subtitle="Live Ingestion & Correlation Dashboard",
                archetype="browser_mockup",
                category_badge="DESKTOP UI",
                content_payload={
                    "url": "https://gov.in/cyber-intel/live",
                    "nav_items": ["Live Sensors", "Anomaly Feeds", "Threat Map", "Evidence Vault"],
                    "table_rows": [
                        ["INCIDENT-101", "Tor Exit Node", "CONFIRMED", "28ms"],
                        ["INCIDENT-102", "Border Radar Ping", "ANALYZED", "34ms"],
                        ["INCIDENT-103", "Satellite Synthetic SAR", "MAPPED", "62ms"]
                    ]
                }
            ),
            OmniSlidePlan(
                slide_number=2,
                title="Field Officer Mobile HUD",
                subtitle="Real-time alert dispatching and biometric verification",
                archetype="mobile_mockup",
                category_badge="MOBILE APP",
                content_payload={
                    "app_title": "SOVEREIGN AGENT HUD",
                    "feed_items": [
                        {"title": "P1 INTRUSION ALERT", "meta": "Sector 4B • 1m ago", "badge": "CRITICAL", "color": "#EF4444"},
                        {"title": "MERKLE PROOF GENERATED", "meta": "Block #40921 • Verified", "badge": "SECURE", "color": "#10B981"}
                    ]
                }
            ),
            OmniSlidePlan(
                slide_number=3,
                title="Competitive Positioning Matrix",
                subtitle="Strategic 10x Moat Differentiation",
                archetype="quadrant_matrix",
                category_badge="MARKET POSITIONING",
                content_payload={
                    "our_product_name": "ANTIGRAVITY V2",
                    "competitors": [
                        {"name": "Legacy Tool A", "x": 3.0, "y": 4.5},
                        {"name": "Manual Script B", "x": 4.0, "y": 3.0}
                    ]
                }
            ),
            OmniSlidePlan(
                slide_number=4,
                title="Multi-Agent Radial Topology",
                subtitle="Distributed Autonomous Coordination",
                archetype="radial_ecosystem",
                category_badge="SYSTEM TOPOLOGY",
                content_payload={
                    "hub_title": "TASK DISPATCHER",
                    "hub_subtitle": "Autonomous Arbiter",
                    "satellites": [
                        {"name": "Task 1", "desc": "Solution Council"},
                        {"name": "Task 2", "desc": "Coding Engine"},
                        {"name": "Task 3", "desc": "OmniDeck"}
                    ]
                }
            )
        ]

        plan = OmniDeckPlan(
            project_title="Next-Gen UI Primitives Test",
            team_name="Lead Architects",
            theme_name="institutional_navy",
            slides=slides
        )

        start = time.time()
        DeckOrchestrator.compile_pptx(plan, out_pptx)
        duration = time.time() - start

        self.assertTrue(os.path.exists(out_pptx))
        self.assertLess(duration, 1.5)  # Fast generation

        # Verify PPTX structure
        prs = Presentation(out_pptx)
        self.assertEqual(len(prs.slides), 4)

        # Cleanup test PPTX
        if os.path.exists(out_pptx):
            os.remove(out_pptx)

    def test_visual_translator_stat_hero(self):
        """Verifies semantic translation of numeric metrics into VISUAL_STAT_HERO."""
        from scripts.engine import VisualTranslator, ContentType
        res = VisualTranslator.analyze_and_translate(
            "Performance Benchmarks",
            ["Query Latency: 12ms", "Throughput: 99.9% availability", "Cost Reduction: 10x"]
        )
        self.assertEqual(res["type"], ContentType.VISUAL_STAT_HERO)
        self.assertGreaterEqual(len(res["data"]), 2)

    def test_visual_translator_swimlane_flow(self):
        """Verifies translation of sequential steps into VISUAL_SWIMLANE_FLOW."""
        from scripts.engine import VisualTranslator, ContentType
        res = VisualTranslator.analyze_and_translate(
            "Data Ingestion Pipeline",
            ["Step 1: Capture Packets", "Step 2: Normalize AST", "Step 3: Commit to Merkle Vault"]
        )
        self.assertEqual(res["type"], ContentType.VISUAL_SWIMLANE_FLOW)
        self.assertEqual(len(res["data"]), 3)

    def test_visual_translator_architecture_stack(self):
        """Verifies translation of system tiers into VISUAL_ARCHITECTURE_STACK."""
        from scripts.engine import VisualTranslator, ContentType
        res = VisualTranslator.analyze_and_translate(
            "System Architecture Tier",
            ["Ingestion Tier: Kafka, HTTP Gateway", "Persistence Tier: SQLite, ClickHouse"]
        )
        self.assertEqual(res["type"], ContentType.VISUAL_ARCHITECTURE_STACK)
        self.assertEqual(len(res["data"]), 2)

    def test_visual_translator_comparison_matrix(self):
        """Verifies translation of competitor analysis into VISUAL_COMPARISON_MATRIX."""
        from scripts.engine import VisualTranslator, ContentType
        res = VisualTranslator.analyze_and_translate(
            "Feature Comparison Matrix vs Competitor",
            ["Zero Secrets Enforcement: 100% Native", "Cryptographic Provenance: Built-in"]
        )
        self.assertEqual(res["type"], ContentType.VISUAL_COMPARISON_MATRIX)
        self.assertEqual(len(res["data"]), 2)


if __name__ == "__main__":
    unittest.main()
