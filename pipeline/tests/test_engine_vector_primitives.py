"""
Test Suite for Presentation Engine Phase 5:
Computer-Vision QA Gate, Closed-Loop Auto-Corrector, and Unstructured Research Chat Ingestion.
"""

import unittest
import os
import shutil
from scripts.engine.themes import THEMES, get_theme
from scripts.engine.vision_qa_gate import VisionQAGate, VisionAuditReport
from scripts.engine.auto_corrector import AutoCorrector
from scripts.engine.chat_research_parser import ChatResearchParser
from scripts.engine.agent_creator import AgentDeckCreator


class TestEnginePhase5(unittest.TestCase):

    def test_wcag_contrast_auditor(self):
        """Validates that all theme presets achieve WCAG compliant contrast ratios."""
        for name, theme in THEMES.items():
            results = VisionQAGate.audit_theme_contrast(theme)
            failures = [r for r in results if not r.passed]
            self.assertEqual(
                len(failures), 0,
                f"Theme '{name}' failed WCAG contrast on: {[(f.element_name, f.ratio, f.required_ratio) for f in failures]}"
            )

    def test_vector_collision_and_margin_audit_existing_decks(self):
        """Audits compiled PDF decks for text bounding-box collisions and margin bounds."""
        pdf_path = "specs/presentations/deck_cyber_dark_agent.pdf"
        if os.path.exists(pdf_path):
            report = VisionQAGate.audit_pdf_and_rendered_deck(
                pdf_path=pdf_path,
                theme_name="cyber_dark_terminal"
            )
            self.assertTrue(report.passed, f"Vision QA failed on cyber dark deck: {report.summary_text}")
            self.assertEqual(report.total_collisions, 0)
            self.assertEqual(report.total_margin_violations, 0)

        sih_pdf = "specs/presentations/deck_sih_light_agent.pdf"
        if os.path.exists(sih_pdf):
            report_sih = VisionQAGate.audit_pdf_and_rendered_deck(
                pdf_path=sih_pdf,
                theme_name="sih_institutional_light"
            )
            self.assertTrue(report_sih.passed, f"Vision QA failed on SIH light deck: {report_sih.summary_text}")
            self.assertEqual(report_sih.total_collisions, 0)
            self.assertEqual(report_sih.total_margin_violations, 0)

    def test_chat_research_parser_ingestion(self):
        """Tests parsing technical chat dump using ChatResearchParser."""
        sample_chat = """
        Team Name: Project Alpha
        Problem Title: Autonomous Edge Infrastructure
        Citations:
        - RFC-8999: Zero-Trust Telemetry
        - NIST SP 800-207: Zero Trust Architecture
        Technologies: Python, TypeScript, SQLite
        Architecture Tiers:
        - Tier 1: Ingestion Gateway
        - Tier 2: Analytical Consensus
        - Tier 3: Immutable Vault
        """
        spec = ChatResearchParser.parse_research_text(sample_chat)
        self.assertIn("team_name", spec)
        self.assertIn("problem_title", spec)
        self.assertIn("citations", spec)
        self.assertIn("technologies", spec)
        self.assertIn("architecture_tiers", spec)
        self.assertGreaterEqual(len(spec["citations"]), 2)
        self.assertGreaterEqual(len(spec["architecture_tiers"]), 3)

    def test_end_to_end_research_to_championship_deck(self):
        """
        Synthesizes a 6-slide deck from structured spec, runs the closed-loop
        auto-corrector, and verifies 0 defects via Vision QA Gate.
        """
        fallback_spec = {
            "team_name": "TEMPLATETEAM",
            "team_subtitle": "(Autonomous)",
            "problem_id": "TEMPLATE-01",
            "problem_title": "Enterprise Agentic Platform",
            "solution_title": "Autonomous Verification & Self-Healing Pipeline",
            "citations": ["Citation A", "Citation B"],
            "technologies": ["Python", "Node.js"],
            "architecture_tiers": [
                {"name": "Tier 1: Ingestion", "nodes": [{"name": "API Gateway", "bullets": ["Ingress"]}]},
                {"name": "Tier 2: Consensus", "nodes": [{"name": "Logic Engine", "bullets": ["Validation"]}]},
                {"name": "Tier 3: Persistence", "nodes": [{"name": "Memory Vault", "bullets": ["Storage"]}]}
            ]
        }
        spec = ChatResearchParser.parse_research_text("", fallback_spec=fallback_spec)

        out_pptx = "specs/presentations/deck_template_research_agent.pptx"
        out_pdf = "specs/presentations/deck_template_research_agent.pdf"
        render_dir = "specs/presentations/rendered/template_research"

        manifest = AgentDeckCreator.synthesize_manifest_from_spec(spec, theme_name="cyber_dark_terminal")

        # Run closed-loop auto-corrector
        healed_manifest, layout_audit, vision_audit, images = AutoCorrector.self_heal_deck(
            manifest=manifest,
            output_pptx_path=out_pptx,
            output_pdf_path=out_pdf,
            render_dir=render_dir,
            max_iterations=3,
            dpi=200
        )

        self.assertTrue(os.path.exists(out_pptx))
        self.assertTrue(os.path.exists(out_pdf))
        if os.path.exists(out_pptx):
            os.remove(out_pptx)
        if os.path.exists(out_pdf):
            os.remove(out_pdf)
        if os.path.exists(render_dir):
            shutil.rmtree(render_dir, ignore_errors=True)
        self.assertEqual(len(images), 6)
        self.assertTrue(layout_audit.passed, f"Layout audit failed: {layout_audit.violations}")
        self.assertTrue(vision_audit.passed, f"Vision QA failed: {vision_audit.summary_text}")
        self.assertEqual(vision_audit.total_collisions, 0)
        self.assertEqual(vision_audit.total_margin_violations, 0)

        # Cleanup transient test presentation & render directory
        for p in [out_pptx, out_pdf]:
            if os.path.exists(p):
                os.remove(p)
        if os.path.exists(render_dir):
            shutil.rmtree(render_dir, ignore_errors=True)
