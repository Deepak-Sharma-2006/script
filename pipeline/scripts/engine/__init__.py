"""
Presentation Engine Package
Declarative Schema, Constraint-based Layout Solver, Native PPTX Compiler, and Render Bridge.
"""

from scripts.engine.schema import (
    DeckConfig, SlideSpec, SlideArchetype, DeckManifest, ColorPalette,
    TaggedItem, TaggedBulletListSpec, SubSectionSpec, MultiSectionColumnSpec,
    CalloutCardSpec, ProjectLinksCardSpec, TableSpec, TechGridSpec, CompetitorMatrixSpec,
    ServiceNodeSpec, ArchitectureTierSpec, ArchitectureDiagramSpec,
    ChevronStepSpec, ChevronPipelineSpec, StatMetricSpec, StatGridSpec
)
from scripts.engine.layout_solver import LayoutSolver, Rect
from scripts.engine.diagram_generator import DiagramGenerator
from scripts.engine.pptx_compiler import PPTXCompiler
from scripts.engine.render_bridge import export_pptx_to_pdf, render_pdf_to_images, compile_and_render_deck
from scripts.engine.themes import Theme, THEMES, get_theme
from scripts.engine.visual_auditor import VisualAuditor, DeckAuditReport, SlideAuditResult
from scripts.engine.agent_creator import AgentDeckCreator
from scripts.engine.vision_qa_gate import (
    VisionQAGate, VisionAuditReport, PageVisionReport, CollisionViolation, ContrastCheckResult
)
from scripts.engine.auto_corrector import AutoCorrector
from scripts.engine.chat_research_parser import ChatResearchParser
from scripts.engine.theme_registry import ThemeRegistry, ExtendedThemeTokens
from scripts.engine.flex_grid_solver import FlexGridSolver, Row, Column, Grid, CardNode, TextNode
from scripts.engine.cognitive_analyzer import CognitiveDeckAnalyzer, DesignGrammar, SlidePattern
from scripts.engine.planner import OmniDeckPlanner, PromptDeconstructor, OmniDeckPlan, OmniSlidePlan
from scripts.engine.deck_orchestrator import DeckOrchestrator
from scripts.engine.visual_translator import VisualTranslator, ContentType
from scripts.engine.primitives import (
    draw_vector_icon, render_stat_hero_card, render_bento_card,
    render_swimlane_architecture, render_radial_ecosystem,
    render_tension_split_card, render_milestone_roadmap
)

__all__ = [
    "DeckConfig",
    "SlideSpec",
    "SlideArchetype",
    "DeckManifest",
    "ColorPalette",
    "TaggedItem",
    "TaggedBulletListSpec",
    "SubSectionSpec",
    "MultiSectionColumnSpec",
    "CalloutCardSpec",
    "ProjectLinksCardSpec",
    "TableSpec",
    "TechGridSpec",
    "CompetitorMatrixSpec",
    "ServiceNodeSpec",
    "ArchitectureTierSpec",
    "ArchitectureDiagramSpec",
    "ChevronStepSpec",
    "ChevronPipelineSpec",
    "StatMetricSpec",
    "StatGridSpec",
    "DiagramGenerator",
    "LayoutSolver",
    "Rect",
    "PPTXCompiler",
    "Theme",
    "THEMES",
    "get_theme",
    "VisualAuditor",
    "DeckAuditReport",
    "SlideAuditResult",
    "AgentDeckCreator",
    "VisionQAGate",
    "VisionAuditReport",
    "PageVisionReport",
    "CollisionViolation",
    "ContrastCheckResult",
    "AutoCorrector",
    "ChatResearchParser",
    "export_pptx_to_pdf",
    "render_pdf_to_images",
    "compile_and_render_deck",
    "ThemeRegistry",
    "ExtendedThemeTokens",
    "FlexGridSolver",
    "Row",
    "Column",
    "Grid",
    "CardNode",
    "TextNode",
    "CognitiveDeckAnalyzer",
    "DesignGrammar",
    "SlidePattern",
    "OmniDeckPlanner",
    "PromptDeconstructor",
    "OmniDeckPlan",
    "OmniSlidePlan",
    "DeckOrchestrator",
    "draw_vector_icon",
    "render_stat_hero_card",
    "render_bento_card",
    "render_swimlane_architecture",
    "render_radial_ecosystem",
    "render_tension_split_card",
    "render_milestone_roadmap",
    "VisualTranslator",
    "ContentType"
]
