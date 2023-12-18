import logging
import sys

from z3 import z3
from wlang.dynamic_sym_state import ConcreteState, ProgramState
from wlang import ast
from wlang.int import Interpreter
from wlang.sym import SymExec
from wlang.undef_visitor import UndefVisitor
from wlang.variables_extractor import VariablesExtractor


# TOD0: Smart concretization: set timeout for z3 and pick concrete values to proceed


class DynamicSysExec(ast.AstVisitor):
    def __init__(self):
        super().__init__()
        self.sym_visitor = SymExec()
        self.concrete_visitor = Interpreter()
        self.variable_extractor = VariablesExtractor()

    def run(self, abstract_syntax_tree, state=None):
        if state is None:
            state = ProgramState()
        states = [state]
        states = self.visit(abstract_syntax_tree, states=states)
        normal_states = []
        for state in states:
            if state.is_error():
                logging.error("Error State:\n" + str(state))
            elif state.is_infeasible():
                logging.info("Infeasible State:\n" + str(state))
            else:
                normal_states.append(state)
        return normal_states

    # No need to visit expressions and atoms

    @staticmethod
    def visit_Stmt(node, *args, **kwargs):
        return kwargs['states']  # PrintState and Skip

    @staticmethod
    def _get_new_sym_state_kwargs(sym_state):
        """
        used for the sym visitor to visit expressions
        """
        return {
            'state': sym_state
        }

    @staticmethod
    def _get_new_sym_states_kwargs(sym_states):
        """
        used for the sym visitor to visit expressions
        """
        return {
            'states': sym_states
        }

    @staticmethod
    def _get_new_concrete_state_kwargs(concrete_state: ConcreteState):
        return {
            'state': concrete_state
        }

    @staticmethod
    def _get_new_states_kwargs(program_states):
        return {
            'states': program_states
        }

    @staticmethod
    def _get_new_while_stmt_kwargs(program_states, loop_unrolling_count):
        return {
            'states': program_states,
            "loop_unrolling_count": loop_unrolling_count
        }

    def _is_expression_symbolic(self, expression_node, program_state):
        used_variables = self.variable_extractor.get_variables(expression_node)
        return program_state.is_any_variable_symbolic(*used_variables)

    def _execute_concrete_expression(self, expression_node, concrete_state):
        new_concrete_state_kwargs = self._get_new_concrete_state_kwargs(concrete_state)
        concrete_value = self.concrete_visitor.visit(expression_node, **new_concrete_state_kwargs)
        return concrete_value

    def _execute_symbolic_expression(self, expression_node, sym_state):
        new_sym_state_kwargs = self._get_new_sym_state_kwargs(sym_state)
        sym_expr = self.sym_visitor.visit(expression_node, **new_sym_state_kwargs)
        return sym_expr

    def visit_AsgnStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        for index, state in enumerate(states):
            if state.is_error() or state.is_infeasible():
                continue

            # concrete exec
            rhs_concrete_value = self._execute_concrete_expression(node.rhs, state.get_concrete_state())
            state.update_variable_concrete(node.lhs.name, rhs_concrete_value)

            if self._is_expression_symbolic(node.rhs, state):
                rhs_sym_expr = self._execute_symbolic_expression(node.rhs, state.get_symbolic_state())
                state.mark_variable_symbolic(node.lhs.name)
            else:
                rhs_sym_expr = z3.IntVal(rhs_concrete_value)
                state.mark_variable_concrete(node.lhs.name)
            state.update_variable_symbolic(node.lhs.name, rhs_sym_expr)
            states[index] = state
        return states

    def _spawn_new_states(self, node, parent_state: ProgramState, **kwargs):
        new_kwargs = self._get_new_states_kwargs([parent_state])
        new_states = self.visit(node, **new_kwargs, **kwargs)
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
                    new_then_states = self._spawn_new_states(node.then_stmt, state)
                    states[index] = new_then_states[0]
                    new_added_states.extend(new_then_states[1:])
                else:
                    # TODO: condition is always false
                    if node.has_else():
                        new_else_states = self._spawn_new_states(node.else_stmt, state)
                        states[index] = new_else_states[0]
                        new_added_states.extend(new_else_states[1:])
            else:
                sym_condition = self._execute_symbolic_expression(node.cond, state.get_symbolic_state())

                if concrete_condition:
                    then_state, else_state = state.fork(sym_condition)
                    # then branch
                    new_then_states = self._spawn_new_states(node.then_stmt, then_state)
                    states[index] = new_then_states[0]
                    new_added_states.extend(new_then_states[1:])

                    # else branch
                    if else_state.is_infeasible():
                        new_added_states.append(else_state)
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
                    if then_state.is_infeasible():
                        # TODO: condition is always true
                        new_added_states.append(then_state)
                    else:
                        new_then_states = self._spawn_new_states(node.then_stmt, then_state)
                        new_added_states.extend(new_then_states)
        states.extend(new_added_states)
        return states

    def visit_WhileStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        if node.has_inv():
            pass  # TODO
        else:
            upstream_loop_unrolling_count = 0
            if "loop_unrolling_count" in kwargs.keys():
                upstream_loop_unrolling_count = kwargs["loop_unrolling_count"]

            new_added_states = []
            for index, state in enumerate(states):
                if state.is_error() or state.is_infeasible():
                    continue
                if not self._is_expression_symbolic(node.cond, state):
                    if upstream_loop_unrolling_count >= 10:
                        continue
                    concrete_condition = self._execute_concrete_expression(node.cond, state.get_concrete_state())
                    if concrete_condition:
                        new_states = self._spawn_new_states(node.body, state)
                        loop_unrolling_count = upstream_loop_unrolling_count + 1
                        new_kwargs = self._get_new_while_stmt_kwargs(new_states, loop_unrolling_count)
                        new_states = self.visit_WhileStmt(node, **new_kwargs)
                        states[index] = new_states[0]
                        new_added_states.extend(new_states[1:])
                    else:
                        continue
                else:
                    concrete_condition = self._execute_concrete_expression(node.cond, state.get_concrete_state())
                    symbolic_condition = self._execute_symbolic_expression(node.cond, state.get_symbolic_state())
                    if concrete_condition:
                        entering_loop_state, exiting_loop_state = state.fork(symbolic_condition)
                        if upstream_loop_unrolling_count >= 10:
                            states[index] = entering_loop_state
                            continue
                        new_entering_loop_states = self._spawn_new_states(node.body, entering_loop_state)

                        # recursive visit while
                        loop_unrolling_count = upstream_loop_unrolling_count + 1
                        new_kwargs = self._get_new_while_stmt_kwargs(new_entering_loop_states, loop_unrolling_count)
                        new_entering_loop_states = self.visit_WhileStmt(node, **new_kwargs)

                        states[index] = new_entering_loop_states[0]
                        new_added_states.extend(new_entering_loop_states[1:])
                        new_added_states.append(exiting_loop_state)
                    else:
                        exiting_loop_state, entering_loop_state = state.fork(z3.Not(symbolic_condition))
                        states[index] = exiting_loop_state
                        if upstream_loop_unrolling_count >= 10:
                            continue
                        if not entering_loop_state.is_infeasible():
                            new_entering_loop_states = self._spawn_new_states(node.body, entering_loop_state)
                            # recursive while
                            loop_unrolling_count = upstream_loop_unrolling_count + 1
                            new_kwargs = self._get_new_while_stmt_kwargs(new_entering_loop_states, loop_unrolling_count)
                            new_entering_loop_states = self.visit_WhileStmt(node, **new_kwargs)
                            new_added_states.extend(new_entering_loop_states)
                        else:
                            new_added_states.append(entering_loop_state)
            states.extend(new_added_states)
            return states

    def visit_AssertStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        for index, state in enumerate(states):
            if state.is_error() or state.is_infeasible():
                continue
            if not self._is_expression_symbolic(node.cond, state):
                concrete_condition = self._execute_concrete_expression(node.cond, state.get_concrete_state())
                if not concrete_condition:
                    state.mark_error_concrete()
                    states[index] = state
            else:

                concrete_condition = self._execute_concrete_expression(node.cond, state.get_concrete_state())
                sym_condition = self._execute_symbolic_expression(node.cond, state.get_symbolic_state())
                state, counter_state = state.fork(sym_condition)
                # TODO: use scope, push and pop for z3
                # if concrete_condition is true, we know the sym_state is satisfiable
                # but we want the sym_state to be valid
                # add negation to the pc. if the not(pc) is unsatisfiable, then pc is valid
                if not counter_state.is_infeasible():
                    state.mark_error_symbolic()
                # no need to do concretization. If assert succeed, the concrete state will always satisfy the assertion.
                states[index] = state
        return states

    def visit_AssumeStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        for index, state in enumerate(states):
            if state.is_error() or state.is_infeasible():
                continue
            if not self._is_expression_symbolic(node.cond, state):
                concrete_condition = self._execute_concrete_expression(node.cond, state.get_concrete_state())
                if not concrete_condition:
                    state.mark_error_concrete()
                    states[index] = state
            else:
                concrete_condition = self._execute_concrete_expression(node.cond, state.get_concrete_state())
                sym_condition = self._execute_symbolic_expression(node.cond, state.get_symbolic_state())
                state.add_path_conditions(sym_condition)
                if not concrete_condition:
                    state.concretize()
                states[index] = state  # feasible or infeasible
        return states

    def visit_HavocStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        for index, state in enumerate(states):
            if state.is_error() or state.is_infeasible():
                continue
            new_sym_state = self._execute_no_branching_stmt_symbolic(node, state.get_symbolic_state())
            new_concrete_state = self._execute_no_branching_stmt_concrete(node, state.get_concrete_state())
            new_state = ProgramState(new_sym_state, new_concrete_state)
            for variable_node in node.vars:
                new_state.mark_variable_symbolic(variable_node.name)
            states[index] = new_state
        return states

    def _execute_no_branching_stmt_symbolic(self, stmt_node, old_sym_state):
        new_kwargs = self._get_new_sym_states_kwargs([old_sym_state])
        new_sym_state = self.sym_visitor.visit(stmt_node, **new_kwargs)[0]
        return new_sym_state

    def _execute_no_branching_stmt_concrete(self, stmt_node, old_concrete_state):
        new_kwargs = self._get_new_concrete_state_kwargs(old_concrete_state)
        new_concrete_state = self.concrete_visitor.visit(stmt_node, **new_kwargs)
        return new_concrete_state

    def visit_StmtList(self, node, *args, **kwargs):
        states = kwargs["states"]
        new_kwargs = dict(kwargs)
        for stmt in node.stmts:
            new_kwargs["states"] = states
            states = self.visit(stmt, *args, **new_kwargs)
        return states


def _parse_args():
    import argparse
    ap = argparse.ArgumentParser(prog='dynamic_sym',
                                 description='WLang Dynamic Symbolic Execution Engine')
    ap.add_argument('in_file', metavar='FILE',
                    help='WLang program to interpret')
    args = ap.parse_args()
    return args


def main():
    args = _parse_args()
    prg = ast.parse_file(args.in_file)
    st = ProgramState()
    sym = DynamicSysExec()

    states = sym.run(prg, st)
    if states is None:
        print('[symexec]: no output states')
    else:
        count = 0
        for out in states:
            count = count + 1
            print('[symexec]: symbolic state reached')
            print(out)
        print('[symexec]: found', count, 'symbolic states')
    return 0


if __name__ == '__main__':
    sys.exit(main())
