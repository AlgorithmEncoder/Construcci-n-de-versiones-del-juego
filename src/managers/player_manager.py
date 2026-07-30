"""
player_manager.py

Stores the player's state.

For now it only tracks the current room, but this manager
will later contain inventory, discovered clues, status,
flags and other persistent player data.
"""

from __future__ import annotations


class PlayerManager:
    """
    Stores the player's current state.
    """

    def __init__(self, initial_room: str):

        self._initial_room = initial_room
        self._current_room = initial_room
        self.computer_warnings = 0

    # ==================================================
    # Properties
    # ==================================================

    @property
    def current_room(self) -> str:
        """Current room where the player is located."""

        return self._current_room

    # ==================================================
    # Public API
    # ==================================================

    def change_room(self, room_id: str):
        """Moves the player to another room."""

        self._current_room = room_id

    # --------------------------------------------------
    
    def add_computer_warning(self):
        self.computer_warnings += 1
        return self.computer_warnings
    
    def reset_warnings(self):
        self.computer_warnings = 0
    
    # --------------------------------------------------

    def reset(self):
        """Restores the initial player state."""

        self._current_room = self._initial_room
        self.reset_warnings()