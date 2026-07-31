"""
Unsupported document viewer.
"""

from __future__ import annotations

from ui.fonts import Fonts
from ui.computer import styles

from .base_viewer import BaseViewer


class UnsupportedViewer(BaseViewer):

    def __init__(
        self,
        title,
        message,
    ):

        super().__init__(title)

        self._message = message

    # ==================================================

    def draw_document(
        self,
        screen,
        area,
    ):

        title = Fonts.title.render(

            "No disponible",

            True,

            styles.TEXT

        )

        body = Fonts.default.render(

            self._message,

            True,

            styles.TEXT_SECONDARY

        )

        screen.blit(

            title,

            (

                area.x + 40,

                area.y + 80

            )

        )

        screen.blit(

            body,

            (

                area.x + 40,

                area.y + 130

            )

        )