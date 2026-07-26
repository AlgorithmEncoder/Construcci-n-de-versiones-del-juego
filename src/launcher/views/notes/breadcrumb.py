"""
Breadcrumb navigation.
"""

from __future__ import annotations

from ui.fonts import Fonts
from launcher import styles


class Breadcrumb:

    def draw(self, screen, area, filesystem):

        names = ["Proyecto"]

        names.extend(
            folder.name
            for folder in filesystem._history
        )

        if filesystem.current != filesystem.root:

            names.append(filesystem.current.name)

        text = " > ".join(names)

        screen.blit(
            Fonts.small.render(
                text,
                True,
                styles.TEXT_SECONDARY
            ),
            (
                area.x,
                area.y
            )
        )