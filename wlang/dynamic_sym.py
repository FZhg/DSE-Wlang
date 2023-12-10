from wlang import ast
from wlang.int import State, Interpreter
from wlang.sym import SymExec, SymState


class ConcreteState(State):
    def __init__(self):
        super().__init__()

    def update_variables(self, variable_name: str, value: int):
        self.env[variable_name] = value


# TODO: finish skeletons
class ProgramState:
    def __init__(self):
        self.sym_state = SymState()
        self.concrete_state = ConcreteState()

    def update_variable(self, variable_name: str, sym_expression, concrete_value: int):
        self.sym_state.update_variable(variable_name, sym_expression)
        self.concrete_state.update_variables(variable_name, concrete_value)

    def get_sym_state(self):
        return self.sym_state

    def get_concrete_state(self):
        return self.concrete_state

    def is_error(self):
        return self.sym_state.is_error()

    def is_infeasible(self):
        return self.sym_state.is_empty()


class DynamicSysExec(ast.AstVisitor):
    def __init__(self):
        super().__init__()
        self.sym_visitor = SymExec()
        self.concrete_visitor = Interpreter()

    # No need to visit expressions and atoms

    @staticmethod
    def visit_Stmt(node, *args, **kwargs):
        return kwargs['states']  # PrintState and Skip

    @staticmethod
    def _get_new_sym__state_kwarg(sym_state: SymState):
        """
        used for the sym visitor to visit expressions
        """
        return {
            'state': sym_state
        }

    @staticmethod
    def _get_new_concrete_state_kwarg(concrete_state: ConcreteState):
        return {
            'state': concrete_state
        }

    def visit_AsgnStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        for index, state in enumerate(states):
            if state.is_error() or state.is_infeasible():
                continue
            # TODO: sym visitor + concrete visitor
            # TODO: modifies the update_variable method to take both sym and con states
            # sym exec
            sym_state = state.get_sym_state()
            new_sym_state_kwargs = self._get_new_sym__state_kwarg(sym_state)
            rhs_sym_expr = self.sym_visitor.visit(node.rhs, **new_sym_state_kwargs)

            # concrete exec
            concrete_state = state.get_concrete_state()
            new_concrete_state_kwargs = self._get_new_concrete_state_kwarg(concrete_state)
            rhs_concrete_value = self.concrete_visitor.visit(node.rhs, **new_concrete_state_kwargs)

            state.update_variable(node.lhs.name, rhs_sym_expr, rhs_concrete_value)
            states[index] = state
        return states

    def visit_IfStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        for index, state in enumerate(states):
            if state.is_error() or state.is_infeasible():
                continue
            # TODO:
            # 1. use concrete value check condition
            # 2. false, execute concrete + symbolic to the else branch;
            # use solver to pick the concrete value for the then branch
            # 3. true, execute concrete + symbolic to the then branch;
            # use solver to pick the concrete value for the else branch
            concrete_state = state.get_concrete_state()
            new_concrete_state_kwargs = self._get_new_concrete_state_kwarg(concrete_state)
            concrete_condition = self.concrete_visitor.visit(node.cond)
            if concrete_condition:
                pass
            else:
                pass

    def visit_WhileStmt(self, node, *args, **kwargs):
        # TODO: Jimmy
        pass