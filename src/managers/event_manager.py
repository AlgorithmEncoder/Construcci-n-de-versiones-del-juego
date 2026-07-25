"""
event_manager.py

Handles every timed event of the current memory.
"""

from __future__ import annotations

from core.event import Event


class EventManager:
    """
    Executes events when their trigger time is reached.
    """

    def __init__(self, events_data: list[dict]):

        self._events: list[Event] = []

        self._handlers = {}

        self._build(events_data)

    # ==================================================
    # Construction
    # ==================================================

    def _build(self, events_data):
        
        from core.time_utils import time_to_seconds

        self._events.clear()

        for data in events_data:

            event = Event(

                trigger_time=time_to_seconds(data["time"]),

                action=data["action"],

                data={
                    k: v
                    for k, v in data.items()
                    if k not in ("time", "action")
                }
            )

            self._events.append(event)

        self._events.sort(
            key=lambda e: e.trigger_time
        )

    # ==================================================
    # Handlers
    # ==================================================

    def register_handler(
        self,
        action: str,
        handler
    ):

        self._handlers[action] = handler

    # ==================================================
    # Update
    # ==================================================

    def update(self, clock):

        for event in self._events:

            if not event.should_trigger(clock.total_seconds):
                continue

            handler = self._handlers.get(
                event.action
            )

            if handler:

                handler(event.data)

            event.mark_executed()

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        for event in self._events:

            event.reset()
