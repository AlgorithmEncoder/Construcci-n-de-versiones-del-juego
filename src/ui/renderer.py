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

from icons import draw_note, draw_iterations

from game import styles


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

        self._exit_rect = pygame.Rect(
            0, 0, 0, 0
        )

        self._quick_note_rect = pygame.Rect(
            0, 0, 0, 0
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

        self._screen.fill(
            styles.BACKGROUND
        )

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

        self._world.fill(
            styles.WORLD_BACKGROUND
        )

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

    # ==================================================
    # HUD
    # ==================================================

    def _draw_hud(
        self,
        state: RenderState,
    ):

        if not state.clock:
            return

        # ==================================================
        # Clock
        # ==================================================

        shadow = Fonts.clock.render(
            state.clock,
            True,
            styles.HUD_CLOCK_SHADOW,
        )

        shadow.set_alpha(
            styles.HUD_CLOCK_SHADOW_ALPHA
        )

        shadow_rect = shadow.get_rect(
            midtop=(
                self._world_width // 2 + 2,
                styles.HUD_TOP_MARGIN + 2,
            )
        )

        self._world.blit(
            shadow,
            shadow_rect,
        )

        text = Fonts.clock.render(
            state.clock,
            True,
            styles.HUD_CLOCK_TEXT,
        )

        text.set_alpha(
            styles.HUD_CLOCK_TEXT_ALPHA
        )

        rect = text.get_rect(
            midtop=(
                self._world_width // 2,
                styles.HUD_TOP_MARGIN,
            )
        )

        self._world.blit(
            text,
            rect,
        )

        # ==================================================
        # Iterations
        # ==================================================

        iterations_rect = pygame.Rect(
            0,
            0,
            95,
            self._exit_rect.height,
        )

        iterations_rect.topright = (
            self._exit_rect.left - 12,
            styles.HUD_TOP_MARGIN,
        )

        badge = pygame.Surface(
            iterations_rect.size,
            pygame.SRCALPHA,
        )

        pygame.draw.rect(
            badge,
            (
                *styles.HUD_BADGE_BACKGROUND,
                styles.HUD_BADGE_BACKGROUND_ALPHA,
            ),
            badge.get_rect(),
            border_radius=8,
        )

        pygame.draw.rect(
            badge,
            (
                *styles.HUD_BADGE_BORDER,
                styles.HUD_BADGE_BORDER_ALPHA,
            ),
            badge.get_rect(),
            width=1,
            border_radius=8,
        )

        self._world.blit(
            badge,
            iterations_rect,
        )

        icon_rect = pygame.Rect(
            iterations_rect.x + 8,
            iterations_rect.y + 8,
            18,
            18,
        )

        draw_iterations(
            self._world,
            icon_rect,
            styles.HUD_BADGE_ICON,
        )

        count = Fonts.default.render(
            f"x {state.iterations}",
            True,
            styles.HUD_BADGE_TEXT,
        )

        count.set_alpha(
            styles.HUD_BADGE_TEXT_ALPHA
        )

        self._world.blit(
            count,
            (
                iterations_rect.x + 34,
                iterations_rect.y + 8,
            ),
        )

        # ==================================================
        # Exit
        # ==================================================

        self._exit_rect.topright = (
            self._world_width // 3,
            styles.HUD_TOP_MARGIN,
        )

        self._draw_button(
            self._world,
            self._exit_rect,
            "Abandonar sueño",
        )

        # ==================================================
        # Quick note
        # ==================================================

        self._quick_note_rect.topright = (
            self._world_width - styles.HUD_LEFT_MARGIN,
            styles.HUD_TOP_MARGIN,
        )

        self._draw_button(
            self._world,
            self._quick_note_rect,
            "Nota",
            icon=draw_note,
        )

    # ==================================================
    # Overlay
    # ==================================================

    def _draw_overlay(
        self,
        state: RenderState,
    ):

        if state.overlay is None:
            return

        state.overlay.draw(
            self._world
        )

    # ==================================================
    # Buttons
    # ==================================================

    def _draw_button(
        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        text: str,
        icon=None,
    ):

        image = Fonts.default.render(
            text,
            True,
            styles.BUTTON_TEXT,
        )

        icon_size = 18
        icon_gap = 8

        icon_width = (
            icon_size + icon_gap
            if icon is not None
            else 0
        )

        padding_x = 16
        padding_y = 8

        rect.size = (
            image.get_width()
            + icon_width
            + padding_x * 2,
            image.get_height()
            + padding_y * 2,
        )

        pygame.draw.rect(
            surface,
            styles.BUTTON,
            rect,
            border_radius=styles.BUTTON_RADIUS,
        )

        pygame.draw.rect(
            surface,
            styles.BUTTON_BORDER,
            rect,
            width=styles.BUTTON_BORDER_WIDTH,
            border_radius=styles.BUTTON_RADIUS,
        )

        # --------------------------------------------------
        # Icon
        # --------------------------------------------------

        start_x = rect.x + padding_x

        if icon is not None:

            icon_rect = pygame.Rect(
                start_x,
                rect.centery - icon_size // 2,
                icon_size,
                icon_size,
            )

            icon(
                surface,
                icon_rect,
                styles.BUTTON_TEXT,
            )

            start_x += icon_width

        # --------------------------------------------------
        # Text
        # --------------------------------------------------

        text_rect = image.get_rect(
            midleft=(
                start_x,
                rect.centery,
            )
        )

        surface.blit(
            image,
            text_rect,
        )

    # ==================================================
    # Hit detection
    # ==================================================

    def exit_button_at(
        self,
        position,
    ):

        return self._exit_rect.collidepoint(
            position
        )

    def quick_note_button_at(
        self,
        position,
    ):

        return self._quick_note_rect.collidepoint(
            position
        )