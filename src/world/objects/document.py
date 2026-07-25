"""
Document world object.
"""

from core.interaction import GameAction

from world.object import WorldObject


class DocumentObject(WorldObject):

    def __init__(
        self,
        object_id,
        position,
        polygon,
        icon,
        document_id
    ):

        super().__init__(
            object_id=object_id,
            object_type="document",
            position=position,
            polygon=polygon,
            icon=icon
        )

        self.document_id = document_id

    # --------------------------------------------------

    def activate(self):

        return GameAction(
            action="open_document",
            target=self.document_id
        )