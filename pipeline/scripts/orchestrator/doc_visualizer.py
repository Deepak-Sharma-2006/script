"""
Documentation Visualizer & Diagram Generator
Generates high-resolution executive-grade visual diagrams (PNG) for direct embedding
into markdown documentation, implementation plans, dossiers, and walkthroughs.
Eliminates naked, unrendered code blocks and delivers publication-grade aesthetics.
"""

import os
from typing import List, Dict, Any, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont


def _get_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    """Loads modern Segoe UI / Arial font with fallback."""
    font_names = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"
    ]
    for path in font_names:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


class DocVisualizer:
    """
    Renders clean, enterprise-aesthetic graphics (dark or light theme)
    for markdown documentation, dossiers, and executive summaries.
    """

    @classmethod
    def render_flowchart(
        cls,
        steps: List[Tuple[str, str]],
        output_path: str,
        title: str = "SYSTEM PIPELINE FLOW",
        theme: str = "dark"
    ) -> str:
        """
        Renders a horizontal process flow pipeline graphic with glowing step connectors.
        steps: list of (Step Name, Description)
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        is_dark = theme == "dark"

        bg_col = _hex_to_rgb("#0B0F19" if is_dark else "#F8FAFC")
        card_col = _hex_to_rgb("#111827" if is_dark else "#FFFFFF")
        border_col = _hex_to_rgb("#1F2937" if is_dark else "#CBD5E1")
        title_col = _hex_to_rgb("#F9FAFB" if is_dark else "#0F172A")
        body_col = _hex_to_rgb("#E5E7EB" if is_dark else "#334155")
        muted_col = _hex_to_rgb("#9CA3AF" if is_dark else "#64748B")
        accent_col = _hex_to_rgb("#00F0FF" if is_dark else "#1D4ED8")
        step_bg = _hex_to_rgb("#1E293B" if is_dark else "#EEF2FF")

        img_w = 1600
        img_h = 420
        img = Image.new("RGB", (img_w, img_h), color=bg_col)
        draw = ImageDraw.Draw(img)

        # Title
        font_title = _get_font(26, bold=True)
        font_card_title = _get_font(18, bold=True)
        font_body = _get_font(14, bold=False)
        font_badge = _get_font(13, bold=True)

        draw.text((60, 40), title, fill=title_col, font=font_title)
        draw.line([(60, 80), (img_w - 60, 80)], fill=border_col, width=2)

        # Step Cards
        n = max(1, len(steps))
        margin_x = 60
        gap = 35
        card_y = 120
        card_h = 240
        avail_w = img_w - (2 * margin_x) - (n - 1) * gap
        card_w = avail_w // n

        for idx, (step_title, step_desc) in enumerate(steps):
            cx = margin_x + idx * (card_w + gap)

            # Connector Arrow to next card
            if idx < n - 1:
                arrow_x = cx + card_w
                arrow_y = card_y + card_h // 2
                draw.line([(arrow_x + 5, arrow_y), (arrow_x + gap - 5, arrow_y)], fill=accent_col, width=3)
                # Arrowhead
                draw.polygon([
                    (arrow_x + gap - 5, arrow_y),
                    (arrow_x + gap - 15, arrow_y - 7),
                    (arrow_x + gap - 15, arrow_y + 7)
                ], fill=accent_col)

            # Card Container
            draw.rounded_rectangle(
                [cx, card_y, cx + card_w, card_y + card_h],
                radius=14,
                fill=card_col,
                outline=border_col,
                width=2
            )

            # Top Accent Badge
            badge_text = f"STAGE {idx + 1:02d}"
            draw.rounded_rectangle(
                [cx + 20, card_y + 20, cx + 110, card_y + 48],
                radius=6,
                fill=step_bg,
                outline=accent_col,
                width=1
            )
            draw.text((cx + 28, card_y + 26), badge_text, fill=accent_col, font=font_badge)

            # Step Title
            draw.text((cx + 20, card_y + 65), step_title, fill=title_col, font=font_card_title)

            # Step Description (Word wrap simple)
            words = step_desc.split()
            lines = []
            curr_line = []
            for w in words:
                curr_line.append(w)
                if len(" ".join(curr_line)) > 26:
                    lines.append(" ".join(curr_line))
                    curr_line = []
            if curr_line:
                lines.append(" ".join(curr_line))

            desc_y = card_y + 105
            for line_str in lines[:5]:
                draw.text((cx + 20, desc_y), line_str, fill=body_col, font=font_body)
                desc_y += 24

        img.save(output_path, "PNG", dpi=(200, 200))
        img.close()
        return output_path

    @classmethod
    def render_architecture_topology(
        cls,
        tiers: List[Dict[str, Any]],
        output_path: str,
        title: str = "SYSTEM ARCHITECTURE & MICROSERVICE TOPOLOGY",
        theme: str = "dark"
    ) -> str:
        """
        Renders a multi-tier horizontal system architecture diagram.
        tiers: list of dicts with keys: 'name', 'nodes' (list of str)
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        is_dark = theme == "dark"

        bg_col = _hex_to_rgb("#0B0F19" if is_dark else "#F8FAFC")
        card_col = _hex_to_rgb("#111827" if is_dark else "#FFFFFF")
        border_col = _hex_to_rgb("#1F2937" if is_dark else "#CBD5E1")
        title_col = _hex_to_rgb("#F9FAFB" if is_dark else "#0F172A")
        tier_header_bg = _hex_to_rgb("#1E293B" if is_dark else "#1D4ED8")
        node_bg = _hex_to_rgb("#1F2937" if is_dark else "#F1F5F9")
        node_border = _hex_to_rgb("#0284C7" if is_dark else "#94A3B8")
        node_text = _hex_to_rgb("#F3F4F6" if is_dark else "#0F172A")
        accent_col = _hex_to_rgb("#00F0FF" if is_dark else "#1D4ED8")

        n_tiers = max(1, len(tiers))
        img_w = 1600
        tier_h = 105
        tier_gap = 25
        img_h = 120 + n_tiers * (tier_h + tier_gap)

        img = Image.new("RGB", (img_w, img_h), color=bg_col)
        draw = ImageDraw.Draw(img)

        font_title = _get_font(26, bold=True)
        font_tier = _get_font(16, bold=True)
        font_node = _get_font(14, bold=True)

        draw.text((60, 35), title, fill=title_col, font=font_title)
        draw.line([(60, 75), (img_w - 60, 75)], fill=border_col, width=2)

        margin_x = 60
        start_y = 100

        for idx, tier in enumerate(tiers):
            ty = start_y + idx * (tier_h + tier_gap)

            # Connector Arrow to next tier down
            if idx < n_tiers - 1:
                mid_x = img_w // 2
                draw.line([(mid_x, ty + tier_h + 2), (mid_x, ty + tier_h + tier_gap - 2)], fill=accent_col, width=3)
                draw.polygon([
                    (mid_x, ty + tier_h + tier_gap - 2),
                    (mid_x - 7, ty + tier_h + tier_gap - 12),
                    (mid_x + 7, ty + tier_h + tier_gap - 12)
                ], fill=accent_col)

            # Tier Outer Container
            draw.rounded_rectangle(
                [margin_x, ty, img_w - margin_x, ty + tier_h],
                radius=12,
                fill=card_col,
                outline=border_col,
                width=2
            )

            # Left Tier Header Ribbon
            ribbon_w = 280
            draw.rounded_rectangle(
                [margin_x, ty, margin_x + ribbon_w, ty + tier_h],
                radius=12,
                fill=tier_header_bg,
                outline=border_col,
                width=2
            )
            draw.text((margin_x + 25, ty + (tier_h - 22) // 2), tier.get("name", f"Tier {idx+1}"), fill=_hex_to_rgb("#FFFFFF"), font=font_tier)

            # Service Nodes inside this tier
            nodes = tier.get("nodes", [])
            if nodes:
                nodes_area_x = margin_x + ribbon_w + 30
                nodes_area_w = img_w - margin_x - nodes_area_x - 30
                n_nodes = len(nodes)
                node_gap = 20
                node_w = (nodes_area_w - (n_nodes - 1) * node_gap) // n_nodes
                node_h = 55
                node_y = ty + (tier_h - node_h) // 2

                for n_idx, node_name in enumerate(nodes):
                    nx = nodes_area_x + n_idx * (node_w + node_gap)
                    draw.rounded_rectangle(
                        [nx, node_y, nx + node_w, node_y + node_h],
                        radius=8,
                        fill=node_bg,
                        outline=node_border,
                        width=1
                    )
                    draw.text((nx + 15, node_y + (node_h - 18) // 2), node_name, fill=node_text, font=font_node)

        img.save(output_path, "PNG", dpi=(200, 200))
        img.close()
        return output_path

    @classmethod
    def render_kpi_dashboard(
        cls,
        kpis: List[Dict[str, str]],
        output_path: str,
        title: str = "EMPIRICAL PERFORMANCE & BENCHMARK METRICS",
        theme: str = "dark"
    ) -> str:
        """
        Renders an executive KPI dashboard graphic with big typography metrics and delta badges.
        kpis: list of dicts with 'number', 'label', 'delta', 'caption'
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        is_dark = theme == "dark"

        bg_col = _hex_to_rgb("#0B0F19" if is_dark else "#F8FAFC")
        card_col = _hex_to_rgb("#111827" if is_dark else "#FFFFFF")
        border_col = _hex_to_rgb("#1F2937" if is_dark else "#CBD5E1")
        title_col = _hex_to_rgb("#F9FAFB" if is_dark else "#0F172A")
        metric_col = _hex_to_rgb("#00F0FF" if is_dark else "#1D4ED8")
        label_col = _hex_to_rgb("#F3F4F6" if is_dark else "#0F172A")
        caption_col = _hex_to_rgb("#9CA3AF" if is_dark else "#64748B")
        green_badge = _hex_to_rgb("#10B981")

        img_w = 1600
        img_h = 380
        img = Image.new("RGB", (img_w, img_h), color=bg_col)
        draw = ImageDraw.Draw(img)

        font_title = _get_font(26, bold=True)
        font_metric = _get_font(42, bold=True)
        font_label = _get_font(18, bold=True)
        font_caption = _get_font(14, bold=False)
        font_badge = _get_font(12, bold=True)

        draw.text((60, 40), title, fill=title_col, font=font_title)
        draw.line([(60, 80), (img_w - 60, 80)], fill=border_col, width=2)

        n = max(1, len(kpis))
        margin_x = 60
        gap = 35
        card_y = 115
        card_h = 220
        avail_w = img_w - (2 * margin_x) - (n - 1) * gap
        card_w = avail_w // n

        for idx, kpi in enumerate(kpis):
            cx = margin_x + idx * (card_w + gap)

            # Card Container
            draw.rounded_rectangle(
                [cx, card_y, cx + card_w, card_y + card_h],
                radius=14,
                fill=card_col,
                outline=border_col,
                width=2
            )

            # Top Delta Pill
            delta = kpi.get("delta") or kpi.get("trend") or "+Verified"
            draw.rounded_rectangle(
                [cx + card_w - 140, card_y + 20, cx + card_w - 20, card_y + 50],
                radius=6,
                fill=green_badge
            )
            draw.text((cx + card_w - 130, card_y + 27), delta, fill=_hex_to_rgb("#FFFFFF"), font=font_badge)

            # Big Metric
            num_str = kpi.get("number") or kpi.get("value") or "100%"
            draw.text((cx + 25, card_y + 25), num_str, fill=metric_col, font=font_metric)

            # Label
            lbl = kpi.get("label", "Metric")
            draw.text((cx + 25, card_y + 115), lbl, fill=label_col, font=font_label)

            # Caption
            cap = kpi.get("caption", "Empirical measurement")
            draw.text((cx + 25, card_y + 155), cap, fill=caption_col, font=font_caption)

        img.save(output_path, "PNG", dpi=(200, 200))
        img.close()
        return output_path
