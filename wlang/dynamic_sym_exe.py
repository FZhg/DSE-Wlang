import z3

from dynamic_sym_state import ConcreteState, ProgramState
from wlang import ast
from wlang.int import Interpreter
from wlang.sym import SymExec, SymState
from wlang.undef_visitor import UndefVisitor


# TOD0: Smart concretization: set timeout for z3 and pick concrete values to proceed


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

    def _execute_concrete_expression(self, expression_node, concrete_state):
        new_concrete_state_kwargs = self._get_new_concrete_state_kwargs(concrete_state)
        rhs_concrete_value = self.concrete_visitor.visit(expression_node.rhs, **new_concrete_state_kwargs)
        return rhs_concrete_value

    def _execute_symbolic_expression(self, expression_node, sym_state):
        new_sym_state_kwargs = self._get_new_sym_state_kwargs(sym_state)
        rhs_sym_expr = self.sym_visitor.visit(expression_node.rhs, **new_sym_state_kwargs)
        return rhs_sym_expr

    def visit_AsgnStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        for index, state in enumerate(states):
            if state.is_error() or state.is_infeasible():
                continue

            # concrete exec
            rhs_concrete_value = self._execute_concrete_expression(node.rhs, state.get_concrete_state())
            state.update_variable_concrete(node.lhs.name, rhs_concrete_value)

            if self._is_expression_symbolic(node.rhs, state):
                rhs_sym_expr = self._execute_symbolic_expression(node.rhs, state.get_sym_state())
                state.update_variable_symbolic(node.lhs.name, rhs_sym_expr)
            states[index] = state
        return states

    def _spawn_new_states(self, node, parent_state: ProgramState):
        new_kwargs = self._get_new_states_kwargs([parent_state])
        new_states = self.visit(node, **new_kwargs)
        return new_states

    def visit_IfStmt(self, node, *args, **kwargs):
        """
        Visit an IfStmt
        If the condition is concrete, then no path conditions is added.

        If the condition is symbolic, then follow the concrete branch first and
        switch to the other branch.
        """
        states = kwargs["states"]
        new_added_states = []
        for index, state in enumerate(states):
            if state.is_error() or state.is_infeasible():
                continue

            concrete_condition = self._execute_concrete_expression(node.cond, state.get_concrete_state())

            if not self._is_expression_symbolic(node.cond, state):
                if concrete_condition:
                    # TODO: condition is always true
                    new_then_state = self._spawn_new_states(node.then_stmt, state)
                    states[index] = new_then_state
                else:
                    # TODO: condition is always false
                    if node.has_else():
                        new_else_state = self._spawn_new_states(node.else_stmt, state)
                        states[index] = new_else_state
            else:
                sym_condition = self._execute_symbolic_expression(node.cond, state.get_sym_state())

                if concrete_condition:
                    then_state, else_state = state.fork(sym_condition)
                    # then branch
                    new_then_states = self._spawn_new_states(node.then_stmt, then_state)
                    states[index] = new_then_states[0]
                    new_added_states.extend(new_then_states[1:])

                    # else branch
                    if else_state is None:
                        pass
                    # else branch is infeasible
                    # TODO: condition is always false
                    else:
                        if node.has_else():
                            new_else_states = self._spawn_new_states(node.else_stmt, else_state)
                            new_added_states.extend(new_else_states)
                        else:
                            new_added_states.append(else_state)
                else:
                    else_state, then_state = state.fork(z3.Not(sym_condition))

                    # else branch
                    if node.has_else():
                        new_else_states = self._spawn_new_states(node.else_stmt, else_state)
                        states[index] = new_else_states[0]
                        new_added_states.extend(new_else_states[1:])
                    else:
                        states[index] = else_state

                    # then branch
                    if then_state is None:
                        # TODO: condition is always true
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
        states = kwargs["states"]
        new_added_states = []
        for index, state in enumerate(states):
            if state.is_error() or state.is_infeasible():
                continue
            if not self._is_expression_symbolic(node.cond, state):
                self.concrete_visitor.visit_AssumeStmt()
            else:
                pass

    def visit_HavocStmt(self, node, *args, **kwargs):
        # TODO: Jimmy
        pass

    def visit_StmtList(self, node, *args, **kwargs):
        # TODO: Fan
        pass
