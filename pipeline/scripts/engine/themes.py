"""
Presentation Engine — Multi-Theme & Design Archetype System
Defines color tokens, typography pairings, and design presets for presentations.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class Theme:
    name: str
    is_dark_mode: bool
    # Canvases & Backgrounds
    canvas_bg: str
    card_bg: str
    card_border: str
    # Typography Colors
    title_primary: str
    subtitle_color: str
    body_text: str
    muted_text: str
    bullet_accent: str
    # Header & Footer Badges
    team_badge_bg: str
    team_badge_border: str
    team_badge_text: str
    header_title_color: str
    footer_bg: str
    footer_text: str
    # Callout Cards & Highlights
    callout_bg: str
    callout_border: str
    callout_title: str
    callout_text: str
    demo_card_bg: str
    demo_card_border: str
    demo_link_color: str
    # Architecture Diagram Tokens
    arch_container_bg: str
    arch_container_border: str
    tier_header_bg: str
    tier_header_text: str
    tier_card_bg: str
    tier_card_border: str
    service_node_bg: str
    service_node_border: str
    service_node_text: str
    flow_arrow_color: str
    # Tech Grid Tokens
    tech_col_bg: str
    tech_col_border: str
    tech_badge_bg: str
    tech_badge_text: str
    # Table Tokens
    table_header_bg: str
    table_header_text: str
    table_zebra_bg: str
    table_cell_text: str
    table_border: str
    table_highlight_bg: str
    # Semantic Status
    success_green: str = "#10B981"
    danger_red: str = "#EF4444"
    accent_orange: str = "#F97316"
    accent_purple: str = "#8B5CF6"
    accent_cyan: str = "#06B6D4"
    # Typography Families
    font_title: str = "Georgia"
    font_body: str = "Arial"


# ==============================================================================
# Theme Registry
# ==============================================================================

THEMES: Dict[str, Theme] = {
    # 1. Official SIH Light Institutional Theme
    "sih_institutional_light": Theme(
        name="sih_institutional_light",
        is_dark_mode=False,
        canvas_bg="#FFFFFF",
        card_bg="#F8FAFC",
        card_border="#CBD5E1",
        title_primary="#0F172A",
        subtitle_color="#334155",
        body_text="#0F172A",
        muted_text="#64748B",
        bullet_accent="#1D4ED8",
        team_badge_bg="#FFFFFF",
        team_badge_border="#6366F1",
        team_badge_text="#0F172A",
        header_title_color="#1E293B",
        footer_bg="#0D5CA8",
        footer_text="#FFFFFF",
        callout_bg="#FEF3C7",
        callout_border="#D97706",
        callout_title="#92400E",
        callout_text="#0F172A",
        demo_card_bg="#FFFFFF",
        demo_card_border="#EF4444",
        demo_link_color="#1D4ED8",
        arch_container_bg="#FFFFFF",
        arch_container_border="#94A3B8",
        tier_header_bg="#0F3A70",
        tier_header_text="#FFFFFF",
        tier_card_bg="#F8FAFC",
        tier_card_border="#CBD5E1",
        service_node_bg="#FFFFFF",
        service_node_border="#0284C7",
        service_node_text="#0F172A",
        flow_arrow_color="#0284C7",
        tech_col_bg="#F8FAFC",
        tech_col_border="#CBD5E1",
        tech_badge_bg="#FFFFFF",
        tech_badge_text="#0F172A",
        table_header_bg="#F1F5F9",
        table_header_text="#0F172A",
        table_zebra_bg="#F8FAFC",
        table_cell_text="#0F172A",
        table_border="#CBD5E1",
        table_highlight_bg="#ECFDF5",
        font_title="Georgia",
        font_body="Arial"
    ),

    # 2. Cyber Dark Terminal Theme (High-Tech Defense / AI / Blockchain)
    "cyber_dark_terminal": Theme(
        name="cyber_dark_terminal",
        is_dark_mode=True,
        canvas_bg="#0B0F19",          # Deep obsidian black
        card_bg="#111827",            # Dark slate card fill
        card_border="#1F2937",        # Subtle gray border
        title_primary="#F9FAFB",      # Crisp white
        subtitle_color="#9CA3AF",     # Cool gray
        body_text="#F3F4F6",          # Off-white
        muted_text="#9CA3AF",         # Muted silver
        bullet_accent="#38BDF8",      # Neon cyan
        team_badge_bg="#111827",
        team_badge_border="#38BDF8",  # Glowing cyan
        team_badge_text="#F9FAFB",
        header_title_color="#F9FAFB",
        footer_bg="#0369A1",          # Deep cyan
        footer_text="#F9FAFB",
        callout_bg="#1E1B4B",          # Deep indigo tint
        callout_border="#6366F1",      # Electric violet
        callout_title="#A5B4FC",
        callout_text="#F3F4F6",
        demo_card_bg="#18181B",
        demo_card_border="#F43F5E",   # Rose crimson
        demo_link_color="#38BDF8",
        arch_container_bg="#0F172A",
        arch_container_border="#334155",
        tier_header_bg="#1E293B",
        tier_header_text="#38BDF8",
        tier_card_bg="#111827",
        tier_card_border="#1F2937",
        service_node_bg="#1E293B",
        service_node_border="#0EA5E9",
        service_node_text="#F8FAFC",
        flow_arrow_color="#38BDF8",
        tech_col_bg="#111827",
        tech_col_border="#1F2937",
        tech_badge_bg="#1E293B",
        tech_badge_text="#F9FAFB",
        table_header_bg="#1E293B",
        table_header_text="#38BDF8",
        table_zebra_bg="#111827",
        table_cell_text="#F3F4F6",
        table_border="#334155",
        table_highlight_bg="#064E3B",  # Deep emerald
        font_title="Segoe UI",
        font_body="Segoe UI"
    ),

    # 3. Enterprise Slate Minimal Theme (Clean Executive / Management / Defense)
    "enterprise_slate": Theme(
        name="enterprise_slate",
        is_dark_mode=False,
        canvas_bg="#F8FAFC",
        card_bg="#FFFFFF",
        card_border="#E2E8F0",
        title_primary="#0F172A",
        subtitle_color="#475569",
        body_text="#1E293B",
        muted_text="#64748B",
        bullet_accent="#2563EB",
        team_badge_bg="#FFFFFF",
        team_badge_border="#2563EB",
        team_badge_text="#0F172A",
        header_title_color="#0F172A",
        footer_bg="#1E293B",
        footer_text="#FFFFFF",
        callout_bg="#EFF6FF",
        callout_border="#3B82F6",
        callout_title="#1E40AF",
        callout_text="#1E293B",
        demo_card_bg="#FFFFFF",
        demo_card_border="#0284C7",
        demo_link_color="#2563EB",
        arch_container_bg="#FFFFFF",
        arch_container_border="#CBD5E1",
        tier_header_bg="#1E293B",
        tier_header_text="#FFFFFF",
        tier_card_bg="#F8FAFC",
        tier_card_border="#E2E8F0",
        service_node_bg="#FFFFFF",
        service_node_border="#3B82F6",
        service_node_text="#0F172A",
        flow_arrow_color="#2563EB",
        tech_col_bg="#F1F5F9",
        tech_col_border="#CBD5E1",
        tech_badge_bg="#FFFFFF",
        tech_badge_text="#0F172A",
        table_header_bg="#E2E8F0",
        table_header_text="#0F172A",
        table_zebra_bg="#F8FAFC",
        table_cell_text="#1E293B",
        table_border="#CBD5E1",
        table_highlight_bg="#ECFDF5",
        font_title="Arial",
        font_body="Arial"
    ),

    # 4. Modern Gradient SaaS / Fintech Theme
    "modern_fintech": Theme(
        name="modern_fintech",
        is_dark_mode=False,
        canvas_bg="#FAF5FF",          # Very light purple/white
        card_bg="#FFFFFF",
        card_border="#E9D5FF",
        title_primary="#1E1B4B",
        subtitle_color="#4C1D95",
        body_text="#1E1B4B",
        muted_text="#6B21A8",
        bullet_accent="#7C3AED",
        team_badge_bg="#FFFFFF",
        team_badge_border="#7C3AED",
        team_badge_text="#1E1B4B",
        header_title_color="#1E1B4B",
        footer_bg="#6D28D9",
        footer_text="#FFFFFF",
        callout_bg="#FDF2F8",
        callout_border="#DB2777",
        callout_title="#9D174D",
        callout_text="#1E1B4B",
        demo_card_bg="#FFFFFF",
        demo_card_border="#7C3AED",
        demo_link_color="#6D28D9",
        arch_container_bg="#FFFFFF",
        arch_container_border="#DDD6FE",
        tier_header_bg="#4C1D95",
        tier_header_text="#FFFFFF",
        tier_card_bg="#FAF5FF",
        tier_card_border="#E9D5FF",
        service_node_bg="#FFFFFF",
        service_node_border="#7C3AED",
        service_node_text="#1E1B4B",
        flow_arrow_color="#7C3AED",
        tech_col_bg="#FAF5FF",
        tech_col_border="#E9D5FF",
        tech_badge_bg="#FFFFFF",
        tech_badge_text="#1E1B4B",
        table_header_bg="#EDE9FE",
        table_header_text="#4C1D95",
        table_zebra_bg="#FAF5FF",
        table_cell_text="#1E1B4B",
        table_border="#DDD6FE",
        table_highlight_bg="#ECFDF5",
        font_title="Georgia",
        font_body="Arial"
    )
}


def get_theme(name: str) -> Theme:
    """Retrieves theme by identifier with fallback to SIH institutional light."""
    return THEMES.get(name, THEMES["sih_institutional_light"])
