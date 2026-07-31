"""
Viewer for images.
"""

from __future__ import annotations

import pygame

from .base_viewer import BaseViewer


class ImageViewer(BaseViewer):

    def __init__(self, path):

        super().__init__(path.name)

        self._image = pygame.image.load(path).convert_alpha()

    # ==================================================

    def draw_document(
        self,
        screen,
        area,
    ):

        image = self._image

        scale = min(

            area.width / image.get_width(),

            area.height / image.get_height(),

            1.0

        )

        if scale != 1:

            image = pygame.transform.smoothscale(

                image,

                (

                    int(image.get_width() * scale),

                    int(image.get_height() * scale)

                )

            )

        rect = image.get_rect(center=area.center)

        screen.blit(image, rect)