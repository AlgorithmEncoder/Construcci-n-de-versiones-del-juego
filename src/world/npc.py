"""
npc.py

Represents a non-player character.

NPCs contain only state.
All behaviour is handled by NPCManager.
"""

from __future__ import annotations

from bisect import bisect_right

from core.interaction import GameAction


class NPC:
    """
    Represents one NPC instance.
    """

    def __init__(
        self,
        npc_id: str,
        name: str,
        sprite: str,
        dialogue: str,
        schedule: list[tuple[int, str]],
        positions: dict[str, tuple[int, int]],
        alert=False
    ):

        self.id = npc_id

        self.name = name

        self.sprite = sprite

        self.dialogue_id = dialogue

        # Sorted list of (time, room)
        self.schedule = sorted(schedule)
        
        self.positions = {
            room: tuple(pos)
            for room, pos in positions.items()
        }

        self.current_room = (
            self.schedule[0][1]
            if self.schedule
            else None
        )
        
        self.alert = alert
    
    @property
    def position(self) -> tuple[int, int]:
        """
        Returns the drawing position for the current room.
        """

        return self.positions.get(
            self.current_room,
            (0, 0)
        )

    # ==================================================
    # Public API
    # ==================================================

    def update(
        self,
        current_time: int
    ):
        """
        Updates the NPC room according to its schedule.
        """

        if not self.schedule:
            return
        
        if self.current_room is "__hidden__":
            return

        index = bisect_right(
            self.schedule,
            (current_time, "\uffff")
        ) - 1

        if index >= 0:
            self.current_room = (
                self.schedule[index][1]
            )

    # --------------------------------------------------

    def reset(self):
        """
        Restores the NPC to its initial room.
        """

        if self.schedule:
            self.current_room = (
                self.schedule[0][1]
            )

    # --------------------------------------------------

    def is_in_room(
        self,
        room_id: str
    ) -> bool:
        """
        Returns True if the NPC is currently
        inside the given room.
        """

        return self.current_room == room_id
    
    def activate(self):

        return GameAction(
            action="open_dialogue",
            target=self.id
        )