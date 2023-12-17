import logging
import sys

from z3 import z3

from wlang import ast, undef_visitor
from wlang.sym_state import SymState


class SymExec(ast.AstVisitor):
    def __init__(self):
        super().__init__()

    def run(self, ast, state=None):
        # set things up and
        # call self.visit (ast, states=states)
        if state is None:
            state = SymState()
        states = [state]
        states = self.visit(ast, states=states)
        normal_states = []
        for state in states:
            if state.is_error():
                logging.error("Error State:\n" + str(state))
            elif state.is_empty():
                logging.info("Infeasible State:\n" + str(state))
            else:
                normal_states.append(state)
        return normal_states

    def visit_IntVar(self, node, *args, **kwargs):
        return kwargs['state'].env[node.name]

    def visit_BoolConst(self, node, *args, **kwargs):
        return z3.BoolVal(node.val)

    def visit_IntConst(self, node, *args, **kwargs):
        return z3.IntVal(node.val)

    def visit_RelExp(self, node, *args, **kwargs):
        lhs = self.visit(node.arg(0), *args, **kwargs)
        rhs = self.visit(node.arg(1), *args, **kwargs)
        if node.op == "<=":
            return lhs <= rhs
        if node.op == "<":
            return lhs < rhs
        if node.op == "=":
            return lhs == rhs
        if node.op == ">=":
            return lhs >= rhs
        if node.op == ">":
            return lhs > rhs
        raise "Unknown Operators"

    def visit_BExp(self, node, *args, **kwargs):
        operands = [self.visit(operand_node, *args, **kwargs) for operand_node in node.args]
        if node.is_unary():
            assert len(operands) == 1
            if node.op == "not":
                return z3.Not(operands[0])
        else:
            assert len(operands) == 2
            if node.op == "and":
                return z3.And(*operands)
            elif node.op == "or":
                return z3.Or(*operands)
        raise "Unknown Operators"

    def visit_AExp(self, node, *args, **kwargs):
        # only a single state is passed down
        # expression will alter state
        operands = [self.visit(operand_node, *args, **kwargs) for operand_node in node.args]
        assert len(operands) == 2
        if node.op == "+":
            return operands[0] + operands[1]
        elif node.op == "-":
            return operands[0] - operands[1]
        elif node.op == "*":
            return operands[0] * operands[1]
        elif node.op == "/":
            return operands[0] / operands[1]
        raise "Unknown Operators"

    def visit_SkipStmt(self, node, *args, **kwargs):
        return kwargs['states']

    def visit_PrintStateStmt(self, node, *args, **kwargs):
        return kwargs['states']

    def visit_AsgnStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        for index, state in enumerate(states):
            if state.is_error() or state.is_empty():
                continue
            new_kwargs = dict(kwargs)
            new_kwargs['state'] = state
            rhs = self.visit(node.rhs, *args, **new_kwargs)
            state.update_variable(node.lhs.name, rhs)
            states[index] = state
        return states

    def visit_IfStmt(self, node, *args, **kwargs):
        # infeasible => else ; if else branch didn't exit, path condition remains the same
        # feasible => then else branch; change the path conditions.

        # feasible run the then branch
        # infeasible => else;

        states = kwargs["states"]
        new_added_states = []
        for index, state in enumerate(states):
            if state.is_error() or state.is_empty():
                continue
            then_state, else_state = state.fork()
            new_kwargs = dict(kwargs)
            new_kwargs["state"] = state
            condition = self.visit(node.cond, *args, **new_kwargs)
            then_state.add_pc(condition)
            if not then_state.is_empty():
                # then branch
                new_then_states = [then_state]
                new_then_kwargs = dict(kwargs)
                new_then_kwargs["states"] = new_then_states
                new_then_states = self.visit(node.then_stmt, *args, **new_then_kwargs)
                states[index] = new_then_states[0]  # TODO: this should be unnecessary
                new_added_states.extend(new_then_states[1:])
            else:
                states[index] = then_state

            # else branch
            else_state.add_pc(z3.Not(condition))
            if not else_state.is_empty():
                if node.has_else():
                    new_else_states = [else_state]
                    new_else_kwargs = dict(kwargs)
                    new_else_kwargs["states"] = new_else_states
                    new_else_states = self.visit(node.else_stmt, *args, **new_else_kwargs)
                    new_added_states.extend(new_else_states)
                else:
                    new_added_states.append(else_state)
            else:
                new_added_states.append(else_state)
        states.extend(new_added_states)
        return states

    def verify_loop_inv(self, inv, cond, body, states):
        node = SymExec._generated_loop_inv_verifying_code(inv, cond, body)
        return self.visit(node, states=states)

    @staticmethod
    def _generated_loop_inv_verifying_code(inv, cond, body):
        assert_stmt_1 = ast.AssertStmt(inv)
        uv = undef_visitor.UndefVisitor()
        uv.check(body)
        variables_modified = list(uv.get_defs())
        if len(variables_modified) == 0:
            havoc_stmt = ast.SkipStmt()
        else:
            havoc_stmt = ast.HavocStmt(variables_modified)
        assume_stmt_1 = ast.AssumeStmt(inv)
        assert_stmt_2 = ast.AssertStmt(inv)
        false_const = ast.BoolConst(False)
        assume_stmt_2 = ast.AssumeStmt(false_const)
        if_body = ast.StmtList([body, assert_stmt_2, assume_stmt_2])
        if_stmt = ast.IfStmt(cond, if_body)
        root_node = ast.StmtList([assert_stmt_1, havoc_stmt, assume_stmt_1, if_stmt])
        # print_visitor = ast.PrintVisitor()
        # print_visitor.visit(root_node)
        return root_node

    def visit_WhileStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        if node.has_inv():
            states = self.verify_loop_inv(node.inv, node.cond, node.body, states)
        else:
            upstream_loop_unrolling_count = 0
            if "loop_unrolling_count" in kwargs.keys():
                upstream_loop_unrolling_count = kwargs["loop_unrolling_count"]
            new_added_states = []
            for index, state in enumerate(states):
                if state.is_error() or state.is_empty():
                    continue
                new_kwargs = dict(kwargs)
                new_kwargs["state"] = state
                condition = self.visit(node.cond, *args, **new_kwargs)
                state, exiting_state = state.fork()
                exiting_state.add_pc(z3.Not(condition))
                state.add_pc(condition)
                if state.is_empty() or upstream_loop_unrolling_count >= 10:
                    states[index] = exiting_state
                    continue
                if not exiting_state.is_empty():
                    new_added_states.append(exiting_state)
                new_states = [state]
                new_kwargs = dict(kwargs)
                new_kwargs["states"] = new_states
                new_states = self.visit(node.body, *args, **new_kwargs)
                new_kwargs["states"] = new_states
                loop_unrolling_count = upstream_loop_unrolling_count + 1
                new_kwargs["loop_unrolling_count"] = loop_unrolling_count
                new_states = self.visit(node, *args, **new_kwargs)
                states[index] = new_states[0]  # TODO: this should be unnecessary
                new_added_states.extend(new_states[1:])
            states.extend(new_added_states)
        return states

    def visit_AssertStmt(self, node, *args, **kwargs):
        # Don't forget to print an error message if an assertion might be violated
        states = kwargs['states']
        for index, state in enumerate(states):
            if state.is_error() or state.is_empty():
                continue
            new_kwargs = dict(kwargs)
            new_kwargs["state"] = state
            condition = self.visit(node.cond, *args, **new_kwargs)
            state, counter_state = state.fork()
            counter_condition = z3.Not(condition)
            counter_state.add_pc(counter_condition)
            if counter_state.is_empty():
                state.add_pc(condition) # TODO: this should be unnecessary
            else:
                state.mk_error()
                logging.error("Assertion Invalid: " + str(node))
            states[index] = state
        return states

    def visit_AssumeStmt(self, node, *args, **kwargs):
        states = kwargs['states']
        for index, state in enumerate(states):
            if state.is_error() or state.is_empty():
                continue
            new_kwargs = dict(kwargs)
            new_kwargs["state"] = state
            condition = self.visit(node.cond, *args, **new_kwargs)
            state.add_pc(condition)
            if state.is_empty():
                logging.info("Assumption unfeasible: " + str(node))
            states[index] = state
        return states

    def visit_HavocStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        for state in states:
            if state.is_error() or state.is_empty():
                continue
            for variable in node.vars:
                state.add_new_variable(variable.name)
        return states

    def visit_StmtList(self, node, *args, **kwargs):
        states = kwargs["states"]
        new_kwargs = dict(kwargs)
        for stmt in node.stmts:
            new_kwargs["states"] = states
            states = self.visit(stmt, *args, **new_kwargs)
        return states


def _parse_args():
    import argparse
    ap = argparse.ArgumentParser(prog='sym',
                                 description='WLang Interpreter')
    ap.add_argument('in_file', metavar='FILE',
                    help='WLang program to interpret')
    args = ap.parse_args()
    return args


def main():
    args = _parse_args()
    prg = ast.parse_file(args.in_file)
    st = SymState()
    sym = SymExec()

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
