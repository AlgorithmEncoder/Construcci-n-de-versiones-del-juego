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
    logger.load()

    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    app = Application(screen, logger)

    running = True

    try:
        while running:

            dt = clock.tick(FPS) / 1000

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    
                    logger.save()

                    running = False

                else:

                    app.handle_event(event)

            app.update(dt)

            app.draw()

            pygame.display.flip()
    
    except Exception:

        logger.save()

        raise

    finally:

        pygame.quit()


if __name__ == "__main__":
    main()