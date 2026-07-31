from pathlib import Path

from constants import MEMORIES_DIR


class PathManager:

    _memory = None

    @classmethod
    def set_memory(cls, memory: str):

        cls._memory = memory

    @classmethod
    def assets(cls) -> Path:

        return MEMORIES_DIR / cls._memory / "assets"

    @classmethod
    def rooms(cls):

        return cls.assets() / "rooms"

    @classmethod
    def npcs(cls):

        return cls.assets() / "npcs"

    @classmethod
    def ui(cls):

        return cls.assets() / "ui"

    @classmethod
    def documents(cls):

        return cls.assets() / "documents"
    
    @classmethod
    def json_folder(cls):
        
        return MEMORIES_DIR / cls._memory