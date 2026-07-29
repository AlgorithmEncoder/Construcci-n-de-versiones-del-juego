"""
text_renderer.py

Utility functions for rendering wrapped text.
Supports:

- Automatic word wrapping.
- Explicit new lines (\n).
- Paragraph spacing.
- Optional automatic headings.
"""

from __future__ import annotations

import pygame


def _wrap_line(
    text: str,
    font: pygame.font.Font,
    max_width: int,
) -> list[str]:
    """
    Wrap a single line to the available width.
    """

    if not text:
        return [""]

    words = text.split()

    if not words:
        return [""]

    lines = []

    current = words[0]

    for word in words[1:]:

        test = f"{current} {word}"

        if font.size(test)[0] <= max_width:

            current = test

        else:

            lines.append(current)

            current = word

    lines.append(current)

    return lines


def _is_heading(
    current: str,
    next_line: str | None,
) -> bool:
    """
    Detect short headings such as:

        Editorial

        Feature Article

        Personal Notes
    """

    current = current.strip()

    if not current:
        return False

    if len(current) > 40:
        return False

    if next_line is None:
        return False

    return next_line.strip() == ""


def draw_wrapped_text(
    surface: pygame.Surface,
    text: str,
    rect: pygame.Rect,
    font: pygame.font.Font,
    color,
    line_spacing: int = 4,
    paragraph_spacing: int | None = None,
    preserve_newlines: bool = False,
    title_font: pygame.font.Font | None = None,
):
    """
    Draw text inside a rectangle.

    Parameters
    ----------
    preserve_newlines
        Keeps explicit \\n from the source text.

    paragraph_spacing
        Extra spacing after empty lines.

    title_font
        Optional font used for automatically detected headings.
    """

    if not text:
        return

    if paragraph_spacing is None:
        paragraph_spacing = line_spacing * 2

    y = rect.top

    # --------------------------------------------------
    # Classic behaviour (compatible with DialogueUI)
    # --------------------------------------------------

    if not preserve_newlines:

        wrapped = _wrap_line(
            text,
            font,
            rect.width,
        )

        line_height = font.get_height() + line_spacing

        for line in wrapped:

            if y + line_height > rect.bottom:
                return

            image = font.render(
                line,
                True,
                color,
            )

            surface.blit(
                image,
                (
                    rect.left,
                    y,
                ),
            )

            y += line_height

        return

    # --------------------------------------------------
    # Document mode
    # --------------------------------------------------

    lines = text.split("\n")

    for index, raw_line in enumerate(lines):

        next_line = None

        if index < len(lines) - 1:
            next_line = lines[index + 1]

        # ----------------------------------------------
        # Empty line = paragraph
        # ----------------------------------------------

        if raw_line.strip() == "":

            y += paragraph_spacing

            continue

        current_font = font

        if (
            title_font is not None
            and _is_heading(raw_line, next_line)
        ):
            current_font = title_font

        wrapped = _wrap_line(
            raw_line,
            current_font,
            rect.width,
        )

        line_height = (
            current_font.get_height()
            + line_spacing
        )

        for line in wrapped:

            if y + line_height > rect.bottom:
                return

            image = current_font.render(
                line,
                True,
                color,
            )

            surface.blit(
                image,
                (
                    rect.left,
                    y,
                ),
            )

            y += line_height