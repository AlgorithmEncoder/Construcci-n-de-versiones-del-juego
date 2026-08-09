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

        self._launcher = MainWindow(screen, logger)

        self._game = None

    # ==================================================
    # Public API
    # ==================================================

    def update(self, dt):

        if self._game is None:

            self._launcher.update(dt)

            if self._launcher.start_requested:

                self._game = Game(
                    self._screen,
                    self._launcher.start_requested
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
    
    def _save_data(self):

        if self._game is None:
            return

        self._launcher.dreams.save_progress(
            self._game.save_data
        )