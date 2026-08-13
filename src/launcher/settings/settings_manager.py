"""
Settings manager.

Loads, manages and saves global application settings.

The manager is responsible only for configuration data.
It does not apply settings to the launcher or the game.
"""

from __future__ import annotations

import json

from pathlib import Path

from constants import GLOBAL_DIR


class SettingsManager:

    """
    Provides access to persistent global settings.
    """

    def __init__(self):

        self._path = (
            GLOBAL_DIR
            / "settings.json"
        )

        self._settings: dict = {}

        self.load()

    # ==================================================
    # Loading
    # ==================================================

    def load(self):

        """
        Loads settings from the persistent JSON file.

        If the file does not exist, is empty or cannot
        be decoded, default settings are generated.
        """

        self._settings = {}

        if not self._path.exists():

            self.generate_default()

            return

        try:

            with self._path.open(
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

        except (
            OSError,
            json.JSONDecodeError
        ):

            self.generate_default()

            return

        if not isinstance(data, dict) or not data:

            self.generate_default()

            return

        self._settings = data

    # ==================================================
    # Default settings
    # ==================================================

    def generate_default(self):

        """
        Generates the default settings configuration.
        """

        self._settings = {

            "general": {
                "auto_save": True,
                "confirm_exit": True,
            },

            "display": {
                "resolution": [
                    1536,
                    1024,
                ],
                "fullscreen": False,
                "vsync": True,
                "scale_ui": 1.0,
                "launcher_theme": "default",
                "game_theme": "default",
                "computer_theme": "default"
            },

            "audio": {
                "master_volume": 1.0,
                "music_volume": 1.0,
                "effects_volume": 1.0,
                "dialogue_volume": 1.0,
                "music_enabled": True,
                "effects_enabled": True,
                "dialogue_enabled": True,
            },

            "language": {
                "launcher_interface": "es",
                "game_interface": "es",
                "documents": "es",
                "story": "es",
                "dialogues": "es",
                "computer_messages": "es",
                "computer_files": "es",
            },

            "accessibility": {
                "text_size": 1.0,
                "high_contrast": False,
                "reduce_motion": False,
                "dialogue_typing": True,
                "dialogue_typing_speed": 40,
            },
        }

    # ==================================================
    # Access
    # ==================================================

    def get(
        self,
        section: str
    ) -> dict:

        """
        Returns the configuration of a specific section.

        The returned dictionary is the current in-memory
        configuration for that section.
        """

        return self._settings.get(
            section,
            {}
        )

    # --------------------------------------------------

    @property
    def settings(self) -> dict:
        """
        Returns the complete settings dictionary.
        """

        return self._settings

    # ==================================================
    # Updating
    # ==================================================

    def save_settings(
        self,
        section: str,
        settings: dict
    ):

        """
        Replaces the configuration of a section.

        Parameters
        ----------
        section:
            Section identifier.

        settings:
            Updated configuration for that section.
        """

        self._settings[section] = settings

    # ==================================================
    # Persistence
    # ==================================================

    def save(self):

        """
        Saves the current settings to settings.json.
        """

        self._path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self._path.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self._settings,
                file,
                indent=4,
                ensure_ascii=False
            )