"""
Global constants for the game engine.

This file should ONLY contain constants.
No game logic should be implemented here.
"""

from pathlib import Path

# ==========================================================
# PROJECT PATHS
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR = ROOT_DIR / "data"

MEMORIES_DIR = DATA_DIR / "memories"

ROOMS_ASSETS_DIR = ASSETS_DIR / "rooms"
UI_ASSETS_DIR = ASSETS_DIR / "ui"
NPC_ASSETS_DIR = ASSETS_DIR / "npcs"

# ==========================================================
# WINDOW
# ==========================================================

WINDOW_TITLE = "Mind Investigation"

SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 1024

HUD_TOP_MARGIN = 170
CLOCK_ALPHA = 170

FPS = 60

NPC_SCALE = 0.40

# ==========================================================
# COLORS
# ==========================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

LIGHT_GREY = (200, 200, 200)
GREY = (120, 120, 120)
DARK_GREY = (40, 40, 40)

RED = (220, 50, 50)
GREEN = (50, 180, 50)
BLUE = (70, 130, 255)

# ==========================================================
# FONTS
# ==========================================================

DEFAULT_FONT = None          # pygame default font
DEFAULT_FONT_SIZE = 24

TITLE_FONT_SIZE = 40

SMALL_FONT_SIZE = 18

# ==========================================================
# GAME
# ==========================================================

DEFAULT_MEMORY = "memory_01"

# ==========================================================
# DEBUG
# ==========================================================

DEBUG_MODE = True

SHOW_FPS = False

SHOW_CLICK_AREAS = False