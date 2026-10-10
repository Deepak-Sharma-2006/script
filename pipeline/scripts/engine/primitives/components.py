"""
Presentation Engine — Championship Visual Primitives Library
Implements 7 native PowerPoint vector diagram components:
1. StatHeroCard (Giant KPI metric + trend badge + icon)
2. BentoCard (Modular feature tile with vector icon & bold lead-in bullets)
3. SwimlaneArchitecture (Multi-tier architectural lanes with forward connectors)
4. RadialEcosystem (Hub-and-spoke central core with satellite nodes)
5. FunnelFlow (Graduated triage / defense-in-depth pipeline)
6. TensionSplitCard (Dual Problem vs. Solution comparative card)
7. MilestoneRoadmap (Phase timeline with pins, status badges & deliverables)
"""

import math
from typing import List, Dict, Any, Optional
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

from scripts.engine.flex_grid_solver import Rect
from scripts.engine.themes import Theme
from scripts.engine.theme_registry import ExtendedThemeTokens
from scripts.engine.primitives.vector_icons import draw_vector_icon


def hex_to_rgb(hex_str: str) -> RGBColor:
    hex_clean = hex_str.lstrip('#')
    if len(hex_clean) == 3:
        hex_clean = ''.join([c * 2 for c in hex_clean])
    return RGBColor(*(int(hex_clean[i:i+2], 16) for i in (0, 2, 4)))


def render_stat_hero_card(
    slide,
    rect: Rect,
    stat_number: str,
    stat_label: str,
    delta_pill: Optional[str] = None,
    caption: Optional[str] = None,
    icon_type: Optional[str] = "chart",
    theme: Optional[Theme] = None,
    tokens: Optional[ExtendedThemeTokens] = None
) -> None:
    """Renders a giant typography KPI metric card with trend pill badge and optional icon."""
    t = theme or Theme(name="default", is_dark_mode=False, canvas_bg="#FFF", card_bg="#FFF", card_border="#DDD", title_primary="#000", subtitle_color="#444", body_text="#222", muted_text="#666", bullet_accent="#1D4ED8", team_badge_bg="#FFF", team_badge_border="#1D4ED8", team_badge_text="#000", header_title_color="#000", footer_bg="#1D4ED8", footer_text="#FFF", callout_bg="#EEE", callout_border="#CCC", callout_title="#000", callout_text="#222", demo_card_bg="#FFF", demo_card_border="#DDD", demo_link_color="#1D4ED8", arch_container_bg="#FFF", arch_container_border="#DDD", tier_header_bg="#1D4ED8", tier_header_text="#FFF", tier_card_bg="#FFF", tier_card_border="#DDD", service_node_bg="#FFF", service_node_border="#DDD", service_node_text="#000", flow_arrow_color="#1D4ED8", tech_col_bg="#FFF", tech_col_border="#DDD", tech_badge_bg="#EEE", tech_badge_text="#000", table_header_bg="#1D4ED8", table_header_text="#FFF", table_zebra_bg="#FFF", table_cell_text="#000", table_border="#DDD", table_highlight_bg="#EEE")
    font_heading = tokens.font_family_heading if tokens else "Calibri"
    font_body = tokens.font_family_body if tokens else "Calibri"

    # 1. Card Container
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(rect.left), Inches(rect.top), Inches(rect.width), Inches(rect.height)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = hex_to_rgb(t.card_bg)
    card.line.color.rgb = hex_to_rgb(t.card_border)
    card.line.width = Pt(1.5)

    # 2. Vector Icon (top left)
    icon_sz = min(0.42, rect.height * 0.28)
    if icon_type:
        draw_vector_icon(
            slide, icon_type,
            left_in=rect.left + 0.18,
            top_in=rect.top + 0.16,
            size_in=icon_sz,
            color_rgb=hex_to_rgb(t.bullet_accent),
            bg_circle=True,
            bg_circle_rgb=hex_to_rgb(t.canvas_bg)
        )

    # 3. Delta Pill (top right)
    if delta_pill:
        pill_w = min(1.4, rect.width * 0.45)
        pill = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(rect.right - pill_w - 0.18), Inches(rect.top + 0.16),
            Inches(pill_w), Inches(0.32)
        )
        pill.fill.solid()
        pill.fill.fore_color.rgb = hex_to_rgb("#10B981" if "+" in delta_pill else t.bullet_accent)
        pill.line.fill.background()
        tf = pill.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.text = delta_pill
        p.font.name = font_heading
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = hex_to_rgb("#FFFFFF")
        p.alignment = PP_ALIGN.CENTER

    # 4. Big Stat Metric Number
    stat_top = rect.top + icon_sz + 0.22
    tb = slide.shapes.add_textbox(
        Inches(rect.left + 0.18), Inches(stat_top),
        Inches(rect.width - 0.36), Inches(rect.height * 0.38)
    )
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = stat_number
    p.font.name = font_heading
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = hex_to_rgb(t.title_primary)

    # 5. Label & Subtext
    lbl_top = stat_top + (rect.height * 0.32)
    tb2 = slide.shapes.add_textbox(
        Inches(rect.left + 0.18), Inches(lbl_top),
        Inches(rect.width - 0.36), Inches(max(0.4, rect.height - (lbl_top - rect.top) - 0.1))
    )
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = stat_label
    p2.font.name = font_body
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = hex_to_rgb(t.body_text)

    if caption:
        p3 = tf2.add_paragraph()
        p3.text = caption
        p3.font.name = font_body
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = hex_to_rgb(t.muted_text)


def render_bento_card(
    slide,
    rect: Rect,
    title: str,
    bullets: List[str],
    badge: Optional[str] = None,
    icon_type: Optional[str] = "cpu",
    theme: Optional[Theme] = None,
    tokens: Optional[ExtendedThemeTokens] = None,
    accent_color: Optional[str] = None
) -> None:
    """Renders a modern Bento grid container card with header icon and formatted bullet list."""
    t = theme or Theme(name="default", is_dark_mode=False, canvas_bg="#FFF", card_bg="#FFF", card_border="#DDD", title_primary="#000", subtitle_color="#444", body_text="#222", muted_text="#666", bullet_accent="#1D4ED8", team_badge_bg="#FFF", team_badge_border="#1D4ED8", team_badge_text="#000", header_title_color="#000", footer_bg="#1D4ED8", footer_text="#FFF", callout_bg="#EEE", callout_border="#CCC", callout_title="#000", callout_text="#222", demo_card_bg="#FFF", demo_card_border="#DDD", demo_link_color="#1D4ED8", arch_container_bg="#FFF", arch_container_border="#DDD", tier_header_bg="#1D4ED8", tier_header_text="#FFF", tier_card_bg="#FFF", tier_card_border="#DDD", service_node_bg="#FFF", service_node_border="#DDD", service_node_text="#000", flow_arrow_color="#1D4ED8", tech_col_bg="#FFF", tech_col_border="#DDD", tech_badge_bg="#EEE", tech_badge_text="#000", table_header_bg="#1D4ED8", table_header_text="#FFF", table_zebra_bg="#FFF", table_cell_text="#000", table_border="#DDD", table_highlight_bg="#EEE")
    font_heading = tokens.font_family_heading if tokens else "Calibri"
    font_body = tokens.font_family_body if tokens else "Calibri"
    acc = accent_color or t.bullet_accent

    # Outer Container
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(rect.left), Inches(rect.top), Inches(rect.width), Inches(rect.height)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = hex_to_rgb(t.card_bg)
    card.line.color.rgb = hex_to_rgb(t.card_border)
    card.line.width = Pt(1.5)

    # Accent Top Stripe
    stripe_h = 0.05
    stripe = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(rect.left + 0.1), Inches(rect.top + 0.04), Inches(rect.width - 0.2), Inches(stripe_h)
    )
    stripe.fill.solid(); stripe.fill.fore_color.rgb = hex_to_rgb(acc); stripe.line.fill.background()

    # Icon & Header Title
    icon_sz = 0.36
    if icon_type:
        draw_vector_icon(
            slide, icon_type,
            left_in=rect.left + 0.16,
            top_in=rect.top + 0.16,
            size_in=icon_sz,
            color_rgb=hex_to_rgb(acc),
            bg_circle=True,
            bg_circle_rgb=hex_to_rgb(t.canvas_bg)
        )

    title_left = rect.left + icon_sz + 0.26 if icon_type else rect.left + 0.18
    title_w = rect.width - (title_left - rect.left) - (1.1 if badge else 0.18)
    tb = slide.shapes.add_textbox(Inches(title_left), Inches(rect.top + 0.14), Inches(title_w), Inches(0.40))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = font_heading
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = hex_to_rgb(t.title_primary)

    # Optional Pill Badge (top right)
    if badge:
        pill_w = 1.0
        pill = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(rect.right - pill_w - 0.16), Inches(rect.top + 0.16),
            Inches(pill_w), Inches(0.28)
        )
        pill.fill.solid(); pill.fill.fore_color.rgb = hex_to_rgb(t.callout_bg)
        pill.line.color.rgb = hex_to_rgb(acc)
        pill.line.width = Pt(1.0)
        ptf = pill.text_frame
        pp = ptf.paragraphs[0]
        pp.text = badge
        pp.font.name = font_heading
        pp.font.size = Pt(8.5)
        pp.font.bold = True
        pp.font.color.rgb = hex_to_rgb(acc)
        pp.alignment = PP_ALIGN.CENTER

    # Bullets
    body_top = rect.top + icon_sz + 0.26
    body_tb = slide.shapes.add_textbox(
        Inches(rect.left + 0.16), Inches(body_top),
        Inches(rect.width - 0.32), Inches(max(0.4, rect.bottom - body_top - 0.1))
    )
    btf = body_tb.text_frame
    btf.word_wrap = True

    for i, b in enumerate(bullets):
        p_b = btf.paragraphs[0] if i == 0 else btf.add_paragraph()
        p_b.space_after = Pt(4)
        if ":" in b:
            lead, rest = b.split(":", 1)
            r1 = p_b.add_run()
            r1.text = "• " + lead.strip() + ": "
            r1.font.name = font_body
            r1.font.size = Pt(10)
            r1.font.bold = True
            r1.font.color.rgb = hex_to_rgb(acc)
            r2 = p_b.add_run()
            r2.text = rest.strip()
            r2.font.name = font_body
            r2.font.size = Pt(9.5)
            r2.font.color.rgb = hex_to_rgb(t.body_text)
        else:
            p_b.text = "• " + b.strip()
            p_b.font.name = font_body
            p_b.font.size = Pt(9.5)
            p_b.font.color.rgb = hex_to_rgb(t.body_text)


def render_swimlane_architecture(
    slide,
    rect: Rect,
    lanes: List[Dict[str, Any]],
    theme: Optional[Theme] = None,
    tokens: Optional[ExtendedThemeTokens] = None
) -> None:
    """Renders a multi-lane system architecture topology with orthogonal node placement."""
    t = theme or Theme(name="default", is_dark_mode=False, canvas_bg="#FFF", card_bg="#FFF", card_border="#DDD", title_primary="#000", subtitle_color="#444", body_text="#222", muted_text="#666", bullet_accent="#1D4ED8", team_badge_bg="#FFF", team_badge_border="#1D4ED8", team_badge_text="#000", header_title_color="#000", footer_bg="#1D4ED8", footer_text="#FFF", callout_bg="#EEE", callout_border="#CCC", callout_title="#000", callout_text="#222", demo_card_bg="#FFF", demo_card_border="#DDD", demo_link_color="#1D4ED8", arch_container_bg="#FFF", arch_container_border="#DDD", tier_header_bg="#1D4ED8", tier_header_text="#FFF", tier_card_bg="#FFF", tier_card_border="#DDD", service_node_bg="#FFF", service_node_border="#DDD", service_node_text="#000", flow_arrow_color="#1D4ED8", tech_col_bg="#FFF", tech_col_border="#DDD", tech_badge_bg="#EEE", tech_badge_text="#000", table_header_bg="#1D4ED8", table_header_text="#FFF", table_zebra_bg="#FFF", table_cell_text="#000", table_border="#DDD", table_highlight_bg="#EEE")
    font_heading = tokens.font_family_heading if tokens else "Calibri"
    font_body = tokens.font_family_body if tokens else "Calibri"

    num_lanes = max(1, len(lanes))
    lane_gap = 0.15
    lane_h = (rect.height - (num_lanes - 1) * lane_gap) / num_lanes

    for idx, lane in enumerate(lanes):
        ly = rect.top + idx * (lane_h + lane_gap)

        # Lane Container
        lane_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(rect.left), Inches(ly), Inches(rect.width), Inches(lane_h)
        )
        lane_box.fill.solid()
        lane_box.fill.fore_color.rgb = hex_to_rgb(t.card_bg)
        lane_box.line.color.rgb = hex_to_rgb(t.card_border)
        lane_box.line.width = Pt(1.2)

        # Left Header Ribbon
        ribbon_w = 2.0
        ribbon = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(rect.left), Inches(ly), Inches(ribbon_w), Inches(lane_h)
        )
        ribbon.fill.solid()
        ribbon.fill.fore_color.rgb = hex_to_rgb(t.tier_header_bg)
        ribbon.line.fill.background()

        # Ribbon Icon + Text
        icon_type = lane.get("icon", "cloud")
        draw_vector_icon(
            slide, icon_type,
            left_in=rect.left + 0.12,
            top_in=ly + (lane_h - 0.34) / 2.0,
            size_in=0.34,
            color_rgb=hex_to_rgb(t.tier_header_text),
            bg_circle=False
        )

        rtb = slide.shapes.add_textbox(Inches(rect.left + 0.50), Inches(ly), Inches(ribbon_w - 0.55), Inches(lane_h))
        rtf = rtb.text_frame
        rtf.word_wrap = True
        rp = rtf.paragraphs[0]
        rp.text = lane.get("name", f"Tier {idx+1}")
        rp.font.name = font_heading
        rp.font.size = Pt(10.5)
        rp.font.bold = True
        rp.font.color.rgb = hex_to_rgb(t.tier_header_text)

        # Service Nodes inside this lane
        nodes = lane.get("nodes", [])
        if nodes:
            avail_w = rect.width - ribbon_w - 0.4
            node_gap = 0.12
            node_w = (avail_w - (len(nodes) - 1) * node_gap) / max(1, len(nodes))
            node_h = max(0.35, lane_h - 0.24)
            node_y = ly + (lane_h - node_h) / 2.0

            for n_idx, node_text in enumerate(nodes):
                nx = rect.left + ribbon_w + 0.2 + n_idx * (node_w + node_gap)
                nbox = slide.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    Inches(nx), Inches(node_y), Inches(node_w), Inches(node_h)
                )
                nbox.fill.solid()
                nbox.fill.fore_color.rgb = hex_to_rgb(t.service_node_bg)
                nbox.line.color.rgb = hex_to_rgb(t.service_node_border)
                nbox.line.width = Pt(1.0)
                ntf = nbox.text_frame
                ntf.word_wrap = True
                np = ntf.paragraphs[0]
                np.text = node_text
                np.font.name = font_body
                np.font.size = Pt(9.5)
                np.font.bold = True
                np.font.color.rgb = hex_to_rgb(t.service_node_text)
                np.alignment = PP_ALIGN.CENTER


def render_radial_ecosystem(
    slide,
    rect: Rect,
    center_title: str,
    satellites: List[Dict[str, str]],
    center_icon: str = "brain",
    theme: Optional[Theme] = None,
    tokens: Optional[ExtendedThemeTokens] = None
) -> None:
    """Renders a central hub-and-spoke ecosystem with radial satellite cards."""
    t = theme or Theme(name="default", is_dark_mode=False, canvas_bg="#FFF", card_bg="#FFF", card_border="#DDD", title_primary="#000", subtitle_color="#444", body_text="#222", muted_text="#666", bullet_accent="#1D4ED8", team_badge_bg="#FFF", team_badge_border="#1D4ED8", team_badge_text="#000", header_title_color="#000", footer_bg="#1D4ED8", footer_text="#FFF", callout_bg="#EEE", callout_border="#CCC", callout_title="#000", callout_text="#222", demo_card_bg="#FFF", demo_card_border="#DDD", demo_link_color="#1D4ED8", arch_container_bg="#FFF", arch_container_border="#DDD", tier_header_bg="#1D4ED8", tier_header_text="#FFF", tier_card_bg="#FFF", tier_card_border="#DDD", service_node_bg="#FFF", service_node_border="#DDD", service_node_text="#000", flow_arrow_color="#1D4ED8", tech_col_bg="#FFF", tech_col_border="#DDD", tech_badge_bg="#EEE", tech_badge_text="#000", table_header_bg="#1D4ED8", table_header_text="#FFF", table_zebra_bg="#FFF", table_cell_text="#000", table_border="#DDD", table_highlight_bg="#EEE")
    font_heading = tokens.font_family_heading if tokens else "Calibri"
    font_body = tokens.font_family_body if tokens else "Calibri"

    cx = rect.center_x
    cy = rect.center_y
    center_r = 1.1

    # 1. Center Core Circle
    core = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(cx - center_r / 2.0), Inches(cy - center_r / 2.0),
        Inches(center_r), Inches(center_r)
    )
    core.fill.solid(); core.fill.fore_color.rgb = hex_to_rgb(t.tier_header_bg)
    core.line.color.rgb = hex_to_rgb(t.bullet_accent); core.line.width = Pt(2.5)

    draw_vector_icon(
        slide, center_icon,
        left_in=cx - 0.20,
        top_in=cy - 0.38,
        size_in=0.40,
        color_rgb=hex_to_rgb(t.tier_header_text),
        bg_circle=False
    )
    ctb = slide.shapes.add_textbox(Inches(cx - 0.45), Inches(cy + 0.05), Inches(0.9), Inches(0.4))
    ctf = ctb.text_frame; ctf.word_wrap = True
    cp = ctf.paragraphs[0]; cp.text = center_title
    cp.font.name = font_heading; cp.font.size = Pt(10.0); cp.font.bold = True
    cp.font.color.rgb = hex_to_rgb(t.tier_header_text); cp.alignment = PP_ALIGN.CENTER

    # 2. Satellites arranged radially
    n_sat = len(satellites)
    if n_sat == 0:
        return

    orbit_rx = (rect.width / 2.0) - 1.2
    orbit_ry = (rect.height / 2.0) - 0.6
    sat_w = 1.9
    sat_h = 0.85

    for idx, sat in enumerate(satellites):
        angle = (2 * math.pi / n_sat) * idx - (math.pi / 2.0)
        sat_cx = cx + orbit_rx * math.cos(angle)
        sat_cy = cy + orbit_ry * math.sin(angle)

        # Connector Line
        line = slide.shapes.add_connector(
            1,  # msoConnectorStraight
            Inches(cx), Inches(cy), Inches(sat_cx), Inches(sat_cy)
        )
        line.line.color.rgb = hex_to_rgb(t.card_border)
        line.line.width = Pt(1.5)

        # Satellite Card
        scard = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(sat_cx - sat_w / 2.0), Inches(sat_cy - sat_h / 2.0),
            Inches(sat_w), Inches(sat_h)
        )
        scard.fill.solid(); scard.fill.fore_color.rgb = hex_to_rgb(t.card_bg)
        scard.line.color.rgb = hex_to_rgb(t.bullet_accent); scard.line.width = Pt(1.2)

        # Text inside satellite
        stb = slide.shapes.add_textbox(
            Inches(sat_cx - sat_w / 2.0 + 0.08), Inches(sat_cy - sat_h / 2.0 + 0.08),
            Inches(sat_w - 0.16), Inches(sat_h - 0.16)
        )
        stf = stb.text_frame; stf.word_wrap = True
        sp = stf.paragraphs[0]; sp.text = sat.get("name", "")
        sp.font.name = font_heading; sp.font.size = Pt(9.5); sp.font.bold = True
        sp.font.color.rgb = hex_to_rgb(t.title_primary); sp.alignment = PP_ALIGN.CENTER

        if "desc" in sat:
            sp2 = stf.add_paragraph()
            sp2.text = sat["desc"]
            sp2.font.name = font_body; sp2.font.size = Pt(8.5)
            sp2.font.color.rgb = hex_to_rgb(t.muted_text); sp2.alignment = PP_ALIGN.CENTER


def render_tension_split_card(
    slide,
    rect: Rect,
    problem_title: str,
    problem_bullets: List[str],
    solution_title: str,
    solution_bullets: List[str],
    theme: Optional[Theme] = None,
    tokens: Optional[ExtendedThemeTokens] = None
) -> None:
    """Renders a comparative Before vs. After (Problem vs. Solution) split screen card."""
    t = theme or Theme(name="default", is_dark_mode=False, canvas_bg="#FFF", card_bg="#FFF", card_border="#DDD", title_primary="#000", subtitle_color="#444", body_text="#222", muted_text="#666", bullet_accent="#1D4ED8", team_badge_bg="#FFF", team_badge_border="#1D4ED8", team_badge_text="#000", header_title_color="#000", footer_bg="#1D4ED8", footer_text="#FFF", callout_bg="#EEE", callout_border="#CCC", callout_title="#000", callout_text="#222", demo_card_bg="#FFF", demo_card_border="#DDD", demo_link_color="#1D4ED8", arch_container_bg="#FFF", arch_container_border="#DDD", tier_header_bg="#1D4ED8", tier_header_text="#FFF", tier_card_bg="#FFF", tier_card_border="#DDD", service_node_bg="#FFF", service_node_border="#DDD", service_node_text="#000", flow_arrow_color="#1D4ED8", tech_col_bg="#FFF", tech_col_border="#DDD", tech_badge_bg="#EEE", tech_badge_text="#000", table_header_bg="#1D4ED8", table_header_text="#FFF", table_zebra_bg="#FFF", table_cell_text="#000", table_border="#DDD", table_highlight_bg="#EEE")
    font_heading = tokens.font_family_heading if tokens else "Calibri"
    font_body = tokens.font_family_body if tokens else "Calibri"

    gap = 0.25
    half_w = (rect.width - gap) / 2.0

    # Left: Problem Card (Red Accent)
    p_rect = Rect(rect.left, rect.top, half_w, rect.height)
    p_card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(p_rect.left), Inches(p_rect.top), Inches(p_rect.width), Inches(p_rect.height)
    )
    p_card.fill.solid(); p_card.fill.fore_color.rgb = hex_to_rgb(t.card_bg)
    p_card.line.color.rgb = hex_to_rgb("#EF4444"); p_card.line.width = Pt(1.5)

    draw_vector_icon(slide, "cross", p_rect.left + 0.18, p_rect.top + 0.16, size_in=0.36, color_rgb=hex_to_rgb("#EF4444"))
    ptb = slide.shapes.add_textbox(Inches(p_rect.left + 0.60), Inches(p_rect.top + 0.14), Inches(p_rect.width - 0.75), Inches(0.4))
    ptf = ptb.text_frame; pp = ptf.paragraphs[0]; pp.text = problem_title
    pp.font.name = font_heading; pp.font.size = Pt(12); pp.font.bold = True
    pp.font.color.rgb = hex_to_rgb("#EF4444")

    p_body = slide.shapes.add_textbox(Inches(p_rect.left + 0.18), Inches(p_rect.top + 0.65), Inches(p_rect.width - 0.36), Inches(p_rect.height - 0.8))
    p_btf = p_body.text_frame; p_btf.word_wrap = True
    for i, b in enumerate(problem_bullets):
        p_p = p_btf.paragraphs[0] if i == 0 else p_btf.add_paragraph()
        p_p.text = "✗ " + b.strip()
        p_p.font.name = font_body; p_p.font.size = Pt(10.0); p_p.font.color.rgb = hex_to_rgb(t.body_text)
        p_p.space_after = Pt(4)

    # Right: Solution Card (Emerald Accent)
    s_rect = Rect(rect.left + half_w + gap, rect.top, half_w, rect.height)
    s_card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(s_rect.left), Inches(s_rect.top), Inches(s_rect.width), Inches(s_rect.height)
    )
    s_card.fill.solid(); s_card.fill.fore_color.rgb = hex_to_rgb(t.card_bg)
    s_card.line.color.rgb = hex_to_rgb("#10B981"); s_card.line.width = Pt(1.5)

    draw_vector_icon(slide, "check", s_rect.left + 0.18, s_rect.top + 0.16, size_in=0.36, color_rgb=hex_to_rgb("#10B981"))
    stb = slide.shapes.add_textbox(Inches(s_rect.left + 0.60), Inches(s_rect.top + 0.14), Inches(s_rect.width - 0.75), Inches(0.4))
    stf = stb.text_frame; sp = stf.paragraphs[0]; sp.text = solution_title
    sp.font.name = font_heading; sp.font.size = Pt(12); sp.font.bold = True
    sp.font.color.rgb = hex_to_rgb("#10B981")

    s_body = slide.shapes.add_textbox(Inches(s_rect.left + 0.18), Inches(s_rect.top + 0.65), Inches(s_rect.width - 0.36), Inches(s_rect.height - 0.8))
    s_btf = s_body.text_frame; s_btf.word_wrap = True
    for i, b in enumerate(solution_bullets):
        s_p = s_btf.paragraphs[0] if i == 0 else s_btf.add_paragraph()
        s_p.text = "✓ " + b.strip()
        s_p.font.name = font_body; s_p.font.size = Pt(10.0); s_p.font.color.rgb = hex_to_rgb(t.body_text)
        s_p.space_after = Pt(4)


def render_milestone_roadmap(
    slide,
    rect: Rect,
    phases: List[Dict[str, str]],
    theme: Optional[Theme] = None,
    tokens: Optional[ExtendedThemeTokens] = None
) -> None:
    """Renders a chronological roadmap timeline with phase status pins and deliverables."""
    t = theme or Theme(name="default", is_dark_mode=False, canvas_bg="#FFF", card_bg="#FFF", card_border="#DDD", title_primary="#000", subtitle_color="#444", body_text="#222", muted_text="#666", bullet_accent="#1D4ED8", team_badge_bg="#FFF", team_badge_border="#1D4ED8", team_badge_text="#000", header_title_color="#000", footer_bg="#1D4ED8", footer_text="#FFF", callout_bg="#EEE", callout_border="#CCC", callout_title="#000", callout_text="#222", demo_card_bg="#FFF", demo_card_border="#DDD", demo_link_color="#1D4ED8", arch_container_bg="#FFF", arch_container_border="#DDD", tier_header_bg="#1D4ED8", tier_header_text="#FFF", tier_card_bg="#FFF", tier_card_border="#DDD", service_node_bg="#FFF", service_node_border="#DDD", service_node_text="#000", flow_arrow_color="#1D4ED8", tech_col_bg="#FFF", tech_col_border="#DDD", tech_badge_bg="#EEE", tech_badge_text="#000", table_header_bg="#1D4ED8", table_header_text="#FFF", table_zebra_bg="#FFF", table_cell_text="#000", table_border="#DDD", table_highlight_bg="#EEE")
    font_heading = tokens.font_family_heading if tokens else "Calibri"
    font_body = tokens.font_family_body if tokens else "Calibri"

    n_phases = max(1, len(phases))
    gap = 0.15
    phase_w = (rect.width - (n_phases - 1) * gap) / n_phases

    # Connecting horizontal bar
    bar_y = rect.top + 0.35
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(rect.left + phase_w * 0.4), Inches(bar_y),
        Inches(rect.width - phase_w * 0.8), Inches(0.06)
    )
    bar.fill.solid(); bar.fill.fore_color.rgb = hex_to_rgb(t.card_border); bar.line.fill.background()

    for idx, p in enumerate(phases):
        px = rect.left + idx * (phase_w + gap)

        # Status Pin Circle
        pin_r = 0.32
        pin = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(px + (phase_w - pin_r) / 2.0), Inches(bar_y - pin_r / 2.0 + 0.03),
            Inches(pin_r), Inches(pin_r)
        )
        status = p.get("status", "").upper()
        pin_col = "#10B981" if "COMPLETED" in status else ("#0284C7" if "PROGRESS" in status else t.muted_text)
        pin.fill.solid(); pin.fill.fore_color.rgb = hex_to_rgb(pin_col)
        pin.line.color.rgb = hex_to_rgb("#FFFFFF"); pin.line.width = Pt(1.5)

        # Pin Number
        ptf = pin.text_frame; pp = ptf.paragraphs[0]; pp.text = str(idx + 1)
        pp.font.name = font_heading; pp.font.size = Pt(10.0); pp.font.bold = True
        pp.font.color.rgb = hex_to_rgb("#FFFFFF"); pp.alignment = PP_ALIGN.CENTER

        # Phase Card
        card_y = bar_y + 0.35
        card_h = rect.height - (card_y - rect.top)
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(px), Inches(card_y), Inches(phase_w), Inches(card_h)
        )
        card.fill.solid(); card.fill.fore_color.rgb = hex_to_rgb(t.card_bg)
        card.line.color.rgb = hex_to_rgb(t.card_border); card.line.width = Pt(1.2)

        # Content inside card
        tb = slide.shapes.add_textbox(Inches(px + 0.1), Inches(card_y + 0.1), Inches(phase_w - 0.2), Inches(card_h - 0.2))
        tf = tb.text_frame; tf.word_wrap = True

        p1 = tf.paragraphs[0]; p1.text = p.get("title", f"Phase {idx+1}")
        p1.font.name = font_heading; p1.font.size = Pt(10.5); p1.font.bold = True
        p1.font.color.rgb = hex_to_rgb(t.title_primary)

        if "date" in p:
            p2 = tf.add_paragraph(); p2.text = p["date"]
            p2.font.name = font_body; p2.font.size = Pt(8.5); p2.font.color.rgb = hex_to_rgb(t.bullet_accent)
            p2.space_after = Pt(4)

        if "deliverable" in p:
            p3 = tf.add_paragraph(); p3.text = "• " + p["deliverable"]
            p3.font.name = font_body; p3.font.size = Pt(9.0); p3.font.color.rgb = hex_to_rgb(t.body_text)


def render_browser_mockup(
    slide,
    rect,
    t,
    tokens,
    url: str = "https://app.sovereign-ai.gov.in/dashboard",
    nav_items: Optional[List[str]] = None,
    table_rows: Optional[List[List[str]]] = None
) -> None:
    """Renders a realistic desktop web application browser chrome with navigation and data grid."""
    font_heading = tokens.font_family_heading
    font_body = tokens.font_family_body

    # 1. Outer Browser Window Shell
    window = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(rect.left), Inches(rect.top), Inches(rect.width), Inches(rect.height)
    )
    window.fill.solid(); window.fill.fore_color.rgb = hex_to_rgb(t.card_bg)
    window.line.color.rgb = hex_to_rgb(t.card_border); window.line.width = Pt(1.5)

    # 2. Browser Header Chrome Bar
    header_h = 0.42
    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(rect.left), Inches(rect.top), Inches(rect.width), Inches(header_h)
    )
    header.fill.solid(); header.fill.fore_color.rgb = hex_to_rgb(t.canvas_bg)
    header.line.color.rgb = hex_to_rgb(t.card_border); header.line.width = Pt(1.0)

    # Traffic Light Dots (Close, Minimize, Maximize)
    dots = ["#EF4444", "#F59E0B", "#10B981"]
    for i, col in enumerate(dots):
        d = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(rect.left + 0.15 + i * 0.18), Inches(rect.top + 0.14),
            Inches(0.12), Inches(0.12)
        )
        d.fill.solid(); d.fill.fore_color.rgb = hex_to_rgb(col)
        d.line.fill.background()

    # Address Bar Pill
    addr_x = rect.left + 0.8
    addr_w = rect.width - 1.2
    addr_pill = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(addr_x), Inches(rect.top + 0.08), Inches(addr_w), Inches(0.26)
    )
    addr_pill.fill.solid(); addr_pill.fill.fore_color.rgb = hex_to_rgb(t.card_bg)
    addr_pill.line.color.rgb = hex_to_rgb(t.card_border); addr_pill.line.width = Pt(0.8)
    
    atf = addr_pill.text_frame
    ap = atf.paragraphs[0]; ap.text = f"🔒 {url}"
    ap.font.name = font_body; ap.font.size = Pt(8.5); ap.font.color.rgb = hex_to_rgb(t.muted_text)
    ap.alignment = PP_ALIGN.LEFT

    # 3. Inner Layout: Left Sidebar + Right Data Surface
    content_y = rect.top + header_h + 0.05
    content_h = rect.height - header_h - 0.1
    sidebar_w = 2.2

    # Left Navigation Sidebar
    sidebar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(rect.left + 0.05), Inches(content_y), Inches(sidebar_w), Inches(content_h)
    )
    sidebar.fill.solid(); sidebar.fill.fore_color.rgb = hex_to_rgb(t.canvas_bg)
    sidebar.line.fill.background()

    stb = slide.shapes.add_textbox(Inches(rect.left + 0.15), Inches(content_y + 0.15), Inches(sidebar_w - 0.3), Inches(content_h - 0.3))
    stf = stb.text_frame; stf.word_wrap = True
    nav_labels = nav_items or ["📊 Dashboard Overview", "⚡ Live Ingestion Feed", "🛡️ Threat Correlator", "📁 Case Evidence Vault", "⚙️ System Configuration"]
    for idx, nl in enumerate(nav_labels):
        np = stf.paragraphs[0] if idx == 0 else stf.add_paragraph()
        np.text = nl
        np.font.name = font_body; np.font.size = Pt(9.5)
        np.font.color.rgb = hex_to_rgb(t.title_primary if idx == 0 else t.muted_text)
        np.font.bold = (idx == 0)
        np.space_after = Pt(8)

    # Right Content Area: Dashboard Cards & Table
    main_x = rect.left + sidebar_w + 0.15
    main_w = rect.width - sidebar_w - 0.25

    # Live Dashboard Table rows
    rows = table_rows or [
        ["ENTITY ID", "SOURCE TELEMETRY", "STATUS", "LATENCY"],
        ["CIRCUIT-8891", "Tor Exit Relay 185.220.101.4", "IDENTIFIED", "38ms"],
        ["WALLET-0x49f", "Ethereum Mempool Deposit", "CORRELATED", "44ms"],
        ["SATELLITE-S2", "Sentinel-2 Catchment SAR", "PROCESSED", "52ms"],
        ["EVIDENCE-63", "BSA Cryptographic Merkle Sign", "VERIFIED", "14ms"]
    ]

    row_h = (content_h - 0.2) / len(rows)
    col_w = main_w / 4.0

    for r_idx, r_data in enumerate(rows):
        ry = content_y + 0.1 + r_idx * row_h
        is_header = (r_idx == 0)
        for c_idx, val in enumerate(r_data):
            cx = main_x + c_idx * col_w
            cell = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(cx), Inches(ry), Inches(col_w - 0.05), Inches(row_h - 0.05)
            )
            cell_bg = t.card_border if is_header else (t.card_bg if r_idx % 2 == 1 else t.canvas_bg)
            cell.fill.solid(); cell.fill.fore_color.rgb = hex_to_rgb(cell_bg)
            cell.line.color.rgb = hex_to_rgb(t.card_border); cell.line.width = Pt(0.6)

            ctf = cell.text_frame
            cp = ctf.paragraphs[0]; cp.text = val
            cp.font.name = font_heading if is_header else font_body
            cp.font.size = Pt(8.5 if is_header else 8.0)
            cp.font.bold = is_header
            text_color = t.title_primary if is_header else ("#10B981" if val in ("IDENTIFIED", "VERIFIED", "CORRELATED") else t.body_text)
            cp.font.color.rgb = hex_to_rgb(text_color)
            cp.alignment = PP_ALIGN.CENTER


def render_mobile_mockup(
    slide,
    rect,
    t,
    tokens,
    app_title: str = "FIELD INCIDENT HUD",
    feed_items: Optional[List[Dict[str, str]]] = None
) -> None:
    """Renders a sleek mobile smartphone app frame with interactive alert cards."""
    font_heading = tokens.font_family_heading
    font_body = tokens.font_family_body

    # 1. Phone Bezel
    phone = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(rect.left), Inches(rect.top), Inches(rect.width), Inches(rect.height)
    )
    phone.fill.solid(); phone.fill.fore_color.rgb = hex_to_rgb(t.card_bg)
    phone.line.color.rgb = hex_to_rgb(t.card_border); phone.line.width = Pt(2.5)

    # 2. Top Notch / Dynamic Island
    island_w = min(1.4, rect.width * 0.4)
    island = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(rect.left + (rect.width - island_w) / 2.0), Inches(rect.top + 0.12),
        Inches(island_w), Inches(0.22)
    )
    island.fill.solid(); island.fill.fore_color.rgb = hex_to_rgb(t.canvas_bg)
    island.line.fill.background()

    # 3. Header Title
    tb = slide.shapes.add_textbox(Inches(rect.left + 0.2), Inches(rect.top + 0.45), Inches(rect.width - 0.4), Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]; p.text = app_title
    p.font.name = font_heading; p.font.size = Pt(11.0); p.font.bold = True
    p.font.color.rgb = hex_to_rgb(t.title_primary); p.alignment = PP_ALIGN.CENTER

    # 4. Feed Cards
    items = feed_items or [
        {"title": "CRITICAL ANOMALY DETECTED", "meta": "Tor Exit Relay • 2 mins ago", "badge": "P1 ALERT", "color": "#EF4444"},
        {"title": "CHAIN-OF-CUSTODY SIGNED", "meta": "Section 63 BSA Bundle #982", "badge": "VERIFIED", "color": "#10B981"},
        {"title": "MODEL INFERENCE STABLE", "meta": "Latency: 38ms • Precision 99.4%", "badge": "OPTIMAL", "color": "#0284C7"}
    ]

    card_y = rect.top + 0.95
    avail_h = rect.height - 1.2
    c_h = (avail_h - (len(items) - 1) * 0.15) / len(items)

    for idx, item in enumerate(items):
        cy = card_y + idx * (c_h + 0.15)
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(rect.left + 0.2), Inches(cy), Inches(rect.width - 0.4), Inches(c_h)
        )
        card.fill.solid(); card.fill.fore_color.rgb = hex_to_rgb(t.canvas_bg)
        card.line.color.rgb = hex_to_rgb(item.get("color", t.card_border)); card.line.width = Pt(1.2)

        ctb = slide.shapes.add_textbox(Inches(rect.left + 0.3), Inches(cy + 0.1), Inches(rect.width - 0.6), Inches(c_h - 0.2))
        ctf = ctb.text_frame; ctf.word_wrap = True
        
        p1 = ctf.paragraphs[0]; p1.text = item["title"]
        p1.font.name = font_heading; p1.font.size = Pt(9.5); p1.font.bold = True
        p1.font.color.rgb = hex_to_rgb(t.title_primary)

        p2 = ctf.add_paragraph(); p2.text = item.get("meta", "")
        p2.font.name = font_body; p2.font.size = Pt(8.0); p2.font.color.rgb = hex_to_rgb(t.muted_text)


def render_quadrant_matrix(
    slide,
    rect,
    t,
    tokens,
    our_product_name: str = "OUR SOLUTION",
    competitors: Optional[List[Dict[str, Any]]] = None
) -> None:
    """Renders a 2x2 competitive positioning matrix (Market Leaders vs Challengers)."""
    font_heading = tokens.font_family_heading
    font_body = tokens.font_family_body

    # Outer Container
    matrix = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(rect.left), Inches(rect.top), Inches(rect.width), Inches(rect.height)
    )
    matrix.fill.solid(); matrix.fill.fore_color.rgb = hex_to_rgb(t.card_bg)
    matrix.line.color.rgb = hex_to_rgb(t.card_border); matrix.line.width = Pt(1.5)

    # Dividing Crosshairs
    mid_x = rect.left + rect.width / 2.0
    mid_y = rect.top + rect.height / 2.0

    # Vertical axis
    v_line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(mid_x - 0.01), Inches(rect.top + 0.4), Inches(0.02), Inches(rect.height - 0.8)
    )
    v_line.fill.solid(); v_line.fill.fore_color.rgb = hex_to_rgb(t.card_border); v_line.line.fill.background()

    # Horizontal axis
    h_line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(rect.left + 0.4), Inches(mid_y - 0.01), Inches(rect.width - 0.8), Inches(0.02)
    )
    h_line.fill.solid(); h_line.fill.fore_color.rgb = hex_to_rgb(t.card_border); h_line.line.fill.background()

    # 4 Quadrant Labels
    quads = [
        ("CHALLENGERS", rect.left + 0.5, rect.top + 0.5),
        ("MARKET LEADERS", mid_x + 0.5, rect.top + 0.5),
        ("NICHE PLAYERS", rect.left + 0.5, mid_y + 0.5),
        ("VISIONARIES", mid_x + 0.5, mid_y + 0.5)
    ]
    for q_text, qx, qy in quads:
        qtb = slide.shapes.add_textbox(Inches(qx), Inches(qy), Inches(rect.width / 2.0 - 0.8), Inches(0.4))
        qtf = qtb.text_frame
        qp = qtf.paragraphs[0]; qp.text = q_text
        qp.font.name = font_heading; qp.font.size = Pt(8.5); qp.font.bold = True
        qp.font.color.rgb = hex_to_rgb(t.muted_text)

    # Highlighted "OUR SOLUTION" in Top-Right Leader Quadrant
    hero_w = 2.4
    hero_h = 1.0
    hero_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(mid_x + (rect.width / 4.0) - hero_w / 2.0),
        Inches(rect.top + (rect.height / 4.0) - hero_h / 2.0 + 0.2),
        Inches(hero_w), Inches(hero_h)
    )
    hero_box.fill.solid(); hero_box.fill.fore_color.rgb = hex_to_rgb(t.canvas_bg)
    hero_box.line.color.rgb = hex_to_rgb("#10B981"); hero_box.line.width = Pt(2.0)
    
    htf = hero_box.text_frame
    hp1 = htf.paragraphs[0]; hp1.text = f"★ {our_product_name}"
    hp1.font.name = font_heading; hp1.font.size = Pt(10.5); hp1.font.bold = True
    hp1.font.color.rgb = hex_to_rgb("#10B981"); hp1.alignment = PP_ALIGN.CENTER
    
    hp2 = htf.add_paragraph(); hp2.text = "10x White-Space Moat • Verified"
    hp2.font.name = font_body; hp2.font.size = Pt(8.0); hp2.font.color.rgb = hex_to_rgb(t.body_text)
    hp2.alignment = PP_ALIGN.CENTER

    # Competitor markers
    comps = competitors or [
        {"name": "Legacy Tool A", "x": rect.left + rect.width * 0.25, "y": rect.top + rect.height * 0.7},
        {"name": "Commercial SaaS B", "x": rect.left + rect.width * 0.35, "y": rect.top + rect.height * 0.35},
        {"name": "Open-Source Script", "x": rect.left + rect.width * 0.75, "y": rect.top + rect.height * 0.75}
    ]
    for comp in comps:
        dot = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(comp["x"] - 0.1), Inches(comp["y"] - 0.1),
            Inches(0.2), Inches(0.2)
        )
        dot.fill.solid(); dot.fill.fore_color.rgb = hex_to_rgb(t.muted_text); dot.line.fill.background()

        dtb = slide.shapes.add_textbox(Inches(comp["x"] + 0.15), Inches(comp["y"] - 0.15), Inches(1.8), Inches(0.3))
        dtf = dtb.text_frame
        dp = dtf.paragraphs[0]; dp.text = comp["name"]
        dp.font.name = font_body; dp.font.size = Pt(8.0); dp.font.color.rgb = hex_to_rgb(t.muted_text)

