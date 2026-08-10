from pathlib import Path

from constants import MEMORIES_DIR


class PathManager:

    _memory = None
    _lang = None

    # ==================================================
    # Context
    # ==================================================

    @classmethod
    def set_memory(cls, memory: str):

        cls._memory = memory

    @classmethod
    def set_language(cls, language: str):

        cls._lang = language

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
            / cls._lang
            / "documents"
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

    @classmethod
    def local_json_folder(cls) -> Path:

        return (
            MEMORIES_DIR
            / cls._memory
            / "locales"
            / cls._lang
        )