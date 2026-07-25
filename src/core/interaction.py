"""
interaction.py

Represents an action to be executed by the game.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class GameAction:

    action: str
    target: str | None = None
    payload: Any = None