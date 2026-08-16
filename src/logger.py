"""
Activity logger.

Stores persistent global activity generated throughout the game.

The logger stores activity identifiers and parameters rather than
presentation text. Text is resolved by the ActivityView through the
language system.

Entries remain in memory during execution and are only written to disk
when save() is explicitly called.
"""

from __future__ import annotations

import json
import os

from datetime import datetime

from constants import GLOBAL_DIR


# ============================================================
# Paths
# ============================================================

ACTIVITY_FILE = GLOBAL_DIR / "activity.json"


class Logger:

    """
    Activity logger.

    Stores persistent global activity entries.

    The logger is responsible only for recording and persisting
    activity. It does not handle presentation or translation.
    """

    def __init__(self):

        self._entries: list[dict] = []

    # ========================================================
    # Public API
    # ========================================================

    def load(self) -> list[dict]:
        """
        Load the activity log from disk.

        Invalid or missing data results in an empty in-memory log.
        """

        self._entries = []

        if not ACTIVITY_FILE.exists():

            return self._entries

        try:

            with ACTIVITY_FILE.open(
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

        except (
            OSError,
            json.JSONDecodeError
        ):

            return self._entries

        if not isinstance(data, list):

            return self._entries

        self._entries = [

            entry

            for entry in data

            if isinstance(entry, dict)

        ]

        return self._entries

    # --------------------------------------------------------

    def register(
        self,
        message_key: str,
        *,
        category: str = "general",
        **parameters
    ) -> dict:
        """
        Register an activity entry in memory.

        Parameters
        ----------
        message_key:
            Identifier used to obtain the activity text from the
            language data.

        category:
            Activity category.

        **parameters:
            Values used when formatting the translated activity text.

        Returns
        -------
        dict
            The newly created activity entry.

        Notes
        -----
        The entry is not written to disk until save() is called.
        """

        entry = {

            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),

            "category": str(category),

            "message_key": str(message_key),

            "parameters": parameters,

        }

        self._entries.append(
            entry
        )

        return entry

    # --------------------------------------------------------

    def register_legacy(
        self,
        message: str,
        *,
        category: str = "general"
    ) -> dict:
        """
        Register a legacy activity containing presentation text.

        This method exists temporarily so old activity registrations
        can coexist while the project is migrated to message keys.

        New code should use register().
        """

        entry = {

            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),

            "category": str(category),

            "message": str(message),

        }

        self._entries.append(
            entry
        )

        return entry

    # ========================================================
    # Persistence
    # ========================================================

    def save(self) -> bool:
        """
        Save the current activity log to disk.

        The file is written through a temporary file and then
        replaced atomically when possible.
        """

        try:

            GLOBAL_DIR.mkdir(
                parents=True,
                exist_ok=True
            )

            temporary_file = ACTIVITY_FILE.with_suffix(
                ".tmp"
            )

            with temporary_file.open(
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self._entries,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

                file.write("\n")

            os.replace(
                temporary_file,
                ACTIVITY_FILE
            )

            return True

        except OSError:

            return False

    # ========================================================
    # Properties
    # ========================================================

    @property
    def entries(self) -> list[dict]:

        return self._entries

    # --------------------------------------------------------

    @property
    def count(self) -> int:

        return len(
            self._entries
        )

    # ========================================================
    # Utility
    # ========================================================

    def clear(self):
        """
        Clear the activity currently held in memory.

        This does not modify the file on disk until save() is called.
        """

        self._entries.clear()