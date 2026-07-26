import pygame

from ui.fonts import Fonts

from launcher import styles


class EmptyView:

    def draw(self, screen, area, text="Not implemented"):

        label = Fonts.default.render(
            text,
            True,
            styles.TEXT_SECONDARY
        )

        rect = label.get_rect(center=area.center)

        screen.blit(label, rect)
    
    def handle_event(self, event):
        pass
    def update (self, current):
        pass