"""
Launcher style manager.

Provides the active visual style used by the launcher.
"""

from __future__ import annotations

from launcher.themes import (
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

BACKGROUND = (235, 238, 242)

HEADER = (47, 53, 66)
FOOTER = (47, 53, 66)

SIDEBAR = (223, 227, 234)
WORKSPACE = (248, 249, 251)
PANEL = (255, 255, 255)

# ==================================================
# TEXT
# ==================================================

TEXT = (35, 35, 35)
TEXT_LIGHT = (245, 245, 245)
TEXT_SECONDARY = (110, 110, 110)

# ==================================================
# BORDERS
# ==================================================

BORDER = (200, 200, 205)

# ==================================================
# ACCENT
# ==================================================

PRIMARY = (55, 95, 210)

ACCENT = (52, 120, 246)
ACCENT_HOVER = (73, 141, 255)

# ==================================================
# STATUS
# ==================================================

SUCCESS = (52, 168, 83)
WARNING = (251, 188, 5)
ERROR = (234, 67, 53)

# ==================================================
# COMPONENTS
# ==================================================

CARD = PANEL
CARD_HOVER = (248, 249, 251)
CARD_SELECTED = (210, 225, 255)


ROW = PANEL
ROW_HOVER = (245, 245, 245)
ROW_SELECTED = (210, 225, 255)

INPUT = PANEL

# ==================================================
# DIALOGS
# ==================================================

DIALOG = PANEL
OVERLAY = (0, 0, 0, 120)

# ==================================================
# BUTTONS
# ==================================================

BUTTON_TEXT = TEXT_LIGHT

# ==================================================
# LAYOUT
# ==================================================

HEADER_HEIGHT = 60
FOOTER_HEIGHT = 28
SIDEBAR_WIDTH = 220

PADDING = 20

# ==================================================
# Theme management
# ==================================================

def set_theme(theme: str) -> bool:
    """
    Changes the active launcher theme.

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
    Returns the identifier of the active theme.
    """

    return _current_theme_name


# --------------------------------------------------


def get_themes() -> tuple[str, ...]:
    """
    Returns the identifiers of all available themes.
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

    global BACKGROUND
    global HEADER
    global FOOTER
    global SIDEBAR
    global WORKSPACE
    global PANEL

    BACKGROUND = _current_theme.BACKGROUND

    HEADER = _current_theme.HEADER
    FOOTER = _current_theme.FOOTER

    SIDEBAR = _current_theme.SIDEBAR
    WORKSPACE = _current_theme.WORKSPACE
    PANEL = _current_theme.PANEL

    # --------------------------------------------------
    # Text
    # --------------------------------------------------

    global TEXT
    global TEXT_LIGHT
    global TEXT_SECONDARY

    TEXT = _current_theme.TEXT
    TEXT_LIGHT = _current_theme.TEXT_LIGHT
    TEXT_SECONDARY = _current_theme.TEXT_SECONDARY

    # --------------------------------------------------
    # Borders
    # --------------------------------------------------

    global BORDER

    BORDER = _current_theme.BORDER

    # --------------------------------------------------
    # Accent
    # --------------------------------------------------

    global PRIMARY
    global ACCENT
    global ACCENT_HOVER

    PRIMARY = _current_theme.PRIMARY

    ACCENT = _current_theme.ACCENT
    ACCENT_HOVER = _current_theme.ACCENT_HOVER

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    global SUCCESS
    global WARNING
    global ERROR

    SUCCESS = _current_theme.SUCCESS
    WARNING = _current_theme.WARNING
    ERROR = _current_theme.ERROR

    # --------------------------------------------------
    # Components
    # --------------------------------------------------

    global CARD
    global CARD_HOVER
    global CARD_SELECTED

    global ROW
    global ROW_HOVER
    global ROW_SELECTED

    global INPUT

    CARD = _current_theme.CARD
    CARD_HOVER = _current_theme.CARD_HOVER
    CARD_SELECTED = _current_theme.CARD_SELECTED

    ROW = _current_theme.ROW
    ROW_HOVER = _current_theme.ROW_HOVER
    ROW_SELECTED = _current_theme.ROW_SELECTED

    INPUT = _current_theme.INPUT

    # --------------------------------------------------
    # Dialogs
    # --------------------------------------------------

    global DIALOG
    global OVERLAY

    DIALOG = _current_theme.DIALOG
    OVERLAY = _current_theme.OVERLAY

    # --------------------------------------------------
    # Buttons
    # --------------------------------------------------

    global BUTTON_TEXT

    BUTTON_TEXT = _current_theme.BUTTON_TEXT