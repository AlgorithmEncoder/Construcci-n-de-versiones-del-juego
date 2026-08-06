"""
Quick notes window.
"""

from __future__ import annotations

import pygame

from ui.overlay import Overlay
from ui.fonts import Fonts

from launcher.widgets.text_editor import TextEditor

from quick_notes import create_quick_note


WHITE = (255, 255, 255)
TEXT = (30, 30, 30)
BORDER = (120, 120, 120)
BUTTON = (70, 110, 210)
BUTTON_CANCEL = (120, 120, 120)


class QuickNotes(Overlay):

    def __init__(
        self,
        world_width: int,
        world_height: int,
    ):

        super().__init__(
            world_width,
            world_height,
            width=760,
            height=640
        )

        self._title = TextEditor()

        self._text = TextEditor()

        self._title_rect = pygame.Rect(0, 0, 0, 0)

        self._text_rect = pygame.Rect(0, 0, 0, 0)

        self._save = pygame.Rect(0, 0, 0, 0)

        self._cancel = pygame.Rect(0, 0, 0, 0)
        
        self._title.focus()

    # ==================================================
    # Draw
    # ==================================================

    def _draw_content(self, screen):

        panel = self.panel

        x = panel.x + self.padding

        y = panel.y + self.padding

        # ------------------------------
        # Title
        # ------------------------------

        screen.blit(

            Fonts.title.render(
                "Nueva nota rápida",
                True,
                WHITE
            ),

            (x, y)

        )

        y += 55

        # ------------------------------
        # Note title
        # ------------------------------

        screen.blit(

            Fonts.default.render(
                "Título",
                True,
                WHITE
            ),

            (x, y)

        )

        y += 30

        self._title_rect = pygame.Rect(

            x,
            y,
            panel.width - self.padding * 2,
            42

        )

        self._title.draw(
            screen,
            self._title_rect
        )

        y += 65

        # ------------------------------
        # Note text
        # ------------------------------

        screen.blit(

            Fonts.default.render(
                "Texto",
                True,
                WHITE
            ),

            (x, y)

        )

        y += 30

        self._text_rect = pygame.Rect(

            x,
            y,
            panel.width - self.padding * 2,
            330

        )

        self._text.draw(
            screen,
            self._text_rect
        )

        # ------------------------------
        # Buttons
        # ------------------------------

        self._cancel = pygame.Rect(

            panel.right - 240,
            panel.bottom - 55,
            100,
            36

        )

        self._save = pygame.Rect(

            panel.right - 120,
            panel.bottom - 55,
            100,
            36

        )

        pygame.draw.rect(
            screen,
            BUTTON_CANCEL,
            self._cancel,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            BUTTON,
            self._save,
            border_radius=6
        )

        screen.blit(

            Fonts.small.render(
                "Cancelar",
                True,
                WHITE
            ),

            (self._cancel.x + 14, self._cancel.y + 10)

        )

        screen.blit(

            Fonts.small.render(
                "Guardar",
                True,
                WHITE
            ),

            (self._save.x + 20, self._save.y + 10)

        )

    # ==================================================
    # Events
    # ==================================================

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_TAB:

                if self._title.focused:

                    self._title.blur()
                    self._text.focus()

                else:

                    self._text.blur()
                    self._title.focus()

                return True

            if self._title.focused:

                return self._title.handle_event(event)

            if self._text.focused:

                return self._text.handle_event(event)

            return False

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        if self._title_rect.collidepoint(event.pos):

            self._text.blur()
            self._title.focus()

            return True

        if self._text_rect.collidepoint(event.pos):

            self._title.blur()
            self._text.focus()

            return True

        if self._cancel.collidepoint(event.pos):

            self.close()

            return True

        if self._save.collidepoint(event.pos):

            create_quick_note(
                title=self._title.text,
                text=self._text.text
            )

            self.close()

            return True

        return False