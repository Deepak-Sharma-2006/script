"""
Presentation Engine — Declarative Slide Schema (DSL)
Defines structured data classes for Decks, Slides, Archetypes, and Visual Component Primitives.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum


class SlideArchetype(str, Enum):
    TITLE_PAGE = "TITLE_PAGE"
    SPLIT_LEFT_RIGHT = "SPLIT_LEFT_RIGHT"
    SPLIT_STACK_AND_GRID = "SPLIT_STACK_AND_GRID"
    TWO_COLUMN_SECTIONS = "TWO_COLUMN_SECTIONS"
    TOP_SPLIT_BOTTOM_TABLE = "TOP_SPLIT_BOTTOM_TABLE"
    TOP_SPLIT_BOTTOM_FLOW = "TOP_SPLIT_BOTTOM_FLOW"
    CUSTOM = "CUSTOM"


@dataclass
class ColorPalette:
    canvas_bg: str = "#FFFFFF"
    header_navy: str = "#0F3A70"
    title_black: str = "#0F172A"
    bullet_blue: str = "#1D4ED8"
    accent_purple: str = "#6366F1"
    footer_blue: str = "#0D5CA8"
    callout_bg: str = "#FEF3C7"
    callout_border: str = "#D97706"
    callout_text: str = "#92400E"
    demo_border: str = "#EF4444"
    table_border: str = "#CBD5E1"
    table_zebra_bg: str = "#F8FAFC"
    success_green: str = "#10B981"
    danger_red: str = "#EF4444"


@dataclass
class DeckConfig:
    title: str
    team_name: str
    team_subtitle: str = ""
    slide_width_inches: float = 13.333
    slide_height_inches: float = 7.5
    theme_name: str = "sih_institutional_light"
    footer_text: str = "@SIH Idea submission- Template"
    sih_logo_small: Optional[str] = "specs/presentations/assets/sih_logo_header.png"
    sih_logo_large: Optional[str] = "specs/presentations/assets/sih_logo_large.png"
    colors: ColorPalette = field(default_factory=ColorPalette)


# ==============================================================================
# Component Primitives
# ==============================================================================

@dataclass
class TaggedItem:
    tag: str
    body: str


@dataclass
class TaggedBulletListSpec:
    title: str
    items: List[TaggedItem]
    title_font_size: float = 20.0
    tag_font_size: float = 10.0
    body_font_size: float = 9.0
    space_after_pt: float = 2.0
    title_color: Optional[str] = None


@dataclass
class SubSectionSpec:
    heading: str
    items: List[str]
    heading_font_size: float = 13.5
    item_font_size: float = 8.5
    space_before_pt: float = 3.0
    space_after_pt: float = 1.0


@dataclass
class MultiSectionColumnSpec:
    sections: List[SubSectionSpec]
    main_title: Optional[str] = None


@dataclass
class CalloutCardSpec:
    title: str
    facts: List[str]
    bg_color: Optional[str] = None
    border_color: Optional[str] = None
    border_width_pt: float = 1.8
    title_font_size: float = 13.0
    fact_font_size: float = 9.5


@dataclass
class ProjectLinksCardSpec:
    title: str = "• Project Links Demo:-"
    github_url: str = ""
    demo_url: str = ""
    border_color: Optional[str] = None
    border_width_pt: float = 2.5
    centered: bool = False


@dataclass
class TableSpec:
    headers: List[str]
    rows: List[List[str]]
    col_width_ratios: Optional[List[float]] = None
    header_bg_color: str = "#F1F5F9"
    zebra_bg_color: str = "#F8FAFC"
    header_font_size: float = 11.0
    body_font_size: float = 9.5
    title: Optional[str] = None


@dataclass
class ProcessFlowStep:
    title: str
    color: str
    badge_symbol: str


@dataclass
class ProcessFlowSpec:
    steps: List[ProcessFlowStep]
    title: Optional[str] = "• Process Flow :-"
    summary_text: Optional[str] = None


@dataclass
class TechBadge:
    name: str
    color: str


@dataclass
class TechCategoryColumn:
    category: str
    header_color: str
    badges: List[TechBadge]


@dataclass
class TechGridSpec:
    title: str = "TECHNOLOGIES TO BE USED:"
    columns: List[TechCategoryColumn] = field(default_factory=list)


@dataclass
class CompetitorMatrixRow:
    capability: str
    results: List[bool]


@dataclass
class CompetitorMatrixSpec:
    headers: List[str]
    rows: List[CompetitorMatrixRow]


@dataclass
class ServiceNodeSpec:
    name: str
    bullets: List[str] = field(default_factory=list)
    badge: Optional[str] = None
    accent_color: Optional[str] = None


@dataclass
class ArchitectureTierSpec:
    tier_name: str
    header_bg: str = "#1E293B"
    header_text_color: str = "#FFFFFF"
    nodes: List[ServiceNodeSpec] = field(default_factory=list)
    tier_bg: str = "#F8FAFC"
    border_color: str = "#CBD5E1"


@dataclass
class ArchitectureDiagramSpec:
    title: str = "TECHNICAL ARCHITECTURE"
    tiers: List[ArchitectureTierSpec] = field(default_factory=list)
    flow_arrow_color: str = "#0284C7"
    container_border: str = "#94A3B8"
    container_bg: str = "#FFFFFF"


@dataclass
class ChevronStepSpec:
    step_num: str
    title: str
    subtitle: str = ""
    color: str = "#1D4ED8"
    text_color: str = "#FFFFFF"


@dataclass
class ChevronPipelineSpec:
    steps: List[ChevronStepSpec] = field(default_factory=list)
    title: Optional[str] = "• Process Flow :-"
    summary_text: Optional[str] = None


@dataclass
class StatMetricSpec:
    value: str
    label: str
    subtext: str = ""
    accent_color: str = "#1D4ED8"


@dataclass
class StatGridSpec:
    metrics: List[StatMetricSpec] = field(default_factory=list)


@dataclass
class ImageAssetSpec:
    image_path: str
    width_inches: Optional[float] = None
    height_inches: Optional[float] = None


# ==============================================================================
# Slide Specification
# ==============================================================================

@dataclass
class SlideSpec:
    slide_number: int
    title: str
    archetype: SlideArchetype
    # Structured Layout Regions (Archetype-driven)
    left_column: Optional[Dict[str, Any]] = None
    right_column: Optional[Dict[str, Any]] = None
    top_left: Optional[Dict[str, Any]] = None
    top_right: Optional[Dict[str, Any]] = None
    bottom_section: Optional[Dict[str, Any]] = None
    # For Title Page
    title_metadata: Optional[List[Tuple[str, str]]] = None
    # Raw component override if custom
    custom_components: Optional[List[Dict[str, Any]]] = None


@dataclass
class DeckManifest:
    deck_config: DeckConfig
    slides: List[SlideSpec]
