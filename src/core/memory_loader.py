"""
Memory loader.

Responsible for loading a complete memory from disk.

It only reads JSON files and returns Python dictionaries.
"""

from pathlib import Path
import json

from constants import MEMORIES_DIR


class MemoryLoader:

    def __init__(self, memory_name: str):

        self.memory_path = MEMORIES_DIR / memory_name
        self.story = self._load_story()

    # --------------------------------------------------

    def load(self):

        return {

            "story": self._load_story(),

            "rooms": self._load_rooms(),

            "npcs": self._load_npcs(),

            "computers": self._load_computers(),

            "events": self._load_events(),

            "metadata": self._load_metadata(),

            "diaglogues": self._load_diaglogues(),

            "documents": self._load_documents(),

            "objects": self._load_objects()
        }

    # --------------------------------------------------

    def _load_story(self):

        return self._load_json("story.json")

    def _load_rooms(self):

        return self._load_json("rooms.json")

    def _load_npcs(self):

        return self._load_json("npcs.json")

    def _load_computers(self):

        return self._load_json("computers.json")

    def _load_events(self):

        return self._load_json("events.json")

    # --------------------------------------------------

    def _load_json(self, filename: str):

        filepath = self.memory_path / filename

        with open(filepath, "r", encoding="utf-8") as file:

            return json.load(file)