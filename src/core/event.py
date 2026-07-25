"""
event.py

Represents a scheduled event inside a memory.

Events are immutable once created.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Event:
    """
    Represents a single scheduled event.

    Attributes
    ----------
    trigger_time:
        Time (in seconds from 00:00) when the event must be fired.

    action:
        Action identifier.

    data:
        Additional parameters required by the action.

    executed:
        Internal flag used by EventManager.
    """

    trigger_time: int

    action: str

    data: dict[str, Any] = field(default_factory=dict)

    executed: bool = False

    # ==================================================
    # Public API
    # ==================================================

    def reset(self):
        """Marks the event as pending again."""

        self.executed = False

    # --------------------------------------------------

    def should_trigger(
        self,
        current_time: int
    ) -> bool:
        """
        Returns True if the event should be fired.
        """

        return (
            not self.executed
            and current_time >= self.trigger_time
        )

    # --------------------------------------------------

    def mark_executed(self):
        """Marks the event as already executed."""

        self.executed = True