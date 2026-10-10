"""
Presentation Engine — Dynamic Theme & Design Tokens Registry
Enables dynamic runtime registration, inheritance, and customization of themes,
typography pairings, and visual styling tokens without modifying core engine code.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from scripts.engine.themes import Theme, THEMES, get_theme as get_legacy_theme


@dataclass
class ExtendedThemeTokens:
    """Rich design tokens extending standard Theme with typography and geometry rules."""
    theme: Theme
    font_family_heading: str = "Calibri"
    font_family_body: str = "Calibri"
    card_border_radius_pt: float = 6.0  # 0.0=sharp, 6.0=subtle, 12.0=modern rounded
    card_border_width_pt: float = 1.2
    accent_glow: str = "#06B6D4"
    accent_secondary: str = "#10B981"
    shadow_elevation: bool = False
    custom_metadata: Dict[str, Any] = field(default_factory=dict)


class ThemeRegistry:
    """Dynamic registry for presentation themes and design system tokens."""
    _registry: Dict[str, ExtendedThemeTokens] = {}

    @classmethod
    def initialize_defaults(cls):
        """Pre-populates registry with built-in championship themes."""
        if cls._registry:
            return

        # 1. Cyber Dark Terminal
        cyber_base = THEMES["cyber_dark_terminal"]
        cls._registry["cyber_dark_terminal"] = ExtendedThemeTokens(
            theme=cyber_base,
            font_family_heading="Segoe UI",
            font_family_body="Segoe UI",
            card_border_radius_pt=4.0,
            card_border_width_pt=1.5,
            accent_glow="#00F0FF",
            accent_secondary="#10B981"
        )

        # 2. SIH Institutional Light
        sih_base = THEMES["sih_institutional_light"]
        cls._registry["sih_institutional_light"] = ExtendedThemeTokens(
            theme=sih_base,
            font_family_heading="Calibri",
            font_family_body="Calibri",
            card_border_radius_pt=3.0,
            card_border_width_pt=1.2,
            accent_glow="#1D4ED8",
            accent_secondary="#F59E0B"
        )

        # 3. Enterprise Slate
        slate_base = THEMES["enterprise_slate"]
        cls._registry["enterprise_slate"] = ExtendedThemeTokens(
            theme=slate_base,
            font_family_heading="Arial",
            font_family_body="Arial",
            card_border_radius_pt=4.0,
            card_border_width_pt=1.0,
            accent_glow="#3B82F6",
            accent_secondary="#64748B"
        )

        # 4. Modern Fintech
        fintech_base = THEMES["modern_fintech"]
        cls._registry["modern_fintech"] = ExtendedThemeTokens(
            theme=fintech_base,
            font_family_heading="Trebuchet MS",
            font_family_body="Trebuchet MS",
            card_border_radius_pt=8.0,
            card_border_width_pt=1.5,
            accent_glow="#10B981",
            accent_secondary="#0EA5E9"
        )

        # 5. Modern SaaS Glass (New Championship Preset)
        saas_theme = Theme(
            name="modern_saas_glass",
            is_dark_mode=False,
            canvas_bg="#F8FAFC",
            card_bg="#FFFFFF",
            card_border="#E2E8F0",
            title_primary="#0F172A",
            subtitle_color="#475569",
            body_text="#1E293B",
            muted_text="#64748B",
            bullet_accent="#4F46E5",
            team_badge_bg="#EEF2FF",
            team_badge_border="#C7D2FE",
            team_badge_text="#3730A3",
            header_title_color="#1E1B4B",
            footer_bg="#4F46E5",
            footer_text="#FFFFFF",
            callout_bg="#F5F3FF",
            callout_border="#DDD6FE",
            callout_title="#5B21B6",
            callout_text="#4C1D95",
            demo_card_bg="#FEF2F2",
            demo_card_border="#FECACA",
            demo_link_color="#B91C1C",
            arch_container_bg="#FFFFFF",
            arch_container_border="#CBD5E1",
            tier_header_bg="#4F46E5",
            tier_header_text="#FFFFFF",
            tier_card_bg="#F8FAFC",
            tier_card_border="#E2E8F0",
            service_node_bg="#FFFFFF",
            service_node_border="#CBD5E1",
            service_node_text="#0F172A",
            flow_arrow_color="#6366F1",
            tech_col_bg="#F8FAFC",
            tech_col_border="#E2E8F0",
            tech_badge_bg="#E0E7FF",
            tech_badge_text="#3730A3",
            table_header_bg="#312E81",
            table_header_text="#FFFFFF",
            table_zebra_bg="#F8FAFC",
            table_cell_text="#0F172A",
            table_border="#CBD5E1",
            table_highlight_bg="#EEF2FF",
            font_title="Outfit",
            font_body="Inter"
        )
        cls._registry["modern_saas_glass"] = ExtendedThemeTokens(
            theme=saas_theme,
            font_family_heading="Outfit",
            font_family_body="Inter",
            card_border_radius_pt=10.0,
            card_border_width_pt=1.5,
            accent_glow="#4F46E5",
            accent_secondary="#06B6D4"
        )

        # 6. Minimalist Editorial Mono (New Championship Preset)
        mono_theme = Theme(
            name="minimalist_editorial_mono",
            is_dark_mode=False,
            canvas_bg="#FAF9F6",
            card_bg="#FFFFFF",
            card_border="#E5E5E5",
            title_primary="#18181B",
            subtitle_color="#52525B",
            body_text="#27272A",
            muted_text="#71717A",
            bullet_accent="#18181B",
            team_badge_bg="#F4F4F5",
            team_badge_border="#D4D4D8",
            team_badge_text="#18181B",
            header_title_color="#09090B",
            footer_bg="#18181B",
            footer_text="#F4F4F5",
            callout_bg="#F4F4F5",
            callout_border="#D4D4D8",
            callout_title="#09090B",
            callout_text="#27272A",
            demo_card_bg="#FAFAFA",
            demo_card_border="#E4E4E7",
            demo_link_color="#18181B",
            arch_container_bg="#FFFFFF",
            arch_container_border="#D4D4D8",
            tier_header_bg="#18181B",
            tier_header_text="#FFFFFF",
            tier_card_bg="#FAFAFA",
            tier_card_border="#E4E4E7",
            service_node_bg="#FFFFFF",
            service_node_border="#D4D4D8",
            service_node_text="#18181B",
            flow_arrow_color="#52525B",
            tech_col_bg="#FAFAFA",
            tech_col_border="#E4E4E7",
            tech_badge_bg="#E4E4E7",
            tech_badge_text="#18181B",
            table_header_bg="#18181B",
            table_header_text="#FFFFFF",
            table_zebra_bg="#FAFAFA",
            table_cell_text="#18181B",
            table_border="#D4D4D8",
            table_highlight_bg="#F4F4F5",
            font_title="Georgia",
            font_body="Calibri"
        )
        cls._registry["minimalist_editorial_mono"] = ExtendedThemeTokens(
            theme=mono_theme,
            font_family_heading="Georgia",
            font_family_body="Calibri",
            card_border_radius_pt=0.0,  # Sharp editorial edges
            card_border_width_pt=1.0,
            accent_glow="#18181B",
            accent_secondary="#71717A"
        )

    @classmethod
    def register_theme(cls, name: str, tokens: ExtendedThemeTokens) -> None:
        """Dynamically registers a new theme or overrides an existing one."""
        cls.initialize_defaults()
        cls._registry[name] = tokens

    @classmethod
    def create_custom_theme(
        cls,
        name: str,
        base_theme: str = "cyber_dark_terminal",
        canvas_bg: Optional[str] = None,
        card_bg: Optional[str] = None,
        card_border: Optional[str] = None,
        accent: Optional[str] = None,
        text_primary: Optional[str] = None,
        font_family: Optional[str] = None,
        font_heading: Optional[str] = None,
        font_body: Optional[str] = None,
        card_border_radius_pt: Optional[float] = None,
        is_dark_mode: Optional[bool] = None,
        **extra_overrides
    ) -> ExtendedThemeTokens:
        """
        Creates and registers a custom theme on the fly by overriding base theme attributes.
        """
        cls.initialize_defaults()
        base = cls.get_extended_theme(base_theme)

        # Clone base theme dataclass
        import copy
        new_theme = copy.deepcopy(base.theme)
        new_theme.name = name

        if is_dark_mode is not None:
            new_theme.is_dark_mode = is_dark_mode
        if canvas_bg:
            new_theme.canvas_bg = canvas_bg
        if card_bg:
            new_theme.card_bg = card_bg
        if card_border:
            new_theme.card_border = card_border
        if text_primary:
            new_theme.title_primary = text_primary
            new_theme.header_title_color = text_primary
            new_theme.body_text = text_primary
        if accent:
            new_theme.bullet_accent = accent
            new_theme.tier_header_bg = accent
            new_theme.table_header_bg = accent
            new_theme.flow_chevron_color = accent

        # Apply any extra overrides directly to theme fields
        for k, v in extra_overrides.items():
            if hasattr(new_theme, k):
                setattr(new_theme, k, v)

        heading_font = font_heading or font_family or base.font_family_heading
        body_font = font_body or font_family or base.font_family_body
        radius = card_border_radius_pt if card_border_radius_pt is not None else base.card_border_radius_pt

        extended = ExtendedThemeTokens(
            theme=new_theme,
            font_family_heading=heading_font,
            font_family_body=body_font,
            card_border_radius_pt=radius,
            card_border_width_pt=base.card_border_width_pt,
            accent_glow=accent or base.accent_glow,
            accent_secondary=base.accent_secondary
        )

        cls.register_theme(name, extended)
        return extended

    @classmethod
    def get_extended_theme(cls, name: str) -> ExtendedThemeTokens:
        """Retrieves an extended theme by name, falling back to cyber_dark_terminal."""
        cls.initialize_defaults()
        if name in cls._registry:
            return cls._registry[name]
        # Check legacy themes
        if name in THEMES:
            t = THEMES[name]
            return ExtendedThemeTokens(theme=t)
        return cls._registry["cyber_dark_terminal"]

    @classmethod
    def get_theme(cls, name: str) -> Theme:
        """Convenience method returning the core Theme object."""
        return cls.get_extended_theme(name).theme

    @classmethod
    def list_themes(cls) -> List[str]:
        """Returns list of all available theme names."""
        cls.initialize_defaults()
        return list(cls._registry.keys())
