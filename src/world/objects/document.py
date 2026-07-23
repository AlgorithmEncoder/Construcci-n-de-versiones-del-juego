"""
Document object.
"""

from world.object import WorldObject


class DocumentObject(WorldObject):

    def __init__(
        self,
        object_id,
        position,
        document_id
    ):

        super().__init__(
            object_id,
            "document",
            position
        )

        self.document_id = document_id

    def activate(self):

        return {

            "type": "document",
            "document_id": self.document_id
        }