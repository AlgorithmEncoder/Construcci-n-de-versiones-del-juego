"""
stats_manager.py

Manages persistent statistics for the current memory.
"""

from __future__ import annotations

import json

from datetime import datetime
from pathlib import Path

from constants import MEMORIES_DIR


class StatsManager:
    """
    Manages persistent statistics of the current memory.

    The manager keeps statistics in memory during the game and
    writes them to stats.json when requested.
    """

    def __init__(self, memory: str):

        self._memory = memory

        self._path = (
            MEMORIES_DIR /
            memory /
            "stats.json"
        )

        self._stats = {}

        self._load()

    # ==================================================
    # Loading
    # ==================================================

    def _load(self):

        if not self._path.exists():

            self._stats = self._default_stats()

            return

        with open(
            self._path,
            encoding="utf-8"
        ) as file:

            self._stats = json.load(file)

        self._ensure_structure()

    # --------------------------------------------------

    def _default_stats(self):

        return {

            "played": {
                "iterations": 0,
                "times_incursion": 0,
                "total_played": 0,
                "last_played": None,
            },

            "progress": {
                "discovered": 0,
                "total": 0,
                "percent": 0,
            },

            "discoveries": {},

            "exploration": {
                "rooms_visited": 0,
                "opened": 0,
                "read": 0,
                "talked": 0,
            },

            "detection": {
                "total": 0,
            },

            "state": {
                "completed": False,
                "locked": False,
            },
        }

    # --------------------------------------------------

    def _ensure_structure(self):

        default = self._default_stats()

        for section, values in default.items():

            if section not in self._stats:

                self._stats[section] = values

                continue

            if isinstance(values, dict):

                for key, value in values.items():

                    if key not in self._stats[section]:

                        self._stats[section][key] = value

    # ==================================================
    # Properties
    # ==================================================

    @property
    def stats(self) -> dict:

        return self._stats
    
    # ==================================================
    # Played
    # ==================================================

    def register_incursion(self):

        self._stats["played"]["times_incursion"] += 1

        self._stats["played"]["last_played"] = (
            datetime.now().isoformat()
        )
    

    # ==================================================
    # Incursion
    # ==================================================

    def register_incursion(self):

        self._stats["played"]["times_incursion"] += 1

        self._stats["played"]["last_played"] = (
            datetime.now().isoformat()
        )

    # ==================================================
    # Exploration
    # ==================================================

    def register_room_visit(self):
        self._stats["exploration"]["rooms_visited"] += 1

    # --------------------------------------------------

    def register_document_opened(self):
        self._stats["exploration"]["documents_opened"] += 1

    # --------------------------------------------------

    def register_computer_opened(self):
        self._stats["exploration"]["computers_opened"] += 1

    # --------------------------------------------------

    def register_email_read(self):
        self._stats["exploration"]["emails_read"] += 1

    # --------------------------------------------------

    def register_chat_read(self):
        self._stats["exploration"]["chats_read"] += 1

    # --------------------------------------------------

    def register_file_opened(self):
        self._stats["exploration"]["files_opened"] += 1

    # --------------------------------------------------

    def register_npc_talked_to(self):
        self._stats["exploration"]["npcs_talked_to"] += 1

    # ==================================================
    # Detection
    # ==================================================
    
    def add_detection(self, reason):
        
        if reason not in self._stats["detection"]:
            return

        self._stats["detection"][reason] += 1
        
        self._stats["detection"]["total"] += 1        

    # ==================================================
    # Discoveries
    # ==================================================
    
    def ensure_discoveries(
        self,
        documents: dict,
        computers: dict
    ):
        discoveries = self._stats.setdefault(
            "discoveries",
            {}
        )

        # --------------------------------------------------
        # Documents
        # --------------------------------------------------

        for document_id in documents:

            discoveries.setdefault(
                document_id,
                0
            )

        # --------------------------------------------------
        # Computers
        # --------------------------------------------------

        for computer_id, computer in computers.items():

            discoveries.setdefault(
                computer_id,
                0
            )

            # ------------------------------
            # Emails
            # ------------------------------

            for email in computer.get(
                "emails",
                []
            ):

                discoveries.setdefault(
                    email["id"],
                    0
                )

            # ------------------------------
            # Chats
            # ------------------------------

            for chat in computer.get(
                "chats",
                []
            ):

                discoveries.setdefault(
                    chat["id"],
                    0
                )

            # ------------------------------
            # Files
            # ------------------------------

            for file in computer.get(
                "files",
                []
            ):

                discoveries.setdefault(
                    file["document_id"],
                    0
                )

    def register_discovery(
        self,
        discovery_id: str
    ):

        discoveries = self._stats.setdefault(
            "discoveries",
            {}
        )

        discoveries[discovery_id] = (
            discoveries.get(discovery_id, 0) + 1
        )

    # ==================================================
    # Save
    # ==================================================

    def save_stats(self, story_data: dict):

        # ----------------------------------------------
        # Iterations
        # ----------------------------------------------

        self._stats["played"]["iterations"] += (
            story_data.get(
                "iterations",
                0
            )
        )

        # ----------------------------------------------
        # Progress
        # ----------------------------------------------

        progress = story_data.get(
            "progress",
            {}
        )

        total = len(progress)

        discovered = sum(
            1
            for value in progress.values()
            if value
        )

        percent = (
            round(
                discovered / total * 100
            )
            if total
            else 0
        )

        self._stats["progress"] = {

            "discovered": discovered,
            "total": total,
            "percent": percent,
        }

        # ----------------------------------------------
        # State
        # ----------------------------------------------

        self._stats["state"]["completed"] = (
            story_data.get(
                "finished",
                False
            )
        )

        # ----------------------------------------------
        # Save
        # ----------------------------------------------

        self.save()

    # --------------------------------------------------

    def save(self):

        self._path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self._path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self._stats,
                file,
                indent=4,
                ensure_ascii=False
            )