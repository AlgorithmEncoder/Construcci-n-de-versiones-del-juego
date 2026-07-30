from ui.computer.computer import ComputerUI

class DetectionManager:

    def __init__(
        self,
        room_manager,
        npc_manager,
        player,
        ui,
        on_detected
    ):

        self._rooms = room_manager
        self._npcs = npc_manager
        self._player = player
        self._ui = ui
        self._callback = on_detected
    
    def update(self):

        room = self._player.current_room

        npcs = self._npcs.visible_npcs(room)

        for npc in npcs:

            # Guardia
            if npc.alert:

                self._callback(
                    npc,
                    "alert"
                )

                return

            # Zona restringida
            if self._rooms.restricted:

                self._callback(
                    npc,
                    "restricted"
                )
                
                return
            
            # Ordenador bloqueado
            if isinstance(self._ui.current_overlay, ComputerUI):
                
                self._callback(
                    npc,
                    "computer_block"
                )

                return