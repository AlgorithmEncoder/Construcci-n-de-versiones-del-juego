from __future__ import annotations

import pygame

from ui.fonts import Fonts

from . import styles


# ==================================================
# Buttons
# ==================================================

def draw_button(
    screen,
    rect,
    text,
    selected=False
):

    mouse = pygame.mouse.get_pos()

    hover = (
        rect.collidepoint(mouse)
        and
        not selected
    )

    colour = styles.BUTTON

    if hover:
        colour = styles.BUTTON_HOVER

    if selected:
        colour = styles.BUTTON_SELECTED

    pygame.draw.rect(
        screen,
        colour,
        rect,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        styles.BORDER,
        rect,
        1,
        border_radius=10
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

    text_rect = surface.get_rect(
        centery=rect.centery
    )

    text_rect.x = rect.x + 46

    screen.blit(
        surface,
        text_rect
    )


# ==================================================
# Header
# ==================================================

def draw_header(
    screen,
    rect,
    title
):

    pygame.draw.rect(
        screen,
        styles.TOPBAR,
        rect
    )

    pygame.draw.line(
        screen,
        styles.DIVIDER,
        (rect.left, rect.bottom),
        (rect.right, rect.bottom),
        1
    )

    radius = 6

    circles = (
        (235, 95, 86),
        (243, 190, 67),
        (89, 201, 98),
    )

    x = rect.x + 22

    for colour in circles:

        pygame.draw.circle(
            screen,
            colour,
            (x, rect.centery),
            radius
        )

        x += 18

    title_surface = Fonts.title.render(
        title,
        True,
        styles.TEXT
    )

    title_rect = title_surface.get_rect(
        center=rect.center
    )

    screen.blit(
        title_surface,
        title_rect
    )