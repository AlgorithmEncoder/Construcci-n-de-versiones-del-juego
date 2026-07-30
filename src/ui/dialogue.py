"""
dialogue.py

Dialogue overlay.
"""

from __future__ import annotations

import pygame

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    DIALOGUE_CURSOR_BLINK,
)

from ui.overlay import Overlay
from ui.fonts import Fonts
from ui.text_renderer import draw_wrapped_text
from ui.text_typer import TextTyper


class DialogueUI(Overlay):

    def __init__(
        self,
        speaker: str,
        dialogue: list[dict],
        world_width: int,
        world_height: int,
        callback = None
    ):

        super().__init__(
            world_width=world_width,
            world_height=world_height,
            width=920,
            height=190,
        )

        self._panel.midbottom = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 30,
        )

        self._speaker = speaker

        self._dialogue = dialogue

        self._line = 0

        # Máquina de escribir
        self._typer = TextTyper()

        if self._dialogue:
            self._typer.set_text(
                self._dialogue[0]["text"]
            )

        # Cursor
        self._cursor_visible = True
        self._cursor_timer = 0.0
        
        self.callback = callback

    # ==================================================
    # Update
    # ==================================================

    def update(
        self,
        delta_time: float,
    ):

        keys = pygame.key.get_pressed()

        fast = keys[pygame.K_SPACE]

        self._typer.update(
            delta_time,
            fast=fast,
        )

        self._cursor_timer += delta_time

        if self._cursor_timer >= DIALOGUE_CURSOR_BLINK:

            self._cursor_timer = 0.0

            self._cursor_visible = (
                not self._cursor_visible
            )

    # ==================================================
    # Events
    # ==================================================

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.close()

                return True

            if event.key in (
                pygame.K_RETURN,
                pygame.K_SPACE,
            ):

                self._advance()

                return True

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            self._advance()

            return True

        return False

    # ==================================================
    # Internal
    # ==================================================

    def _advance(self):

        # Si todavía está escribiendo,
        # completar la línea actual.

        if not self._typer.finished:

            self._typer.show_all()

            return

        # Siguiente línea

        self._line += 1

        if self._line >= len(self._dialogue):

            self.close()
            
            if self.callback: self.callback()

            return

        self._typer.set_text(
            self._dialogue[self._line]["text"]
        )

    # ==================================================
    # Draw
    # ==================================================

    def _draw_content(
        self,
        screen: pygame.Surface,
    ):

        self._draw_speaker(screen)

        self._draw_text(screen)

        self._draw_continue(screen)

    # --------------------------------------------------

    def _draw_speaker(
        self,
        screen: pygame.Surface,
    ):

        title = Fonts.title.render(
            self._speaker,
            True,
            WHITE,
        )

        rect = title.get_rect()

        rect.topleft = (
            self.panel.left + 24,
            self.panel.top + 18,
        )

        screen.blit(
            title,
            rect,
        )

        y = rect.bottom + 10

        pygame.draw.line(
            screen,
            (170, 170, 170),
            (
                self.panel.left + 20,
                y,
            ),
            (
                self.panel.right - 20,
                y,
            ),
            2,
        )
    
        # --------------------------------------------------

    def _draw_text(
        self,
        screen: pygame.Surface,
    ):

        if self._line >= len(self._dialogue):
            return

        rect = pygame.Rect(

            self.panel.left + 24,

            self.panel.top + 62,

            self.panel.width - 48,

            self.panel.height - 90,
        )

        draw_wrapped_text(

            surface=screen,

            text=self._typer.visible_text,

            rect=rect,

            font=Fonts.default,

            color=WHITE,

            line_spacing=6,

            paragraph_spacing=10,

            preserve_newlines=True,
        )

    # --------------------------------------------------

    def _draw_continue(
        self,
        screen: pygame.Surface,
    ):

        #
        # Mientras se escribe el texto
        # no mostramos el indicador.
        #

        if not self._typer.finished:
            return

        #
        # Última línea:
        # mostramos una X para indicar
        # que el diálogo terminará.
        #

        if self._line >= len(self._dialogue) - 1:

            if not self._cursor_visible:
                return

            indicator = Fonts.default.render(

                "✕",

                True,

                WHITE,
            )

        else:

            if not self._cursor_visible:
                return

            indicator = Fonts.default.render(

                "▶",

                True,

                WHITE,
            )

        rect = indicator.get_rect()

        rect.bottomright = (

            self.panel.right - 22,

            self.panel.bottom - 18,
        )

        screen.blit(
            indicator,
            rect,
        )