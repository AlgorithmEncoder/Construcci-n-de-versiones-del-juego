"""
Computer world object.
"""

from core.interaction import GameAction

from world.object import WorldObject


class ComputerObject(WorldObject):

    def __init__(
        self,
        object_id,
        position,
        polygon,
        icon,
        computer_id
    ):

        super().__init__(
            object_id=object_id,
            object_type="computer",
            position=position,
            polygon=polygon,
            icon=icon
        )

        self.computer_id = computer_id

    # --------------------------------------------------

    def activate(self):

        return GameAction(
            action="open_computer",
            target=self.computer_id
        )