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

        self.metadata = {}
        self.story = {}

        self.rooms = {}
        self.objects = {}

        self.documents = {}
        self.computers = {}

        self.npcs = {}
        self.dialogues = {}

        self.events = []

    # --------------------------------------------------

    def load(self):

        self.metadata = self._load_metadata()

        self.story = self._load_story()

        self.rooms = self._load_rooms()
        self.objects = self._load_objects()

        self.documents = self._load_documents()
        self.computers = self._load_computers()

        self.npcs = self._load_npcs()
        self.dialogues = self._load_dialogues()

        self.events = self._load_events()

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
    
    def _load_metadata(self):
    
        return self._load_json("metadata.json")
    
    def _load_dialogues(self):

        return self._load_json("dialogues.json")
    
    def _load_documents(self):

        return self._load_json("documents.json")
    
    def _load_objects(self):

        return self._load_json("objects.json")

    # --------------------------------------------------

    def _load_json(self, filename: str):

        filepath = self.memory_path / filename

        with open(filepath, "r", encoding="utf-8") as file:

            return json.load(file)