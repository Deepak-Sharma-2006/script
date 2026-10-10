"""
Presentation Engine — Native PPTX Compiler
Compiles declarative DeckManifest and resolved layout geometries into native PowerPoint (.pptx) presentations.
"""

import os
from typing import Dict, Any, List, Optional
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

from scripts.engine.schema import (
    DeckManifest, SlideSpec, SlideArchetype, TaggedBulletListSpec,
    MultiSectionColumnSpec, CalloutCardSpec, ProjectLinksCardSpec,
    TableSpec, TechGridSpec, CompetitorMatrixSpec,
    ArchitectureDiagramSpec, ChevronPipelineSpec, StatGridSpec
)
from scripts.engine.layout_solver import LayoutSolver, Rect
from scripts.engine.diagram_generator import DiagramGenerator
from scripts.engine.themes import Theme, get_theme


def hex_to_rgb(hex_str: str) -> RGBColor:
    hex_clean = hex_str.lstrip('#')
    return RGBColor(*(int(hex_clean[i:i+2], 16) for i in (0, 2, 4)))


class PPTXCompiler:
    """
    Translates a DeckManifest and LayoutSolver geometries into native PowerPoint slides.
    """

    def __init__(self, manifest: DeckManifest):
        self.manifest = manifest
        self.config = manifest.deck_config
        self.theme: Theme = get_theme(self.config.theme_name)
        self.colors = self.config.colors
        
        self.prs = Presentation()
        self.prs.slide_width = Inches(self.config.slide_width_inches)
        self.prs.slide_height = Inches(self.config.slide_height_inches)
        self.blank_layout = self.prs.slide_layouts[6]

    def add_header_footer(self, slide, title_text: str, slide_number: int):
        """Adds official team badge, center category title, small SIH logo, and bottom ribbon."""
        # Top-Left Team Oval
        oval = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.40), Inches(0.32), Inches(1.80), Inches(0.85)
        )
        oval.fill.solid()
        oval.fill.fore_color.rgb = hex_to_rgb(self.theme.team_badge_bg)
        oval.line.color.rgb = hex_to_rgb(self.theme.team_badge_border)
        oval.line.width = Pt(2.5)

        tf = oval.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = self.config.team_name
        p.font.name = self.theme.font_body
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = hex_to_rgb(self.theme.team_badge_text)
        p.alignment = PP_ALIGN.CENTER

        if self.config.team_subtitle:
            p2 = tf.add_paragraph()
            p2.text = self.config.team_subtitle
            p2.font.name = self.theme.font_body
            p2.font.size = Pt(11)
            p2.font.bold = True
            p2.font.color.rgb = hex_to_rgb(self.theme.bullet_accent)
            p2.alignment = PP_ALIGN.CENTER

        # Top Center Category Title
        tb = slide.shapes.add_textbox(Inches(2.40), Inches(0.35), Inches(8.50), Inches(0.80))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = self.theme.font_title
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = hex_to_rgb(self.theme.header_title_color)
        p.alignment = PP_ALIGN.CENTER

        # Top Right SIH Logo
        if self.config.sih_logo_small and os.path.exists(self.config.sih_logo_small):
            slide.shapes.add_picture(
                self.config.sih_logo_small,
                Inches(11.20), Inches(0.18), width=Inches(1.80), height=Inches(0.84)
            )

        # Bottom Footer Ribbon
        banner = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(7.00), Inches(self.config.slide_width_inches), Inches(0.50)
        )
        banner.fill.solid()
        banner.fill.fore_color.rgb = hex_to_rgb(self.theme.footer_bg)
        banner.line.fill.background()

        tf = banner.text_frame
        p = tf.paragraphs[0]
        p.text = self.config.footer_text
        p.font.name = self.theme.font_body
        p.font.size = Pt(13)
        p.font.color.rgb = hex_to_rgb(self.theme.footer_text)
        p.alignment = PP_ALIGN.CENTER

        # Slide Number Right
        num_box = slide.shapes.add_textbox(Inches(12.20), Inches(7.00), Inches(1.00), Inches(0.50))
        tf_n = num_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = str(slide_number)
        p_n.font.name = self.theme.font_body
        p_n.font.size = Pt(14)
        p_n.font.bold = True
        p_n.font.color.rgb = hex_to_rgb(self.theme.footer_text)
        p_n.alignment = PP_ALIGN.RIGHT

    def render_tagged_bullets(self, slide, rect: Rect, spec: TaggedBulletListSpec):
        """Renders tagged bullets with dynamic text fitting to guarantee no vertical overflow."""
        tb = slide.shapes.add_textbox(Inches(rect.x), Inches(rect.y), Inches(rect.w), Inches(rect.h))
        tf = tb.text_frame
        tf.word_wrap = True

        # Compute dynamic text fitting
        paragraphs_data = []
        for it in spec.items:
            combined_txt = f"{it.tag} {it.body}"
            paragraphs_data.append({"text": combined_txt, "is_bold": False})

        # Reserve ~0.45" for title
        available_body_h = max(1.0, rect.h - 0.50)
        opt_font_size, opt_space_after, _ = LayoutSolver.fit_text_block(
            paragraphs_data,
            container_width=rect.w,
            max_height=available_body_h,
            base_font_size=spec.body_font_size,
            min_font_size=7.5,
            base_space_after=spec.space_after_pt
        )

        # Title
        p_title = tf.paragraphs[0]
        p_title.text = spec.title
        p_title.font.name = self.theme.font_body
        p_title.font.size = Pt(spec.title_font_size)
        p_title.font.bold = True
        p_title.font.color.rgb = hex_to_rgb(spec.title_color or self.theme.bullet_accent)
        p_title.space_after = Pt(4.0)

        # Items
        for it in spec.items:
            p = tf.add_paragraph()
            p.space_after = Pt(opt_space_after)

            run_bullet = p.add_run()
            run_bullet.text = "• "
            run_bullet.font.name = self.theme.font_body
            run_bullet.font.size = Pt(opt_font_size)
            run_bullet.font.bold = True
            run_bullet.font.color.rgb = hex_to_rgb(self.theme.bullet_accent)

            run_tag = p.add_run()
            run_tag.text = it.tag + " " if not it.tag.endswith(" ") else it.tag
            run_tag.font.name = self.theme.font_body
            run_tag.font.size = Pt(opt_font_size + 0.5)
            run_tag.font.bold = True
            run_tag.font.color.rgb = hex_to_rgb(self.theme.title_primary)

            run_body = p.add_run()
            run_body.text = it.body
            run_body.font.name = self.theme.font_body
            run_body.font.size = Pt(opt_font_size)
            run_body.font.color.rgb = hex_to_rgb(self.theme.body_text)

    def render_multi_section_column(self, slide, rect: Rect, spec: MultiSectionColumnSpec):
        """Renders multiple subheadings with dynamic text fitting."""
        tb = slide.shapes.add_textbox(Inches(rect.x), Inches(rect.y), Inches(rect.w), Inches(rect.h))
        tf = tb.text_frame
        tf.word_wrap = True

        all_paras = []
        for sec in spec.sections:
            all_paras.append({"text": sec.heading, "is_bold": True})
            for it in sec.items:
                all_paras.append({"text": it, "is_bold": False})

        opt_font, opt_space, _ = LayoutSolver.fit_text_block(
            all_paras,
            container_width=rect.w,
            max_height=rect.h,
            base_font_size=8.5,
            min_font_size=7.5,
            base_space_after=1.0
        )

        is_first = True
        for sec in spec.sections:
            p_hdr = tf.paragraphs[0] if is_first else tf.add_paragraph()
            is_first = False
            p_hdr.space_before = Pt(sec.space_before_pt)
            p_hdr.space_after = Pt(sec.space_after_pt)
            p_hdr.text = sec.heading
            p_hdr.font.name = self.theme.font_body
            p_hdr.font.size = Pt(sec.heading_font_size)
            p_hdr.font.bold = True
            p_hdr.font.color.rgb = hex_to_rgb(self.theme.title_primary)

            for it in sec.items:
                p_it = tf.add_paragraph()
                p_it.space_after = Pt(opt_space)
                p_it.text = "• " + it if not it.startswith("•") else it
                p_it.font.name = self.theme.font_body
                p_it.font.size = Pt(opt_font)
                p_it.font.color.rgb = hex_to_rgb(self.theme.body_text)

    def render_callout_card(self, slide, rect: Rect, spec: CalloutCardSpec):
        """Renders an styled callout card with theme integration."""
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(rect.x), Inches(rect.y), Inches(rect.w), Inches(rect.h)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = hex_to_rgb(spec.bg_color or self.theme.callout_bg)
        card.line.color.rgb = hex_to_rgb(spec.border_color or self.theme.callout_border)
        card.line.width = Pt(spec.border_width_pt)

        tf = card.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = spec.title
        p.font.name = self.theme.font_body
        p.font.size = Pt(spec.title_font_size)
        p.font.bold = True
        p.font.color.rgb = hex_to_rgb(self.theme.callout_title)
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(5.0)

        for f in spec.facts:
            pf = tf.add_paragraph()
            pf.space_after = Pt(2.5)
            pf.text = "• " + f if not f.startswith("•") else f
            pf.font.name = self.theme.font_body
            pf.font.size = Pt(spec.fact_font_size)
            pf.font.bold = True
            pf.font.color.rgb = hex_to_rgb(self.theme.callout_text)

    def render_project_links_box(self, slide, rect: Rect, spec: ProjectLinksCardSpec):
        """Renders styled demo link card with theme integration."""
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(rect.x), Inches(rect.y), Inches(rect.w), Inches(rect.h)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = hex_to_rgb(self.theme.demo_card_bg)
        box.line.color.rgb = hex_to_rgb(spec.border_color or self.theme.demo_card_border)
        box.line.width = Pt(spec.border_width_pt)

        tf = box.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = spec.title
        p.font.name = self.theme.font_body
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = hex_to_rgb(self.theme.bullet_accent)
        p.space_after = Pt(4)
        if spec.centered:
            p.alignment = PP_ALIGN.CENTER

        if spec.github_url:
            p_gh = tf.add_paragraph()
            if spec.centered:
                p_gh.alignment = PP_ALIGN.CENTER
            r1 = p_gh.add_run()
            r1.text = "• Github: " if not spec.centered else ""
            r1.font.name = self.theme.font_body
            r1.font.size = Pt(11)
            r1.font.bold = True
            r1.font.color.rgb = hex_to_rgb(self.theme.body_text)
            r2 = p_gh.add_run()
            r2.text = spec.github_url
            r2.font.name = self.theme.font_body
            r2.font.size = Pt(11)
            r2.font.color.rgb = hex_to_rgb(self.theme.demo_link_color)
            r2.font.underline = True

        if spec.demo_url:
            p_dm = tf.add_paragraph()
            if spec.centered:
                p_dm.alignment = PP_ALIGN.CENTER
            r1 = p_dm.add_run()
            r1.text = "• Demo Live Prototype : " if not spec.centered else ""
            r1.font.name = self.theme.font_body
            r1.font.size = Pt(11)
            r1.font.bold = True
            r1.font.color.rgb = hex_to_rgb(self.theme.body_text)
            r2 = p_dm.add_run()
            r2.text = spec.demo_url
            r2.font.name = self.theme.font_body
            r2.font.size = Pt(11)
            r2.font.color.rgb = hex_to_rgb(self.theme.demo_link_color)
            r2.font.underline = True

    def render_table(self, slide, rect: Rect, spec: TableSpec):
        """Renders native PowerPoint table with zebra striping and column distribution."""
        if spec.title:
            tb_hdr = slide.shapes.add_textbox(Inches(rect.x), Inches(rect.y - 0.40), Inches(rect.w), Inches(0.35))
            tf_h = tb_hdr.text_frame
            p_h = tf_h.paragraphs[0]
            p_h.text = spec.title
            p_h.font.name = self.theme.font_body
            p_h.font.size = Pt(16)
            p_h.font.bold = True
            p_h.font.color.rgb = hex_to_rgb(self.theme.bullet_accent)

        num_rows = len(spec.rows) + 1
        num_cols = len(spec.headers)
        table_shape = slide.shapes.add_table(num_rows, num_cols, Inches(rect.x), Inches(rect.y), Inches(rect.w), Inches(rect.h))
        table = table_shape.table

        # Assign column widths
        if spec.col_width_ratios and len(spec.col_width_ratios) == num_cols:
            total_ratio = sum(spec.col_width_ratios)
            for i, r in enumerate(spec.col_width_ratios):
                table.columns[i].width = Inches(rect.w * (r / total_ratio))

        # Header Row
        for col_idx, h_text in enumerate(spec.headers):
            cell = table.cell(0, col_idx)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.fill.solid()
            hdr_bg = self.theme.table_header_bg if spec.header_bg_color == "#0F3A70" else spec.header_bg_color
            cell.fill.fore_color.rgb = hex_to_rgb(hdr_bg)
            p = cell.text_frame.paragraphs[0]
            p.text = h_text
            p.font.name = self.theme.font_body
            p.font.size = Pt(spec.header_font_size)
            p.font.bold = True
            p.font.color.rgb = hex_to_rgb(self.theme.table_header_text)

        # Data Rows
        for row_idx, row_data in enumerate(spec.rows):
            for col_idx, cell_text in enumerate(row_data):
                cell = table.cell(row_idx + 1, col_idx)
                cell.margin_top = Inches(0.04)
                cell.margin_bottom = Inches(0.04)
                cell.margin_left = Inches(0.08)
                cell.margin_right = Inches(0.08)
                cell.fill.solid()
                if (row_idx + 1) % 2 == 1:
                    cell.fill.fore_color.rgb = hex_to_rgb(self.theme.card_bg)
                else:
                    z_bg = self.theme.table_zebra_bg if spec.zebra_bg_color == "#F8FAFC" else spec.zebra_bg_color
                    cell.fill.fore_color.rgb = hex_to_rgb(z_bg)

                p = cell.text_frame.paragraphs[0]
                p.text = cell_text
                p.font.name = self.theme.font_body
                p.font.size = Pt(spec.body_font_size)
                p.font.color.rgb = hex_to_rgb(self.theme.table_cell_text)
                if col_idx == 0 and cell_text != "":
                    p.font.bold = True
                    p.font.color.rgb = hex_to_rgb(self.theme.bullet_accent)

    def render_architecture_diagram(self, slide, rect: Rect, spec: ArchitectureDiagramSpec):
        """Renders a multi-tier microservice architecture diagram using native shapes."""
        layout = DiagramGenerator.solve_architecture_layout(rect, spec)

        # Outer border container
        container = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(layout.outer_rect.x), Inches(layout.outer_rect.y),
            Inches(layout.outer_rect.w), Inches(layout.outer_rect.h)
        )
        container.fill.solid()
        c_bg = self.theme.arch_container_bg if spec.container_bg == "#FFFFFF" else spec.container_bg
        c_border = self.theme.arch_container_border if spec.container_border == "#94A3B8" else spec.container_border
        container.fill.fore_color.rgb = hex_to_rgb(c_bg)
        container.line.color.rgb = hex_to_rgb(c_border)
        container.line.width = Pt(1.5)

        # Optional Title
        if layout.title_rect and spec.title:
            tb = slide.shapes.add_textbox(
                Inches(layout.title_rect.x), Inches(layout.title_rect.y),
                Inches(layout.title_rect.w), Inches(layout.title_rect.h)
            )
            p = tb.text_frame.paragraphs[0]
            p.text = "• " + spec.title
            p.font.name = self.theme.font_body
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = hex_to_rgb(self.theme.bullet_accent)

        # Tiers
        for tier_geom in layout.tiers:
            # Tier boundary box
            t_box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(tier_geom.tier_rect.x), Inches(tier_geom.tier_rect.y),
                Inches(tier_geom.tier_rect.w), Inches(tier_geom.tier_rect.h)
            )
            t_box.fill.solid()
            t_bg = self.theme.tier_card_bg if tier_geom.tier_spec.tier_bg == "#F8FAFC" else tier_geom.tier_spec.tier_bg
            t_border = self.theme.tier_card_border if tier_geom.tier_spec.border_color == "#CBD5E1" else tier_geom.tier_spec.border_color
            t_box.fill.fore_color.rgb = hex_to_rgb(t_bg)
            t_box.line.color.rgb = hex_to_rgb(t_border)
            t_box.line.width = Pt(1.0)

            # Tier header banner
            h_box = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(tier_geom.header_rect.x), Inches(tier_geom.header_rect.y),
                Inches(tier_geom.header_rect.w), Inches(tier_geom.header_rect.h)
            )
            h_box.fill.solid()
            h_bg = self.theme.tier_header_bg if tier_geom.tier_spec.header_bg == "#1E293B" else tier_geom.tier_spec.header_bg
            h_text_col = self.theme.tier_header_text if tier_geom.tier_spec.header_text_color == "#FFFFFF" else tier_geom.tier_spec.header_text_color
            h_box.fill.fore_color.rgb = hex_to_rgb(h_bg)
            h_box.line.fill.background()
            p_h = h_box.text_frame.paragraphs[0]
            p_h.text = "  " + tier_geom.tier_spec.tier_name.upper()
            p_h.font.name = self.theme.font_body
            p_h.font.size = Pt(8.5)
            p_h.font.bold = True
            p_h.font.color.rgb = hex_to_rgb(h_text_col)
            p_h.alignment = PP_ALIGN.LEFT

            # Nodes inside tier
            for node_geom in tier_geom.nodes:
                n_box = slide.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    Inches(node_geom.rect.x), Inches(node_geom.rect.y),
                    Inches(node_geom.rect.w), Inches(node_geom.rect.h)
                )
                n_box.fill.solid()
                n_box.fill.fore_color.rgb = hex_to_rgb(self.theme.service_node_bg)
                n_box.line.color.rgb = hex_to_rgb(node_geom.node.accent_color or self.theme.service_node_border)
                n_box.line.width = Pt(1.2)

                tf_n = n_box.text_frame
                tf_n.word_wrap = True
                tf_n.margin_left = Inches(0.06)
                tf_n.margin_right = Inches(0.06)
                tf_n.margin_top = Inches(0.04)
                tf_n.margin_bottom = Inches(0.04)

                p_n = tf_n.paragraphs[0]
                p_n.text = node_geom.node.name
                p_n.font.name = self.theme.font_body
                p_n.font.size = Pt(8.5)
                p_n.font.bold = True
                p_n.font.color.rgb = hex_to_rgb(self.theme.service_node_text)
                p_n.space_after = Pt(1.5)

                for b in node_geom.node.bullets:
                    p_b = tf_n.add_paragraph()
                    p_b.text = "• " + b
                    p_b.font.name = self.theme.font_body
                    p_b.font.size = Pt(7.2)
                    p_b.font.color.rgb = hex_to_rgb(self.theme.muted_text if self.theme.is_dark_mode else "#334155")
                    p_b.space_after = Pt(1.0)

        # Inter-tier connectors
        for (x1, y1, x2, y2) in layout.inter_tier_connectors:
            arr_w = 0.18
            arr_h = y2 - y1
            arr = slide.shapes.add_shape(
                MSO_SHAPE.DOWN_ARROW,
                Inches(x1 - arr_w / 2.0), Inches(y1),
                Inches(arr_w), Inches(arr_h)
            )
            arr.fill.solid()
            arr_col = self.theme.flow_arrow_color if spec.flow_arrow_color == "#0284C7" else spec.flow_arrow_color
            arr.fill.fore_color.rgb = hex_to_rgb(arr_col)
            arr.line.fill.background()

    def render_chevron_pipeline(self, slide, rect: Rect, spec: ChevronPipelineSpec):
        """Renders horizontal multi-step process pipeline with native vector shapes."""
        layout = DiagramGenerator.solve_chevron_pipeline(rect, spec)

        # Title
        if layout.title_rect and spec.title:
            tb = slide.shapes.add_textbox(
                Inches(layout.title_rect.x), Inches(layout.title_rect.y),
                Inches(layout.title_rect.w), Inches(layout.title_rect.h)
            )
            p = tb.text_frame.paragraphs[0]
            p.text = spec.title
            p.font.name = self.theme.font_body
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = hex_to_rgb(self.theme.bullet_accent)

        for step_geom in layout.steps:
            # Step card
            s_box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(step_geom.rect.x), Inches(step_geom.rect.y),
                Inches(step_geom.rect.w), Inches(step_geom.rect.h)
            )
            s_box.fill.solid()
            s_box.fill.fore_color.rgb = hex_to_rgb(step_geom.step.color)
            s_box.line.fill.background()

            tf_s = s_box.text_frame
            tf_s.word_wrap = True
            tf_s.margin_left = Inches(0.04)
            tf_s.margin_right = Inches(0.04)
            tf_s.margin_top = Inches(0.04)
            tf_s.margin_bottom = Inches(0.04)

            p1 = tf_s.paragraphs[0]
            p1.text = f"{step_geom.step.step_num}. {step_geom.step.title}"
            p1.font.name = self.theme.font_body
            p1.font.size = Pt(8.0)
            p1.font.bold = True
            p1.font.color.rgb = hex_to_rgb(step_geom.step.text_color)
            p1.alignment = PP_ALIGN.CENTER

            if step_geom.step.subtitle:
                p2 = tf_s.add_paragraph()
                p2.text = step_geom.step.subtitle
                p2.font.name = self.theme.font_body
                p2.font.size = Pt(7.0)
                p2.font.color.rgb = hex_to_rgb(step_geom.step.text_color)
                p2.alignment = PP_ALIGN.CENTER

            # Connector arrow
            if step_geom.arrow_rect:
                arr = slide.shapes.add_shape(
                    MSO_SHAPE.RIGHT_ARROW,
                    Inches(step_geom.arrow_rect.x), Inches(step_geom.arrow_rect.y),
                    Inches(step_geom.arrow_rect.w), Inches(step_geom.arrow_rect.h)
                )
                arr.fill.solid()
                arr.fill.fore_color.rgb = hex_to_rgb("#F97316")
                arr.line.fill.background()

        # Optional summary text
        if layout.summary_rect and spec.summary_text:
            tb_s = slide.shapes.add_textbox(
                Inches(layout.summary_rect.x), Inches(layout.summary_rect.y),
                Inches(layout.summary_rect.w), Inches(layout.summary_rect.h)
            )
            p_sum = tb_s.text_frame.paragraphs[0]
            p_sum.text = spec.summary_text
            p_sum.font.name = self.theme.font_body
            p_sum.font.size = Pt(9.5)
            p_sum.font.bold = True
            p_sum.font.color.rgb = hex_to_rgb(self.theme.title_primary)

    def render_native_tech_grid(self, slide, rect: Rect, spec: TechGridSpec):
        """Renders categorized tech stack cards and badges natively."""
        layout = DiagramGenerator.solve_tech_grid(rect, spec)

        if layout.title_rect and spec.title:
            tb = slide.shapes.add_textbox(
                Inches(layout.title_rect.x), Inches(layout.title_rect.y),
                Inches(layout.title_rect.w), Inches(layout.title_rect.h)
            )
            p = tb.text_frame.paragraphs[0]
            p.text = spec.title
            p.font.name = self.theme.font_body
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = hex_to_rgb(self.theme.title_primary)

        for col in layout.columns:
            # Column container
            c_box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(col.outer_rect.x), Inches(col.outer_rect.y),
                Inches(col.outer_rect.w), Inches(col.outer_rect.h)
            )
            c_box.fill.solid()
            c_box.fill.fore_color.rgb = hex_to_rgb(self.theme.tech_col_bg)
            c_box.line.color.rgb = hex_to_rgb(self.theme.tech_col_border)
            c_box.line.width = Pt(1.0)

            # Column header
            h_box = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(col.header_rect.x), Inches(col.header_rect.y),
                Inches(col.header_rect.w), Inches(col.header_rect.h)
            )
            h_box.fill.solid()
            h_box.fill.fore_color.rgb = hex_to_rgb(col.header_color)
            h_box.line.fill.background()
            p_h = h_box.text_frame.paragraphs[0]
            p_h.text = col.category_name
            p_h.font.name = self.theme.font_body
            p_h.font.size = Pt(9.5)
            p_h.font.bold = True
            p_h.font.color.rgb = hex_to_rgb("#FFFFFF")
            p_h.alignment = PP_ALIGN.CENTER

            # Badges
            for badge in col.badges:
                b_box = slide.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    Inches(badge.rect.x), Inches(badge.rect.y),
                    Inches(badge.rect.w), Inches(badge.rect.h)
                )
                b_box.fill.solid()
                b_box.fill.fore_color.rgb = hex_to_rgb(self.theme.tech_badge_bg)
                b_box.line.color.rgb = hex_to_rgb(badge.color)
                b_box.line.width = Pt(1.2)

                tf_b = b_box.text_frame
                tf_b.margin_top = Inches(0.02)
                tf_b.margin_bottom = Inches(0.02)
                p_b = tf_b.paragraphs[0]
                p_b.text = badge.name
                p_b.font.name = self.theme.font_body
                p_b.font.size = Pt(8.5)
                p_b.font.bold = True
                p_b.font.color.rgb = hex_to_rgb(self.theme.tech_badge_text)
                p_b.alignment = PP_ALIGN.CENTER

    def render_native_competitor_matrix(self, slide, rect: Rect, spec: CompetitorMatrixSpec):
        """Renders native PowerPoint table for competitor feature comparisons with check/cross glyphs."""
        num_rows = len(spec.rows) + 1
        num_cols = len(spec.headers)

        table_shape = slide.shapes.add_table(
            num_rows, num_cols,
            Inches(rect.x), Inches(rect.y), Inches(rect.w), Inches(rect.h)
        )
        tbl = table_shape.table

        # Column widths
        first_col_w = min(2.7, rect.w * 0.44)
        other_cols_w = (rect.w - first_col_w) / max(1, (num_cols - 1))
        tbl.columns[0].width = Inches(first_col_w)
        for c in range(1, num_cols):
            tbl.columns[c].width = Inches(other_cols_w)

        # Header row
        for c, h_text in enumerate(spec.headers):
            cell = tbl.cell(0, c)
            cell.margin_left = Inches(0.04)
            cell.margin_right = Inches(0.04)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            cell.fill.solid()
            cell.fill.fore_color.rgb = hex_to_rgb(self.theme.table_header_bg)
            p = cell.text_frame.paragraphs[0]
            p.text = h_text
            p.font.name = self.theme.font_body
            p.font.size = Pt(8.5 if c > 0 else 9.0)
            p.font.bold = True
            p.font.color.rgb = hex_to_rgb(self.theme.table_header_text)
            p.alignment = PP_ALIGN.CENTER if c > 0 else PP_ALIGN.LEFT

        # Data rows
        for r_idx, row in enumerate(spec.rows):
            cell_cap = tbl.cell(r_idx + 1, 0)
            cell_cap.margin_left = Inches(0.05)
            cell_cap.margin_right = Inches(0.05)
            cell_cap.margin_top = Inches(0.03)
            cell_cap.margin_bottom = Inches(0.03)
            cell_cap.fill.solid()
            cell_cap.fill.fore_color.rgb = hex_to_rgb(self.theme.card_bg if (r_idx % 2 == 0) else self.theme.table_zebra_bg)
            p_cap = cell_cap.text_frame.paragraphs[0]
            p_cap.text = row.capability
            p_cap.font.name = self.theme.font_body
            p_cap.font.size = Pt(8.0)
            p_cap.font.bold = True
            p_cap.font.color.rgb = hex_to_rgb(self.theme.table_cell_text)

            for c_idx, res in enumerate(row.results):
                col_num = c_idx + 1
                if col_num >= num_cols:
                    break
                cell_res = tbl.cell(r_idx + 1, col_num)
                cell_res.fill.solid()
                if col_num == 1:
                    cell_res.fill.fore_color.rgb = hex_to_rgb(self.theme.table_highlight_bg if res else ("#7F1D1D" if self.theme.is_dark_mode else "#FEF2F2"))
                else:
                    cell_res.fill.fore_color.rgb = hex_to_rgb(self.theme.card_bg if (r_idx % 2 == 0) else self.theme.table_zebra_bg)

                p_res = cell_res.text_frame.paragraphs[0]
                p_res.alignment = PP_ALIGN.CENTER
                if res:
                    p_res.text = "✔"
                    p_res.font.name = self.theme.font_body
                    p_res.font.size = Pt(13)
                    p_res.font.bold = True
                    p_res.font.color.rgb = hex_to_rgb(self.theme.success_green)
                else:
                    p_res.text = "✖"
                    p_res.font.name = self.theme.font_body
                    p_res.font.size = Pt(13)
                    p_res.font.bold = True
                    p_res.font.color.rgb = hex_to_rgb(self.theme.danger_red)

    def render_stat_grid(self, slide, rect: Rect, spec: StatGridSpec):
        """Renders horizontal row of KPI / stat cards."""
        cards = DiagramGenerator.solve_stat_grid(rect, spec)
        for c in cards:
            card = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(c.rect.x), Inches(c.rect.y),
                Inches(c.rect.w), Inches(c.rect.h)
            )
            card.fill.solid()
            card.fill.fore_color.rgb = hex_to_rgb(self.theme.card_bg)
            card.line.color.rgb = hex_to_rgb(c.metric.accent_color)
            card.line.width = Pt(1.5)

            tf = card.text_frame
            tf.word_wrap = True
            tf.margin_top = Inches(0.08)

            p1 = tf.paragraphs[0]
            p1.text = c.metric.value
            p1.font.name = self.theme.font_body
            p1.font.size = Pt(22)
            p1.font.bold = True
            p1.font.color.rgb = hex_to_rgb(c.metric.accent_color)
            p1.alignment = PP_ALIGN.CENTER

            p2 = tf.add_paragraph()
            p2.text = c.metric.label
            p2.font.name = self.theme.font_body
            p2.font.size = Pt(9.5)
            p2.font.bold = True
            p2.font.color.rgb = hex_to_rgb(self.theme.title_primary)
            p2.alignment = PP_ALIGN.CENTER

            if c.metric.subtext:
                p3 = tf.add_paragraph()
                p3.text = c.metric.subtext
                p3.font.name = self.theme.font_body
                p3.font.size = Pt(8.0)
                p3.font.color.rgb = hex_to_rgb(self.theme.muted_text)
                p3.alignment = PP_ALIGN.CENTER

    def render_title_page(self, slide, spec: SlideSpec, regions: Dict[str, Rect]):
        """Renders Slide 1 Title Page."""
        tb_top = slide.shapes.add_textbox(Inches(regions["header_title"].x), Inches(regions["header_title"].y), Inches(regions["header_title"].w), Inches(regions["header_title"].h))
        p = tb_top.text_frame.paragraphs[0]
        p.text = "SMART INDIA HACKATHON 2026"
        p.font.name = self.theme.font_title
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = hex_to_rgb(self.theme.bullet_accent)
        p.alignment = PP_ALIGN.CENTER

        if self.config.sih_logo_small and os.path.exists(self.config.sih_logo_small):
            slide.shapes.add_picture(self.config.sih_logo_small, Inches(11.20), Inches(0.18), width=Inches(1.80), height=Inches(0.84))

        tb_sub = slide.shapes.add_textbox(Inches(regions["header_subtitle"].x), Inches(regions["header_subtitle"].y), Inches(regions["header_subtitle"].w), Inches(regions["header_subtitle"].h))
        tf_sub = tb_sub.text_frame
        tf_sub.word_wrap = True
        p = tf_sub.paragraphs[0]
        p.text = spec.title
        p.font.name = self.theme.font_title
        if len(spec.title) > 65:
            p.font.size = Pt(22)
        elif len(spec.title) > 45:
            p.font.size = Pt(25)
        else:
            p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = hex_to_rgb(self.theme.title_primary)
        p.alignment = PP_ALIGN.CENTER

        meta_rect = regions["metadata_box"]
        tb_meta = slide.shapes.add_textbox(Inches(meta_rect.x), Inches(meta_rect.y), Inches(meta_rect.w), Inches(meta_rect.h))
        tf = tb_meta.text_frame
        tf.word_wrap = True

        if spec.title_metadata:
            for i, (label, val) in enumerate(spec.title_metadata):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                p.space_after = Pt(14.0)

                lbl_clean = label if (label.endswith(" ") or label.endswith(":-") or label.endswith("–")) else (label + " ")
                if not lbl_clean.endswith(" "):
                    lbl_clean += " "

                run1 = p.add_run()
                run1.text = "•  " + lbl_clean
                run1.font.name = self.theme.font_body
                run1.font.size = Pt(17 if "Title" not in label else 16)
                run1.font.bold = True
                run1.font.color.rgb = hex_to_rgb(self.theme.title_primary)

                run2 = p.add_run()
                run2.text = val
                run2.font.name = self.theme.font_body
                run2.font.size = Pt(17 if "Title" not in label else 15.5)
                run2.font.bold = True if label in ["Team Name :- ", "Problem Statement ID – "] else False
                run2.font.color.rgb = hex_to_rgb(self.theme.bullet_accent) if label in ["Team Name :- ", "Problem Statement ID – "] else hex_to_rgb(self.theme.title_primary)

        if self.config.sih_logo_large and os.path.exists(self.config.sih_logo_large):
            emblem_rect = regions["emblem_image"]
            slide.shapes.add_picture(self.config.sih_logo_large, Inches(emblem_rect.x), Inches(emblem_rect.y), width=Inches(emblem_rect.w), height=Inches(emblem_rect.h))

    def compile(self, output_pptx_path: str):
        """Executes full presentation compilation."""
        os.makedirs(os.path.dirname(output_pptx_path), exist_ok=True)

        for slide_spec in self.manifest.slides:
            slide = self.prs.slides.add_slide(self.blank_layout)
            # Apply Theme Canvas Background Fill
            bg = slide.background
            fill = bg.fill
            fill.solid()
            fill.fore_color.rgb = hex_to_rgb(self.theme.canvas_bg)

            regions = LayoutSolver.get_archetype_layout(slide_spec.archetype)

            # Slide 1 (Title Page)
            if slide_spec.archetype == SlideArchetype.TITLE_PAGE:
                self.render_title_page(slide, slide_spec, regions)
                continue

            # Standard Header & Footer for Slides 2-6
            self.add_header_footer(slide, slide_spec.title, slide_spec.slide_number)

            # Archetype-Driven Component Dispatch
            if slide_spec.archetype == SlideArchetype.SPLIT_LEFT_RIGHT:
                if slide_spec.left_column and isinstance(slide_spec.left_column.get("component"), TaggedBulletListSpec):
                    self.render_tagged_bullets(slide, regions["left_column"], slide_spec.left_column["component"])
                if slide_spec.right_column:
                    if isinstance(slide_spec.right_column.get("diagram_component"), ArchitectureDiagramSpec):
                        self.render_architecture_diagram(slide, regions["right_column"], slide_spec.right_column["diagram_component"])
                    elif "image_path" in slide_spec.right_column:
                        img_p = slide_spec.right_column["image_path"]
                        if os.path.exists(img_p):
                            slide.shapes.add_picture(img_p, Inches(regions["right_column"].x), Inches(regions["right_column"].y), width=Inches(regions["right_column"].w), height=Inches(regions["right_column"].h))

            elif slide_spec.archetype == SlideArchetype.SPLIT_STACK_AND_GRID:
                # Left Top: Tech Bullets
                if slide_spec.left_column and isinstance(slide_spec.left_column.get("top_component"), TaggedBulletListSpec):
                    self.render_tagged_bullets(slide, regions["left_top"], slide_spec.left_column["top_component"])

                # Left Mid: Native Flow or Image
                if slide_spec.left_column:
                    if isinstance(slide_spec.left_column.get("flow_component"), ChevronPipelineSpec):
                        self.render_chevron_pipeline(slide, regions["left_mid_diagram"], slide_spec.left_column["flow_component"])
                    elif "mid_image_path" in slide_spec.left_column:
                        p_img = slide_spec.left_column["mid_image_path"]
                        if os.path.exists(p_img):
                            slide.shapes.add_picture(p_img, Inches(regions["left_mid_diagram"].x), Inches(regions["left_mid_diagram"].y), width=Inches(regions["left_mid_diagram"].w), height=Inches(regions["left_mid_diagram"].h))

                # Left Bottom: Process Text
                if slide_spec.left_column and "bottom_text" in slide_spec.left_column:
                    tb_flow = slide.shapes.add_textbox(Inches(regions["left_bottom_text"].x), Inches(regions["left_bottom_text"].y), Inches(regions["left_bottom_text"].w), Inches(regions["left_bottom_text"].h))
                    tf_f = tb_flow.text_frame
                    tf_f.word_wrap = True
                    p = tf_f.paragraphs[0]
                    p.text = "• Process Flow :-"
                    p.font.name = self.theme.font_body
                    p.font.size = Pt(15)
                    p.font.bold = True
                    p.font.color.rgb = hex_to_rgb(self.theme.bullet_accent)
                    p.space_after = Pt(4)
                    p2 = tf_f.add_paragraph()
                    p2.text = slide_spec.left_column["bottom_text"]
                    p2.font.name = self.theme.font_body
                    p2.font.size = Pt(9.5)
                    p2.font.bold = True
                    p2.font.color.rgb = hex_to_rgb(self.theme.title_primary)

                # Right Top: Native Tech Grid or Image
                if slide_spec.right_column:
                    if isinstance(slide_spec.right_column.get("tech_grid_component"), TechGridSpec):
                        self.render_native_tech_grid(slide, regions["right_top_grid"], slide_spec.right_column["tech_grid_component"])
                    elif "top_image_path" in slide_spec.right_column:
                        g_img = slide_spec.right_column["top_image_path"]
                        if os.path.exists(g_img):
                            slide.shapes.add_picture(g_img, Inches(regions["right_top_grid"].x), Inches(regions["right_top_grid"].y), width=Inches(regions["right_top_grid"].w), height=Inches(regions["right_top_grid"].h))

                # Right Bottom: Links Box
                if slide_spec.right_column and isinstance(slide_spec.right_column.get("bottom_component"), ProjectLinksCardSpec):
                    self.render_project_links_box(slide, regions["right_bottom_links"], slide_spec.right_column["bottom_component"])

            elif slide_spec.archetype == SlideArchetype.TWO_COLUMN_SECTIONS:
                # Left Column Multi-Sections
                if slide_spec.left_column and isinstance(slide_spec.left_column.get("component"), MultiSectionColumnSpec):
                    self.render_multi_section_column(slide, regions["left_column"], slide_spec.left_column["component"])
                # Right Top Multi-Sections
                if slide_spec.right_column and isinstance(slide_spec.right_column.get("top_component"), MultiSectionColumnSpec):
                    self.render_multi_section_column(slide, regions["right_top_sections"], slide_spec.right_column["top_component"])
                # Right Bottom Callout Card
                if slide_spec.right_column and isinstance(slide_spec.right_column.get("bottom_component"), CalloutCardSpec):
                    self.render_callout_card(slide, regions["right_bottom_card"], slide_spec.right_column["bottom_component"])

            elif slide_spec.archetype == SlideArchetype.TOP_SPLIT_BOTTOM_TABLE:
                # Top Left Multi-Sections
                if slide_spec.top_left and isinstance(slide_spec.top_left.get("component"), MultiSectionColumnSpec):
                    self.render_multi_section_column(slide, regions["top_left"], slide_spec.top_left["component"])
                # Top Right Multi-Sections
                if slide_spec.top_right and isinstance(slide_spec.top_right.get("component"), MultiSectionColumnSpec):
                    self.render_multi_section_column(slide, regions["top_right"], slide_spec.top_right["component"])
                # Bottom Table
                if slide_spec.bottom_section and isinstance(slide_spec.bottom_section.get("component"), TableSpec):
                    self.render_table(slide, regions["bottom_table"], slide_spec.bottom_section["component"])

            elif slide_spec.archetype == SlideArchetype.TOP_SPLIT_BOTTOM_FLOW:
                # Left Top Multi-Sections (Citations & Platforms)
                if slide_spec.top_left and isinstance(slide_spec.top_left.get("component"), MultiSectionColumnSpec):
                    self.render_multi_section_column(slide, regions["top_left_citations"], slide_spec.top_left["component"])
                # Left Mid Demo Links
                if slide_spec.left_column and isinstance(slide_spec.left_column.get("component"), ProjectLinksCardSpec):
                    self.render_project_links_box(slide, regions["left_mid_demo_box"], slide_spec.left_column["component"])
                # Right Top Native Competitor Matrix or Image
                if slide_spec.top_right:
                    if isinstance(slide_spec.top_right.get("matrix_component"), CompetitorMatrixSpec):
                        self.render_native_competitor_matrix(slide, regions["top_right_matrix"], slide_spec.top_right["matrix_component"])
                    elif "image_path" in slide_spec.top_right:
                        m_img = slide_spec.top_right["image_path"]
                        if os.path.exists(m_img):
                            slide.shapes.add_picture(m_img, Inches(regions["top_right_matrix"].x), Inches(regions["top_right_matrix"].y), width=Inches(regions["top_right_matrix"].w), height=Inches(regions["top_right_matrix"].h))
                # Bottom Flow Diagram & Header
                if slide_spec.bottom_section:
                    if isinstance(slide_spec.bottom_section.get("flow_component"), ChevronPipelineSpec):
                        bot_rect = Rect(
                            x=regions["bottom_flow_header"].x,
                            y=regions["bottom_flow_header"].y,
                            w=regions["bottom_flow_header"].w,
                            h=regions["bottom_flow_header"].h + regions["bottom_flow_diagram"].h
                        )
                        self.render_chevron_pipeline(slide, bot_rect, slide_spec.bottom_section["flow_component"])
                    elif "flow_image_path" in slide_spec.bottom_section:
                        tb_rf = slide.shapes.add_textbox(Inches(regions["bottom_flow_header"].x), Inches(regions["bottom_flow_header"].y), Inches(regions["bottom_flow_header"].w), Inches(regions["bottom_flow_header"].h))
                        p = tb_rf.text_frame.paragraphs[0]
                        p.text = slide_spec.bottom_section.get("title", "• Research Flow:")
                        p.font.name = self.theme.font_body
                        p.font.size = Pt(16)
                        p.font.bold = True
                        p.font.color.rgb = hex_to_rgb(self.theme.bullet_accent)

                        rf_img = slide_spec.bottom_section["flow_image_path"]
                        if os.path.exists(rf_img):
                            slide.shapes.add_picture(rf_img, Inches(regions["bottom_flow_diagram"].x), Inches(regions["bottom_flow_diagram"].y), width=Inches(regions["bottom_flow_diagram"].w), height=Inches(regions["bottom_flow_diagram"].h))

        self.prs.save(output_pptx_path)
        print(f"Compiled PPTX presentation successfully: {output_pptx_path}")
