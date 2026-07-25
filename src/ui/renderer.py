"""
renderer.py

Pure renderer.

Draws the entire world at native resolution and finally
scales it to the current window.
"""

from __future__ import annotations

import pygame

from core.render_state import RenderState

from ui.assets import Assets
from ui.fonts import Fonts

from constants import BLACK, WHITE, HUD_TOP_MARGIN


class Renderer:

    def __init__(
        self,
        screen: pygame.Surface,
        world_width: int,
        world_height: int,
    ):

        self._screen = screen

        self._world_width = world_width
        self._world_height = world_height

        # World rendered at native resolution.
        self._world = pygame.Surface(
            (world_width, world_height)
        )

    # ==================================================
    # Public
    # ==================================================

    def draw(
        self,
        state: RenderState,
        scale: float,
        offset_x: float,
        offset_y: float,
    ):

        self._draw_world(state)

        scaled = pygame.transform.smoothscale(
            self._world,
            (
                int(self._world_width * scale),
                int(self._world_height * scale),
            ),
        )

        self._screen.fill(BLACK)

        self._screen.blit(
            scaled,
            (
                int(offset_x),
                int(offset_y),
            ),
        )

    # ==================================================
    # World
    # ==================================================

    def _draw_world(
        self,
        state: RenderState,
    ):

        self._world.fill(BLACK)

        self._draw_background(state)
        self._draw_npcs(state)
        self._draw_hud(state)
        self._draw_overlay(state)

    # --------------------------------------------------

    def _draw_background(
        self,
        state: RenderState,
    ):

        if state.background is None:
            return

        background = Assets.get_background(
            state.background
        )

        self._world.blit(
            background,
            (0, 0),
        )

    # --------------------------------------------------

    def _draw_npcs(
        self,
        state: RenderState,
    ):

        for npc in state.npcs:

            sprite = Assets.get_sprite(
                npc.sprite
            )

            rect = sprite.get_rect()

            rect.midtop = npc.position

            self._world.blit(
                sprite,
                rect,
            )

    # --------------------------------------------------

    def _draw_hud(
        self,
        state: RenderState,
    ):

        if not state.clock:
            return

        text = Fonts.clock.render(
            state.clock,
            True,
            (240, 240, 240)
        )

        text.set_alpha(170)

        rect = text.get_rect(
            midtop=(
                self._world_width // 2,
                HUD_TOP_MARGIN
            )
        )

        self._world.blit(text, rect)
        
        shadow = Fonts.clock.render(
            state.clock,
            True,
            (0, 0, 0)
        )

        shadow.set_alpha(100)

        shadow_rect = shadow.get_rect(
            midtop=(
                self._world_width // 2 + 2,
                HUD_TOP_MARGIN + 2
            )
        )

        self._world.blit(shadow, shadow_rect)

    # --------------------------------------------------

    def _draw_overlay(
        self,
        state: RenderState,
    ):

        if state.overlay is None:
            return

        state.overlay.draw(
            self._world
        )