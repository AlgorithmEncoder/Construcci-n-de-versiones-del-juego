class Navigation:

    def __init__(self):

        self._history = []

    def push(self, state):

        self._history.append(state)

    def pop(self):

        if self._history:

            return self._history.pop()

        return None

    @property
    def can_go_back(self):

        return len(self._history) > 0