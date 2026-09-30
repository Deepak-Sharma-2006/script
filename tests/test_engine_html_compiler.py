"""
Test Suite — Presentation Engine Phase 6A: Dynamic 2D Flex/Grid Layout Solver & Theme Registry
Verifies:
1. Dynamic theme registration, inheritance, custom fonts, and geometry tokens.
2. 2D Flexbox Row, Column, and 2D Grid mathematical layout solving.
3. Strict margin containment and pairwise collision freedom across arbitrary layout configurations.
"""

import unittest
from scripts.engine.theme_registry import ThemeRegistry, ExtendedThemeTokens
from scripts.engine.flex_grid_solver import (
    FlexGridSolver, Rect, LayoutNode, Row, Column, Grid, CardNode, TextNode
)


class TestEnginePhase6A(unittest.TestCase):
    """Test suite for Phase 6A flex-grid solver and dynamic theme registry."""

    def test_theme_registry_defaults(self):
        """Verifies default championship themes and design tokens are properly loaded."""
        themes = ThemeRegistry.list_themes()
        self.assertIn("cyber_dark_terminal", themes)
        self.assertIn("sih_institutional_light", themes)
        self.assertIn("modern_saas_glass", themes)
        self.assertIn("minimalist_editorial_mono", themes)

        saas = ThemeRegistry.get_extended_theme("modern_saas_glass")
        self.assertEqual(saas.font_family_heading, "Outfit")
        self.assertEqual(saas.card_border_radius_pt, 10.0)
        self.assertFalse(saas.theme.is_dark_mode)

    def test_custom_theme_registration_and_override(self):
        """Verifies dynamic runtime creation of new custom themes from user parameters."""
        custom = ThemeRegistry.create_custom_theme(
            name="emerald_agritech",
            base_theme="cyber_dark_terminal",
            canvas_bg="#064E3B",
            card_bg="#065F46",
            accent="#34D399",
            text_primary="#ECFDF5",
            font_family="Plus Jakarta Sans",
            card_border_radius_pt=14.0
        )
        self.assertEqual(custom.theme.name, "emerald_agritech")
        self.assertEqual(custom.font_family_heading, "Plus Jakarta Sans")
        self.assertEqual(custom.card_border_radius_pt, 14.0)
        self.assertEqual(custom.theme.canvas_bg, "#064E3B")

        # Verify it can be retrieved from registry
        retrieved = ThemeRegistry.get_extended_theme("emerald_agritech")
        self.assertEqual(retrieved.theme.bullet_accent, "#34D399")

    def test_flex_row_multi_column_distribution(self):
        """Verifies Row accurately distributes available width across varying flex ratios."""
        row = Row(id="main_row", gap=0.3)
        c1 = CardNode(id="col_1", flex_grow=1.0)
        c2 = CardNode(id="col_2", flex_grow=2.0)
        c3 = CardNode(id="col_3", flex_grow=1.0)
        row.add_child(c1).add_child(c2).add_child(c3)

        results = FlexGridSolver.solve(row, canvas_width=13.333, canvas_height=7.5)

        r1 = results["col_1"]
        r2 = results["col_2"]
        r3 = results["col_3"]

        # col_2 should be twice as wide as col_1 and col_3
        self.assertAlmostEqual(r2.width, r1.width * 2.0, places=2)
        self.assertAlmostEqual(r1.width, r3.width, places=2)

        # Monotonic left-to-right progression
        self.assertLess(r1.right, r2.left)
        self.assertLess(r2.right, r3.left)

        # Zero pairwise intersections
        self.assertFalse(r1.intersects(r2))
        self.assertFalse(r2.intersects(r3))
        self.assertFalse(r1.intersects(r3))

    def test_flex_grid_2x3_matrix(self):
        """Verifies 2x3 Grid mathematically divides canvas into 6 non-overlapping cells."""
        grid = Grid(id="main_grid", rows=2, cols=3, row_gap=0.25, col_gap=0.25)
        for i in range(6):
            grid.add_child(CardNode(id=f"card_{i}"))

        results = FlexGridSolver.solve(grid, canvas_width=13.333, canvas_height=7.5)
        self.assertEqual(len(results), 7)  # grid + 6 cards

        # Verify all cards have identical size
        first_card = results["card_0"]
        for i in range(1, 6):
            c = results[f"card_{i}"]
            self.assertAlmostEqual(c.width, first_card.width, places=2)
            self.assertAlmostEqual(c.height, first_card.height, places=2)

        # Verify zero pairwise intersections among all 6 cards
        card_rects = [results[f"card_{i}"] for i in range(6)]
        for i in range(6):
            for j in range(i + 1, 6):
                self.assertFalse(
                    card_rects[i].intersects(card_rects[j]),
                    f"Collision between card_{i} and card_{j}"
                )

    def test_nested_hierarchy_containment(self):
        """Verifies nested layout: Column containing top KPI row and bottom 2-column comparison."""
        root_col = Column(id="root", gap=0.3)

        # Top section: 3 KPI cards
        kpi_row = Row(id="kpi_row", height=1.6, gap=0.2)
        for i in range(3):
            kpi_row.add_child(CardNode(id=f"kpi_{i}"))

        # Bottom section: 2 feature columns (flex=1 each)
        content_row = Row(id="content_row", flex_grow=1.0, gap=0.3)
        content_row.add_child(CardNode(id="feature_left", flex_grow=1.0))
        content_row.add_child(CardNode(id="feature_right", flex_grow=1.0))

        root_col.add_child(kpi_row).add_child(content_row)

        results = FlexGridSolver.solve(root_col, canvas_width=13.333, canvas_height=7.5)

        # Verify top row is placed cleanly above content row
        kpi_rect = results["kpi_row"]
        content_rect = results["content_row"]
        self.assertLess(kpi_rect.bottom, content_rect.top)
        self.assertFalse(kpi_rect.intersects(content_rect))

        # Verify all elements stay within safe canvas boundaries
        canvas_rect = Rect(0.0, 0.0, 13.333, 7.5)
        for node_id, rect in results.items():
            self.assertTrue(canvas_rect.contains(rect), f"Node {node_id} violates canvas bounds")


if __name__ == "__main__":
    unittest.main()
