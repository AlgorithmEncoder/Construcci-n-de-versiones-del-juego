"""
Application entry point.
"""

import pygame

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WINDOW_TITLE,
    FPS,
)

from ui.fonts import Fonts
from application import Application
from logger import Logger


def main():

    pygame.init()

    Fonts.initialize()
    
    info = pygame.display.Info()

    screen = pygame.display.set_mode(
        (
            info.current_w,
            info.current_h
        )
    )
    
    logger = Logger()
    logger.register(
    "Has iniciado una nueva incursión.",
    category="incursion"
)

    logger.register(
        "Has encontrado un documento en el despacho.",
        category="discovery"
    )

    logger.register(
        "Has interactuado con el ordenador de recepción.",
        category="interaction"
    )

    logger.register(
        "La incursión ha terminado.",
        category="system"
    )

    logger.register(
        "Has desbloqueado un nuevo logro.",
        category="achievement"
    )

    logger.register(
        "Has encontrado una nota rápida abandonada.",
        category="discovery"
    )

    logger.register(
        "Has examinado una puerta cerrada.",
        category="interaction"
    )

    logger.register(
        "El sistema ha reiniciado la incursión.",
        category="system"
    )

    logger.register(
        "Has descubierto una información importante relacionada con el caso.",
        category="mystery"
    )

    logger.register(
        "Has iniciado una nueva investigación.",
        category="general"
    )

    logger.register(
        "Has encontrado una segunda pista que podría cambiar el rumbo de la investigación.",
        category="discovery"
    )

    logger.register(
        "Has hablado con un personaje sospechoso.",
        category="interaction"
    )

    logger.register(
        "Has completado una incursión sin ser descubierto.",
        category="achievement"
    )

    logger.register(
        "Se ha detectado una anomalía en el entorno.",
        category="system"
    )

    logger.register(
        "Has regresado a la zona principal.",
        category="incursion"
    )

    logger.save()

    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    app = Application(screen, logger)

    running = True

    while running:

        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            else:

                app.handle_event(event)

        app.update(dt)

        app.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()