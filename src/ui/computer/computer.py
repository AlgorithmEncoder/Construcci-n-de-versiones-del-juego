"""
computer.py

Main computer UI.
"""

from __future__ import annotations

import pygame

from ui.overlay import Overlay

from . import styles

from .sidebar import Sidebar
from .widgets import draw_header

from .email_list import EmailList
from .email_view import EmailView

from .chat_list import ChatList
from .chat_view import ChatView

from .file_list import FileList
from .file_view import FileView
from .document_viewer import DocumentViewer

class ComputerUI(Overlay):

    def __init__(
        self,
        computer: dict,
        files_manager,
        world_width: int,
        world_height: int,
        progress_callback=None,
        activity_callback=None
    ):

        super().__init__(
            world_width=world_width,
            world_height=world_height,
            width=1000,
            height=650,
        )

        self._computer = computer

        self._sidebar = Sidebar()

        self._section = "emails"

        self._selected_email = None
        self._selected_chat = None
        self._selected_file = None

        self._email_list = EmailList()
        self._email_view = EmailView()

        self._chat_list = ChatList()
        self._chat_view = ChatView()

        self._file_list = FileList()
        self._file_view = FileView()
        
        self._files = files_manager
        self._document = None
        
        self._progress_callback = progress_callback
        self._activity_callback = activity_callback

    # ==================================================
    # Events
    # ==================================================

    def handle_event(self, event):
        
        if self._document is not None:

            handled = self._document.handle_event(event)

            if not self._document.visible:

                self._document = None

            return handled
        
        if event.type == pygame.MOUSEWHEEL:

            if self._section == "emails":

                if self._selected_email is None:
                    return self._email_list.handle_event(event)

                return self._email_view.handle_event(event)

            elif self._section == "chats":

                if self._selected_chat is None:
                    return self._chat_list.handle_event(event)

                return self._chat_view.handle_event(event)

            elif self._section == "files":

                if self._selected_file is None:
                    return self._file_list.handle_event(event)

                return self._file_view.handle_event(event)

            return False

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        # ---------------- Sidebar ----------------

        section = self._sidebar.handle_click(event.pos)

        if section is not None:

            self._section = section

            self._selected_email = None
            self._selected_chat = None
            self._selected_file = None

            return True

        # ---------------- Emails ----------------

        if self._section == "emails":

            emails = self._computer.get(
                "emails",
                []
            )

            if self._selected_email is None:
                
                if self._email_list.handle_event(event):
                    return True

                index = self._email_list.click(event.pos)

                if index is not None:

                    self._selected_email = index
                    
                    if self._progress_callback:

                        self._progress_callback(
                            emails[index]["id"]
                        )
                    
                    if self._activity_callback:

                        self._activity_callback(
                            f"Email consultado: {emails[index]['id']}",
                            category="discovery"
                        )

                    return True

            else:

                if self._email_view.click(event.pos):

                    self._selected_email = None

                    return True

        # ---------------- Chats ----------------

        elif self._section == "chats":

            chats = self._computer.get(
                "chats",
                []
            )

            if self._selected_chat is None:
                
                if self._chat_list.handle_event(event):
                    return True

                index = self._chat_list.click(event.pos)

                if index is not None:

                    self._selected_chat = index
                    
                    if self._progress_callback:

                        self._progress_callback(
                            chats[index]["id"]
                        )
                    
                    if self._activity_callback:

                        self._activity_callback(
                            f"Chat consultado: {chats[index]['id']}",
                            category="discovery"
                        )

                    return True

            else:

                if self._chat_view.click(event.pos):

                    self._selected_chat = None

                    return True

        # ---------------- Files ----------------

        elif self._section == "files":

            files = self._computer.get(
                "files",
                []
            )

            if self._selected_file is None:

                if self._file_list.handle_event(event):
                    return True

                index = self._file_list.click(event.pos)

                if index is not None:

                    self._selected_file = index
                    
                    self._progress_callback(
                        files[index]["document_id"]
                    )

                    return True

            else:

                action = self._file_view.click(event.pos)

                if action == "back":

                    self._selected_file = None

                    return True

                elif action == "open":

                    file = files[self._selected_file]

                    path = self._files.path(
                        file["document_id"]
                    )

                    if path is not None:

                        self._document = DocumentViewer.create(path)
                        
                        if self._activity_callback:

                            self._activity_callback(
                                f"Archivo consultado: {file['document_id']}",
                                category="discovery"
                            )


                    return True

        return False

    # ==================================================
    # Draw
    # ==================================================

    def _draw_content(self, screen):

        self._sidebar.draw(
            screen,
            self.panel,
            self._section
        )

        content = pygame.Rect(
            self.panel.x + styles.SIDEBAR_WIDTH,
            self.panel.y,
            self.panel.width - styles.SIDEBAR_WIDTH,
            self.panel.height
        )

        pygame.draw.rect(
            screen,
            styles.PANEL,
            content,
            border_top_right_radius=12,
            border_bottom_right_radius=12
        )

        header = pygame.Rect(
            content.x,
            content.y,
            content.width,
            styles.HEADER_HEIGHT
        )

        draw_header(
            screen,
            header,
            self._section.title()
        )

        # ==========================================
        # Emails
        # ==========================================

        if self._section == "emails":

            emails = self._computer.get(
                "emails",
                []
            )

            if self._selected_email is None:

                self._email_list.draw(
                    screen,
                    content,
                    emails
                )

            else:

                self._email_view.draw(
                    screen,
                    content,
                    emails[self._selected_email]
                )

        # ==========================================
        # Chats
        # ==========================================

        elif self._section == "chats":

            chats = self._computer.get(
                "chats",
                []
            )

            if self._selected_chat is None:

                self._chat_list.draw(
                    screen,
                    content,
                    chats
                )

            else:

                self._chat_view.draw(
                    screen,
                    content,
                    chats[self._selected_chat]
                )

        # ==========================================
        # Files
        # ==========================================

        elif self._section == "files":

            files = self._computer.get(
                "files",
                []
            )

            if self._selected_file is None:

                self._file_list.draw(
                    screen,
                    content,
                    files
                )

            else:

                if self._document is not None:

                    self._document.draw(
                        screen,
                        content
                    )

                else:

                    self._file_view.draw(
                        screen,
                        content,
                        files[self._selected_file]
                    )