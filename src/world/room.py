"""
Room manager.

Responsible for managing the current room.
It does not know anything about NPCs, events or the player.
"""

from __future__ import annotations


class RoomManager:

    def __init__(self, rooms_data: dict, initial_room: str):

        self._rooms = rooms_data
        self._current_room = initial_room

    # ==================================================
    # Internal
    # ==================================================

    @property
    def _current_data(self) -> dict:
        """Returns the data of the current room."""

        return self._rooms[self._current_room]

    def _get(self, key: str, default=None):
        """Safely retrieves a value from the current room."""

        return self._current_data.get(key, default)

    # ==================================================
    # Properties
    # ==================================================

    @property
    def current_room(self) -> str:
        """Returns the current room ID."""

        return self._current_room

    @property
    def name(self) -> str:
        """Returns the room display name."""

        return self._get("name")

    @property
    def background(self) -> str:
        """Returns the room background asset."""

        return self._get("background")

    @property
    def objects(self) -> tuple:
        """Returns the object IDs contained in this room."""

        return tuple(self._get("objects", []))

    @property
    def connections(self) -> tuple:
        """Returns the connected room IDs."""

        return tuple(self._get("connections", []))

    # ==================================================
    # Public API
    # ==================================================

    def change_room(self, room_id: str):

        if room_id not in self._rooms:
            raise ValueError(f"Room '{room_id}' does not exist.")

        self._current_room = room_id

    def room_exists(self, room_id: str) -> bool:
        """Checks whether a room exists."""

        return room_id in self._rooms

    def get_room(self, room_id: str) -> dict:
        """Returns the raw data of any room."""

        if not self.room_exists(room_id):
            raise ValueError(f"Room '{room_id}' does not exist.")

        return self._rooms[room_id]

    def reset(self, initial_room: str):
        """Resets the manager to the initial room."""

        if not self.room_exists(initial_room):
            raise ValueError(f"Room '{initial_room}' does not exist.")

        self._current_room = initial_room