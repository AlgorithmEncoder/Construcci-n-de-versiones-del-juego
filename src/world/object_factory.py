"""
Factory responsible for creating world objects.
"""

from world.objects.computer import ComputerObject
from world.objects.document import DocumentObject
from world.objects.door import DoorObject


class ObjectFactory:

    @staticmethod
    def create(object_id: str, data: dict):

        object_type = data["type"]

        if object_type == "computer":
            return ComputerObject(
                object_id=object_id,
                position=data["position"],
                computer_id=data["computer_id"]
            )

        elif object_type == "document":
            return DocumentObject(
                object_id=object_id,
                position=data["position"],
                document_id=data["document_id"]
            )

        elif object_type == "door":
            return DoorObject(
                object_id=object_id,
                position=data["position"],
                destination=data["destination"]
            )

        raise ValueError(
            f"Unknown object type '{object_type}'."
        )