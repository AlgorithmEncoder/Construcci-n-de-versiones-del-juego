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

from game import Game


def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    game = Game(screen)

    running = True

    while running:

        dt = clock.tick(FPS) / 1000

        running = game.handle_events()

        game.update(dt)

        game.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()