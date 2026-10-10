"""
Presentation Engine — Computer-Vision & Pixel-Level Visual QA Gate
Inspects compiled PDF vector streams and rendered 200 DPI PNG slides for text collisions,
WCAG contrast compliance, margin violations, and visual mass balance.
"""

import os
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field
import numpy as np
from PIL import Image

try:
    import pymupdf as fitz
except ImportError:
    import fitz

from scripts.engine.themes import Theme, get_theme


@dataclass
class CollisionViolation:
    page_number: int
    block_a_text: str
    block_b_text: str
    intersection_rect: Tuple[float, float, float, float]
    severity: str = "ERROR"


@dataclass
class ContrastCheckResult:
    element_name: str
    fg_color: str
    bg_color: str
    ratio: float
    required_ratio: float
    passed: bool


@dataclass
class PageVisionReport:
    page_number: int
    has_collisions: bool
    collisions: List[CollisionViolation]
    margin_violations: List[str]
    contrast_checks: List[ContrastCheckResult]
    visual_balance_score: float  # 0.0 - 1.0 (1.0 = perfectly balanced)
    passed: bool


@dataclass
class VisionAuditReport:
    total_pages: int
    passed: bool
    total_collisions: int
    total_margin_violations: int
    total_contrast_failures: int
    page_reports: List[PageVisionReport]
    summary_text: str = ""

    def generate_summary(self) -> str:
        lines = [
            "=== VISION & PIXEL QA AUDIT REPORT ===",
            f"Total Pages Audited: {self.total_pages}",
            f"Overall Status: {'PASSED (Zero Defects)' if self.passed else 'FAILED'}",
            f"Text Collisions: {self.total_collisions}",
            f"Margin Violations: {self.total_margin_violations}",
            f"Contrast Failures: {self.total_contrast_failures}",
            "---------------------------------------"
        ]
        for p in self.page_reports:
            status = "PASS" if p.passed else "FAIL"
            lines.append(f"Page {p.page_number}: [{status}] Balance Score: {p.visual_balance_score:.2f}")
            for c in p.collisions:
                lines.append(f"   [COLLISION] Overlap between '{c.block_a_text[:30]}...' and '{c.block_b_text[:30]}...'")
            for m in p.margin_violations:
                lines.append(f"   [MARGIN] {m}")
            for con in p.contrast_checks:
                if not con.passed:
                    lines.append(f"   [CONTRAST FAIL] {con.element_name}: {con.ratio:.2f}:1 (Required: {con.required_ratio}:1)")
        self.summary_text = "\n".join(lines)
        return self.summary_text


class VisionQAGate:
    """
    Automated Computer Vision and Vector Auditor.
    """

    @staticmethod
    def hex_to_linear_rgb(hex_str: str) -> Tuple[float, float, float]:
        """Converts hex color string to normalized sRGB linear components."""
        clean = hex_str.lstrip('#')
        rgb = [int(clean[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
        linear = []
        for c in rgb:
            if c <= 0.04045:
                linear.append(c / 12.92)
            else:
                linear.append(((c + 0.055) / 1.055) ** 2.4)
        return linear[0], linear[1], linear[2]

    @classmethod
    def calculate_wcag_contrast(cls, hex_fg: str, hex_bg: str) -> float:
        """Calculates WCAG 2.1 relative luminance contrast ratio."""
        r1, g1, b1 = cls.hex_to_linear_rgb(hex_fg)
        r2, g2, b2 = cls.hex_to_linear_rgb(hex_bg)
        lum1 = 0.2126 * r1 + 0.7152 * g1 + 0.0722 * b1
        lum2 = 0.2126 * r2 + 0.7152 * g2 + 0.0722 * b2
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        return (lighter + 0.05) / (darker + 0.05)

    @classmethod
    def audit_theme_contrast(cls, theme: Theme) -> List[ContrastCheckResult]:
        """Validates all foreground and background pairs in a Theme."""
        checks = [
            ("Canvas Title Text", theme.title_primary, theme.canvas_bg, 4.5),
            ("Canvas Body Text", theme.body_text, theme.canvas_bg, 4.5),
            ("Card Body Text", theme.body_text, theme.card_bg, 4.5),
            ("Service Node Text", theme.service_node_text, theme.service_node_bg, 4.5),
            ("Tier Header Text", theme.tier_header_text, theme.tier_header_bg, 3.0),
            ("Footer Text", theme.footer_text, theme.footer_bg, 3.0),
            ("Callout Title Text", theme.callout_title, theme.callout_bg, 4.5),
            ("Callout Body Text", theme.callout_text, theme.callout_bg, 4.0),
            ("Tech Badge Text", theme.tech_badge_text, theme.tech_badge_bg, 4.5),
            ("Table Header Text", theme.table_header_text, theme.table_header_bg, 3.0),
            ("Table Cell Text", theme.table_cell_text, theme.table_zebra_bg, 4.5),
        ]
        results = []
        for name, fg, bg, req in checks:
            ratio = cls.calculate_wcag_contrast(fg, bg)
            passed = (ratio >= req)
            results.append(ContrastCheckResult(
                element_name=name,
                fg_color=fg,
                bg_color=bg,
                ratio=ratio,
                required_ratio=req,
                passed=passed
            ))
        return results

    @staticmethod
    def compute_image_balance(image_path: str) -> float:
        """
        Analyzes pixel mass and density across left and right halves of a slide image.
        Returns a balance score between 0.0 and 1.0 (1.0 = balanced visual mass).
        """
        if not os.path.exists(image_path):
            return 1.0
        
        with Image.open(image_path) as img:
            gray = img.convert('L')
            arr = np.array(gray)
            h, w = arr.shape
            mid = w // 2
            
            left_half = arr[:, :mid]
            right_half = arr[:, mid:]
            
            # Measure contrast variance (content presence) in each half
            left_var = float(np.std(left_half))
            right_var = float(np.std(right_half))
            
            denom = max(1.0, max(left_var, right_var))
            diff = abs(left_var - right_var)
            balance = max(0.0, 1.0 - (diff / denom))
            return float(balance)

    @classmethod
    def audit_pdf_and_rendered_deck(
        cls,
        pdf_path: str,
        image_paths: Optional[List[str]] = None,
        theme_name: str = "sih_institutional_light"
    ) -> VisionAuditReport:
        """
        Executes end-to-end vector collision and pixel audit on compiled presentation.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at {pdf_path}")

        theme = get_theme(theme_name)
        theme_contrast_results = cls.audit_theme_contrast(theme)
        contrast_failures = [c for c in theme_contrast_results if not c.passed]

        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        page_reports = []
        total_collisions = 0
        total_margins = 0

        for page_idx in range(total_pages):
            page = doc[page_idx]
            page_num = page_idx + 1
            p_rect = page.rect
            width, height = p_rect.width, p_rect.height

            # 1. Text lines extraction from vector layout dictionary
            page_dict = page.get_text("dict")
            text_lines = []
            for b in page_dict.get("blocks", []):
                if "lines" in b:
                    for l in b["lines"]:
                        txt = "".join([s.get("text", "") for s in l.get("spans", [])]).strip()
                        if txt:
                            text_lines.append({
                                "bbox": l["bbox"],
                                "text": txt,
                                "w": l["bbox"][2] - l["bbox"][0],
                                "h": l["bbox"][3] - l["bbox"][1]
                            })

            # 2. Check pairwise bounding box collisions
            collisions = []
            for i in range(len(text_lines)):
                for j in range(i + 1, len(text_lines)):
                    b1 = text_lines[i]["bbox"]
                    b2 = text_lines[j]["bbox"]

                    # Compute intersection
                    ix0 = max(b1[0], b2[0])
                    iy0 = max(b1[1], b2[1])
                    ix1 = min(b1[2], b2[2])
                    iy1 = min(b1[3], b2[3])

                    if ix1 > ix0 and iy1 > iy0:
                        inter_w = ix1 - ix0
                        inter_h = iy1 - iy0
                        
                        # True collision threshold: significant horizontal and vertical overlap
                        # (eliminating minor ascender/descender touching of <= 4.0pt between lines)
                        if inter_w > 10.0 and inter_h > 4.0:
                            collisions.append(CollisionViolation(
                                page_number=page_num,
                                block_a_text=text_lines[i]["text"],
                                block_b_text=text_lines[j]["text"],
                                intersection_rect=(ix0, iy0, ix1, iy1)
                            ))

            # 3. Check margin containment (safe canvas zone)
            margin_violations = []
            safe_margin_x = 10.0  # 10 pt safe edge
            safe_margin_y = 8.0
            for tl in text_lines:
                bx0, by0, bx1, by1 = tl["bbox"]
                if bx0 < safe_margin_x:
                    margin_violations.append(f"Left edge overflow: x={bx0:.1f}pt for text '{tl['text'][:20]}...'")
                if bx1 > (width - safe_margin_x):
                    margin_violations.append(f"Right edge overflow: x={bx1:.1f}pt for text '{tl['text'][:20]}...'")
                if by1 > (height - safe_margin_y):
                    margin_violations.append(f"Bottom edge overflow: y={by1:.1f}pt for text '{tl['text'][:20]}...'")

            # 4. Image balance score
            balance_score = 0.85
            if image_paths and page_idx < len(image_paths):
                balance_score = cls.compute_image_balance(image_paths[page_idx])

            total_collisions += len(collisions)
            total_margins += len(margin_violations)

            page_passed = (len(collisions) == 0 and len(margin_violations) == 0 and len(contrast_failures) == 0)
            page_reports.append(PageVisionReport(
                page_number=page_num,
                has_collisions=(len(collisions) > 0),
                collisions=collisions,
                margin_violations=margin_violations,
                contrast_checks=theme_contrast_results if page_num == 1 else [],
                visual_balance_score=balance_score,
                passed=page_passed
            ))

        doc.close()

        overall_passed = (total_collisions == 0 and total_margins == 0 and len(contrast_failures) == 0)
        report = VisionAuditReport(
            total_pages=total_pages,
            passed=overall_passed,
            total_collisions=total_collisions,
            total_margin_violations=total_margins,
            total_contrast_failures=len(contrast_failures),
            page_reports=page_reports
        )
        report.generate_summary()
        return report
