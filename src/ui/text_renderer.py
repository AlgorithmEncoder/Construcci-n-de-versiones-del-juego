"""
text_renderer.py

Utility functions for rendering wrapped text.
"""

from __future__ import annotations

import pygame


def draw_wrapped_text(
    surface: pygame.Surface,
    text: str,
    rect: pygame.Rect,
    font: pygame.font.Font,
    color,
    line_spacing: int = 4,
):
    """
    Draws multiline text inside a rectangle.

    Words are automatically wrapped.
    Text outside the rectangle is clipped.
    """

    if not text:
        return

    words = text.split()

    lines = []
    current = ""

    for word in words:

        test = word if not current else f"{current} {word}"

        if font.size(test)[0] <= rect.width:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    y = rect.top

    line_height = font.get_height() + line_spacing

    for line in lines:

        if y + line_height > rect.bottom:
            break

        image = font.render(line, True, color)

        surface.blit(image, (rect.left, y))

        y += line_height