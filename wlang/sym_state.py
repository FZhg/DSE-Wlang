import io

from z3 import z3


class SymState(object):
    def __init__(self, solver=None):
        # environment mapping variables to symbolic constants
        self.env = dict()
        # path condition
        self.path = list()
        self._solver = solver
        if self._solver is None:
            self._solver = z3.Solver()
        self._solver.set("timeout", 1000)
        # true if this is an error state
        self._is_error = False
        self._is_infeasible = False

    def add_new_variable(self, variable_name):
        symbolic_variable = z3.FreshInt(variable_name)
        self.env[variable_name] = symbolic_variable

    def update_variable(self, variable_name, symbolic_expression):
        symbolic_expression = z3.simplify(symbolic_expression)
        self.env[variable_name] = symbolic_expression

    def add_pc(self, *exp):
        """Add constraints to the path condition"""
        self.path.extend(exp)
        self._solver.append(exp)

    def is_error(self):
        return self._is_error

    def mk_error(self):
        self._is_error = True

    def is_empty(self):
        """Check whether the current symbolic state has any concrete states"""
        if self._is_infeasible:
            return self._is_infeasible
        res = self._solver.check()
        self._is_infeasible = (res != z3.sat)
        return self._is_infeasible

    def pick_concrete(self, symbolic_variables, concrete_environment):
        """Pick a concrete state consistent with the symbolic state.
           Return None if no such state exists"""

        res = self._solver.check()

        if res == z3.unsat:
            self._is_infeasible = True
            return concrete_environment

        symbolic_variables_copy = symbolic_variables.copy()
        while res == z3.unknown or res == z3.unsat:
            if len(symbolic_variables_copy) == 0:
                break
            concretized_symbolic_variable = symbolic_variables_copy.pop()
            rhs = z3.IntVal(concrete_environment[concretized_symbolic_variable])
            lhs = self.env[concretized_symbolic_variable]
            concretizing_path_condition = (lhs == rhs)
            new_solver = z3.Solver()
            for path_condition in self.path:
                new_path_condition = z3.substitute(path_condition, (lhs, rhs))
                new_solver.add(new_path_condition)
            new_solver.add(concretizing_path_condition)
            new_solver.set("timeout", 1000)
            res = new_solver.check()
            if res == z3.sat:
                self._solver = new_solver

        if res != z3.sat:
            self._is_infeasible = True
            return concrete_environment

        model = self._solver.model()
        for variable in symbolic_variables:
            rhs_expression = self.env[variable]
            symbolic_rhs_value = model.eval(rhs_expression)
            try:
                concrete_environment[variable] = symbolic_rhs_value.as_long()
            except AttributeError:
                pass
        return concrete_environment

    def fork(self):
        """Fork the current state into two identical states that can evolve separately"""
        child_solver = z3.Solver()
        child_solver = self._solver.translate(child_solver.ctx)
        child = SymState(solver=child_solver)
        child.path = self.path.copy()
        child.env = dict(self.env)
        child._is_infeasible = self._is_infeasible
        return self, child

    def __repr__(self):
        return str(self)

    def to_smt2(self):
        """Returns the current state as an SMT-LIB2 benchmark"""
        return self._solver.to_smt2()

    def __str__(self):
        buf = io.StringIO()
        for k, v in self.env.items():
            buf.write(str(k))
            buf.write(': ')
            buf.write(str(v))
            buf.write('\n')
        buf.write('pc: ')
        buf.write(str(self.path))
        buf.write('\n')

        return buf.getvalue()
