"""
object_manager.py

Creates and stores every world object.

Objects are created once when the memory is loaded and
remain alive until the memory is reset.
"""

from __future__ import annotations

from world.object_factory import ObjectFactory


class ObjectManager:
    """
    Manages every interactable object in the world.
    """

    def __init__(self, objects_data: dict):

        self._objects: dict = {}

        self._build(objects_data)

    # ==================================================
    # Internal
    # ==================================================

    def _build(self, objects_data: dict):

        """
        Creates every world object from JSON.
        """

        self._objects.clear()

        for object_id, data in objects_data.items():

            obj = ObjectFactory.create(
                object_id,
                data
            )

            self._objects[object_id] = obj

    # ==================================================
    # Public API
    # ==================================================

    def get(self, object_id: str):

        """
        Returns a world object.

        Raises:
            ValueError if the object does not exist.
        """

        if object_id not in self._objects:
            raise ValueError(f"Object '{object_id}' does not exist.")

        return self._objects[object_id]

    # --------------------------------------------------

    def exists(self, object_id: str) -> bool:

        return object_id in self._objects

    # --------------------------------------------------

    def all(self) -> tuple:

        """
        Returns every object in the world.
        """

        return tuple(self._objects.values())

    # --------------------------------------------------

    def reset(self, objects_data: dict):

        """
        Rebuilds every object.

        Used when restarting the memory.
        """

        self._build(objects_data)

    # ==================================================
    # Magic methods
    # ==================================================

    def __contains__(self, object_id: str):

        return object_id in self._objects

    def __len__(self):

        return len(self._objects)

    def __iter__(self):

        return iter(self._objects.values())