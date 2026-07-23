"""
Game clock.

Responsible only for keeping track of in-game time.
It knows nothing about events, NPCs or memories.
"""

from __future__ import annotations


class GameClock:

    def __init__(
        self,
        start_hour: int = 8,
        start_minute: int = 0,
        start_second: int = 0,
        time_scale: float = 1.0
    ):

        self._start_time = (
            start_hour * 3600
            + start_minute * 60
            + start_second
        )

        self._current_time = float(self._start_time)

        self._time_scale = time_scale

        self._paused = False

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    def update(self, dt: float) -> float:

        if not self._paused:
            self._current_time += dt * self._time_scale

        return self._current_time

    # --------------------------------------------------
    # Controls
    # --------------------------------------------------

    def reset(self):

        self._current_time = float(self._start_time)

    def pause(self):

        self._paused = True

    def resume(self):

        self._paused = False

    def toggle_pause(self):

        self._paused = not self._paused

    # --------------------------------------------------
    # Time Scale
    # --------------------------------------------------

    def set_time_scale(self, scale: float):

        self._time_scale = max(0.0, scale)

    @property
    def time_scale(self):

        return self._time_scale

    # --------------------------------------------------
    # Time
    # --------------------------------------------------
    
    def has_reached(self, seconds: float) -> bool:
        return self.elapsed_seconds >= seconds
    
    @property
    def current_time(self):
        return self._current_time

    @property
    def start_time(self):
        return self._start_time

    @property
    def total_seconds(self):

        return self._current_time

    @property
    def hours(self):

        return int(self._current_time // 3600)

    @property
    def minutes(self):

        return int((self._current_time % 3600) // 60)

    @property
    def seconds(self):

        return int(self._current_time % 60)

    @property
    def time_string(self):

        return f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}"
    
    @property
    def elapsed_seconds(self):

        return self._current_time - self._start_time