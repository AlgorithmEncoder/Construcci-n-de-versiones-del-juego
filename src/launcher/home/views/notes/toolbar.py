"""
Toolbar.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts
from launcher import styles


class Toolbar:

    BUTTONS = [
        ("new_folder", "folder"),
        ("new_note", "note"),
        ("rename", "rename"),
        ("delete", "delete"),
        ("move", "move"),
        ("back", "back"),
    ]

    def __init__(self, language_manager):

        self._buttons = []
        self._language = language_manager

    def draw(self, screen, area):

        self._buttons.clear()

        x = area.x

        for label_id, action in self.BUTTONS:
            
            label = self._language.get(
                "launcher",
                "toolbar",
                label_id
            )

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

            if rect.collidepoint(event.pos):

                return action

        return None