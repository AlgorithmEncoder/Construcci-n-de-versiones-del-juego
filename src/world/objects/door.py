"""
Door world object.
"""

from core.interaction import GameAction

from world.object import WorldObject


class DoorObject(WorldObject):

    def __init__(
        self,
        object_id,
        position,
        polygon,
        icon,
        destination
    ):

        super().__init__(
            object_id=object_id,
            object_type="door",
            position=position,
            polygon=polygon,
            icon=icon
        )

        self.destination = destination

    # --------------------------------------------------

    def activate(self):

        return GameAction(
            action="change_room",
            target=self.destination
        )