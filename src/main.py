"""
Application entry point.
"""

import pygame

from constants import (
    WINDOW_TITLE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS
)

from core.game import Game
from ui.fonts import Fonts


def main():

    pygame.init()
    Fonts.initialize()

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    game = Game(screen)

    running = True

    while running:

        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            game.handle_event(event)

        game.update(dt)

        game.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()