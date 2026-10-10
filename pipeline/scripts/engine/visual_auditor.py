"""
Presentation Engine — Visual Layout & Density Heuristic Auditor
Automated quality gate inspecting slide manifests, geometric boundaries, and readability metrics.
"""

from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field
from scripts.engine.schema import DeckManifest, SlideSpec, SlideArchetype
from scripts.engine.layout_solver import LayoutSolver, Rect


@dataclass
class SlideAuditResult:
    slide_number: int
    title: str
    archetype: str
    character_count: int
    density_status: str  # "OPTIMAL", "SPARSE", "OVERCROWDED"
    has_visual_element: bool
    violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class DeckAuditReport:
    total_slides: int
    passed: bool
    violations: List[str]
    warnings: List[str]
    slide_results: List[SlideAuditResult]

    def summary(self) -> str:
        lines = [
            f"=== PRESENTATION QUALITY AUDIT REPORT ===",
            f"Total Slides: {self.total_slides}",
            f"Audit Status: {'PASSED (Zero Violations)' if self.passed else 'FAILED'}",
            f"Total Violations: {len(self.violations)}",
            f"Total Warnings: {len(self.warnings)}",
            "-----------------------------------------"
        ]
        for r in self.slide_results:
            lines.append(f"Slide {r.slide_number} ({r.archetype}): {r.character_count} chars | Density: {r.density_status} | Visual Element: {'YES' if r.has_visual_element else 'NO'}")
            for v in r.violations:
                lines.append(f"   [VIOLATION] {v}")
            for w in r.warnings:
                lines.append(f"   [WARNING] {w}")
        return "\n".join(lines)


class VisualAuditor:
    """
    Analyzes presentation manifests and layout constraints before final export.
    """

    @staticmethod
    def count_characters(obj: Any) -> int:
        """Recursively counts characters across text fields in a component."""
        count = 0
        if isinstance(obj, str):
            return len(obj)
        elif isinstance(obj, list):
            for item in obj:
                count += VisualAuditor.count_characters(item)
        elif isinstance(obj, dict):
            for val in obj.values():
                count += VisualAuditor.count_characters(val)
        elif hasattr(obj, "__dict__"):
            for val in obj.__dict__.values():
                count += VisualAuditor.count_characters(val)
        return count

    @classmethod
    def audit_deck(cls, manifest: DeckManifest) -> DeckAuditReport:
        """Runs comprehensive visual quality and density heuristics on manifest."""
        violations = []
        warnings = []
        slide_results = []

        total_slides = len(manifest.slides)
        if total_slides < 5 or total_slides > 12:
            warnings.append(f"Slide count ({total_slides}) is atypical for championship pitch (expected 6-8 slides).")

        for slide in manifest.slides:
            s_violations = []
            s_warnings = []
            char_count = cls.count_characters(slide)

            # Density heuristics
            if char_count < 250:
                density = "SPARSE"
                if slide.slide_number > 1:
                    s_warnings.append(f"Slide content may be too sparse ({char_count} chars). Add more technical specifics.")
            elif char_count > 1800:
                density = "OVERCROWDED"
                s_violations.append(f"Slide text ({char_count} chars) exceeds 1800 character ceiling. Risk of text overflow.")
            else:
                density = "OPTIMAL"

            # Check for visual components
            has_visual = False
            if slide.archetype == SlideArchetype.TITLE_PAGE:
                has_visual = True
            else:
                for col in [slide.left_column, slide.right_column, slide.top_left, slide.top_right, slide.bottom_section]:
                    if col and any(k in col for k in [
                        "diagram_component", "flow_component", "tech_grid_component",
                        "matrix_component", "component", "image_path", "top_image_path", "mid_image_path"
                    ]):
                        has_visual = True
                        break

            if not has_visual and slide.slide_number > 1:
                s_violations.append("Slide contains zero visual elements (pure text detected). SIH guidelines mandate visuals.")

            # Bounds validation
            regions = LayoutSolver.get_archetype_layout(slide.archetype)
            for name, r in regions.items():
                if r.x < 0.30 or (r.x + r.w) > 13.05:
                    s_violations.append(f"Region '{name}' violates horizontal margin bounds: x={r.x}, right={r.x + r.w}.")
                if r.y < 0.25 or (r.y + r.h) > 7.10:
                    s_violations.append(f"Region '{name}' violates vertical canvas limits: y={r.y}, bottom={r.y + r.h}.")

            violations.extend(s_violations)
            warnings.extend(s_warnings)

            slide_results.append(SlideAuditResult(
                slide_number=slide.slide_number,
                title=slide.title,
                archetype=slide.archetype.value,
                character_count=char_count,
                density_status=density,
                has_visual_element=has_visual,
                violations=s_violations,
                warnings=s_warnings
            ))

        passed = (len(violations) == 0)
        return DeckAuditReport(
            total_slides=total_slides,
            passed=passed,
            violations=violations,
            warnings=warnings,
            slide_results=slide_results
        )
