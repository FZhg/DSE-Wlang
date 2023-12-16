from wlang.int import State


class ConcreteState(State):
    def __init__(self):
        super().__init__()
        self._is_error = False

    def is_error(self):
        return self._is_error

    def mark_error(self):
        self._is_error = True

    def update_variables(self, variable_name: str, value: int):
        self.env[variable_name] = value
