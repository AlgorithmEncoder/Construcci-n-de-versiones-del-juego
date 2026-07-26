"""
Represents a text note.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Note:

    name: str

    text: str = ""

    # --------------------------------------------------

    @property
    def filename(self):

        return f"{self.name}.txt"