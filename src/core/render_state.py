"""
Render state.

Contains everything required to draw a frame.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RenderState:

    background: str | None = None

    objects: tuple = field(default_factory=tuple)

    npcs: tuple = field(default_factory=tuple)

    overlay = None

    clock: str = ""

    @property
    def has_overlay(self):

        return self.overlay is not None