"""
Presentation Engine — Native Vector Diagram Generator
Calculates coordinate geometry and layout structures for complex technical visuals
(Multi-tier architectures, chevron process flows, tech stack grids, and stat cards).
"""

from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from scripts.engine.layout_solver import Rect
from scripts.engine.schema import (
    ArchitectureDiagramSpec,
    ArchitectureTierSpec,
    ServiceNodeSpec,
    ChevronPipelineSpec,
    ChevronStepSpec,
    TechGridSpec,
    StatGridSpec,
    StatMetricSpec,
)


@dataclass
class ServiceNodeGeometry:
    rect: Rect
    node: ServiceNodeSpec


@dataclass
class TierGeometry:
    tier_rect: Rect
    header_rect: Rect
    nodes: List[ServiceNodeGeometry]
    tier_spec: ArchitectureTierSpec


@dataclass
class ArchitectureLayout:
    outer_rect: Rect
    title_rect: Optional[Rect]
    tiers: List[TierGeometry]
    inter_tier_connectors: List[Tuple[float, float, float, float]]  # (x1, y1, x2, y2)


@dataclass
class ChevronStepGeometry:
    rect: Rect
    step: ChevronStepSpec
    arrow_rect: Optional[Rect] = None


@dataclass
class ChevronPipelineLayout:
    title_rect: Optional[Rect]
    steps: List[ChevronStepGeometry]
    summary_rect: Optional[Rect] = None


@dataclass
class TechBadgeGeometry:
    rect: Rect
    name: str
    color: str


@dataclass
class TechColumnGeometry:
    outer_rect: Rect
    header_rect: Rect
    category_name: str
    header_color: str
    badges: List[TechBadgeGeometry]


@dataclass
class TechGridLayout:
    title_rect: Optional[Rect]
    columns: List[TechColumnGeometry]


@dataclass
class StatCardGeometry:
    rect: Rect
    metric: StatMetricSpec


class DiagramGenerator:
    """
    Computes strict vector geometry for complex visual components
    ensuring mathematical boundary containment.
    """

    @staticmethod
    def solve_architecture_layout(
        rect: Rect,
        spec: ArchitectureDiagramSpec
    ) -> ArchitectureLayout:
        """
        Solves multi-tier microservice architecture layout.
        Each tier is stacked vertically with a header bar, inner service nodes,
        and connector arrows between tiers.
        """
        has_title = bool(spec.title)
        title_h = 0.32 if has_title else 0.0
        title_rect = Rect(x=rect.x, y=rect.y, w=rect.w, h=title_h) if has_title else None

        avail_y = rect.y + title_h + (0.06 if has_title else 0.0)
        avail_h = rect.h - title_h - (0.06 if has_title else 0.0)

        num_tiers = len(spec.tiers)
        if num_tiers == 0:
            return ArchitectureLayout(outer_rect=rect, title_rect=title_rect, tiers=[], inter_tier_connectors=[])

        tier_gap = 0.12
        total_gap = (num_tiers - 1) * tier_gap
        tier_h = (avail_h - total_gap) / num_tiers

        tier_geometries = []
        connectors = []

        for i, tier in enumerate(spec.tiers):
            t_y = avail_y + i * (tier_h + tier_gap)
            t_rect = Rect(x=rect.x, y=t_y, w=rect.w, h=tier_h)

            # Header bar inside tier
            hdr_h = 0.24
            hdr_rect = Rect(x=t_rect.x, y=t_rect.y, w=t_rect.w, h=hdr_h)

            # Service nodes inside tier
            num_nodes = len(tier.nodes)
            node_geoms = []
            if num_nodes > 0:
                node_gap = 0.08
                node_margin_x = 0.08
                node_margin_y = 0.06
                node_area_w = t_rect.w - 2 * node_margin_x
                node_area_h = t_rect.h - hdr_h - 2 * node_margin_y

                node_w = (node_area_w - (num_nodes - 1) * node_gap) / num_nodes
                node_y = t_rect.y + hdr_h + node_margin_y

                for j, node in enumerate(tier.nodes):
                    n_x = t_rect.x + node_margin_x + j * (node_w + node_gap)
                    n_rect = Rect(x=n_x, y=node_y, w=node_w, h=node_area_h)
                    node_geoms.append(ServiceNodeGeometry(rect=n_rect, node=node))

            tier_geoms = TierGeometry(
                tier_rect=t_rect,
                header_rect=hdr_rect,
                nodes=node_geoms,
                tier_spec=tier
            )
            tier_geometries.append(tier_geoms)

            # Connector arrows to next tier
            if i < num_tiers - 1:
                # Downward connector in the center
                c_x = rect.x + rect.w / 2.0
                c_y1 = t_y + tier_h
                c_y2 = t_y + tier_h + tier_gap
                connectors.append((c_x, c_y1, c_x, c_y2))

        return ArchitectureLayout(
            outer_rect=rect,
            title_rect=title_rect,
            tiers=tier_geometries,
            inter_tier_connectors=connectors
        )

    @staticmethod
    def solve_chevron_pipeline(
        rect: Rect,
        spec: ChevronPipelineSpec
    ) -> ChevronPipelineLayout:
        """
        Solves horizontal chevron process pipeline.
        Distributes steps evenly across container width.
        """
        has_title = bool(spec.title)
        title_h = 0.32 if has_title else 0.0
        title_rect = Rect(x=rect.x, y=rect.y, w=rect.w, h=title_h) if has_title else None

        has_summary = bool(spec.summary_text)
        summary_h = 0.28 if has_summary else 0.0

        flow_y = rect.y + title_h + (0.04 if has_title else 0.0)
        flow_h = rect.h - title_h - summary_h - (0.08 if has_title or has_summary else 0.0)

        num_steps = len(spec.steps)
        if num_steps == 0:
            return ChevronPipelineLayout(title_rect=title_rect, steps=[], summary_rect=None)

        step_gap = 0.06
        arrow_w = 0.12  # between cards if not using raw chevron shape
        total_gaps = (num_steps - 1) * (step_gap + arrow_w)
        step_w = (rect.w - total_gaps) / num_steps

        step_geometries = []
        for i, step in enumerate(spec.steps):
            s_x = rect.x + i * (step_w + step_gap + arrow_w)
            s_rect = Rect(x=s_x, y=flow_y, w=step_w, h=flow_h)

            arr_rect = None
            if i < num_steps - 1:
                a_x = s_x + step_w + (step_gap / 2.0)
                a_y = flow_y + flow_h / 2.0 - 0.08
                arr_rect = Rect(x=a_x, y=a_y, w=arrow_w, h=0.16)

            step_geometries.append(ChevronStepGeometry(rect=s_rect, step=step, arrow_rect=arr_rect))

        summary_rect = None
        if has_summary:
            summary_y = flow_y + flow_h + 0.06
            summary_rect = Rect(x=rect.x, y=summary_y, w=rect.w, h=summary_h)

        return ChevronPipelineLayout(
            title_rect=title_rect,
            steps=step_geometries,
            summary_rect=summary_rect
        )

    @staticmethod
    def solve_tech_grid(
        rect: Rect,
        spec: TechGridSpec
    ) -> TechGridLayout:
        """
        Solves multi-column categorized tech stack grid.
        """
        has_title = bool(spec.title)
        title_h = 0.28 if has_title else 0.0
        title_rect = Rect(x=rect.x, y=rect.y, w=rect.w, h=title_h) if has_title else None

        grid_y = rect.y + title_h + (0.05 if has_title else 0.0)
        grid_h = rect.h - title_h - (0.05 if has_title else 0.0)

        num_cols = len(spec.columns)
        if num_cols == 0:
            return TechGridLayout(title_rect=title_rect, columns=[])

        col_gap = 0.10
        total_col_gap = (num_cols - 1) * col_gap
        col_w = (rect.w - total_col_gap) / num_cols

        columns_geoms = []
        for i, col in enumerate(spec.columns):
            c_x = rect.x + i * (col_w + col_gap)
            c_rect = Rect(x=c_x, y=grid_y, w=col_w, h=grid_h)

            # Header rect
            hdr_h = 0.32
            hdr_rect = Rect(x=c_rect.x, y=c_rect.y, w=c_rect.w, h=hdr_h)

            # Badges stacked inside column
            num_badges = len(col.badges)
            badge_geoms = []
            if num_badges > 0:
                badge_gap = 0.06
                badge_margin_y = 0.08
                badge_margin_x = 0.08
                avail_badge_h = c_rect.h - hdr_h - 2 * badge_margin_y
                badge_h = min(0.32, (avail_badge_h - (num_badges - 1) * badge_gap) / num_badges)
                badge_w = c_rect.w - 2 * badge_margin_x

                for j, b in enumerate(col.badges):
                    b_y = c_rect.y + hdr_h + badge_margin_y + j * (badge_h + badge_gap)
                    b_rect = Rect(x=c_rect.x + badge_margin_x, y=b_y, w=badge_w, h=badge_h)
                    badge_geoms.append(TechBadgeGeometry(rect=b_rect, name=b.name, color=b.color))

            columns_geoms.append(TechColumnGeometry(
                outer_rect=c_rect,
                header_rect=hdr_rect,
                category_name=col.category,
                header_color=col.header_color,
                badges=badge_geoms
            ))

        return TechGridLayout(title_rect=title_rect, columns=columns_geoms)

    @staticmethod
    def solve_stat_grid(
        rect: Rect,
        spec: StatGridSpec
    ) -> List[StatCardGeometry]:
        """
        Solves horizontal row of KPI / stat cards.
        """
        num_metrics = len(spec.metrics)
        if num_metrics == 0:
            return []

        gap = 0.10
        card_w = (rect.w - (num_metrics - 1) * gap) / num_metrics

        cards = []
        for i, m in enumerate(spec.metrics):
            c_x = rect.x + i * (card_w + gap)
            c_rect = Rect(x=c_x, y=rect.y, w=card_w, h=rect.h)
            cards.append(StatCardGeometry(rect=c_rect, metric=m))

        return cards
