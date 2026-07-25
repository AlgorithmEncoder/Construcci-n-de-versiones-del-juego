"""
Render state.

Contains everything required to draw a frame.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.overlay import Overlay


@dataclass(slots=True)
class RenderState:

    background: str | None = None

    objects: tuple = field(default_factory=tuple)

    npcs: tuple = field(default_factory=tuple)

    overlay: Overlay | None = None

    clock: str = ""

    @property
    def has_overlay(self):

        return self.overlay is not None