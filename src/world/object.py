"""
Base world object.
"""

from __future__ import annotations


class WorldObject:

    def __init__(
        self,
        object_id: str,
        object_type: str,
        position: tuple
    ):

        self.id = object_id
        self.type = object_type
        self.position = tuple(position)

    # --------------------------------------------------

    def activate(self):

        raise NotImplementedError(
            f"{self.__class__.__name__} must implement activate()."
        )