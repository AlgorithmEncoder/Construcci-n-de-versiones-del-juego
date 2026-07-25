"""
object.py

Base class for every interactive object in the world.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from core.interaction import GameAction


class WorldObject(ABC):
    """
    Base class for every interactable object.
    """

    def __init__(
        self,
        object_id: str,
        object_type: str,
        position: tuple[int, int],
        polygon: list[tuple[int, int]],
        icon: str | None = None
    ):

        self.id = object_id
        self.type = object_type

        self.position = tuple(position)

        self.polygon = polygon

        self.icon = icon

    # ==================================================
    # Public API
    # ==================================================

    @abstractmethod
    def activate(self) -> GameAction:
        """
        Returns the action produced when interacting
        with this object.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement activate()."
        )

    # --------------------------------------------------

    def contains(
        self,
        point: tuple[int, int]
    ) -> bool:
        """
        Returns True if the point lies inside the polygon.

        Ray Casting algorithm.
        """

        x, y = point

        inside = False

        vertices = self.polygon

        n = len(vertices)

        j = n - 1

        for i in range(n):

            xi, yi = vertices[i]
            xj, yj = vertices[j]

            intersects = (
                (yi > y) != (yj > y)
            ) and (
                x <
                (xj - xi) *
                (y - yi) /
                ((yj - yi) + 1e-9)
                + xi
            )

            if intersects:
                inside = not inside

            j = i

        return inside