"""
stats_view.py

Statistics view.

Displays global investigation statistics and the statistics
of one selected unlocked memory.

The two columns scroll independently.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts
from launcher import styles
from icons import draw_chevron_down


class StatsView:

    # ==================================================
    # Layout
    # ==================================================

    CARD_HEIGHT = 72
    CARD_GAP = 10

    COLUMN_GAP = 18

    SCROLL_STEP = 12
    SCROLL_BAR_WIDTH = 4
    SCROLL_BAR_MIN_HEIGHT = 30

    # ==================================================
    # Construction
    # ==================================================

    def __init__(self, stats):

        self._stats = stats

        # ----------------------------------------------
        # Memory selector
        # ----------------------------------------------

        self._selected_memory = None
        self._selector_open = False

        self._selector_rect = pygame.Rect(
            0,
            0,
            0,
            0
        )

        self._selector_options_rects = []

        # ----------------------------------------------
        # Global scroll
        # ----------------------------------------------

        self._global_scroll = 0

        self._global_content_rect = pygame.Rect(
            0,
            0,
            0,
            0
        )

        self._global_content_height = 0
        self._global_visible_height = 0

        # ----------------------------------------------
        # Memory scroll
        # ----------------------------------------------

        self._memory_scroll = 0

        self._memory_content_rect = pygame.Rect(
            0,
            0,
            0,
            0
        )

        self._memory_content_height = 0
        self._memory_visible_height = 0

    # ==================================================
    # Public API
    # ==================================================

    def update(self, dt):
        pass

    # --------------------------------------------------

    def draw(
        self,
        screen,
        area
    ):

        pygame.draw.rect(
            screen,
            styles.BACKGROUND,
            area
        )

        # ==================================================
        # Fixed header
        # ==================================================

        self._draw_header(
            screen,
            area
        )

        # ==================================================
        # Columns
        # ==================================================

        columns_top = (
            area.y +
            92
        )

        columns_height = (
            area.bottom -
            columns_top -
            10
        )

        column_width = (
            area.width -
            self.COLUMN_GAP
        ) // 2

        global_area = pygame.Rect(
            area.x,
            columns_top,
            column_width,
            columns_height
        )

        memory_area = pygame.Rect(
            global_area.right +
            self.COLUMN_GAP,
            columns_top,
            column_width,
            columns_height
        )

        # ==================================================
        # Column backgrounds
        # ==================================================

        pygame.draw.rect(
            screen,
            styles.PANEL,
            global_area,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            styles.PANEL,
            memory_area,
            border_radius=10
        )

        # ==================================================
        # Vertical divider
        # ==================================================

        divider_x = (
            global_area.right +
            self.COLUMN_GAP // 2
        )

        pygame.draw.line(
            screen,
            styles.BORDER,
            (
                divider_x,
                columns_top + 6
            ),
            (
                divider_x,
                columns_top +
                columns_height -
                6
            ),
            1
        )

        # ==================================================
        # Global statistics
        # ==================================================

        self._draw_global_column(
            screen,
            global_area
        )

        # ==================================================
        # Memory statistics
        # ==================================================

        self._draw_memory_column(
            screen,
            memory_area
        )

        # ==================================================
        # Selector dropdown
        #
        # Draw last so it appears above the memory
        # scrollable content.
        # ==================================================

        if self._selector_open:

            self._draw_selector_options(
                screen
            )

    # ==================================================
    # Events
    # ==================================================

    def handle_event(
        self,
        event
    ):

        # ==================================================
        # Mouse wheel
        # ==================================================

        if event.type == pygame.MOUSEWHEEL:

            mouse_pos = pygame.mouse.get_pos()

            # Selector is open: scrolling over it should
            # not scroll either statistics column.
            if (
                self._selector_open and
                self._selector_rect.collidepoint(
                    mouse_pos
                )
            ):
                return True

            if self._global_content_rect.collidepoint(
                mouse_pos
            ):

                self._global_scroll -= (
                    event.y *
                    self.SCROLL_STEP
                )

                self._clamp_global_scroll()

                return True

            if self._memory_content_rect.collidepoint(
                mouse_pos
            ):

                self._memory_scroll -= (
                    event.y *
                    self.SCROLL_STEP
                )

                self._clamp_memory_scroll()

                return True

            return False

        # ==================================================
        # Keyboard
        # ==================================================

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if self._selector_open:

                    self._selector_open = False

                    return True

                return False

            if event.key in (
                pygame.K_UP,
                pygame.K_DOWN,
                pygame.K_PAGEUP,
                pygame.K_PAGEDOWN,
                pygame.K_HOME,
                pygame.K_END
            ):

                mouse_pos = pygame.mouse.get_pos()

                if self._global_content_rect.collidepoint(
                    mouse_pos
                ):

                    self._handle_scroll_key(
                        event.key,
                        global_column=True
                    )

                    return True

                if self._memory_content_rect.collidepoint(
                    mouse_pos
                ):

                    self._handle_scroll_key(
                        event.key,
                        global_column=False
                    )

                    return True

        # ==================================================
        # Mouse click
        # ==================================================

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        # ----------------------------------------------
        # Selector
        # ----------------------------------------------

        if self._selector_open:

            for memory, rect in self._selector_options_rects:

                if rect.collidepoint(event.pos):

                    self._selected_memory = memory
                    self._selector_open = False

                    self._memory_scroll = 0

                    return True

            if not self._selector_rect.collidepoint(
                event.pos
            ):

                self._selector_open = False

                return True

        elif self._selector_rect.collidepoint(
            event.pos
        ):

            self._selector_open = True

            return True

        return False

    # ==================================================
    # Header
    # ==================================================

    def _draw_header(
        self,
        screen,
        area
    ):

        title = Fonts.title.render(
            "Estadísticas",
            True,
            styles.TEXT
        )

        screen.blit(
            title,
            (
                area.x + 10,
                area.y + 10
            )
        )

        subtitle = Fonts.small.render(
            "Resumen de tu investigación",
            True,
            styles.TEXT_SECONDARY
        )

        screen.blit(
            subtitle,
            (
                area.x + 10,
                area.y + 50
            )
        )
    
    def _draw_memory_header(
        self,
        screen,
        area,
        separator_y
    ):

        y = separator_y + 18

        # ==================================================
        # Title
        # ==================================================

        title = Fonts.default.render(
            "Memoria",
            True,
            styles.TEXT
        )

        screen.blit(
            title,
            (
                area.x + 14,
                y
            )
        )

        # ==================================================
        # Selector
        # ==================================================

        self._draw_memory_selector(
            screen,
            area,
            y
        )

        # ==================================================
        # Subtitle
        # ==================================================

        subtitle_y = (
            y +
            title.get_height() +
            8
        )

        memory_title = self._stats.get_title(
            self._selected_memory
        )

        subtitle = Fonts.small.render(
            f"Estadísticas de {memory_title}",
            True,
            styles.TEXT_SECONDARY
        )

        screen.blit(
            subtitle,
            (
                area.x + 14,
                subtitle_y
            )
        )

        return (
            subtitle_y +
            subtitle.get_height()
        )

    # ==================================================
    # Global column
    # ==================================================

    def _draw_global_column(
        self,
        screen,
        area
    ):

        title_y = area.y + 16

        y = self._draw_section_title(
            screen,
            "Global",
            "Resumen de toda la investigación",
            area.x + 14,
            title_y
        )

        content_top = (
            y + 12
        )

        content_rect = pygame.Rect(
            area.x + 10,
            content_top,
            area.width - 20,
            area.bottom -
            content_top -
            10
        )

        self._global_content_rect = content_rect

        cards = self._get_global_cards()

        self._global_content_height = (
            self._calculate_cards_height(
                cards
            )
        )

        self._global_visible_height = (
            content_rect.height
        )

        self._clamp_global_scroll()

        old_clip = screen.get_clip()

        screen.set_clip(
            content_rect
        )

        self._draw_cards(
            screen,
            content_rect,
            -self._global_scroll,
            cards
        )

        screen.set_clip(
            old_clip
        )

        self._draw_scroll_indicator(
            screen,
            content_rect,
            self._global_content_height,
            self._global_visible_height,
            self._global_scroll
        )

    # ==================================================
    # Memory column
    # ==================================================

    def _draw_memory_column(
        self,
        screen,
        area
    ):

        # ----------------------------------------------
        # Available memories
        # ----------------------------------------------

        memories = self._unlocked_memories()

        # ----------------------------------------------
        # No memory selected
        # ----------------------------------------------

        if not memories:
            self._memory_content_rect = pygame.Rect(
                area.x,
                area.y,
                area.width,
                0
            )

            self._memory_content_height = 0
            self._memory_visible_height = 0

            self._draw_memory_header(
                screen,
                area,
                area.y
            )

            self._draw_empty_memory(
                screen,
                area,
                area.y + 70
            )

            return

        # ----------------------------------------------
        # Select memory BEFORE drawing header
        # ----------------------------------------------

        if self._selected_memory not in memories:
            self._selected_memory = memories[0]

        # ----------------------------------------------
        # Header
        # ----------------------------------------------

        y = self._draw_memory_header(
                screen,
                area,
                area.y
            )

        # ----------------------------------------------
        # Scrollable content
        # ----------------------------------------------

        content_top = (
            y +
            14
        )

        content_rect = pygame.Rect(
            area.x + 10,
            content_top,
            area.width - 20,
            area.bottom -
            content_top -
            10
        )

        self._memory_content_rect = content_rect

        cards = self._get_memory_cards()

        self._memory_content_height = (
            self._calculate_cards_height(
                cards
            )
        )

        self._memory_visible_height = (
            content_rect.height
        )

        self._clamp_memory_scroll()

        old_clip = screen.get_clip()

        screen.set_clip(
            content_rect
        )

        self._draw_cards(
            screen,
            content_rect,
            -self._memory_scroll,
            cards
        )

        screen.set_clip(
            old_clip
        )

        self._draw_scroll_indicator(
            screen,
            content_rect,
            self._memory_content_height,
            self._memory_visible_height,
            self._memory_scroll
        )

    # ==================================================
    # Section title
    # ==================================================

    def _draw_section_title(
        self,
        screen,
        title,
        subtitle,
        x,
        y
    ):

        title_surface = Fonts.default.render(
            title,
            True,
            styles.TEXT
        )

        screen.blit(
            title_surface,
            (
                x,
                y
            )
        )

        subtitle_surface = Fonts.small.render(
            subtitle,
            True,
            styles.TEXT_SECONDARY
        )

        screen.blit(
            subtitle_surface,
            (
                x,
                y + 28
            )
        )

        return (
            y +
            title_surface.get_height() +
            28 +
            subtitle_surface.get_height()
        )

    # ==================================================
    # Memory selector
    # ==================================================

    def _draw_memory_selector(
        self,
        screen,
        area,
        y
    ):

        selector_width = 220
        selector_height = 34

        rect = pygame.Rect(
            area.right - selector_width - 10,
            y,
            selector_width,
            selector_height
        )

        self._selector_rect = rect

        pygame.draw.rect(
            screen,
            styles.PANEL,
            rect,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            styles.BORDER,
            rect,
            width=1,
            border_radius=6
        )

        title = self._memory_display_name(
            self._selected_memory
        )

        text = Fonts.default.render(
            title,
            True,
            styles.TEXT
        )

        text_rect = text.get_rect(
            midleft=(
                rect.x + 12,
                rect.centery
            )
        )

        screen.blit(
            text,
            text_rect
        )

        # Flecha
        arrow_rect = pygame.Rect(
            0,
            0,
            16,
            16
        )

        arrow_rect.midright = (
            rect.right - 10,
            rect.centery
        )

        draw_chevron_down(
            screen,
            arrow_rect,
            styles.TEXT_SECONDARY
        )

    # --------------------------------------------------

    def _draw_selector_options(
        self,
        screen
    ):

        memories = self._unlocked_memories()

        if not memories:
            return

        self._selector_options_rects = []

        width = self._selector_rect.width
        height = 36

        x = self._selector_rect.x
        y = self._selector_rect.bottom + 3

        for memory in memories:

            rect = pygame.Rect(
                x,
                y,
                width,
                height
            )

            pygame.draw.rect(
                screen,
                styles.PANEL,
                rect,
                border_radius=5
            )

            pygame.draw.rect(
                screen,
                styles.BORDER,
                rect,
                width=1,
                border_radius=5
            )

            text = Fonts.small.render(
                self._memory_display_name(
                    memory
                ),
                True,
                styles.TEXT
            )

            text_rect = text.get_rect(
                midleft=(
                    rect.x + 10,
                    rect.centery
                )
            )

            screen.blit(
                text,
                text_rect
            )

            self._selector_options_rects.append(
                (
                    memory,
                    rect
                )
            )

            y += height + 3

    # ==================================================
    # Cards
    # ==================================================

    def _draw_cards(
        self,
        screen,
        area,
        offset_y,
        cards
    ):

        columns = 2
        gap = 10

        width = (
            area.width -
            gap
        ) // columns

        for index, (
            label,
            value
        ) in enumerate(cards):

            row = (
                index //
                columns
            )

            column = (
                index %
                columns
            )

            x = (
                area.x +
                column *
                (
                    width +
                    gap
                )
            )

            card_y = (
                area.y +
                offset_y +
                row *
                (
                    self.CARD_HEIGHT +
                    self.CARD_GAP
                )
            )

            self._draw_card(
                screen,
                pygame.Rect(
                    x,
                    card_y,
                    width,
                    self.CARD_HEIGHT
                ),
                label,
                value
            )

    # --------------------------------------------------

    def _draw_card(
        self,
        screen,
        rect,
        label,
        value
    ):

        pygame.draw.rect(
            screen,
            styles.BACKGROUND,
            rect,
            border_radius=8
        )

        label_surface = Fonts.small.render(
            str(label),
            True,
            styles.TEXT_SECONDARY
        )

        screen.blit(
            label_surface,
            (
                rect.x + 12,
                rect.y + 10
            )
        )

        value_surface = Fonts.default.render(
            str(value),
            True,
            styles.TEXT
        )

        value_rect = value_surface.get_rect(
            midleft=(
                rect.x + 12,
                rect.y + 45
            )
        )

        screen.blit(
            value_surface,
            value_rect
        )

    # ==================================================
    # Empty memory
    # ==================================================

    def _draw_empty_memory(
        self,
        screen,
        area,
        y
    ):

        text = Fonts.default.render(
            "No hay memorias desbloqueadas.",
            True,
            styles.TEXT_SECONDARY
        )

        rect = text.get_rect(
            center=(
                area.centerx,
                y + 70
            )
        )

        screen.blit(
            text,
            rect
        )

    # ==================================================
    # Scroll
    # ==================================================

    def _calculate_cards_height(
        self,
        cards
    ):

        if not cards:
            return 0

        columns = 2

        rows = (
            len(cards) +
            columns -
            1
        ) // columns

        return (
            rows *
            self.CARD_HEIGHT
            +
            max(
                0,
                rows - 1
            ) *
            self.CARD_GAP
        )

    # --------------------------------------------------

    def _draw_scroll_indicator(
        self,
        screen,
        area,
        content_height,
        visible_height,
        scroll
    ):

        if content_height <= visible_height:
            return

        track = pygame.Rect(
            area.right - 5,
            area.y,
            self.SCROLL_BAR_WIDTH,
            area.height
        )

        pygame.draw.rect(
            screen,
            styles.SIDEBAR,
            track,
            border_radius=2
        )

        visible_ratio = (
            visible_height /
            content_height
        )

        thumb_height = max(
            self.SCROLL_BAR_MIN_HEIGHT,
            int(
                track.height *
                visible_ratio
            )
        )

        max_scroll = (
            content_height -
            visible_height
        )

        scroll_ratio = (
            scroll /
            max_scroll
        ) if max_scroll > 0 else 0

        thumb_y = (
            track.y +
            int(
                (
                    track.height -
                    thumb_height
                ) *
                scroll_ratio
            )
        )

        thumb = pygame.Rect(
            track.x,
            thumb_y,
            track.width,
            thumb_height
        )

        pygame.draw.rect(
            screen,
            styles.PRIMARY,
            thumb,
            border_radius=2
        )

    # --------------------------------------------------

    def _handle_scroll_key(
        self,
        key,
        global_column
    ):

        if global_column:

            scroll = self._global_scroll
            visible = self._global_visible_height
            content = self._global_content_height

        else:

            scroll = self._memory_scroll
            visible = self._memory_visible_height
            content = self._memory_content_height

        max_scroll = max(
            0,
            content - visible
        )

        if key == pygame.K_UP:

            scroll -= self.SCROLL_STEP

        elif key == pygame.K_DOWN:

            scroll += self.SCROLL_STEP

        elif key == pygame.K_PAGEUP:

            scroll -= visible

        elif key == pygame.K_PAGEDOWN:

            scroll += visible

        elif key == pygame.K_HOME:

            scroll = 0

        elif key == pygame.K_END:

            scroll = max_scroll

        scroll = max(
            0,
            min(
                scroll,
                max_scroll
            )
        )

        if global_column:

            self._global_scroll = scroll

        else:

            self._memory_scroll = scroll

    # --------------------------------------------------

    def _clamp_global_scroll(self):

        max_scroll = max(
            0,
            self._global_content_height -
            self._global_visible_height
        )

        self._global_scroll = max(
            0,
            min(
                self._global_scroll,
                max_scroll
            )
        )

    # --------------------------------------------------

    def _clamp_memory_scroll(self):

        max_scroll = max(
            0,
            self._memory_content_height -
            self._memory_visible_height
        )

        self._memory_scroll = max(
            0,
            min(
                self._memory_scroll,
                max_scroll
            )
        )

    # ==================================================
    # Data
    # ==================================================

    def _get_global_cards(self):

        stats = self._stats.global_stats

        return [

            (
                "Incursiones",
                stats.get(
                    "incursions",
                    0
                )
            ),

            (
                "Memorias completadas",
                stats.get(
                    "completed_memories",
                    0
                )
            ),

            (
                "Iteraciones",
                stats.get(
                    "iterations",
                    0
                )
            ),

            (
                "Tiempo jugado",
                self._format_seconds(
                    stats.get(
                        "total_played",
                        0
                    )
                )
            ),

            (
                "Habitaciones visitadas",
                stats.get(
                    "rooms_visited",
                    0
                )
            ),

            (
                "Documentos abiertos",
                stats.get(
                    "documents_opened",
                    0
                )
            ),

            (
                "Ordenadores consultados",
                stats.get(
                    "computers_opened",
                    0
                )
            ),

            (
                "Conversaciones consultadas",
                stats.get(
                    "chats_opened",
                    0
                )
            ),

            (
                "Correos leídos",
                stats.get(
                    "emails_read",
                    0
                )
            ),

            (
                "Archivos abiertos",
                stats.get(
                    "files_opened",
                    0
                )
            ),

            (
                "Detecciones",
                stats.get(
                    "detections",
                    0
                )
            ),
        ]

    # --------------------------------------------------

    def _get_memory_cards(self):

        if self._selected_memory is None:
            return []

        stats = self._stats.get(
            self._selected_memory
        )

        if stats is None:
            return []

        progress = stats.get(
            "progress",
            {}
        )

        played = stats.get(
            "played",
            {}
        )

        exploration = stats.get(
            "exploration",
            {}
        )

        detection = stats.get(
            "detection",
            {}
        )

        return [

            (
                "Progreso",
                f"{progress.get('discovered', 0)} / "
                f"{progress.get('total', 0)} "
                f"({progress.get('percent', 0)}%)"
            ),

            (
                "Incursiones",
                played.get(
                    "times_incursion",
                    0
                )
            ),

            (
                "Iteraciones",
                played.get(
                    "iterations",
                    0
                )
            ),

            (
                "Tiempo jugado",
                self._format_seconds(
                    played.get(
                        "total_played",
                        0
                    )
                )
            ),

            (
                "Última partida",
                played.get(
                    "last_played",
                    "Nunca"
                )
            ),

            (
                "Habitaciones visitadas",
                exploration.get(
                    "rooms_visited",
                    0
                )
            ),

            (
                "Documentos abiertos",
                exploration.get(
                    "documents_opened",
                    0
                )
            ),

            (
                "Ordenadores consultados",
                exploration.get(
                    "computers_opened",
                    0
                )
            ),

            (
                "Conversaciones consultadas",
                exploration.get(
                    "chats_opened",
                    0
                )
            ),

            (
                "Correos leídos",
                exploration.get(
                    "emails_read",
                    0
                )
            ),

            (
                "Archivos abiertos",
                exploration.get(
                    "files_opened",
                    0
                )
            ),

            (
                "Detecciones",
                detection.get(
                    "total",
                    0
                )
            ),
        ]

    # ==================================================
    # Memories
    # ==================================================

    def _unlocked_memories(self):

        memories = []

        for memory in self._stats.memories:

            stats = self._stats.get(
                memory
            )

            state = stats.get(
                "state",
                {}
            )

            if not state.get(
                "locked",
                False
            ):

                memories.append(
                    memory
                )

        return memories

    # --------------------------------------------------

    def _memory_display_name(
        self,
        memory
    ):

        if memory is None:
            return "Sin memoria seleccionada"

        try:

            return self._stats.get_title(
                memory
            )

        except AttributeError:

            return str(memory)

    # ==================================================
    # Formatting
    # ==================================================

    def _format_seconds(
        self,
        seconds
    ):

        try:

            seconds = int(
                seconds
            )

        except (
            TypeError,
            ValueError
        ):

            return "0 s"

        hours = seconds // 3600
        minutes = (
            seconds % 3600
        ) // 60
        remaining = seconds % 60

        if hours > 0:

            return (
                f"{hours} h "
                f"{minutes:02d} min"
            )

        if minutes > 0:

            return (
                f"{minutes} min "
                f"{remaining:02d} s"
            )

        return f"{remaining} s"
    
    def refresh(self):
        self._stats.refresh()