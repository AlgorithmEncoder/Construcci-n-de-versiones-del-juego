from __future__ import annotations

import pygame

from . import styles
from .widgets import draw_button


class Sidebar:

    ITEMS = (
        ("emails", "Emails"),
        ("chats", "Chats"),
        ("files", "Files"),
    )

    def __init__(self):

        self._buttons = {}

    def draw(
        self,
        screen,
        panel,
        current
    ):

        sidebar = pygame.Rect(
            panel.x,
            panel.y,
            styles.SIDEBAR_WIDTH,
            panel.height
        )

        pygame.draw.rect(
            screen,
            styles.SIDEBAR,
            sidebar,
            border_top_left_radius=12,
            border_bottom_left_radius=12
        )

        y = panel.y + 30

        self._buttons.clear()

        for key, label in self.ITEMS:

            rect = pygame.Rect(
                sidebar.x + 15,
                y,
                sidebar.width - 30,
                42
            )

            draw_button(
                screen,
                rect,
                label,
                key == current
            )

            self._buttons[key] = rect

            y += 55

    def handle_click(
        self,
        position
    ):

        for key, rect in self._buttons.items():

            if rect.collidepoint(position):
                return key

        return None