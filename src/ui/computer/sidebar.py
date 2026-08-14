from __future__ import annotations

import pygame

from ui.fonts import Fonts

from . import styles
from .widgets import draw_button

from icons import (
    draw_email,
    draw_chat,
    draw_folder,
)


class Sidebar:

    ITEMS = (
        ("emails", "Emails", draw_email),
        ("chats", "Chats", draw_chat),
        ("files", "Files", draw_folder),
    )

    def __init__(self):

        self._buttons = {}

    # ==================================================

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

        # Fondo
        pygame.draw.rect(
            screen,
            styles.SIDEBAR,
            sidebar,
            border_top_left_radius=12,
            border_bottom_left_radius=12
        )

        # Separador vertical
        pygame.draw.line(
            screen,
            styles.DIVIDER,
            (sidebar.right - 1, sidebar.top),
            (sidebar.right - 1, sidebar.bottom),
            1
        )

        # Título
        title = Fonts.small.render(
            "WORKSTATION",
            True,
            styles.TEXT_SECONDARY
        )

        screen.blit(
            title,
            (
                sidebar.x + 22,
                sidebar.y + 20
            )
        )

        # Línea decorativa
        pygame.draw.line(
            screen,
            styles.DIVIDER,
            (sidebar.x + 20, sidebar.y + 48),
            (sidebar.right - 20, sidebar.y + 48),
            1
        )

        y = sidebar.y + 70

        self._buttons.clear()

        for key, label, icon in self.ITEMS:

            rect = pygame.Rect(
                sidebar.x + 14,
                y,
                sidebar.width - 28,
                46
            )

            draw_button(
                screen,
                rect,
                label,
                key == current
            )

            icon_rect = pygame.Rect(
                rect.x + 16,
                rect.centery - 9,
                18,
                18
            )

            colour = (
                styles.TEXT_LIGHT
                if key == current
                else styles.TEXT
            )

            icon(
                screen,
                icon_rect,
                colour
            )

            self._buttons[key] = rect

            y += 58

    # ==================================================

    def handle_click(
        self,
        position
    ):

        for key, rect in self._buttons.items():

            if rect.collidepoint(position):
                return key

        return None