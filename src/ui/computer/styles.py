"""
Computer style manager.

Provides the active visual style used by the in-game computers
and their document viewers.
"""

from __future__ import annotations

from ui.computer.themes import (
    default,
    dark,
    midnight,
    forest,
    warm,
    high_contrast,
)


# ==================================================
# Available themes
# ==================================================

THEMES = {
    "default": default,
    "dark": dark,
    "midnight": midnight,
    "forest": forest,
    "warm": warm,
    "high_contrast": high_contrast,
}


# ==================================================
# Active theme
# ==================================================

_current_theme_name = "default"
_current_theme = THEMES[_current_theme_name]


# ==================================================
# GENERAL
# ==================================================

WINDOW = (224, 228, 234)

SIDEBAR = (42, 46, 54)

TOPBAR = (245, 246, 248)

CONTENT = (250, 250, 251)

PANEL = CONTENT


# ==================================================
# TEXT
# ==================================================

TEXT = (42, 45, 50)
TEXT_SECONDARY = (120, 126, 136)
TEXT_LIGHT = (245, 245, 245)


# ==================================================
# ACCENT
# ==================================================

ACCENT = (63, 124, 255)
ACCENT_LIGHT = (232, 240, 255)


# ==================================================
# BUTTONS
# ==================================================

BUTTON = (240, 242, 245)
BUTTON_HOVER = (228, 232, 238)
BUTTON_SELECTED = ACCENT


# ==================================================
# BORDERS
# ==================================================

BORDER = (214, 218, 224)
DIVIDER = (228, 231, 236)


# ==================================================
# SHADOWS
# ==================================================

SHADOW = (205, 209, 215)


# ==================================================
# LAYOUT
# ==================================================

SIDEBAR_WIDTH = 230

TOPBAR_HEIGHT = 42
HEADER_HEIGHT = 58

PADDING = 24

CARD_MARGIN = 14
CARD_RADIUS = 10

# ==================================================
# WINDOW CONTROLS
# ==================================================

WINDOW_CLOSE = (235, 95, 86)
WINDOW_MINIMIZE = (243, 190, 67)
WINDOW_MAXIMIZE = (89, 201, 98)


# ==================================================
# Theme management
# ==================================================

def set_theme(theme: str) -> bool:
    """
    Changes the active computer theme.

    Parameters
    ----------
    theme:
        Identifier of the theme to activate.

    Returns
    -------
    bool
        True if the theme was changed successfully.
    """

    if theme not in THEMES:
        return False

    global _current_theme_name
    global _current_theme

    _current_theme_name = theme
    _current_theme = THEMES[theme]

    _apply_theme()

    return True


# --------------------------------------------------


def get_theme() -> str:
    """
    Returns the identifier of the active computer theme.
    """

    return _current_theme_name


# --------------------------------------------------


def get_themes() -> tuple[str, ...]:
    """
    Returns the identifiers of all available computer themes.
    """

    return tuple(THEMES.keys())


# ==================================================
# Internal
# ==================================================

def _apply_theme():
    """
    Applies the active theme to the public style values.
    """

    # --------------------------------------------------
    # General
    # --------------------------------------------------

    global WINDOW
    global SIDEBAR
    global TOPBAR
    global CONTENT
    global PANEL

    WINDOW = _current_theme.WINDOW

    SIDEBAR = _current_theme.SIDEBAR
    TOPBAR = _current_theme.TOPBAR

    CONTENT = _current_theme.CONTENT
    PANEL = _current_theme.PANEL

    # --------------------------------------------------
    # Text
    # --------------------------------------------------

    global TEXT
    global TEXT_SECONDARY
    global TEXT_LIGHT

    TEXT = _current_theme.TEXT
    TEXT_SECONDARY = _current_theme.TEXT_SECONDARY
    TEXT_LIGHT = _current_theme.TEXT_LIGHT

    # --------------------------------------------------
    # Accent
    # --------------------------------------------------

    global ACCENT
    global ACCENT_LIGHT

    ACCENT = _current_theme.ACCENT
    ACCENT_LIGHT = _current_theme.ACCENT_LIGHT

    # --------------------------------------------------
    # Buttons
    # --------------------------------------------------

    global BUTTON
    global BUTTON_HOVER
    global BUTTON_SELECTED

    BUTTON = _current_theme.BUTTON
    BUTTON_HOVER = _current_theme.BUTTON_HOVER
    BUTTON_SELECTED = _current_theme.BUTTON_SELECTED

    # --------------------------------------------------
    # Borders
    # --------------------------------------------------

    global BORDER
    global DIVIDER

    BORDER = _current_theme.BORDER
    DIVIDER = _current_theme.DIVIDER

    # --------------------------------------------------
    # Shadows
    # --------------------------------------------------

    global SHADOW

    SHADOW = _current_theme.SHADOW