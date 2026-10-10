"""
Presentation Engine — Cognitive PPT/PDF Design Analyzer
Deeply inspects reference presentations to extract abstract design grammar,
typographic hierarchy, color palettes, and visual structural patterns.
Zero shallow cloning: Extracts the design intelligence to inform new bespoke decks.
"""

import os
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE


@dataclass
class SlidePattern:
    """Represents the abstract structural pattern of a slide."""
    slide_index: int
    archetype_detected: str  # title, stat_kpis, bento_cards, architecture_lanes, split_tension, table_matrix, roadmap
    title_text: str
    card_count: int
    has_metrics: bool
    has_table: bool
    has_flow: bool
    density_chars: int


@dataclass
class DesignGrammar:
    """Extracted design intelligence from a reference presentation."""
    is_dark_mode: bool
    primary_bg: str
    primary_card_bg: str
    accent_color: str
    heading_font: str
    body_font: str
    slide_patterns: List[SlidePattern] = field(default_factory=list)
    detected_density_mode: str = "MODERATE"  # SPARSE, MODERATE, DENSE
    color_palette: List[str] = field(default_factory=list)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02X}{g:02X}{b:02X}"


class CognitiveDeckAnalyzer:
    """
    Analyzes an existing PowerPoint (.pptx) presentation to extract abstract
    visual design grammar, enabling synthesis of new bespoke decks with matching design quality.
    """

    @classmethod
    def analyze_pptx(cls, pptx_path: str) -> DesignGrammar:
        """Parses a PPTX file and returns its abstract design grammar."""
        if not os.path.exists(pptx_path):
            raise FileNotFoundError(f"PPTX file not found: {pptx_path}")

        prs = Presentation(pptx_path)

        color_counts: Dict[str, int] = {}
        font_counts: Dict[str, int] = {}
        slide_patterns: List[SlidePattern] = []
        total_chars = 0

        for s_idx, slide in enumerate(prs.slides):
            s_title = ""
            card_count = 0
            has_metrics = False
            has_table = False
            has_flow = False
            s_chars = 0

            for shape in slide.shapes:
                # 1. Inspect Fills & Colors
                if hasattr(shape, "fill") and shape.fill.type is not None:
                    try:
                        if hasattr(shape.fill, "fore_color") and shape.fill.fore_color.rgb:
                            rgb = shape.fill.fore_color.rgb
                            h = rgb_to_hex(rgb[0], rgb[1], rgb[2])
                            color_counts[h] = color_counts.get(h, 0) + 1
                    except Exception:
                        pass

                # 2. Inspect Shape Archetypes
                if shape.has_table:
                    has_table = True
                elif shape.shape_type == 1:  # AutoShape
                    if hasattr(shape, "auto_shape_type"):
                        ast = shape.auto_shape_type
                        if ast in (MSO_SHAPE.ROUNDED_RECTANGLE, MSO_SHAPE.RECTANGLE):
                            # Count cards that are larger than a small badge
                            if shape.width > Inches(1.5).inches and shape.height > Inches(0.8).inches:
                                card_count += 1
                        elif ast in (MSO_SHAPE.CHEVRON, MSO_SHAPE.RIGHT_ARROW, MSO_SHAPE.UP_ARROW):
                            has_flow = True

                # 3. Inspect Text Frames & Fonts
                if shape.has_text_frame:
                    tf = shape.text_frame
                    text_str = tf.text.strip()
                    s_chars += len(text_str)

                    if not s_title and len(text_str) < 80:
                        s_title = text_str.split('\n')[0]

                    for p in tf.paragraphs:
                        for run in p.runs:
                            if run.font.name:
                                font_counts[run.font.name] = font_counts.get(run.font.name, 0) + len(run.text)
                            if run.font.size and run.font.size.pt >= 24:
                                # Giant numbers often indicate KPI stats
                                if any(c.isdigit() for c in run.text) or "%" in run.text:
                                    has_metrics = True

            total_chars += s_chars

            # Classify archetype
            if s_idx == 0:
                archetype = "title"
            elif has_metrics and card_count >= 2:
                archetype = "stat_kpis"
            elif has_table:
                archetype = "table_matrix"
            elif has_flow:
                archetype = "roadmap" if s_idx >= 4 else "process_flow"
            elif card_count >= 3:
                archetype = "bento_cards"
            elif card_count == 2:
                archetype = "split_tension"
            else:
                archetype = "architecture_lanes"

            slide_patterns.append(SlidePattern(
                slide_index=s_idx + 1,
                archetype_detected=archetype,
                title_text=s_title,
                card_count=card_count,
                has_metrics=has_metrics,
                has_table=has_table,
                has_flow=has_flow,
                density_chars=s_chars
            ))

        # Determine Dominant Fonts
        sorted_fonts = sorted(font_counts.items(), key=lambda x: x[1], reverse=True)
        heading_font = sorted_fonts[0][0] if sorted_fonts else "Calibri"
        body_font = sorted_fonts[1][0] if len(sorted_fonts) > 1 else heading_font

        # Determine Palette & Dark/Light mode
        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
        top_colors = [c[0] for c in sorted_colors[:8]]

        # Assess background lightness
        is_dark = False
        primary_bg = "#0B0F19" if is_dark else "#FFFFFF"
        primary_card = "#111827" if is_dark else "#F8FAFC"
        accent = "#1D4ED8"

        for hex_col in top_colors:
            # Simple luminance check
            r = int(hex_col[1:3], 16)
            g = int(hex_col[3:5], 16)
            b = int(hex_col[5:7], 16)
            lum = (0.299 * r + 0.587 * g + 0.114 * b)
            if lum < 60:
                is_dark = True
                primary_bg = hex_col
                break
            elif lum > 200:
                is_dark = False
                primary_bg = hex_col
                break

        # Pick accent as highest saturation color
        for hex_col in top_colors:
            r = int(hex_col[1:3], 16)
            g = int(hex_col[3:5], 16)
            b = int(hex_col[5:7], 16)
            if max(r, g, b) - min(r, g, b) > 60:
                accent = hex_col
                break

        avg_density = total_chars / max(1, len(slide_patterns))
        density_mode = "SPARSE" if avg_density < 600 else ("DENSE" if avg_density > 1400 else "MODERATE")

        return DesignGrammar(
            is_dark_mode=is_dark,
            primary_bg=primary_bg,
            primary_card_bg=primary_card,
            accent_color=accent,
            heading_font=heading_font,
            body_font=body_font,
            slide_patterns=slide_patterns,
            detected_density_mode=density_mode,
            color_palette=top_colors
        )
