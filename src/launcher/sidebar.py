from __future__ import annotations

import pygame

from ui.fonts import Fonts

from . import styles

from icons import (
    draw_incursion,
    draw_note,
    draw_inventory,
    draw_stats,
    draw_achievement,
    draw_activity,
    draw_settings,
    draw_audio,
    draw_display,
    draw_language,
    draw_accessibility,
    draw_placeholder
)


class Sidebar:
    
    MODULES = {
        "home": [
            "incursions",
            "notes",
            "inventory",
        ],

        "profile": [
            "stats",
            "achievements",
            "activity",
        ],

        "settings": [
            "general",
            "display",
            "audio",
            "language",
            "accessibility",
        ],
    }

    def __init__(self, language_manager):
        
        self._language = language_manager
        
        self.module = "home"

        self.buttons = []
        
        self._icons = {

            "incursions": draw_incursion,
            "notes": draw_note,
            "inventory": draw_inventory,

            # Pendientes
            "stats": draw_stats,
            "achievements": draw_achievement,
            "activity": draw_activity,

            "general": draw_settings,
            "display": draw_display,
            "audio": draw_audio,
            "language": draw_language,
            "accessibility": draw_accessibility,
        }

    def draw(self, screen, rect, module, current):

        pygame.draw.rect(screen, styles.SIDEBAR, rect)

        self.buttons.clear()

        y = rect.y + 25

        for key in self.MODULES[module]:
            
            label = self._language.get(
                "launcher",
                "sidebar",
                module,
                key
            )

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
    
    def set_module(self, module):
        """
        Cambia el módulo mostrado en la barra lateral.

        Parameters
        ----------
        module : str
            Nombre del módulo ("home", "profile", "settings"...).

        Returns
        -------
        bool
            True si el cambio se realizó, False si el módulo no existe.
        """

        if module not in self.MODULES:
            return False

        self.module = module

        return True
    
    def update(self, rect):

        self.buttons.clear()

        y = rect.y + 25

        for key in self.MODULES[self.module]:

            button = pygame.Rect(
                rect.x + 10,
                y,
                rect.width - 20,
                40,
            )

            self.buttons.append((button, key))

            y += 50