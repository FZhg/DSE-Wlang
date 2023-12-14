import z3

from wlang import ast
from wlang.int import State, Interpreter
from wlang.sym import SymExec, SymState
from wlang.undef_visitor import UndefVisitor


# TOD0: Smart concretization: set timeout for z3 and pick concrete values to proceed

class ConcreteState(State):
    def __init__(self):
        super().__init__()

    def update_variables(self, variable_name: str, value: int):
        self.env[variable_name] = value


# TODO: finish skeletons
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
        return self.sym_state.is_error()

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
            return None  # infeasible
        new_state = ProgramState(new_sym_state, new_concrete_state)
        return self, new_state

    def add_path_condition(self, *exp):
        self.sym_state.add_pc(*exp)

    def are_variable_symbolic(self, *variable_nodes):
        for variable_node in variable_nodes:
            if variable_node.name in self.sym_state.env:
                return True
        return False


class DynamicSysExec(ast.AstVisitor):
    def __init__(self):
        super().__init__()
        self.sym_visitor = SymExec()
        self.concrete_visitor = Interpreter()

    def run(self, program):
        # TODO: Jimmy
        pass

    # No need to visit expressions and atoms

    @staticmethod
    def visit_Stmt(node, *args, **kwargs):
        return kwargs['states']  # PrintState and Skip

    @staticmethod
    def _get_new_sym_state_kwargs(sym_state: SymState):
        """
        used for the sym visitor to visit expressions
        """
        return {
            'state': sym_state
        }

    @staticmethod
    def _get_new_concrete_state_kwargs(concrete_state: ConcreteState):
        return {
            'state': concrete_state
        }

    @staticmethod
    def _get_new_states_kwargs(program_states):
        return {
            'program_states': program_states
        }

    @staticmethod
    def _is_expression_symbolic(expression_node, program_state):
        undef_visitor = UndefVisitor()
        undef_visitor.visit(expression_node)
        used_variables = undef_visitor.get_defs()
        return program_state.is_expression_symbolic(used_variables)

    def visit_AsgnStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        for index, state in enumerate(states):
            if state.is_error() or state.is_infeasible():
                continue

            # concrete exec
            concrete_state = state.get_concrete_state()
            new_concrete_state_kwargs = self._get_new_concrete_state_kwargs(concrete_state)
            rhs_concrete_value = self.concrete_visitor.visit(node.rhs, **new_concrete_state_kwargs)
            state.update_variable_concrete(node.lhs.name, rhs_concrete_value)

            if self._is_expression_symbolic(node.rhs, state):
                # sym exec
                sym_state = state.get_sym_state()
                new_sym_state_kwargs = self._get_new_sym_state_kwargs(sym_state)
                rhs_sym_expr = self.sym_visitor.visit(node.rhs, **new_sym_state_kwargs)
                state.update_variable_symbolic(node.lhs.name, rhs_sym_expr)
            states[index] = state
        return states

    def _spawn_new_states(self, node, parent_state: ProgramState):
        new_kwargs = self._get_new_states_kwargs([parent_state])
        new_states = self.visit(node, **new_kwargs)
        return new_states

    def visit_IfStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        new_added_states = []
        for index, state in enumerate(states):
            if state.is_error() or state.is_infeasible():
                continue
            # TODO:
            # 1. use concrete value check condition
            # 2. true, execute concrete + symbolic to the then branch;
            # use solver to pick the concrete value for the else branch
            # 3. false, execute concrete + symbolic to the else branch;
            # use solver to pick the concrete value for the then branch
            concrete_state = state.get_concrete_state()
            new_concrete_state_kwargs = self._get_new_concrete_state_kwargs(concrete_state)
            concrete_condition = self.concrete_visitor.visit(node.cond, **new_concrete_state_kwargs)

            sym_state = state.get_sym_state()
            new_sym_state_kwargs = self._get_new_sym_state_kwargs(sym_state)
            sym_condition = self.sym_visitor.visit(node.cond, **new_sym_state_kwargs)

            if concrete_condition:
                then_state, else_state = state.fork(sym_condition)
                # then branch
                new_then_states = self._spawn_new_states(node.then_stmt, then_state)
                states[index] = new_then_states[0]
                new_added_states.extend(new_then_states[1:])

                # else branch
                if else_state is None:
                    pass  # else branch is infeasible
                else:
                    if node.has_else():
                        new_else_states = self._spawn_new_states(node.else_stmt, else_state)
                        new_added_states.extend(new_else_states)
                    else:
                        new_added_states.append(else_state)
            else:
                else_state, then_state = state.fork(z3.Not(concrete_condition))

                # else branch
                if node.has_else():
                    new_else_states = self._spawn_new_states(node.else_stmt, else_state)
                    states[index] = new_else_states[0]
                    new_added_states.extend(new_else_states[1:])
                else:
                    states[index] = else_state

                # then branch
                if then_state is None:
                    pass  # the then branch is infeasible
                else:
                    new_then_states = self._spawn_new_states(node.then_stmt, then_state)
                    new_added_states.extend(new_then_states)
        states.extend(new_added_states)
        return states

    def visit_WhileStmt(self, node, *args, **kwargs):
        # TODO: Jimmy
        pass

    def visit_AssertStmt(self, node, *args, **kwargs):
        # TODO: Jimmy
        # assert x > 1; x = 2; x = y ^ 2  + z ^3
        pass

    def visit_AssumeStmt(self, node, *args, **kwargs):
        # TODO: Fan
        pass

    def visit_HavocStmt(self, node, *args, **kwargs):
        # TODO: Jimmy
        pass

    def visit_StmtList(self, node, *args, **kwargs):
        # TODO: Fan
        pass
