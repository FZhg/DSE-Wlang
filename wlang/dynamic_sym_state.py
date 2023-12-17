from z3 import z3

from wlang.concrete_state import ConcreteState
from wlang.sym_state import SymState


class ProgramState:
    def __init__(self, sym_state: SymState = None, concrete_state: ConcreteState = None, concrete_variables=None,
                 symbolic_variables=None):
        if sym_state is None:
            self.sym_state = SymState()
        else:
            self.sym_state = sym_state
        if concrete_state is None:
            self.concrete_state = ConcreteState()
        else:
            self.concrete_state = concrete_state
        if concrete_variables is not None:
            self._concrete_variables = concrete_variables
        else:
            self._concrete_variables = set()

        if symbolic_variables is not None:
            self._symbolic_variables = symbolic_variables
        else:
            self._symbolic_variables = set()

    def update_variable_concrete(self, variable_name: str, concrete_value: int):
        self.concrete_state.update_variables(variable_name, concrete_value)

    def update_variable_symbolic(self, variable_name: str, sym_expression):
        self.sym_state.update_variable(variable_name, sym_expression)

    def get_symbolic_state(self):
        return self.sym_state

    def get_concrete_state(self):
        return self.concrete_state


    def is_error(self):
        return self.sym_state.is_error() or self.concrete_state.is_error()

    def mark_error_concrete(self):
        self.concrete_state.mark_error()

    def mark_error_symbolic(self):
        self.sym_state.mk_error()

    def is_infeasible(self):
        return self.sym_state.is_empty()

    def fork(self, condition):
        """
        Fork the current state of the execution
        :param condition: the conditions is true for the current state
        :return: a copy of the current state with the negation of this condition
        """
        self.sym_state, new_sym_state = self.sym_state.fork()
        self.sym_state.add_pc(condition)
        new_sym_state.add_pc(z3.Not(condition))
        new_concrete_state = self.concrete_state.copy()
        new_state = ProgramState(new_sym_state, new_concrete_state, self._concrete_variables.copy(), self.
                                 _symbolic_variables.copy())
        new_state.concretize()
        return self, new_state

    def concretize(self):
        new_concrete_environment = self.sym_state.pick_concrete(*self._symbolic_variables)
        if not self.is_infeasible():
            self.concrete_state.env = self.concrete_state.env | new_concrete_environment  # new_concrete_state could be None

    def add_path_conditions(self, *exp):
        self.sym_state.add_pc(*exp)

    def is_any_variable_symbolic(self, *variable_names):
        for variable_name in variable_names:
            if variable_name in self._symbolic_variables:
                return True
        return False

    def mark_variable_concrete(self, variable_name):
        self._concrete_variables.add(variable_name)
        if variable_name in self._symbolic_variables:
            self._symbolic_variables.remove(variable_name)

    def mark_variable_symbolic(self, variable_name):
        self._symbolic_variables.add(variable_name)
        if variable_name in self._concrete_variables:
            self._concrete_variables.remove(variable_name)

    def __str__(self):
        return "sym_state:\n" + str(self.sym_state) + "\nconcrete_state:\n" + str(self.concrete_state)
