"""
game.py

Main game coordinator.

This class owns every manager of the engine and coordinates
the game loop. It contains no gameplay logic.
"""

from __future__ import annotations

import pygame

from core.clock import GameClock
from core.render_state import RenderState

from core.memory_loader import MemoryLoader

from managers.room_manager import RoomManager
from managers.object_manager import ObjectManager

from ui.renderer import Renderer

from managers.ui_manager import UIManager
from managers.input_manager import InputManager
from managers.npc_manager import NPCManager
from managers.event_manager import EventManager
from managers.detection_manager import DetectionManager
from managers.player_manager import PlayerManager

from ui.transition import TransitionUI

from constants import (
    ROOM_CHANGE_TIME,
    DOCUMENT_OPEN_TIME,
    COMPUTER_BOOT_TIME,
    RESET_TIME,
)


class Game:
    """
    Main game coordinator.
    """

    # ==================================================
    # Construction
    # ==================================================

    def __init__(
        self,
        screen: pygame.Surface,
        memory: str = "memory_01"
    ):

        self._screen = screen

        self._memory_name = memory

        self._loader = None

        self._clock = None
        self._room_manager = None
        self._ui = None
        self._renderer = None
        self._object_manager = None
        self._input = None
        
        self._scale = (1.0, 1.0)
        
        self._offset_x = 0
        self._offset_y = 0

        self._native_width = 0
        self._native_height = 0
        
        self._npc_manager = None
        self._event_manager = None
        
        self._action_handlers = {
            "change_room": self._change_room,
            "open_document": self._open_document,
            "open_computer": self._open_computer,
            "open_dialogue": self._open_dialogue
        }

        self._render_state = RenderState()

        self._load_memory()

        self._create_managers()

    # ==================================================
    # Initialization
    # ==================================================

    def _load_memory(self):

        self._loader = MemoryLoader(self._memory_name)

        self._loader.load()

    # --------------------------------------------------

    def _create_managers(self):

        self._clock = GameClock(
            start_hour = 8,
            start_minute = 0,
            start_second = 0,
            time_scale=1.0
        )
        
        self._object_manager = ObjectManager(
            self._loader.objects
        )

        self._room_manager = RoomManager(
            rooms_data=self._loader.rooms,
            initial_room=self._loader.story["initial_room"],
            object_manager=self._object_manager
        )

        self._ui = UIManager()
        
        self._calculate_viewport()

        self._renderer = Renderer(self._screen, self._native_width, self._native_height)
        
        self._input = InputManager(self)
        
        self._npc_manager = NPCManager(
            self._loader.npcs
        )
        
        self._player = PlayerManager(
            self._loader.story["initial_room"]
        )

        self._detection = DetectionManager(
            self._room_manager,
            self._npc_manager,
            self._player,
            self._on_detected
        )

        self._event_manager = EventManager(
            self._loader.events
        )

        self._event_manager.register_handler(
            "end_loop",
            self._end_loop
        )

        self._event_manager.register_handler(
            "sound",
            self._play_sound
        )

        self._event_manager.register_handler(
            "npc_move",
            self._npc_move
        )

    # ==================================================
    # Public API
    # ==================================================

    def update(self, delta_time: float):

        self._clock.update(delta_time)
        
        self._npc_manager.update(self._clock)

        self._event_manager.update(self._clock)
        
        self._detection.update()
        
        if self._ui.is_open:

            self._ui.update(delta_time)

        self._build_render_state()

    # --------------------------------------------------

    def draw(self):
        
        self._renderer.draw(self._render_state, self._scale, self._offset_x, self._offset_y)

    # --------------------------------------------------

    def handle_event(self, event):

        self._input.handle_event(event)

    # --------------------------------------------------

    def _calculate_viewport(self):

        resolution = self._loader.metadata["resolution"]

        self._native_width = resolution["width"]
        self._native_height = resolution["height"]

        screen_width = self._screen.get_width()
        screen_height = self._screen.get_height()

        self._scale = min(
            screen_width / self._native_width,
            screen_height / self._native_height
        )

        world_width = self._native_width * self._scale
        world_height = self._native_height * self._scale

        self._offset_x = (screen_width - world_width) / 2
        self._offset_y = (screen_height - world_height) / 2

    # ==================================================
    # Render state
    # ==================================================

    def _build_render_state(self):

        self._render_state.background = (
            self._room_manager.background
        )

        self._render_state.objects = (
            self._room_manager.objects
        )

        self._render_state.npcs = (
            self._npc_manager.visible_npcs(
                self._room_manager.current_room
            )
        )

        self._render_state.overlay = (
            self._ui.current_overlay
        )

        self._render_state.clock = (
            self._clock.time_string
        )

    # ==================================================
    # Properties
    # ==================================================

    @property
    def clock(self):

        return self._clock

    @property
    def room_manager(self):

        return self._room_manager

    @property
    def ui(self):

        return self._ui
    
    @property
    def input(self):

        return self._input
    
    @property
    def object_manager(self):

        return self._object_manager
    
    @property
    def scale(self):
        return self._scale


    @property
    def offset_x(self):
        return self._offset_x


    @property
    def offset_y(self):
        return self._offset_y
    
    @property
    def native_width(self):
        return self._native_width


    @property
    def native_height(self):
        return self._native_height
    
    @property
    def npc_manager(self):
        return self._npc_manager


    @property
    def event_manager(self):
        return self._event_manager
    
    @property
    def player(self):

        return self._player
    
    # ==================================================
    # Actions
    # ==================================================
    def _change_room(self, room_id):

        self._start_transition(

            duration=ROOM_CHANGE_TIME,

            text="Cambiando de habitación",

            callback=lambda: self._finish_change_room(room_id)
        )

    def _finish_change_room(self, room_id):

        self._room_manager.change_room(room_id)

        self._player.change_room(room_id)
    
    def _open_document(self, document_id):

        self._start_transition(

            duration=DOCUMENT_OPEN_TIME,

            text="Leyendo documento",

            callback=lambda: self._finish_open_document(document_id)

        )


    def _finish_open_document(self, document_id):

        document = self._loader.documents[document_id]

        from ui.document import DocumentUI

        self._ui.open(

            DocumentUI(

                document,

                self._native_width,

                self._native_height

            )

        )
    
    def _open_computer(self, computer_id):

        self._start_transition(

            duration=COMPUTER_BOOT_TIME,

            text="Encendiendo ordenador",

            callback=lambda: self._finish_open_computer(computer_id)

        )


    def _finish_open_computer(self, computer_id):

        computer = self._loader.computers[computer_id]

        from ui.computer import ComputerUI

        self._ui.open(

            ComputerUI(

                computer,

                self._native_width,

                self._native_height

            )

        )
    
    def _open_dialogue(self, dialogue_id: str):

        dialogue = self._loader.dialogues[dialogue_id]

        npc = next(
            (
                npc
                for npc in self._npc_manager.visible_npcs(
                    self._room_manager.current_room
                )
                if npc.dialogue == dialogue_id
            ),
            None
        )

        speaker = npc.name if npc else ""

        from ui.dialogue import DialogueUI

        self._ui.open(
            DialogueUI(
                speaker=speaker,
                dialogue=dialogue,
                world_width=self._native_width,
                world_height=self._native_height
            )
        )
    
    def execute_action(self, action):

        if action is None:
            return

        handler = self._action_handlers.get(action.action)

        if handler:
            handler(action.target)
    
    def _on_detected(self, npc, reason):
        
        npc.current_room = "__hidden__"

        self._start_transition(

            duration=RESET_TIME,

            text="REINICIANDO MEMORIA",

            callback=self.reset

        )
    
    def _start_transition(
        self,
        duration: float,
        callback,
        text: str | None = None
    ):

        self._ui.open(

            TransitionUI(

                world_width=self._native_width,

                world_height=self._native_height,

                duration=duration,

                callback=callback,

                text=text

            )

        )
    
    def _end_loop(self, data):

        print("Loop finished")

        # De momento solo reiniciamos.

        self._start_transition(

            duration=RESET_TIME,

            text="REINICIANDO MEMORIA",

            callback=self.reset

        )

    def _play_sound(self, data):

        print(f"Play sound: {data['sound']}")

    def _npc_move(self, data):

        npc = self._npc_manager.get(data["npc"])

        npc.current_room = data["room"]
    
    def find_click_target(self, position):

        npc = self._npc_manager.find_at(self._room_manager.current_room, position)

        if npc:
            return npc

        return self._room_manager.find_object_at(position)
    
    def reset(self):

        # Reiniciar reloj

        self._clock.reset()

        # Reiniciar sala

        self._room_manager.reset(
            self._loader.story["initial_room"]
        )

        # Reiniciar objetos

        self._object_manager.reset(
            self._loader.objects
        )

        # Reiniciar NPC

        self._npc_manager.reset()

        # Reiniciar eventos

        self._event_manager.reset()
        
        # Reiniciar player
        
        self._player.reset()

        # Cerrar interfaces

        self._ui.close()