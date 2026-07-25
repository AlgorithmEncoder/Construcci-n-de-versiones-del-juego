"""
ui.py

UI manager.
"""

from __future__ import annotations

from ui.overlay import Overlay


class UIManager:
    """
    Handles every modal window.

    Only one overlay can be open at a time.
    """

    def __init__(self):

        self._current_overlay: Overlay | None = None

    # ==================================================
    # Public API
    # ==================================================

    def open(
        self,
        overlay: Overlay
    ):

        self._current_overlay = overlay

    # --------------------------------------------------

    def close(self):

        if self._current_overlay is not None:
            self._current_overlay.close()

        self._current_overlay = None

    # --------------------------------------------------

    def toggle(
        self,
        overlay: Overlay
    ):

        if self.is_open:
            self.close()
        else:
            self.open(overlay)
    
    def handle_event(self, event):

        if self._current_overlay is None:
            return False

        handled = self._current_overlay.handle_event(event)

        if not self._current_overlay.visible:
            self.close()

        return handled
    
    def update(self, delta_time):

        if self.is_open:
            self._current_overlay.update(delta_time)

    # ==================================================
    # Properties
    # ==================================================

    @property
    def current_overlay(self):

        return self._current_overlay

    @property
    def is_open(self):

        return self._current_overlay is not None

    @property
    def blocks_input(self):

        if not self.is_open:
            return False

        return self._current_overlay.blocks_input