"""
Computer object.
"""

from world.object import WorldObject


class ComputerObject(WorldObject):

    def __init__(
        self,
        object_id,
        position,
        computer_id
    ):

        super().__init__(
            object_id,
            "computer",
            position
        )

        self.computer_id = computer_id

    def activate(self):

        return {

            "type": "computer",
            "computer_id": self.computer_id
        }