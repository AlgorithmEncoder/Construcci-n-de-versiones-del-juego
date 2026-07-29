"""
Detailed information about a dream.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts
from launcher import styles
from ui.computer.icons import draw_back


class IncursionDetail:

    BUTTON_WIDTH = 260
    BUTTON_HEIGHT = 54

    def __init__(self, dream):

        self._dream = dream

        self._start_rect = pygame.Rect(0, 0, 0, 0)
        self._back_rect = pygame.Rect(0, 0, 0, 0)

    # --------------------------------------------------

    def update(self, dt):
        pass

    # --------------------------------------------------

    def draw(self, screen, area):

        x = area.x + 40
        y = area.y + 35

        # ---------- Header ----------

        title = Fonts.title.render(
            self._dream["title"],
            True,
            styles.TEXT
        )

        screen.blit(title, (x, y))

        # Icono
        icon_rect = pygame.Rect(
            area.right - 110,
            y + 2,
            16,
            16
        )

        draw_back(
            screen,
            icon_rect,
            styles.ACCENT
        )

        # Texto
        back = Fonts.default.render(
            "Volver",
            True,
            styles.ACCENT
        )

        text_pos = (
            icon_rect.right + 8,
            y
        )

        screen.blit(back, text_pos)

        # Área clicable (icono + texto)
        self._back_rect = pygame.Rect(
            icon_rect.left,
            y,
            back.get_width() + icon_rect.width + 8,
            max(back.get_height(), icon_rect.height)
        )
        
        y += 70

        # ---------- Information ----------

        info = [

            ("Estado",
             "Bloqueado" if self._dream["locked"] else "Disponible"),

            ("Duración",
             f"{self._dream['duration']//60} minutos"),

            ("Incursiones",
             str(self._dream["iterations"])),

            ("Progreso",
             f"{self._dream['progress']}%")
        ]

        for name, value in info:

            screen.blit(
                Fonts.default.render(
                    name,
                    True,
                    styles.TEXT_SECONDARY
                ),
                (x, y)
            )

            screen.blit(
                Fonts.default.render(
                    value,
                    True,
                    styles.TEXT
                ),
                (x + 170, y)
            )

            y += 34

        y += 25

        # ---------- Objective ----------

        screen.blit(
            Fonts.subtitle.render(
                "Objetivo",
                True,
                styles.TEXT
            ),
            (x, y)
        )

        y += 40

        for line in self._dream["objective"].split("\n"):

            txt = Fonts.default.render(
                line,
                True,
                styles.TEXT
            )

            screen.blit(txt, (x, y))

            y += 26

        # ---------- Button ----------

        self._start_rect = pygame.Rect(
            x,
            area.bottom - 95,
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )

        pygame.draw.rect(
            screen,
            styles.ACCENT,
            self._start_rect,
            border_radius=8
        )

        label = Fonts.default.render(
            "Iniciar incursión",
            True,
            (255, 255, 255)
        )

        screen.blit(
            label,
            label.get_rect(center=self._start_rect.center)
        )

    # --------------------------------------------------

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        if self._back_rect.collidepoint(event.pos):
            return ("back", None)

        if self._start_rect.collidepoint(event.pos):
            return ("start", self._dream["id"])

        return None