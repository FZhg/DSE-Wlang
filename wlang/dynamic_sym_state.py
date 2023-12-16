from z3 import z3

from wlang.concrete_state import ConcreteState
from wlang.sym_state import SymState


class ProgramState:
    def __init__(self, sym_state: SymState = None, concrete_state: ConcreteState = None):
        if sym_state is None:
            self.sym_state = SymState()
        else:
            self.sym_state = sym_state
        if concrete_state is None:
            self.concrete_state = ConcreteState()
        else:
            self.concrete_state = concrete_state

    def update_variable_concrete(self, variable_name: str, concrete_value: int):
        self.concrete_state.update_variables(variable_name, concrete_value)

    def update_variable_symbolic(self, variable_name: str, sym_expression):
        self.sym_state.update_variable(variable_name, sym_expression)

    def get_sym_state(self):
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
        '''
        Fork the current state of the execution
        :param condition: the conditions is true for the current state
        :return: a copy of the current state with the negation of this condition
        '''
        _, new_sym_state = self.sym_state.fork()
        self.sym_state.add_pc(condition)
        new_sym_state.add_pc(z3.Not(condition))
        new_concrete_state = new_sym_state.pick_concrete()
        if new_concrete_state is None:
            return self, None  # infeasible
        new_state = ProgramState(new_sym_state, new_concrete_state)
        return self, new_state

    def concretize(self):
        new_concrete_state = self.sym_state.pick_concrete()
        self.concrete_state = new_concrete_state  # new_concrete_state could be None

    def add_path_conditions(self, *exp):
        self.sym_state.add_pc(*exp)

    def are_variables_symbolic(self, *variable_nodes):
        for variable_name in variable_nodes:
            if variable_name in self.sym_state.env:
                return True
        return False

    def mark_variable_concrete(self, variable_name):
        self.sym_state.remove_variable(variable_name)

    def __str__(self):
        return "sym_state:" + str(self.sym_state) + "\nconcrete_state:" + str(self.concrete_state)
