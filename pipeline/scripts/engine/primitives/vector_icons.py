"""
Presentation Engine — Native Vector Icon Glyphs
Draws clean, geometric vector icons directly onto PowerPoint slides using native shapes.
Zero raster image dependencies. Zero external font dependencies.
"""

from typing import Optional
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor


def draw_vector_icon(
    slide,
    icon_type: str,
    left_in: float,
    top_in: float,
    size_in: float = 0.4,
    color_rgb: Optional[RGBColor] = None,
    bg_circle: bool = True,
    bg_circle_rgb: Optional[RGBColor] = None
) -> None:
    """
    Renders a clean geometric vector icon onto a PowerPoint slide.
    Icon types: shield, database, cloud, cpu, lock, chart, network, brain,
                lightbulb, user, document, gear, check, cross, target, rocket.
    """
    fill_color = color_rgb or RGBColor(29, 78, 216)  # Default SIH Blue

    # Optional background circle/rounded container
    if bg_circle:
        bg_col = bg_circle_rgb or RGBColor(241, 245, 249)
        bg = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(left_in), Inches(top_in), Inches(size_in), Inches(size_in)
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = bg_col
        bg.line.fill.background()  # No border

    # Inner glyph coordinate box (centered with 25% padding)
    pad = size_in * 0.22
    gx = left_in + pad
    gy = top_in + pad
    gw = size_in - (2 * pad)
    gh = size_in - (2 * pad)

    icon_key = icon_type.lower().strip()

    if icon_key in ("shield", "security", "defense"):
        # Plaque / Hexagon badge shape
        s = slide.shapes.add_shape(MSO_SHAPE.HEXAGON, Inches(gx), Inches(gy), Inches(gw), Inches(gh))
        s.fill.solid()
        s.fill.fore_color.rgb = fill_color
        s.line.fill.background()

    elif icon_key in ("database", "storage", "sql"):
        # Cylinder shape
        s = slide.shapes.add_shape(MSO_SHAPE.CAN, Inches(gx), Inches(gy), Inches(gw), Inches(gh))
        s.fill.solid()
        s.fill.fore_color.rgb = fill_color
        s.line.fill.background()

    elif icon_key in ("cloud", "saas", "api"):
        # Cloud shape
        s = slide.shapes.add_shape(MSO_SHAPE.CLOUD, Inches(gx), Inches(gy + gh * 0.1), Inches(gw), Inches(gh * 0.8))
        s.fill.solid()
        s.fill.fore_color.rgb = fill_color
        s.line.fill.background()

    elif icon_key in ("cpu", "chip", "hardware", "iot"):
        # Rounded rectangle with gear/diamond accent
        s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(gx + gw * 0.15), Inches(gy + gh * 0.15), Inches(gw * 0.7), Inches(gh * 0.7))
        s.fill.solid()
        s.fill.fore_color.rgb = fill_color
        s.line.fill.background()

    elif icon_key in ("lock", "privacy", "crypto"):
        # Lock body (rect) + shackle (arc)
        shackle = slide.shapes.add_shape(MSO_SHAPE.ARC, Inches(gx + gw * 0.2), Inches(gy), Inches(gw * 0.6), Inches(gh * 0.6))
        shackle.line.color.rgb = fill_color
        shackle.line.width = Pt(2)
        body = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(gx + gw * 0.1), Inches(gy + gh * 0.45), Inches(gw * 0.8), Inches(gh * 0.55))
        body.fill.solid()
        body.fill.fore_color.rgb = fill_color
        body.line.fill.background()

    elif icon_key in ("chart", "analytics", "metrics", "kpi"):
        # 3 ascending vertical bars
        bar_w = gw * 0.24
        spacing = gw * 0.12
        b1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(gx), Inches(gy + gh * 0.55), Inches(bar_w), Inches(gh * 0.45))
        b1.fill.solid(); b1.fill.fore_color.rgb = fill_color; b1.line.fill.background()
        b2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(gx + bar_w + spacing), Inches(gy + gh * 0.3), Inches(bar_w), Inches(gh * 0.7))
        b2.fill.solid(); b2.fill.fore_color.rgb = fill_color; b2.line.fill.background()
        b3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(gx + 2 * (bar_w + spacing)), Inches(gy), Inches(bar_w), Inches(gh))
        b3.fill.solid(); b3.fill.fore_color.rgb = fill_color; b3.line.fill.background()

    elif icon_key in ("network", "graph", "cluster"):
        # 3 small node circles connected in triangle
        node_r = gw * 0.28
        n1 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(gx + gw * 0.36), Inches(gy), Inches(node_r), Inches(node_r))
        n1.fill.solid(); n1.fill.fore_color.rgb = fill_color; n1.line.fill.background()
        n2 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(gx), Inches(gy + gh * 0.6), Inches(node_r), Inches(node_r))
        n2.fill.solid(); n2.fill.fore_color.rgb = fill_color; n2.line.fill.background()
        n3 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(gx + gw * 0.72), Inches(gy + gh * 0.6), Inches(node_r), Inches(node_r))
        n3.fill.solid(); n3.fill.fore_color.rgb = fill_color; n3.line.fill.background()

    elif icon_key in ("brain", "ai", "ml", "neural"):
        # Two symmetrical rounded lobes
        l1 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(gx), Inches(gy + gh * 0.1), Inches(gw * 0.48), Inches(gh * 0.8))
        l1.fill.solid(); l1.fill.fore_color.rgb = fill_color; l1.line.fill.background()
        l2 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(gx + gw * 0.52), Inches(gy + gh * 0.1), Inches(gw * 0.48), Inches(gh * 0.8))
        l2.fill.solid(); l2.fill.fore_color.rgb = fill_color; l2.line.fill.background()

    elif icon_key in ("check", "success", "verified"):
        tb = slide.shapes.add_textbox(Inches(gx - 0.05), Inches(gy - 0.08), Inches(gw + 0.1), Inches(gh + 0.1))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = "✓"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = fill_color

    elif icon_key in ("cross", "danger", "error"):
        s = slide.shapes.add_shape(MSO_SHAPE.CROSS, Inches(gx), Inches(gy), Inches(gw), Inches(gh))
        s.fill.solid()
        s.fill.fore_color.rgb = fill_color
        s.line.fill.background()

    elif icon_key in ("target", "goal", "accuracy"):
        # Outer ring + center dot
        s = slide.shapes.add_shape(MSO_SHAPE.DONUT, Inches(gx), Inches(gy), Inches(gw), Inches(gh))
        s.fill.solid(); s.fill.fore_color.rgb = fill_color; s.line.fill.background()
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(gx + gw * 0.35), Inches(gy + gh * 0.35), Inches(gw * 0.3), Inches(gh * 0.3))
        dot.fill.solid(); dot.fill.fore_color.rgb = fill_color; dot.line.fill.background()

    elif icon_key in ("rocket", "launch", "performance"):
        s = slide.shapes.add_shape(MSO_SHAPE.UP_ARROW, Inches(gx + gw * 0.2), Inches(gy), Inches(gw * 0.6), Inches(gh))
        s.fill.solid()
        s.fill.fore_color.rgb = fill_color
        s.line.fill.background()

    elif icon_key in ("gear", "settings"):
        s = slide.shapes.add_shape(MSO_SHAPE.GEAR_6, Inches(gx), Inches(gy), Inches(gw), Inches(gh))
        s.fill.solid()
        s.fill.fore_color.rgb = fill_color
        s.line.fill.background()

    elif icon_key in ("document", "file"):
        s = slide.shapes.add_shape(MSO_SHAPE.FOLDED_CORNER, Inches(gx), Inches(gy), Inches(gw), Inches(gh))
        s.fill.solid()
        s.fill.fore_color.rgb = fill_color
        s.line.fill.background()

    elif icon_key in ("user", "person", "team"):
        # Circle head + curved body
        head = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(gx + gw * 0.25), Inches(gy), Inches(gw * 0.5), Inches(gh * 0.45))
        head.fill.solid(); head.fill.fore_color.rgb = fill_color; head.line.fill.background()
        body = slide.shapes.add_shape(MSO_SHAPE.CHORD, Inches(gx + gw * 0.1), Inches(gy + gh * 0.5), Inches(gw * 0.8), Inches(gh * 0.5))
        body.fill.solid(); body.fill.fore_color.rgb = fill_color; body.line.fill.background()

    else:
        # Generic diamond/bullet fallback
        s = slide.shapes.add_shape(MSO_SHAPE.DIAMOND, Inches(gx + gw * 0.15), Inches(gy + gh * 0.15), Inches(gw * 0.7), Inches(gh * 0.7))
        s.fill.solid()
        s.fill.fore_color.rgb = fill_color
        s.line.fill.background()
