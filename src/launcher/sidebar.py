from __future__ import annotations

import pygame

from ui.fonts import Fonts

from . import styles


class Sidebar:

    MODULES = {

        "home": [
            ("incursions", "🧠 Incursiones"),
            ("notes", "📝 Notas"),
            ("inventory", "🎒 Inventario"),
        ],

        "profile": [
            ("stats", "👤 Estadísticas"),
            ("achievements", "🏆 Logros"),
            ("activity", "📊 Actividad"),
        ],

        "settings": [
            ("general", "🎮 General"),
            ("audio", "🔊 Audio"),
            ("display", "🖥 Pantalla"),
            ("language", "🌐 Idioma"),
        ],
    }

    def __init__(self):

        self.buttons = []

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

            screen.blit(
                Fonts.default.render(
                    label,
                    True,
                    text_color
                ),
                (r.x + 12, r.y + 10)
            )

            self.buttons.append((r, key))

            y += 50

    def click(self, pos):

        for rect, key in self.buttons:

            if rect.collidepoint(pos):

                return key

        return None