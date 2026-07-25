"""
npc_manager.py

Creates, updates and manages every NPC in the current memory.
"""

from __future__ import annotations

from ui.assets import Assets
from world.npc import NPC
import random


class NPCManager:
    """
    Manages every NPC of the loaded memory.
    """

    def __init__(self, npcs_data: dict):

        self._npcs: dict[str, NPC] = {}

        self._build(npcs_data)

    # ==================================================
    # Construction
    # ==================================================

    def _build(self, npcs_data: dict):
        
        from core.time_utils import time_to_seconds

        self._npcs.clear()

        for npc_id, data in npcs_data.items():

            schedule = []

            for entry in data.get("schedule", []):

                schedule.append(
                    (
                        time_to_seconds(entry["time"]),
                        entry["room"]
                    )
                )

            npc = NPC(

                npc_id=npc_id,

                name=data["name"],

                sprite=data["sprite"],

                dialogue=data["dialogue"],

                schedule=schedule,
                
                positions=data.get("positions", {})
            )

            self._npcs[npc_id] = npc

    # ==================================================
    # Update
    # ==================================================

    def update(self, clock):

        for npc in self._npcs.values():

            npc.update(clock.total_seconds)

    # ==================================================
    # Queries
    # ==================================================

    def visible_npcs(self, room_id: str):

        return tuple(

            npc

            for npc in self._npcs.values()

            if npc.is_in_room(room_id)

        )

    # --------------------------------------------------

    def get(self, npc_id: str):

        return self._npcs[npc_id]

    # --------------------------------------------------

    def exists(self, npc_id: str):

        return npc_id in self._npcs
    
    def find_at(self, room_id, position):

        for npc in reversed(tuple(self._npcs.values())):

            if npc.current_room != room_id:
                continue

            sprite = Assets.get_sprite(npc.sprite)

            mask = Assets.get_mask(npc.sprite)

            rect = sprite.get_rect()
            rect.midtop = npc.position

            if not rect.collidepoint(position):
                continue

            local = (
                position[0] - rect.x,
                position[1] - rect.y
            )

            if mask.get_at(local):

                return npc

        return None
    
    def get_dialogue(
        self,
        npc_id: str,
        current_time: int,
        dialogues: dict
    ):

        npc = self.get(npc_id)

        entries = dialogues.get(
            npc.dialogue_id,
            []
        )

        for entry in entries:

            if (
                entry["from"] <= current_time
                <
                entry["to"]
            ):

                lines = entry["lines"]

                if not lines:
                    return ""

                return {"text": random.choice(lines)}

        return ""

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        for npc in self._npcs.values():

            npc.reset()
