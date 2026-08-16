"""
input_manager.py

Handles player input.

This class translates pygame events into game interactions.
"""

from __future__ import annotations

import pygame

from ui.quick_notes import QuickNotes

class InputManager:

    def __init__(self, game):

        self._game = game

    # ==================================================
    # Public API
    # ==================================================

    def handle_event(self, event):
        
        if event.type == pygame.MOUSEWHEEL:

            if self._game.ui.is_open:

                if self._game.ui.handle_event(event):
                    return

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                scale = self._game.scale

                memory_position = (
                    (event.pos[0] - self._game.offset_x) / scale,
                    (event.pos[1] - self._game.offset_y) / scale
                )
                
                world_event = pygame.event.Event(
                    event.type,
                    {
                        **event.dict,
                        "pos": memory_position
                    }
                )
                
                mx, my = event.pos

                world_left = self._game.offset_x
                world_top = self._game.offset_y

                world_right = world_left + (
                    self._game.native_width * self._game.scale
                )

                world_bottom = world_top + (
                    self._game.native_height * self._game.scale
                )

                if not (
                    world_left <= mx <= world_right
                    and
                    world_top <= my <= world_bottom
                ):
                    return

                self._handle_left_click(memory_position, world_event)

        elif event.type == pygame.KEYDOWN:
            
            if self._game.ui.is_open:

                if self._game.ui.handle_event(event):
                    return

            self._handle_key(event)
        

    # ==================================================
    # Mouse
    # ==================================================

    def _handle_left_click(self, position, world_event):

        # Si hay una ventana abierta,
        # por ahora cualquier clic la cierra.

        if self._game.ui.is_open:

            handled = self._game.ui.handle_event(world_event)

            if not handled:
                self._game.ui.close()

            return
        
        if self._game.renderer.exit_button_at(position):

            self._game.exit_dream()

            return
        
        if self._game.renderer.quick_note_button_at(position):
            
            self._game.logger.register(
                "launcher.notes.register.quick_note_creator_opened",
                category="notes"
            )

            self._game.ui.open(

                QuickNotes(
                    self._game.native_width,
                    self._game.native_height
                )

            )

            return

        entity = self._game.find_click_target(position)

        if entity is None:
            return

        action = entity.activate()

        self._game.execute_action(action)

    # ==================================================
    # Keyboard
    # ==================================================

    def _handle_key(self, event):

        if event.key == pygame.K_ESCAPE:

            if self._game.ui.is_open:

                self._game.ui.close()