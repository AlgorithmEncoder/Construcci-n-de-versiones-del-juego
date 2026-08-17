from pathlib import Path

from constants import MEMORIES_DIR


class PathManager:

    _memory = None
    _lang = {}

    # ==================================================
    # Context
    # ==================================================

    @classmethod
    def set_memory(cls, memory: str):

        cls._memory = memory

    @classmethod
    def set_language(cls, language_dict: str):

        cls._lang = language_dict

    # ==================================================
    # Shared assets
    # ==================================================

    @classmethod
    def assets(cls) -> Path:

        return (
            MEMORIES_DIR
            / cls._memory
            / "assets"
        )

    @classmethod
    def rooms(cls) -> Path:

        return cls.assets() / "rooms"

    @classmethod
    def npcs(cls) -> Path:

        return cls.assets() / "npcs"

    @classmethod
    def ui(cls) -> Path:

        return cls.assets() / "ui"

    # ==================================================
    # Language-dependent assets
    # ==================================================

    @classmethod
    def documents(cls) -> Path:

        return (
            MEMORIES_DIR
            / cls._memory
            / "locales"
            / cls._lang.get("computer_files")
            / "documents"
        )
    
    @classmethod
    def story_path(cls, memory=None) -> Path:
        
        if memory:
            return (
                MEMORIES_DIR
                / memory
                / "locales"
                / cls._lang.get("story", "es")
                / "story.json"
            )
        else:
            return (
                MEMORIES_DIR
                / cls._memory
                / "locales"
                / cls._lang.get("story", "es")
                / "story.json"
            )

    # ==================================================
    # JSON
    # ==================================================

    @classmethod
    def json_folder(cls) -> Path:

        return (
            MEMORIES_DIR
            / cls._memory
        )