"""
Theme: Quantum Diagnostics
A modern dark theme inspired by Windows 11 diagnostics, MSI Center,
and professional system monitoring tools.

All colors, fonts, spacing, and reusable component styles live here
so the whole UI stays consistent.
"""


# -- Color palette --
# Deep carbon-black base with sapphire blue as primary accent.
# Feels technical and trustworthy without going "hacker mode."

COLORS = {
    # backgrounds (layered depth — deepest to surface)
    "bg_base": "#050816",       # carbon black — app root
    "bg_sidebar": "#0A0F1E",    # sidebar — slightly lighter
    "bg_surface": "#111827",    # graphite blue — main content
    "bg_card": "#1A2235",       # card / panel surface
    "bg_card_hover": "#1F2A40", # card hover
    "bg_input": "#0D1525",      # input fields, text areas

    # primary accent — neon sapphire
    "accent": "#3B82F6",
    "accent_hover": "#2563EB",
    "accent_subtle": "#1E3A5F",  # nav active bg, subtle highlights
    "accent_glow": "#3B82F6",    # status dots, glows

    # secondary accent — tech violet
    "secondary": "#8B5CF6",
    "secondary_hover": "#7C3AED",

    # highlight — aqua pulse (for special indicators)
    "highlight": "#22D3EE",

    # text hierarchy
    "text_primary": "#F8FAFC",   # ice white
    "text_secondary": "#94A3B8", # slate frost
    "text_muted": "#475569",     # quiet labels, footers
    "text_accent": "#3B82F6",    # links, active text

    # status colors
    "success": "#22C55E",        # matrix green
    "warning": "#F59E0B",        # signal amber
    "danger": "#EF4444",         # critical red
    "info": "#3B82F6",           # sapphire info

    # borders & dividers
    "border": "#1E293B",         # card borders
    "border_subtle": "#172033",  # very faint separators
    "divider": "#1E293B",

    # progress bars
    "progress_bg": "#0F172A",
    "progress_fill": "#3B82F6",
}


# -- Typography scale --
FONT = {
    "heading_lg": 22,
    "heading_md": 16,
    "heading_sm": 14,
    "body": 13,
    "body_sm": 12,
    "caption": 11,
    "tiny": 10,
}


# -- Spacing rhythm --
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 20,
    "xxl": 28,
}


# -- Reusable component style dicts (pass as **kwargs) --

CARD_STYLE = {
    "corner_radius": 12,
    "fg_color": COLORS["bg_card"],
    "border_width": 1,
    "border_color": COLORS["border"],
}

BUTTON_PRIMARY = {
    "corner_radius": 8,
    "fg_color": COLORS["accent"],
    "hover_color": COLORS["accent_hover"],
    "text_color": "#FFFFFF",
    "height": 38,
}

BUTTON_SECONDARY = {
    "corner_radius": 8,
    "fg_color": COLORS["bg_card"],
    "hover_color": COLORS["bg_card_hover"],
    "border_width": 1,
    "border_color": COLORS["border"],
    "text_color": COLORS["text_primary"],
    "height": 38,
}

BUTTON_DANGER = {
    "corner_radius": 8,
    "fg_color": "#7F1D1D",
    "hover_color": "#991B1B",
    "text_color": "#FCA5A5",
    "height": 38,
}

NAV_BUTTON = {
    "corner_radius": 8,
    "fg_color": "transparent",
    "hover_color": COLORS["accent_subtle"],
    "text_color": COLORS["text_secondary"],
    "height": 36,
    "anchor": "w",
}

NAV_BUTTON_ACTIVE = {
    "fg_color": COLORS["accent_subtle"],
    "text_color": COLORS["accent"],
}

INPUT_STYLE = {
    "corner_radius": 8,
    "fg_color": COLORS["bg_input"],
    "border_width": 1,
    "border_color": COLORS["border"],
    "text_color": COLORS["text_primary"],
    "height": 36,
}


def rating_color(rating):
    """Map health rating to its status color."""
    return {
        "Excellent": COLORS["success"],
        "Good": COLORS["accent"],
        "Moderate": COLORS["warning"],
        "Poor": COLORS["danger"],
    }.get(rating, COLORS["accent"])


def usage_color(percent):
    """Color based on resource usage level (higher = worse)."""
    if percent >= 90:
        return COLORS["danger"]
    elif percent >= 75:
        return COLORS["warning"]
    elif percent >= 50:
        return COLORS["accent"]
    return COLORS["success"]
