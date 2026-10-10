"""
Presentation Engine — Closed-Loop Auto-Corrector
Provides self-healing optimization on slide manifests when visual layout collisions or density warnings are detected.
"""

import os
from typing import Tuple, List, Optional
from scripts.engine.schema import (
    DeckManifest, SlideSpec, TaggedBulletListSpec, MultiSectionColumnSpec
)
from scripts.engine.pptx_compiler import PPTXCompiler
from scripts.engine.render_bridge import RenderBridge
from scripts.engine.visual_auditor import VisualAuditor, DeckAuditReport
from scripts.engine.vision_qa_gate import VisionQAGate, VisionAuditReport


class AutoCorrector:
    """
    Closed-loop iterative self-correction engine for presentations.
    """

    @classmethod
    def tune_slide_typography(cls, slide: SlideSpec, font_delta: float = -0.5, space_delta: float = -0.5):
        """Reduces typography scale and paragraph padding on a slide."""
        cols = [slide.left_column, slide.right_column, slide.top_left, slide.top_right, slide.bottom_section]
        for c in cols:
            if not c:
                continue
            # Tagged bullet lists
            for key in ["component", "top_component"]:
                if key in c and isinstance(c[key], TaggedBulletListSpec):
                    spec: TaggedBulletListSpec = c[key]
                    spec.body_font_size = max(7.0, spec.body_font_size + font_delta)
                    spec.title_font_size = max(10.0, spec.title_font_size + font_delta)
                    spec.space_after_pt = max(1.0, spec.space_after_pt + space_delta)

            # Multi section columns
            for key in ["component", "top_component"]:
                if key in c and isinstance(c[key], MultiSectionColumnSpec):
                    ms_spec: MultiSectionColumnSpec = c[key]
                    for sec in ms_spec.sections:
                        sec.heading_font_size = max(8.0, sec.heading_font_size + font_delta)
                        sec.space_before_pt = max(1.0, sec.space_before_pt + space_delta)
                        sec.space_after_pt = max(1.0, sec.space_after_pt + space_delta)

    @classmethod
    def self_heal_deck(
        cls,
        manifest: DeckManifest,
        output_pptx_path: str,
        output_pdf_path: str,
        render_dir: str,
        max_iterations: int = 3,
        dpi: int = 200
    ) -> Tuple[DeckManifest, DeckAuditReport, VisionAuditReport, List[str]]:
        """
        Executes an iterative compile-audit-heal feedback loop.
        """
        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            # 1. Pre-render Layout Audit
            layout_audit = VisualAuditor.audit_deck(manifest)

            # 2. Compile to PPTX
            compiler = PPTXCompiler(manifest)
            compiler.compile(output_pptx_path)

            # 3. Export PDF & Render PNGs
            bridge = RenderBridge()
            bridge.export_pptx_to_pdf(output_pptx_path, output_pdf_path)
            images = bridge.render_pdf_to_images(output_pdf_path, render_dir, dpi=dpi)

            # 4. Computer-Vision & Vector Audit
            vision_audit = VisionQAGate.audit_pdf_and_rendered_deck(
                pdf_path=output_pdf_path,
                image_paths=images,
                theme_name=manifest.deck_config.theme_name
            )

            # Check if 100% clean
            if layout_audit.passed and vision_audit.passed:
                print(f"[AutoCorrector] Deck verified 100% clean on iteration {iteration}!")
                return manifest, layout_audit, vision_audit, images

            print(f"[AutoCorrector] Iteration {iteration}: Flagged {len(layout_audit.violations)} layout violations, "
                  f"{vision_audit.total_collisions} text collisions, {vision_audit.total_margin_violations} margin overflows. Self-healing...")

            # Self-heal flagged slides
            for p_rep in vision_audit.page_reports:
                if not p_rep.passed:
                    slide_idx = p_rep.page_number - 1
                    if slide_idx < len(manifest.slides):
                        cls.tune_slide_typography(manifest.slides[slide_idx], font_delta=-0.5, space_delta=-0.5)

            for s_res in layout_audit.slide_results:
                if s_res.density_status == "OVERCROWDED":
                    slide_idx = s_res.slide_number - 1
                    if slide_idx < len(manifest.slides):
                        cls.tune_slide_typography(manifest.slides[slide_idx], font_delta=-0.5, space_delta=-1.0)

        # Return final state after max iterations
        return manifest, layout_audit, vision_audit, images
