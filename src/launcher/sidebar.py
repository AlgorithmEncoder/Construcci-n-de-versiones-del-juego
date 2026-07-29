from __future__ import annotations

import pygame

from ui.fonts import Fonts

from . import styles

from ui.computer.icons import (
    draw_incursion,
    draw_note,
    draw_inventory,
    draw_placeholder
)


class Sidebar:
    
    MODULES = {

        "home": [
            ("incursions", "Incursiones"),
            ("notes", "Notas"),
            ("inventory", "Inventario"),
        ],

        "profile": [
            ("stats", "Estadísticas"),
            ("achievements", "Logros"),
            ("activity", "Actividad"),
        ],

        "settings": [
            ("general", "General"),
            ("audio", "Audio"),
            ("display", "Pantalla"),
            ("language", "Idioma"),
        ],
    }

    def __init__(self):

        self.buttons = []
        
        self._icons = {

            "incursions": draw_incursion,
            "notes": draw_note,
            "inventory": draw_inventory,

            # Pendientes
            "stats": draw_placeholder,
            "achievements": draw_placeholder,
            "activity": draw_placeholder,

            "general": draw_placeholder,
            "audio": draw_placeholder,
            "display": draw_placeholder,
            "language": draw_placeholder,
        }

    def draw(self, screen, rect, module, current):

        pygame.draw.rect(screen, styles.SIDEBAR, rect)

        self.buttons.clear()

        y = rect.y + 25

        for key, label in self.MODULES[module]:

            r = pygame.Rect(
                rect.x + 10,
                y,
                rect.width - 20,
                40
            )

            color = (
                styles.PRIMARY
                if key == current
                else styles.SIDEBAR
            )

            pygame.draw.rect(screen, color, r, border_radius=6)

            text_color = (
                styles.TEXT_LIGHT
                if key == current
                else styles.TEXT
            )

            icon = self._icons.get(key)

            if icon is not None:

                icon_rect = pygame.Rect(
                    r.x + 12,
                    r.centery - 9,
                    18,
                    18,
                )

                icon(
                    screen,
                    icon_rect,
                    text_color,
                )
            
            screen.blit(
                Fonts.default.render(
                    label,
                    True,
                    text_color,
                ),
                (
                    r.x + 42,
                    r.y + 10,
                ),
            )

            self.buttons.append((r, key))

            y += 50

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        for rect, key in self.buttons:

            if rect.collidepoint(event.pos):

                return key

        return None