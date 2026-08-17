"""
Global constants for the game engine.

This file should ONLY contain constants.
No game logic should be implemented here.
"""

from pathlib import Path
import sys

GAME_VERSION = "v.1.5.4"
AUTHOR_NAME = "Ferran Clausell Sánchez"

# ==========================================================
# PROJECT PATHS
# ==========================================================

if getattr(sys, "frozen", False):
    ROOT_DIR = Path(sys.executable).parent / "_internal"
else:
    ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

MEMORIES_DIR = DATA_DIR / "memories"

ASSETS_DIR = ROOT_DIR / "assets"

GLOBAL_DIR = DATA_DIR / "global"

# ==========================================================
# WINDOW
# ==========================================================

WINDOW_TITLE = "DreamWalker"

SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 1024

HUD_TOP_MARGIN = 50
HUD_LEFT_MARGIN = 200
CLOCK_ALPHA = 170

FPS = 60

NPC_SCALE = 0.40

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

# ==========================================================
# TIME - seconds
# ==========================================================

ROOM_CHANGE_TIME = 1.0

DOCUMENT_OPEN_TIME = 0.5

COMPUTER_BOOT_TIME = 2.0

RESET_TIME = 3.0

OBJECTIVE_DURATION = 3.0

# ==================================================
# Dialogue typing
# ==================================================

DIALOGUE_TYPING_SPEED = 40          # caracteres por segundo

DIALOGUE_FAST_MULTIPLIER = 3        # mantener Espacio

DIALOGUE_PERIOD_DELAY = 0.35        # .
DIALOGUE_COMMA_DELAY = 0.15         # ,
DIALOGUE_ELLIPSIS_DELAY = 0.45      # ...

DIALOGUE_CURSOR_BLINK = 0.45        # segundos

DIALOGUE_ENABLE_TYPING = True

DIALOGUE_AUTO_WRAP_NEWLINES = True
DIALOGUE_PLAY_TYPING_SOUND = False