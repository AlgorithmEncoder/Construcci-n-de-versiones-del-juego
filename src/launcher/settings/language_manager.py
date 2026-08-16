"""
Language manager.

Loads and provides access to global application language data.

The manager is responsible only for loading and retrieving
language data. It does not modify settings or apply translations
to the launcher or the game.
"""

from __future__ import annotations

import json

from constants import GLOBAL_DIR


class LanguageManager:

    """
    Provides access to persistent global language data.
    """

    def __init__(
        self,
        settings_manager
    ):

        self._settings_manager = settings_manager

        self._path = (
            GLOBAL_DIR
            / "language.json"
        )

        self._language: dict = {}

        self.load()

    # ==================================================
    # Loading
    # ==================================================

    def load(self):

        """
        Loads the global language data.

        If the file does not exist, cannot be read or does
        not contain a valid dictionary, the language data
        is initialized as empty.
        """

        self._language = {}

        if not self._path.exists():
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

            return

        if not isinstance(
            data,
            dict
        ):

            return

        self._language = data

    # ==================================================
    # Access
    # ==================================================

    @property
    def language(self) -> dict:

        """
        Returns the complete loaded language data.
        """

        return self._language

    # --------------------------------------------------

    def get(
        self,
        section: str,
        *keys: str,
        default: str = ""
    ) -> str:

        """
        Returns a translated text from a language section.

        The selected language is obtained automatically from
        SettingsManager according to the requested section.

        Examples
        --------
        get("launcher", "settings", "title")

        get("game", "hud", "inventory")

        The method returns the provided default value when
        the requested text cannot be found.
        """

        language = self._get_language_for_section(
            section
        )

        data = self._language.get(
            section,
            {}
        )

        if not isinstance(
            data,
            dict
        ):

            return default

        data = data.get(
            language,
            {}
        )

        if not isinstance(
            data,
            dict
        ):

            return default

        for key in keys:

            if not isinstance(
                data,
                dict
            ):

                return default

            data = data.get(
                key
            )

        if isinstance(
            data,
            str
        ):

            return data

        return default

    # ==================================================
    # Available languages
    # ==================================================

    def get_available_languages(
        self,
        section: str
    ) -> dict:

        """
        Returns the languages available for a specific
        language block.

        Example:

        get_available_languages(
            "launcher_interface"
        )
        """

        available = self._language.get(
            "available_languages",
            {}
        )

        if not isinstance(
            available,
            dict
        ):

            return {}

        languages = available.get(
            section,
            {}
        )

        if not isinstance(
            languages,
            dict
        ):

            return {}

        return languages

    # --------------------------------------------------

    def is_language_available(
        self,
        section: str,
        language: str
    ) -> bool:

        """
        Returns whether a language is available for
        a specific language block.
        """

        return language in (
            self.get_available_languages(
                section
            )
        )

    # ==================================================
    # Language selection
    # ==================================================

    def get_selected_language(
        self,
        section: str
    ) -> str:

        """
        Returns the language selected in SettingsManager
        for the requested language block.

        The section corresponds to one of the language
        settings:

            launcher_interface
            game_interface
            documents
            story
            dialogues
            computer_messages
            computer_files
        """

        settings = self._settings_manager.get(
            "language"
        )

        if not isinstance(
            settings,
            dict
        ):

            return "es"

        return settings.get(
            section,
            "es"
        )

    # ==================================================
    # Internal helpers
    # ==================================================

    def _get_language_for_section(
        self,
        section: str
    ) -> str:

        """
        Resolves the SettingsManager language key
        associated with a language data section.
        """

        if section == "launcher":
            setting = "launcher_interface"

        elif section == "game":
            setting = "game_interface"

        else:
            setting = section

        return self.get_selected_language(
            setting
        )