"""
Door object.
"""

from world.object import WorldObject


class DoorObject(WorldObject):

    def __init__(
        self,
        object_id,
        position,
        destination
    ):

        super().__init__(
            object_id,
            "door",
            position
        )

        self.destination = destination

    def activate(self):

        return {

            "type": "door",
            "destination": self.destination
        }