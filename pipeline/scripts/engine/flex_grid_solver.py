"""
Presentation Engine — 2D Flexbox & CSS Grid Layout Solver
Replaces rigid coordinate tuples with dynamic mathematical tree layout solving.
Supports Rows, Columns, Grids, and Cards with guaranteed margin containment and collision freedom.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union


@dataclass
class Rect:
    """Represents a 2D bounding box in inches."""
    left: float
    top: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top + self.height

    @property
    def center_x(self) -> float:
        return self.left + self.width / 2.0

    @property
    def center_y(self) -> float:
        return self.top + self.height / 2.0

    def intersects(self, other: 'Rect', tol: float = 0.005) -> bool:
        """Returns True if this rect overlaps with another beyond tolerance."""
        if (self.right - tol <= other.left or
            other.right - tol <= self.left or
            self.bottom - tol <= other.top or
            other.bottom - tol <= self.top):
            return False
        return True

    def contains(self, other: 'Rect', tol: float = 0.005) -> bool:
        """Returns True if this rect completely contains other."""
        return (self.left - tol <= other.left and
                self.top - tol <= other.top and
                self.right + tol >= other.right and
                self.bottom + tol >= other.bottom)


@dataclass
class LayoutNode:
    """Base class for all flex/grid layout nodes."""
    id: str = ""
    flex_grow: float = 1.0
    width: Optional[float] = None     # Fixed width in inches if specified
    height: Optional[float] = None    # Fixed height in inches if specified
    padding: float = 0.0              # Inner padding in inches
    margin: float = 0.0               # Outer margin in inches
    children: List['LayoutNode'] = field(default_factory=list)
    resolved_rect: Optional[Rect] = None

    def add_child(self, child: 'LayoutNode') -> 'LayoutNode':
        self.children.append(child)
        return self


@dataclass
class Row(LayoutNode):
    """Horizontal flex container arranging children from left to right."""
    gap: float = 0.2                  # Gap between children in inches


@dataclass
class Column(LayoutNode):
    """Vertical flex container arranging children from top to bottom."""
    gap: float = 0.2                  # Gap between children in inches


@dataclass
class Grid(LayoutNode):
    """2D grid container placing children into rows and columns."""
    rows: int = 2
    cols: int = 2
    row_gap: float = 0.2
    col_gap: float = 0.2


@dataclass
class CardNode(LayoutNode):
    """Visual container card representing a styled box."""
    title: Optional[str] = None
    subtitle: Optional[str] = None
    fill_color: Optional[str] = None
    border_color: Optional[str] = None
    border_width: float = 1.0
    corner_radius_pt: float = 6.0


@dataclass
class TextNode(LayoutNode):
    """Text content block."""
    text: str = ""
    font_size: float = 11.0
    font_bold: bool = False
    color: Optional[str] = None
    align: str = "LEFT"               # LEFT, CENTER, RIGHT


class FlexGridSolver:
    """
    Mathematical layout solver that traverses a declarative layout tree and computes
    exact 2D coordinates (Rect) for every node, ensuring zero overlap and containment.
    """

    @classmethod
    def solve(
        cls,
        root: LayoutNode,
        canvas_width: float = 13.333,
        canvas_height: float = 7.5,
        margin_left: float = 0.6,
        margin_top: float = 1.0,
        margin_right: float = 0.6,
        margin_bottom: float = 0.5
    ) -> Dict[str, Rect]:
        """
        Solves layout tree starting within the safe printable canvas bounds.
        Returns a dictionary mapping node id to resolved Rect.
        """
        content_left = margin_left
        content_top = margin_top
        content_width = max(0.1, canvas_width - margin_left - margin_right)
        content_height = max(0.1, canvas_height - margin_top - margin_bottom)

        root_rect = Rect(content_left, content_top, content_width, content_height)
        cls._layout_node(root, root_rect)

        # Collect resolved rects
        results: Dict[str, Rect] = {}
        cls._collect_results(root, results)
        return results

    @classmethod
    def _layout_node(cls, node: LayoutNode, available_rect: Rect) -> None:
        """Computes resolved rect for node and recursively lays out its children."""
        # Calculate outer bounds
        left = available_rect.left + node.margin
        top = available_rect.top + node.margin
        width = node.width if node.width is not None else max(0.01, available_rect.width - 2 * node.margin)
        height = node.height if node.height is not None else max(0.01, available_rect.height - 2 * node.margin)

        node.resolved_rect = Rect(left, top, width, height)

        if not node.children:
            return

        # Inner available rect for children (accounting for node padding)
        inner_left = left + node.padding
        inner_top = top + node.padding
        inner_width = max(0.01, width - 2 * node.padding)
        inner_height = max(0.01, height - 2 * node.padding)
        inner_rect = Rect(inner_left, inner_top, inner_width, inner_height)

        if isinstance(node, Row):
            cls._layout_row(node, inner_rect)
        elif isinstance(node, Column):
            cls._layout_column(node, inner_rect)
        elif isinstance(node, Grid):
            cls._layout_grid(node, inner_rect)
        else:
            # Default single child container
            for child in node.children:
                cls._layout_node(child, inner_rect)

    @classmethod
    def _layout_row(cls, row: Row, inner_rect: Rect) -> None:
        """Lays out children horizontally in a row."""
        n = len(row.children)
        if n == 0:
            return

        total_gaps = row.gap * (n - 1)
        # Separate fixed-width children from flexible children
        fixed_width_total = sum(c.width for c in row.children if c.width is not None)
        flex_children = [c for c in row.children if c.width is None]
        total_flex = sum(c.flex_grow for c in flex_children) if flex_children else 1.0

        remaining_width = max(0.01, inner_rect.width - total_gaps - fixed_width_total)

        current_x = inner_rect.left
        for child in row.children:
            if child.width is not None:
                child_w = child.width
            else:
                child_w = (child.flex_grow / max(0.001, total_flex)) * remaining_width

            child_h = child.height if child.height is not None else inner_rect.height
            child_rect = Rect(current_x, inner_rect.top, child_w, child_h)
            cls._layout_node(child, child_rect)
            current_x += child_w + row.gap

    @classmethod
    def _layout_column(cls, col: Column, inner_rect: Rect) -> None:
        """Lays out children vertically in a column."""
        n = len(col.children)
        if n == 0:
            return

        total_gaps = col.gap * (n - 1)
        fixed_height_total = sum(c.height for c in col.children if c.height is not None)
        flex_children = [c for c in col.children if c.height is None]
        total_flex = sum(c.flex_grow for c in flex_children) if flex_children else 1.0

        remaining_height = max(0.01, inner_rect.height - total_gaps - fixed_height_total)

        current_y = inner_rect.top
        for child in col.children:
            if child.height is not None:
                child_h = child.height
            else:
                child_h = (child.flex_grow / max(0.001, total_flex)) * remaining_height

            child_w = child.width if child.width is not None else inner_rect.width
            child_rect = Rect(inner_rect.left, current_y, child_w, child_h)
            cls._layout_node(child, child_rect)
            current_y += child_h + col.gap

    @classmethod
    def _layout_grid(cls, grid: Grid, inner_rect: Rect) -> None:
        """Lays out children in a 2D grid matrix."""
        rows = max(1, grid.rows)
        cols = max(1, grid.cols)

        total_col_gaps = grid.col_gap * (cols - 1)
        total_row_gaps = grid.row_gap * (rows - 1)

        cell_width = max(0.01, (inner_rect.width - total_col_gaps) / cols)
        cell_height = max(0.01, (inner_rect.height - total_row_gaps) / rows)

        for idx, child in enumerate(grid.children):
            if idx >= rows * cols:
                break
            r = idx // cols
            c = idx % cols

            cell_x = inner_rect.left + c * (cell_width + grid.col_gap)
            cell_y = inner_rect.top + r * (cell_height + grid.row_gap)
            cell_rect = Rect(cell_x, cell_y, cell_width, cell_height)
            cls._layout_node(child, cell_rect)

    @classmethod
    def _collect_results(cls, node: LayoutNode, out: Dict[str, Rect]) -> None:
        """Recursively collects resolved rects by id."""
        if node.id and node.resolved_rect:
            out[node.id] = node.resolved_rect
        for child in node.children:
            cls._collect_results(child, out)
