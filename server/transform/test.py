import ast

class Visitor(ast.NodeVisitor):

    def match_operation(self, node: cst.SimpleStatementLine):

        match node:
            case cst.Expr:
                console