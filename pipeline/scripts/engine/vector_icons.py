"""
Presentation Engine — Offline Vector SVG & Geometry Icon Pack
Provides clean, scalable vector icons and badge geometry for enterprise presentation slides
without external network dependencies.
"""

from typing import Dict, Optional


# Offline SVG Icons (Curated from Feather/Lucide icons for Enterprise & Tech Decks)
SVG_ICONS: Dict[str, str] = {
    "shield": (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
    ),
    "database": (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>'
        '<path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>'
        '<path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg>'
    ),
    "server": (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>'
        '<rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>'
        '<line x1="6" y1="6" x2="6.01" y2="6"></line>'
        '<line x1="6" y1="18" x2="6.01" y2="18"></line></svg>'
    ),
    "lock": (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>'
        '<path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>'
    ),
    "cpu": (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect>'
        '<rect x="9" y="9" width="6" height="6"></rect>'
        '<line x1="9" y1="1" x2="9" y2="4"></line>'
        '<line x1="15" y1="1" x2="15" y2="4"></line>'
        '<line x1="9" y1="20" x2="9" y2="23"></line>'
        '<line x1="15" y1="20" x2="15" y2="23"></line>'
        '<line x1="20" y1="9" x2="23" y2="9"></line>'
        '<line x1="20" y1="14" x2="23" y2="14"></line>'
        '<line x1="1" y1="9" x2="4" y2="9"></line>'
        '<line x1="1" y1="14" x2="4" y2="14"></line></svg>'
    ),
    "network": (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="16" y="16" width="6" height="6" rx="1"></rect>'
        '<rect x="2" y="16" width="6" height="6" rx="1"></rect>'
        '<rect x="9" y="2" width="6" height="6" rx="1"></rect>'
        '<path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3"></path>'
        '<line x1="12" y1="12" x2="12" y2="8"></line></svg>'
    ),
    "check_circle": (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10B981" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>'
        '<polyline points="22 4 12 14.01 9 11.01"></polyline></svg>'
    ),
    "alert_triangle": (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>'
        '<line x1="12" y1="9" x2="12" y2="13"></line>'
        '<line x1="12" y1="17" x2="12.01" y2="17"></line></svg>'
    ),
    "terminal": (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="4 17 10 11 4 5"></polyline>'
        '<line x1="12" y1="19" x2="20" y2="19"></line></svg>'
    ),
    "chart": (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<line x1="18" y1="20" x2="18" y2="10"></line>'
        '<line x1="12" y1="20" x2="12" y2="4"></line>'
        '<line x1="6" y1="20" x2="6" y2="14"></line></svg>'
    ),
    "zap": (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#06B6D4" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'
    ),
    "globe": (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="10"></circle>'
        '<line x1="2" y1="12" x2="22" y2="12"></line>'
        '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'
    )
}


def get_svg_icon(name: str, color: Optional[str] = None, size: int = 24) -> str:
    """Returns the SVG string for a requested icon with custom color and size."""
    icon_svg = SVG_ICONS.get(name.lower(), SVG_ICONS["shield"])
    if color:
        icon_svg = icon_svg.replace('stroke="currentColor"', f'stroke="{color}"')
    if size != 24:
        icon_svg = icon_svg.replace('width="24"', f'width="{size}"').replace('height="24"', f'height="{size}"')
    return icon_svg
