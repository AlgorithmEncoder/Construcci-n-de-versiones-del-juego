"""
Workspace navigation history.
"""


class Navigation:

    def __init__(self):

        self._history = []

    # --------------------------------------------------

    def push(self, view):

        self._history.append(view)

    # --------------------------------------------------

    def back(self):

        if not self._history:
            return None

        return self._history.pop()

    # --------------------------------------------------

    @property
    def can_go_back(self):

        return bool(self._history)

    # --------------------------------------------------

    def clear(self):

        self._history.clear()