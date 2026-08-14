"""
Game style manager.

Provides the active visual style used by the game.
Themes define the actual visual values, while this module
exposes them to the rest of the game.
"""

from __future__ import annotations

from game.themes import dark, default, forest, midnight, warm, high_contrast


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

BACKGROUND = None

# ==================================================
# WORLD
# ==================================================

WORLD_BACKGROUND = None


# ==================================================
# HUD
# ==================================================

HUD_CLOCK_SHADOW = (0, 0, 0)
HUD_CLOCK_SHADOW_ALPHA = 100

HUD_CLOCK_TEXT = (240, 240, 240)
HUD_CLOCK_TEXT_ALPHA = 170

HUD_BADGE_BACKGROUND = (20, 20, 20)
HUD_BADGE_BACKGROUND_ALPHA = 135

HUD_BADGE_BORDER = (255, 255, 255)
HUD_BADGE_BORDER_ALPHA = 55

HUD_BADGE_ICON = (235, 235, 235)

HUD_BADGE_TEXT = (240, 240, 240)
HUD_BADGE_TEXT_ALPHA = 210


# ==================================================
# OVERLAYS
# ==================================================

OVERLAY_BACKGROUND = (0, 0, 0)
OVERLAY_BACKGROUND_ALPHA = 160

OVERLAY_PANEL = None
OVERLAY_BORDER = None


# ==================================================
# TEXT
# ==================================================

TEXT = None
TEXT_LIGHT = None
TEXT_SECONDARY = None


# ==================================================
# BORDERS
# ==================================================

BORDER = None


# ==================================================
# ACCENT
# ==================================================

PRIMARY = None
ACCENT = None
ACCENT_HOVER = None


# ==================================================
# STATUS
# ==================================================

SUCCESS = None
WARNING = None
ERROR = None


# ==================================================
# BUTTONS
# ==================================================

BUTTON = None
BUTTON_HOVER = None
BUTTON_BORDER = None
BUTTON_TEXT = None

BUTTON_CANCEL = None
BUTTON_CONFIRM = None


# ==================================================
# DIALOGUE
# ==================================================

DIALOGUE_PANEL = None
DIALOGUE_BORDER = None

DIALOGUE_TITLE = None
DIALOGUE_TEXT = None
DIALOGUE_DIVIDER = None
DIALOGUE_INDICATOR = None


# ==================================================
# DOCUMENT
# ==================================================

DOCUMENT_PAPER_TOP = None
DOCUMENT_PAPER_BOTTOM = None
DOCUMENT_PAPER_BORDER = None

DOCUMENT_TITLE = None
DOCUMENT_TEXT = None
DOCUMENT_DIVIDER = None

DOCUMENT_BUTTON = None
DOCUMENT_BUTTON_HOVER = None
DOCUMENT_BUTTON_BORDER = None
DOCUMENT_BUTTON_ICON = (255,255,255)

DOCUMENT_SHADOW = (0,0,0)
DOCUMENT_SHADOW_ALPHA = None


# ==================================================
# CONFIRMATION
# ==================================================

CONFIRM_TITLE = None
CONFIRM_MESSAGE = None

CONFIRM_CANCEL_BUTTON = None
CONFIRM_CONFIRM_BUTTON = None


# ==================================================
# QUICK NOTES
# ==================================================

QUICK_NOTES_TITLE = None
QUICK_NOTES_LABEL = None
QUICK_NOTES_INPUT = None

QUICK_NOTES_CANCEL_BUTTON = None
QUICK_NOTES_SAVE_BUTTON = None


# ==================================================
# TRANSITION
# ==================================================

TRANSITION_TEXT = None


# ==================================================
# LAYOUT
# ==================================================

HUD_TOP_MARGIN = 20
HUD_LEFT_MARGIN = 30

OVERLAY_PADDING = 20

DIALOGUE_WIDTH = 920
DIALOGUE_HEIGHT = 190
DIALOGUE_DIVIDER_WIDTH = 2

DOCUMENT_WIDTH = 900
DOCUMENT_HEIGHT = 550
DOCUMENT_DIVIDER_WIDTH = 2

CONFIRM_WIDTH = 600
CONFIRM_HEIGHT = 280

QUICK_NOTES_WIDTH = 760
QUICK_NOTES_HEIGHT = 640


# ==================================================
# Game UI dimensions
# ==================================================

BUTTON_RADIUS = 8
BUTTON_BORDER_WIDTH = 2

OVERLAY_RADIUS = 12
OVERLAY_BORDER_WIDTH = 2


# ==================================================
# Theme management
# ==================================================

def set_theme(theme: str) -> bool:
    """
    Changes the active game theme.

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
    Returns the identifier of the active game theme.
    """

    return _current_theme_name


# --------------------------------------------------


def get_themes() -> tuple[str, ...]:
    """
    Returns the identifiers of all available game themes.
    """

    return tuple(THEMES.keys())


# ==================================================
# Internal
# ==================================================

def _apply_theme():
    """
    Applies the active theme to the public style values.
    """

    # ==================================================
    # GENERAL
    # ==================================================

    global BACKGROUND

    BACKGROUND = _current_theme.BACKGROUND

    # ==================================================
    # WORLD
    # ==================================================

    global WORLD_BACKGROUND

    WORLD_BACKGROUND = _current_theme.WORLD_BACKGROUND

    # ==================================================
    # HUD
    # ==================================================

    global HUD_CLOCK_SHADOW
    global HUD_CLOCK_SHADOW_ALPHA
    global HUD_CLOCK_TEXT
    global HUD_CLOCK_TEXT_ALPHA

    global HUD_BADGE_BACKGROUND
    global HUD_BADGE_BACKGROUND_ALPHA
    global HUD_BADGE_BORDER
    global HUD_BADGE_BORDER_ALPHA
    global HUD_BADGE_ICON
    global HUD_BADGE_TEXT
    global HUD_BADGE_TEXT_ALPHA

    HUD_CLOCK_SHADOW = _current_theme.HUD_CLOCK_SHADOW
    HUD_CLOCK_SHADOW_ALPHA = (
        _current_theme.HUD_CLOCK_SHADOW_ALPHA
    )

    HUD_CLOCK_TEXT = _current_theme.HUD_CLOCK_TEXT
    HUD_CLOCK_TEXT_ALPHA = (
        _current_theme.HUD_CLOCK_TEXT_ALPHA
    )

    HUD_BADGE_BACKGROUND = (
        _current_theme.HUD_BADGE_BACKGROUND
    )
    HUD_BADGE_BACKGROUND_ALPHA = (
        _current_theme.HUD_BADGE_BACKGROUND_ALPHA
    )

    HUD_BADGE_BORDER = (
        _current_theme.HUD_BADGE_BORDER
    )
    HUD_BADGE_BORDER_ALPHA = (
        _current_theme.HUD_BADGE_BORDER_ALPHA
    )

    HUD_BADGE_ICON = (
        _current_theme.HUD_BADGE_ICON
    )

    HUD_BADGE_TEXT = (
        _current_theme.HUD_BADGE_TEXT
    )
    HUD_BADGE_TEXT_ALPHA = (
        _current_theme.HUD_BADGE_TEXT_ALPHA
    )

    # ==================================================
    # OVERLAYS
    # ==================================================

    global OVERLAY_BACKGROUND
    global OVERLAY_BACKGROUND_ALPHA
    global OVERLAY_PANEL
    global OVERLAY_BORDER

    OVERLAY_BACKGROUND = (
        _current_theme.OVERLAY_BACKGROUND
    )
    OVERLAY_BACKGROUND_ALPHA = (
        _current_theme.OVERLAY_BACKGROUND_ALPHA
    )

    OVERLAY_PANEL = (
        _current_theme.OVERLAY_PANEL
    )
    OVERLAY_BORDER = (
        _current_theme.OVERLAY_BORDER
    )

    # ==================================================
    # TEXT
    # ==================================================

    global TEXT
    global TEXT_LIGHT
    global TEXT_SECONDARY

    TEXT = _current_theme.TEXT
    TEXT_LIGHT = _current_theme.TEXT_LIGHT
    TEXT_SECONDARY = _current_theme.TEXT_SECONDARY

    # ==================================================
    # BORDERS
    # ==================================================

    global BORDER

    BORDER = _current_theme.BORDER

    # ==================================================
    # ACCENT
    # ==================================================

    global PRIMARY
    global ACCENT
    global ACCENT_HOVER

    PRIMARY = _current_theme.PRIMARY
    ACCENT = _current_theme.ACCENT
    ACCENT_HOVER = _current_theme.ACCENT_HOVER

    # ==================================================
    # STATUS
    # ==================================================

    global SUCCESS
    global WARNING
    global ERROR

    SUCCESS = _current_theme.SUCCESS
    WARNING = _current_theme.WARNING
    ERROR = _current_theme.ERROR

    # ==================================================
    # BUTTONS
    # ==================================================

    global BUTTON
    global BUTTON_HOVER
    global BUTTON_BORDER
    global BUTTON_TEXT

    global BUTTON_CANCEL
    global BUTTON_CONFIRM

    BUTTON = _current_theme.BUTTON
    BUTTON_HOVER = _current_theme.BUTTON_HOVER
    BUTTON_BORDER = _current_theme.BUTTON_BORDER
    BUTTON_TEXT = _current_theme.BUTTON_TEXT

    BUTTON_CANCEL = _current_theme.BUTTON_CANCEL
    BUTTON_CONFIRM = _current_theme.BUTTON_CONFIRM

    # ==================================================
    # DIALOGUE
    # ==================================================

    global DIALOGUE_PANEL
    global DIALOGUE_BORDER

    global DIALOGUE_TITLE
    global DIALOGUE_TEXT
    global DIALOGUE_DIVIDER
    global DIALOGUE_INDICATOR

    DIALOGUE_PANEL = (
        _current_theme.DIALOGUE_PANEL
    )
    DIALOGUE_BORDER = (
        _current_theme.DIALOGUE_BORDER
    )

    DIALOGUE_TITLE = (
        _current_theme.DIALOGUE_TITLE
    )
    DIALOGUE_TEXT = (
        _current_theme.DIALOGUE_TEXT
    )
    DIALOGUE_DIVIDER = (
        _current_theme.DIALOGUE_DIVIDER
    )
    DIALOGUE_INDICATOR = (
        _current_theme.DIALOGUE_INDICATOR
    )

    # ==================================================
    # DOCUMENT
    # ==================================================

    global DOCUMENT_PAPER_TOP
    global DOCUMENT_PAPER_BOTTOM
    global DOCUMENT_PAPER_BORDER

    global DOCUMENT_TITLE
    global DOCUMENT_TEXT
    global DOCUMENT_DIVIDER

    global DOCUMENT_BUTTON
    global DOCUMENT_BUTTON_HOVER
    global DOCUMENT_BUTTON_BORDER

    global DOCUMENT_SHADOW_ALPHA

    DOCUMENT_PAPER_TOP = (
        _current_theme.DOCUMENT_PAPER_TOP
    )
    DOCUMENT_PAPER_BOTTOM = (
        _current_theme.DOCUMENT_PAPER_BOTTOM
    )
    DOCUMENT_PAPER_BORDER = (
        _current_theme.DOCUMENT_PAPER_BORDER
    )

    DOCUMENT_TITLE = (
        _current_theme.DOCUMENT_TITLE
    )
    DOCUMENT_TEXT = (
        _current_theme.DOCUMENT_TEXT
    )
    DOCUMENT_DIVIDER = (
        _current_theme.DOCUMENT_DIVIDER
    )

    DOCUMENT_BUTTON = (
        _current_theme.DOCUMENT_BUTTON
    )
    DOCUMENT_BUTTON_HOVER = (
        _current_theme.DOCUMENT_BUTTON_HOVER
    )
    DOCUMENT_BUTTON_BORDER = (
        _current_theme.DOCUMENT_BUTTON_BORDER
    )

    DOCUMENT_SHADOW_ALPHA = (
        _current_theme.DOCUMENT_SHADOW_ALPHA
    )

    # ==================================================
    # CONFIRMATION
    # ==================================================

    global CONFIRM_TITLE
    global CONFIRM_MESSAGE
    global CONFIRM_CANCEL_BUTTON
    global CONFIRM_CONFIRM_BUTTON

    CONFIRM_TITLE = (
        _current_theme.CONFIRM_TITLE
    )
    CONFIRM_MESSAGE = (
        _current_theme.CONFIRM_MESSAGE
    )

    CONFIRM_CANCEL_BUTTON = (
        _current_theme.CONFIRM_CANCEL_BUTTON
    )
    CONFIRM_CONFIRM_BUTTON = (
        _current_theme.CONFIRM_CONFIRM_BUTTON
    )

    # ==================================================
    # QUICK NOTES
    # ==================================================

    global QUICK_NOTES_TITLE
    global QUICK_NOTES_LABEL
    global QUICK_NOTES_INPUT

    global QUICK_NOTES_CANCEL_BUTTON
    global QUICK_NOTES_SAVE_BUTTON

    QUICK_NOTES_TITLE = (
        _current_theme.QUICK_NOTES_TITLE
    )
    QUICK_NOTES_LABEL = (
        _current_theme.QUICK_NOTES_LABEL
    )
    QUICK_NOTES_INPUT = (
        _current_theme.QUICK_NOTES_INPUT
    )

    QUICK_NOTES_CANCEL_BUTTON = (
        _current_theme.QUICK_NOTES_CANCEL_BUTTON
    )
    QUICK_NOTES_SAVE_BUTTON = (
        _current_theme.QUICK_NOTES_SAVE_BUTTON
    )

    # ==================================================
    # TRANSITION
    # ==================================================

    global TRANSITION_TEXT

    TRANSITION_TEXT = (
        _current_theme.TRANSITION_TEXT
    )