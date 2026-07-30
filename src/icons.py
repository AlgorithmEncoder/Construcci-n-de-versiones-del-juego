"""
icons.py

Simple vector icons for the computer UI.
"""

from __future__ import annotations

import pygame


LINE_WIDTH = 2


# ==================================================
# Helpers
# ==================================================

def _draw_file_outline(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):
    """
    Draws a generic file with a folded corner.
    Returns the inner drawing area.
    """

    fold = rect.width // 4

    # Main outline
    points = [
        (rect.left, rect.top),
        (rect.right - fold, rect.top),
        (rect.right, rect.top + fold),
        (rect.right, rect.bottom),
        (rect.left, rect.bottom),
    ]

    pygame.draw.lines(
        surface,
        colour,
        True,
        points,
        LINE_WIDTH,
    )

    # Fold
    pygame.draw.line(
        surface,
        colour,
        (rect.right - fold, rect.top),
        (rect.right - fold, rect.top + fold),
        LINE_WIDTH,
    )

    pygame.draw.line(
        surface,
        colour,
        (rect.right - fold, rect.top + fold),
        (rect.right, rect.top + fold),
        LINE_WIDTH,
    )

    return rect.inflate(-6, -6)


# ==================================================
# Navigation
# ==================================================

def draw_back(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    pygame.draw.line(
        surface,
        colour,
        (rect.right, rect.centery),
        (rect.left + 5, rect.centery),
        LINE_WIDTH,
    )

    pygame.draw.line(
        surface,
        colour,
        (rect.left + 5, rect.centery),
        (rect.left + 10, rect.top + 4),
        LINE_WIDTH,
    )

    pygame.draw.line(
        surface,
        colour,
        (rect.left + 5, rect.centery),
        (rect.left + 10, rect.bottom - 4),
        LINE_WIDTH,
    )


def draw_search(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    radius = min(rect.width, rect.height) // 3

    center = (
        rect.centerx - 2,
        rect.centery - 2,
    )

    pygame.draw.circle(
        surface,
        colour,
        center,
        radius,
        LINE_WIDTH,
    )

    pygame.draw.line(
        surface,
        colour,
        (center[0] + radius - 1, center[1] + radius - 1),
        (rect.right - 1, rect.bottom - 1),
        LINE_WIDTH,
    )


# ==================================================
# Communication
# ==================================================

def draw_email(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    pygame.draw.rect(
        surface,
        colour,
        rect,
        LINE_WIDTH,
        border_radius=3,
    )

    pygame.draw.line(
        surface,
        colour,
        rect.topleft,
        rect.center,
        LINE_WIDTH,
    )

    pygame.draw.line(
        surface,
        colour,
        rect.topright,
        rect.center,
        LINE_WIDTH,
    )


def draw_chat(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    bubble = pygame.Rect(
        rect.x,
        rect.y,
        rect.width,
        rect.height - 4,
    )

    pygame.draw.rect(
        surface,
        colour,
        bubble,
        LINE_WIDTH,
        border_radius=4,
    )

    pygame.draw.polygon(
        surface,
        colour,
        [
            (bubble.left + 4, bubble.bottom),
            (bubble.left + 8, bubble.bottom),
            (bubble.left + 5, bubble.bottom + 4),
        ],
        LINE_WIDTH,
    )


# ==================================================
# Files
# ==================================================

def draw_folder(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    tab = pygame.Rect(
        rect.x + 2,
        rect.y,
        rect.width // 3,
        rect.height // 3,
    )

    body = pygame.Rect(
        rect.x,
        rect.y + rect.height // 4,
        rect.width,
        rect.height * 3 // 4,
    )

    pygame.draw.rect(
        surface,
        colour,
        tab,
        LINE_WIDTH,
        border_top_left_radius=2,
        border_top_right_radius=2,
    )

    pygame.draw.rect(
        surface,
        colour,
        body,
        LINE_WIDTH,
        border_radius=3,
    )


def draw_pdf(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    inner = _draw_file_outline(
        surface,
        rect,
        colour,
    )

    y = inner.centery

    pygame.draw.line(
        surface,
        colour,
        (inner.left + 2, y),
        (inner.right - 2, y),
        LINE_WIDTH,
    )


def draw_text(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    inner = _draw_file_outline(
        surface,
        rect,
        colour,
    )

    for i in range(4):

        y = inner.top + 3 + i * 4

        pygame.draw.line(
            surface,
            colour,
            (inner.left + 2, y),
            (inner.right - 2, y),
            1,
        )


def draw_document(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    inner = _draw_file_outline(
        surface,
        rect,
        colour,
    )

    pygame.draw.rect(
        surface,
        colour,
        (
            inner.left + 2,
            inner.top + 2,
            inner.width - 4,
            3,
        ),
    )

    for i in range(2):

        y = inner.top + 9 + i * 5

        pygame.draw.line(
            surface,
            colour,
            (inner.left + 2, y),
            (inner.right - 2, y),
            1,
        )


def draw_spreadsheet(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    inner = _draw_file_outline(
        surface,
        rect,
        colour,
    )

    grid = pygame.Rect(
        inner.left + 2,
        inner.top + 2,
        inner.width - 4,
        inner.height - 4,
    )

    pygame.draw.rect(
        surface,
        colour,
        grid,
        1,
    )

    pygame.draw.line(
        surface,
        colour,
        (grid.centerx, grid.top),
        (grid.centerx, grid.bottom),
        1,
    )

    pygame.draw.line(
        surface,
        colour,
        (grid.left, grid.centery),
        (grid.right, grid.centery),
        1,
    )


def draw_image(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    inner = _draw_file_outline(
        surface,
        rect,
        colour,
    )

    pygame.draw.circle(
        surface,
        colour,
        (inner.right - 4, inner.top + 4),
        2,
    )

    pygame.draw.lines(
        surface,
        colour,
        False,
        [
            (inner.left + 2, inner.bottom - 2),
            (inner.left + 7, inner.centery),
            (inner.left + 11, inner.bottom - 6),
            (inner.right - 2, inner.bottom - 2),
        ],
        LINE_WIDTH,
    )


# ==================================================
# Lookup
# ==================================================

FILE_ICONS = {
    ".pdf": draw_pdf,
    ".txt": draw_text,
    ".doc": draw_document,
    ".docx": draw_document,
    ".xls": draw_spreadsheet,
    ".xlsx": draw_spreadsheet,
    ".png": draw_image,
    ".jpg": draw_image,
    ".jpeg": draw_image,
}


def get_file_icon(extension: str):

    return FILE_ICONS.get(
        extension.lower(),
        draw_document,
    )


def draw_note(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    inner = _draw_file_outline(
        surface,
        rect,
        colour,
    )

    for i in range(3):

        y = inner.top + 4 + i * 5

        pygame.draw.line(
            surface,
            colour,
            (inner.left + 2, y),
            (inner.right - 4, y),
            1,
        )


# ==================================================
# Gameplay
# ==================================================

def draw_inventory(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    body = pygame.Rect(
        rect.x + 2,
        rect.y + 5,
        rect.width - 4,
        rect.height - 6,
    )

    pygame.draw.rect(
        surface,
        colour,
        body,
        LINE_WIDTH,
        border_radius=3,
    )

    pygame.draw.arc(
        surface,
        colour,
        (
            rect.x + 4,
            rect.y,
            rect.width - 8,
            8,
        ),
        3.14,
        0,
        LINE_WIDTH,
    )

    pygame.draw.line(
        surface,
        colour,
        (rect.centerx, body.top),
        (rect.centerx, body.top + 5),
        LINE_WIDTH,
    )


def draw_incursion(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    radius = min(rect.width, rect.height) // 2 - 2

    pygame.draw.circle(
        surface,
        colour,
        rect.center,
        radius,
        LINE_WIDTH,
    )

    # Remolino interior
    pygame.draw.arc(
        surface,
        colour,
        (
            rect.centerx - radius + 4,
            rect.centery - radius + 4,
            (radius - 2) * 2,
            (radius - 2) * 2,
        ),
        0.5,
        4.7,
        LINE_WIDTH,
    )

    pygame.draw.line(
        surface,
        colour,
        (
            rect.centerx + 2,
            rect.centery - 2,
        ),
        (
            rect.centerx + radius - 2,
            rect.centery,
        ),
        LINE_WIDTH,
    )

def draw_placeholder(
    surface: pygame.Surface,
    rect: pygame.Rect,
    colour,
):

    pygame.draw.circle(
        surface,
        colour,
        rect.center,
        min(rect.width, rect.height) // 2 - 2,
        LINE_WIDTH,
    )

    pygame.draw.line(
        surface,
        colour,
        (rect.centerx, rect.top + 4),
        (rect.centerx, rect.bottom - 5),
        LINE_WIDTH,
    )

    pygame.draw.circle(
        surface,
        colour,
        (rect.centerx, rect.top + 3),
        1,
    )