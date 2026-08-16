"""
Main launcher window.
"""

from __future__ import annotations

import pygame

from launcher.header import Header
from launcher.sidebar import Sidebar
from launcher.workspace import Workspace
from launcher.footer import Footer

from launcher.navigation import Navigation
from launcher.dream_manager import DreamManager

from launcher.widgets.empty_view import EmptyView

from launcher.home.views.incursions.incursions_view import (
    IncursionsView
)
from launcher.home.views.incursions.incursion_detail import IncursionDetail
from launcher import styles

from launcher.home.notes.notes_manager import NotesManager
from launcher.home.views.notes.notes_view import NotesView
from launcher.profile.views.activity_view import ActivityView
from launcher.profile.views.stats_view import StatsView
from launcher.profile.views.achievements_view import AchievementsView
from launcher.settings.views.general import GeneralView
from launcher.settings.views.display import DisplayView
from launcher.settings.views.language import LanguageView
from launcher.settings.views.accessibility import AccessibilityView

from launcher.profile.stats.stats_manager import StatsManager
from launcher.profile.achievements.achievement import AchievementsManager
from launcher.settings.settings_manager import SettingsManager
from launcher.settings.language_manager import LanguageManager


class MainWindow:

    def __init__(self, screen: pygame.Surface, logger):

        self._screen = screen
        self._logger = logger
        
        self._start_requested = None
        self._running = True
        
        self._settings = SettingsManager()
        self._language = LanguageManager(self._settings)

        self._header = Header(self._language)
        self._sidebar = Sidebar(self._language)
        self._workspace = Workspace()
        self._footer = Footer(self._language)

        self._navigation = Navigation()

        self._dreams = DreamManager()
        self._dreams.load()
        self._notes = NotesManager(self._logger.register)
        self._notes_view = NotesView(self._notes, self._language)
        
        self._stats = StatsManager()
        self._achievements = AchievementsManager( self._stats )
        
        self._apply_launcher_theme()
        
        self._sections = {
            "incursions": IncursionsView(self),
            "notes": self._notes_view,
            "inventory": EmptyView(),
            "stats": StatsView(self._stats),
            "achievements": AchievementsView(self._achievements),
            "activity": ActivityView(self._logger, self._language),
            "general": GeneralView(self._settings),
            "display": DisplayView(self._settings),
            "audio": EmptyView(),
            "language": LanguageView(self._settings),
            "accessibility": AccessibilityView(self._settings)
        }
        
        self._workspace.set_view(
            self._sections["incursions"]
        )

        self._module = "home"
        self._section = "incursions"

        self._start_requested = None
        
        self._calculate_layout()
    
    # --------------------------------------------------

    def _calculate_layout(self):

        width = self._screen.get_width()
        height = self._screen.get_height()

        # ==================================================
        # Header
        # ==================================================

        self._header_rect = pygame.Rect(
            0,
            0,
            width,
            styles.HEADER_HEIGHT
        )

        # ==================================================
        # Footer
        # ==================================================

        self._footer_rect = pygame.Rect(
            0,
            height - styles.FOOTER_HEIGHT,
            width,
            styles.FOOTER_HEIGHT
        )

        # ==================================================
        # Sidebar
        # ==================================================

        content_height = (
            height
            - styles.HEADER_HEIGHT
            - styles.FOOTER_HEIGHT
        )

        self._sidebar_rect = pygame.Rect(
            0,
            styles.HEADER_HEIGHT,
            styles.SIDEBAR_WIDTH,
            content_height
        )

        # ==================================================
        # Workspace
        # ==================================================

        self._workspace_rect = pygame.Rect(
            styles.SIDEBAR_WIDTH,
            styles.HEADER_HEIGHT,
            width - styles.SIDEBAR_WIDTH,
            content_height
        )

    # --------------------------------------------------

    def update(self, dt):
        
        if self._workspace.current:

            self._workspace.current.update(dt)

    # --------------------------------------------------

    def draw(self):

        self._header.draw(
            self._screen,
            self._header_rect,
            self._module
        )

        self._sidebar.draw(
            self._screen,
            self._sidebar_rect,
            self._module,
            self._section
        )

        self._workspace.draw(
            self._screen,
            self._workspace_rect
        )

        self._footer.draw(
            self._screen,
            self._footer_rect
        )

    # --------------------------------------------------

    def handle_event(self, event):
        
        # HEADER ------------
        module = self._header.handle_event(event)

        if module:

            self._change_module(module)

            return True
        
        # SIDEBAR ----------------
        section = self._sidebar.handle_event(event)

        if section:

            self._change_section(section)

            return True
        
        # CONTENT -------------

        handled = self._workspace.handle_event(event)

        view = self._workspace.current

        if isinstance(view, IncursionDetail) or isinstance(view, IncursionsView):

            result = handled

            if result is None or result is False:
                return False

            if result == True:
                return True

            action, data = result

            if action == "back":

                previous = self._navigation.back()

                if previous:

                    self._workspace.set_view(previous)

                return True

            if action == "start":

                self._start_requested = data

                return True
            
            if action == "open":

                self._navigation.push(
                    view
                )

                self._workspace.set_view(
                    IncursionDetail(
                        self._dreams,
                        data["id"]
                    )
                )
        
        elif isinstance(view, NotesView):

            result = handled

            if result is None:
                return False

        return handled
    
    def _change_section(self, section):
        
        current_view = self._workspace.current
        if hasattr(current_view, "save"):
            current_view.save()

        valid_sections = {
            key
            for key in self._sidebar.MODULES[self._module]
        }

        if section not in valid_sections:
            return False

        view = self._sections.get(section)

        if view is None:
            return False

        self._section = section
        self._workspace.set_view(view)

        return True
    
    def _change_module(self, module):

        if not self._sidebar.set_module(module):
            return False

        self._module = module
        self._sidebar.update(self._sidebar_rect)

        first_section = self._sidebar.MODULES[module][0][0]
        self._change_section(first_section)
        
        return True

    # ==================================================

    @property
    def start_requested(self):
        return self._start_requested

    @property
    def running(self):
        return self._running
    
    @property
    def dreams(self):
        return self._dreams
    
    @property
    def notes(self):

        return self._notes

    @property
    def navigation(self):
        return self._navigation

    @property
    def workspace(self):
        return self._workspace

    @property
    def start_requested(self):
        return self._start_requested
    
    @property
    def display_settings(self):
        return self._sections["display"].settings

    # --------------------------------------------------

    def start_memory(self, memory):

        self._start_requested = memory
    
    def clear_requests(self):

        self._start_requested = None
    
    def refresh(self):
        
        self._dreams.load()
        self._notes.load()
        self._achievements.load()
        
        # Refresh views
        for view in self._sections.values():
            
            if hasattr(view, "refresh"):

                view.refresh()
        
        current_view = self._workspace.current
        if hasattr(current_view, "refresh"):
            current_view.refresh()
    
    def set_screen(self, screen):

        self._screen = screen
        self._calculate_layout()

        current_view = self._workspace.current

        if hasattr(current_view, "on_resize"):
            current_view.on_resize(
                self._workspace_rect
            )
        
        self._sidebar.update(self._sidebar_rect)
    
    def _apply_launcher_theme(self):

        theme = self._settings.get(
            "display"
        ).get(
            "launcher_theme",
            "default"
        )

        if not styles.set_theme(theme):

            styles.set_theme("default")