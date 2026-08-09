"""
Represents a text note.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Note:

    name: str

    text: str = ""

    parent: "Folder | None" = field(
        default=None,
        repr=False
    )

    id: str = field(
        default_factory=lambda: uuid4().hex
    )

    @property
    def filename(self):

        return f"{self.name}.txt"

    @property
    def path(self):

        parts = [self.name]

        current = self.parent

        while current:

            parts.append(current.name)

            current = current.parent

        return list(reversed(parts))