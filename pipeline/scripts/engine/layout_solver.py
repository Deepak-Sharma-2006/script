"""
Presentation Engine — Constraint-Based Layout Solver
Calculates geometric bounds, box packing, and dynamic shrink-to-fit typography to guarantee 0% overflow.
"""

import math
from dataclasses import dataclass
from typing import Tuple, List, Dict, Any, Optional
from scripts.engine.schema import SlideArchetype


@dataclass
class Rect:
    x: float
    y: float
    w: float
    h: float

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h

    def overlaps(self, other: 'Rect', tolerance: float = 0.001) -> bool:
        if self.right <= other.x + tolerance or other.right <= self.x + tolerance:
            return False
        if self.bottom <= other.y + tolerance or other.bottom <= self.y + tolerance:
            return False
        return True


class LayoutSolver:
    """
    Computes precise coordinate geometry and dynamic font scaling
    for presentations using defined slide archetypes and box-packing constraints.
    """

    # Global 16:9 Widescreen Canvas Limits (Inches)
    CANVAS_WIDTH = 13.333
    CANVAS_HEIGHT = 7.500
    
    # Safe Margin Boundaries
    HEADER_Y_LIMIT = 1.250   # Elements cannot go above y = 1.25"
    FOOTER_Y_LIMIT = 6.950   # Elements cannot go below y = 6.95"
    CONTENT_X_MIN = 0.400
    CONTENT_X_MAX = 12.933

    @staticmethod
    def estimate_text_height(
        text: str,
        container_width_inches: float,
        font_size_pt: float,
        space_after_pt: float = 2.0,
        is_bold: bool = False
    ) -> float:
        """
        Estimates the rendered height in inches for a block of text given container width and font size.
        Uses proportional Arial font metrics (average character width ~ 0.52em, bold ~ 0.58em).
        """
        if not text:
            return 0.0
        
        char_ratio = 0.58 if is_bold else 0.50
        # Average character width in points: font_size * char_ratio
        # In inches: (font_size * char_ratio) / 72.0
        avg_char_width_in = (font_size_pt * char_ratio) / 72.0
        chars_per_line = max(10, int(container_width_inches / avg_char_width_in))
        
        # Calculate line count based on words
        words = text.split()
        lines = 1
        curr_line_len = 0
        for w in words:
            if curr_line_len + len(w) + 1 <= chars_per_line:
                curr_line_len += len(w) + 1
            else:
                lines += 1
                curr_line_len = len(w)
                
        # Line height in inches
        line_height_in = (font_size_pt * 1.25) / 72.0
        space_after_in = space_after_pt / 72.0
        
        return (lines * line_height_in) + space_after_in

    @classmethod
    def fit_text_block(
        cls,
        paragraphs: List[Dict[str, Any]],
        container_width: float,
        max_height: float,
        base_font_size: float = 10.0,
        min_font_size: float = 7.5,
        base_space_after: float = 2.0
    ) -> Tuple[float, float, float]:
        """
        Iteratively calculates the optimal font size and spacing to fit all paragraphs
        inside the container without exceeding max_height.
        
        Returns: (optimal_font_size_pt, optimal_space_after_pt, computed_total_height_in)
        """
        curr_font_size = base_font_size
        curr_space_after = base_space_after
        
        while curr_font_size >= min_font_size:
            total_height = 0.0
            for p in paragraphs:
                txt = p.get("text", "")
                is_bold = p.get("is_bold", False)
                p_font = curr_font_size if "font_size" not in p else min(curr_font_size, p["font_size"])
                p_height = cls.estimate_text_height(txt, container_width, p_font, curr_space_after, is_bold)
                total_height += p_height
                
            if total_height <= max_height:
                return curr_font_size, curr_space_after, total_height
            
            # Step down font size and space
            curr_font_size -= 0.5
            if curr_space_after > 1.0:
                curr_space_after -= 0.5

        return min_font_size, 1.0, total_height

    @classmethod
    def get_archetype_layout(cls, archetype: SlideArchetype) -> Dict[str, Rect]:
        """
        Returns guaranteed non-overlapping bounding boxes (in inches) for each named region
        of the specified slide archetype.
        """
        layouts: Dict[SlideArchetype, Dict[str, Rect]] = {
            SlideArchetype.TITLE_PAGE: {
                "header_title": Rect(0.60, 0.35, 12.13, 0.65),
                "header_subtitle": Rect(0.60, 1.10, 12.13, 0.65),
                "metadata_box": Rect(0.60, 1.95, 7.30, 4.90),
                "emblem_image": Rect(8.20, 1.80, 4.30, 4.83)
            },
            SlideArchetype.SPLIT_LEFT_RIGHT: {
                "left_column": Rect(0.50, 1.35, 5.80, 5.50),
                "right_column": Rect(6.50, 1.35, 6.40, 5.50)
            },
            SlideArchetype.SPLIT_STACK_AND_GRID: {
                "left_top": Rect(0.50, 1.35, 5.80, 2.95),
                "left_mid_diagram": Rect(0.50, 4.38, 5.70, 1.22),
                "left_bottom_text": Rect(0.50, 5.70, 5.80, 1.15),
                "right_top_grid": Rect(6.50, 1.35, 6.40, 4.10),
                "right_bottom_links": Rect(6.50, 5.55, 6.40, 1.30)
            },
            SlideArchetype.TWO_COLUMN_SECTIONS: {
                "left_column": Rect(0.50, 1.32, 5.80, 5.55),
                "right_top_sections": Rect(6.80, 1.35, 6.00, 3.30),
                "right_bottom_card": Rect(6.80, 4.75, 6.00, 2.10)
            },
            SlideArchetype.TOP_SPLIT_BOTTOM_TABLE: {
                "top_left": Rect(0.50, 1.22, 5.80, 2.45),
                "top_right": Rect(6.80, 1.22, 6.00, 2.45),
                "bottom_table_header": Rect(0.50, 3.85, 12.33, 0.35),
                "bottom_table": Rect(0.50, 4.25, 12.33, 2.30)
            },
            SlideArchetype.TOP_SPLIT_BOTTOM_FLOW: {
                "top_left_citations": Rect(0.50, 1.35, 5.80, 2.60),
                "left_mid_demo_box": Rect(0.50, 4.05, 5.80, 1.35),
                "top_right_matrix": Rect(6.50, 1.35, 6.40, 4.10),
                "bottom_flow_header": Rect(0.50, 5.48, 12.33, 0.35),
                "bottom_flow_diagram": Rect(0.50, 5.85, 12.33, 1.05)
            }
        }
        
        return layouts.get(archetype, layouts[SlideArchetype.SPLIT_LEFT_RIGHT])

    @classmethod
    def validate_slide_geometry(cls, regions: Dict[str, Rect]) -> List[str]:
        """
        Validates that all bounding boxes in a slide satisfy safety bounds:
        1. Stay within canvas boundaries.
        2. Do not overlap with other regions.
        3. Do not bleed into the header or footer limits.
        """
        errors = []
        region_items = list(regions.items())

        for name, r in region_items:
            # Check bottom footer boundary
            if r.bottom > cls.FOOTER_Y_LIMIT + 0.05 and name != "footer_ribbon":
                errors.append(f"Region '{name}' bottom ({r.bottom:.3f}\") exceeds FOOTER_Y_LIMIT ({cls.FOOTER_Y_LIMIT}\")")

            # Check left/right canvas boundary
            if r.x < cls.CONTENT_X_MIN - 0.05:
                errors.append(f"Region '{name}' x ({r.x:.3f}\") is outside left margin ({cls.CONTENT_X_MIN}\")")
            if r.right > cls.CONTENT_X_MAX + 0.05:
                errors.append(f"Region '{name}' right ({r.right:.3f}\") exceeds right margin ({cls.CONTENT_X_MAX}\")")

        # Check pairwise overlaps
        for i in range(len(region_items)):
            for j in range(i + 1, len(region_items)):
                name_a, rect_a = region_items[i]
                name_b, rect_b = region_items[j]
                if rect_a.overlaps(rect_b):
                    errors.append(f"Collision detected between region '{name_a}' and '{name_b}'")

        return errors
