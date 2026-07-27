"""
Toolbar.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts
from launcher import styles


class Toolbar:

    BUTTONS = [

        ("Nueva carpeta", "folder"),

        ("Nueva nota", "note"),

        ("Renombrar", "rename"),

        ("Eliminar", "delete"),
        
        ("Mover", "move"),
        
        ("Volver", "back")
    ]

    def __init__(self):

        self._buttons = []

    def draw(self, screen, area):

        self._buttons.clear()

        x = area.x

        for label, action in self.BUTTONS:

            rect = pygame.Rect(
                x,
                area.y,
                145,
                36
            )

            pygame.draw.rect(
                screen,
                styles.ACCENT,
                rect,
                border_radius=6
            )

            screen.blit(
                Fonts.small.render(
                    label,
                    True,
                    (255,255,255)
                ),
                (rect.x + 10, rect.y + 9)
            )

            self._buttons.append(
                (rect, action)
            )

            x += 155

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        for rect, action in self._buttons:
            if action =="back":print(rect, event.pos)

            if rect.collidepoint(event.pos):
                if action =="back":print("in")

                return action

        return None