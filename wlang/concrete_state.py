from wlang.int import State


class ConcreteState(State):
    def __init__(self, env=None, is_error=False):
        super().__init__(env)
        if is_error:
            self._is_error = True
        else:
            self._is_error = False

    def is_error(self):
        return self._is_error

    def mark_error(self):
        self._is_error = True

    def update_variables(self, variable_name: str, value: int):
        self.env[variable_name] = value

    def copy(self):
        return ConcreteState(env=self.env.copy(), is_error=self._is_error)
