"""
Main application controller.
"""

from __future__ import annotations

import pygame

from launcher.main_window import MainWindow
from core.game import Game


class Application:

    def __init__(self, screen, logger):

        self._screen = screen
        
        self._logger = logger

        self._launcher = MainWindow(screen, logger)

        self._game = None
        
        self._applied_resolution = (
            self._screen.get_width(),
            self._screen.get_height()
        )
        
        self._display_state = None

    # ==================================================
    # Public API
    # ==================================================

    def update(self, dt):
        
        self._apply_display_settings()

        if self._game is None:

            self._launcher.update(dt)

            if self._launcher.start_requested:

                self._game = Game(
                    self._screen,
                    self._launcher.start_requested,
                    self._logger,
                    self._launcher._settings
                )

                self._launcher.clear_requests()

        else:

            self._game.update(dt)

            if self._game.finished:
                
                self._save_data()

                self._game = None
                
                self._launcher.refresh()

    # --------------------------------------------------

    def draw(self):

        if self._game is None:

            self._launcher.draw()

        else:

            self._game.draw()

    # --------------------------------------------------

    def handle_event(self, event):

        if self._game is None:

            self._launcher.handle_event(event)

        else:

            self._game.handle_event(event)
    
    # --------------------------------------------------
    
    def _apply_display_settings(self):

        settings = self._launcher.display_settings

        resolution = settings.get(
            "resolution",
            [1536, 1024]
        )

        fullscreen = bool(
            settings.get(
                "fullscreen",
                False
            )
        )

        vsync = bool(
            settings.get(
                "vsync",
                True
            )
        )

        # --------------------------------------------------
        # Effective resolution
        # --------------------------------------------------

        if fullscreen:

            info = pygame.display.Info()

            width = info.current_w
            height = info.current_h

        else:

            width = int(resolution[0])
            height = int(resolution[1])

        # --------------------------------------------------
        # Check whether anything changed
        # --------------------------------------------------

        state = (
            width,
            height,
            fullscreen,
            vsync
        )

        if state == self._display_state:
            return

        # --------------------------------------------------
        # Window flags
        # --------------------------------------------------

        flags = pygame.RESIZABLE

        if fullscreen:
            flags |= pygame.FULLSCREEN

        # --------------------------------------------------
        # Recreate display
        # --------------------------------------------------

        self._screen = pygame.display.set_mode(
            (width, height),
            flags,
            vsync=1 if vsync else 0
        )

        # --------------------------------------------------
        # Propagate new Surface
        # --------------------------------------------------

        self._launcher.set_screen(
            self._screen
        )

        if self._game is not None:

            self._game.set_screen(
                self._screen
            )

        self._display_state = state
    
    # --------------------------------------------------
    
    def _save_data(self):
        
        current_view = self._launcher._workspace.current
        if hasattr(current_view, "save"):
            current_view.save()
        self._launcher._settings.save()

        if self._game is None:
            return
        
        self._logger.save()
        
        story_data = self._game.save_data

        self._launcher.dreams.save_progress(
            story_data
        )
        
        self._game.stats.save_stats(story_data)
        
        self._launcher._achievements.check_memory(
            self._game.stats._stats
        )

        self._launcher._achievements.check()