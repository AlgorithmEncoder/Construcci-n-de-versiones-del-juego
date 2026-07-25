"""
object_factory.py

Creates world objects from JSON data.
"""

from __future__ import annotations

from world.objects.computer import ComputerObject
from world.objects.document import DocumentObject
from world.objects.door import DoorObject


class ObjectFactory:

    _OBJECT_TYPES = {
        "computer": ComputerObject,
        "document": DocumentObject,
        "door": DoorObject,
    }

    # ==================================================
    # Public API
    # ==================================================

    @classmethod
    def create(
        cls,
        object_id: str,
        data: dict
    ):

        object_type = data["type"]

        object_class = cls._OBJECT_TYPES.get(object_type)

        if object_class is None:
            raise ValueError(
                f"Unknown object type: {object_type}"
            )

        position = tuple(data["position"])

        polygon = cls._make_absolute_polygon(
            position,
            data.get("polygon", [])
        )
        if not polygon:
            raise ValueError(
                f"Object '{object_id}' has no polygon."
            )

        icon = data.get("icon")

        if object_type == "computer":

            return object_class(
                object_id=object_id,
                position=position,
                polygon=polygon,
                icon=icon,
                computer_id=data["computer_id"]
            )

        if object_type == "document":

            return object_class(
                object_id=object_id,
                position=position,
                polygon=polygon,
                icon=icon,
                document_id=data["document_id"]
            )

        if object_type == "door":

            return object_class(
                object_id=object_id,
                position=position,
                polygon=polygon,
                icon=icon,
                destination=data["destination"]
            )

        raise ValueError(
            f"Unsupported object type: {object_type}"
        )

    # ==================================================
    # Helpers
    # ==================================================

    @staticmethod
    def _make_absolute_polygon(
        position: tuple[int, int],
        polygon: list[list[int]]
    ) -> list[tuple[int, int]]:

        px, py = position

        return [
            (int(px + x), int(py + y))
            for x, y in polygon
        ]