from wlang import ast


class VariablesExtractor(ast.AstVisitor):

    def get_variables(self, expression_node):
        variable_names = set()
        return self.visit(expression_node, variable_names=variable_names)

    def visit_Exp(self, node, *args, **kwargs):
        variable_names = kwargs["variable_names"]
        for arg in node.args:
            variable_names = self.visit(arg, variable_names=variable_names)
        return variable_names

    def visit_IntVar(self, node, *args, **kwargs):
        variable_names = kwargs["variable_names"]
        variable_names.add(node.name)
        return variable_names

    @staticmethod
    def visit_Const(node, *args, **kwargs):
        return kwargs["variable_names"]


