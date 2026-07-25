from __future__ import annotations

import pygame

from ui.fonts import Fonts

from . import styles


def draw_button(
    screen,
    rect,
    text,
    selected=False
):

    colour = (
        styles.ACCENT
        if selected
        else styles.BUTTON
    )

    pygame.draw.rect(
        screen,
        colour,
        rect,
        border_radius=6
    )

    pygame.draw.rect(
        screen,
        styles.BORDER,
        rect,
        1,
        border_radius=6
    )

    font = Fonts.default

    colour = (
        styles.TEXT_LIGHT
        if selected
        else styles.TEXT
    )

    surface = font.render(
        text,
        True,
        colour
    )

    screen.blit(
        surface,
        surface.get_rect(center=rect.center)
    )


def draw_header(
    screen,
    rect,
    title
):

    pygame.draw.rect(
        screen,
        styles.PANEL,
        rect
    )

    font = Fonts.title

    text = font.render(
        title,
        True,
        styles.TEXT
    )

    screen.blit(
        text,
        (
            rect.x + styles.PADDING,
            rect.y + 12
        )
    )