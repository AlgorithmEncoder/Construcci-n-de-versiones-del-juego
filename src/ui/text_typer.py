"""
text_typer.py

Progressively reveals text (typewriter effect).
"""

from __future__ import annotations

from constants import (
    DIALOGUE_TYPING_SPEED,
    DIALOGUE_FAST_MULTIPLIER,
    DIALOGUE_PERIOD_DELAY,
    DIALOGUE_COMMA_DELAY,
    DIALOGUE_ELLIPSIS_DELAY,
    DIALOGUE_ENABLE_TYPING,
)


class TextTyper:

    def __init__(self):

        self._text = ""
        self._visible = ""

        self._index = 0

        self._timer = 0.0
        self._pause = 0.0

        self._finished = True
        self._dialogue_settings = None

    # ==================================================
    # Public API
    # ==================================================

    def set_text(self, text: str):

        self._text = text or ""

        self._visible = ""

        self._index = 0

        self._timer = 0.0
        self._pause = 0.0

        self._finished = len(self._text) == 0

        dialogue_typing = (
            self._dialogue_settings.get(
                "dialogue_typing",
                DIALOGUE_ENABLE_TYPING
            )
            if self._dialogue_settings
            else DIALOGUE_ENABLE_TYPING
        )

        if not dialogue_typing:

            self.show_all()

    # --------------------------------------------------

    def update(
        self,
        delta_time: float,
        fast: bool = False,
    ):

        if self._finished:
            return

        if self._pause > 0:

            self._pause -= delta_time

            return

        dialogue_speed = (
            self._dialogue_settings.get(
                "dialogue_typing_speed",
                DIALOGUE_TYPING_SPEED
            )
            if self._dialogue_settings
            else DIALOGUE_TYPING_SPEED
        )

        speed = dialogue_speed

        if fast:
            speed *= DIALOGUE_FAST_MULTIPLIER

        self._timer += delta_time

        seconds_per_char = 1.0 / speed

        while (
            self._timer >= seconds_per_char
            and not self._finished
        ):

            self._timer -= seconds_per_char

            self._append_character()

    # --------------------------------------------------

    def show_all(self):

        self._visible = self._text

        self._index = len(self._text)

        self._finished = True

    # ==================================================
    # Internal
    # ==================================================

    def _append_character(self):

        if self._index >= len(self._text):

            self._finished = True

            return

        ch = self._text[self._index]

        self._visible += ch

        self._index += 1

        self._apply_pause(ch)

        if self._index >= len(self._text):

            self._finished = True

    # --------------------------------------------------

    def _apply_pause(
        self,
        character: str,
    ):

        if character == ",":

            self._pause = DIALOGUE_COMMA_DELAY

            return

        if character in ".!?":

            self._pause = DIALOGUE_PERIOD_DELAY

            return

        if (
            len(self._visible) >= 3
            and self._visible.endswith("...")
        ):

            self._pause = DIALOGUE_ELLIPSIS_DELAY

    # ==================================================
    # Properties
    # ==================================================

    @property
    def visible_text(self):

        return self._visible

    @property
    def finished(self):

        return self._finished