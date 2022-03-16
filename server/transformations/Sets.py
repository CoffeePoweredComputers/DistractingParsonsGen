import ast
import os
import yaml

from . import Transformer as st

class SetTransformer(st.Transformer):

    def __init__(self):

        super().__init__(["distractors", "set.yaml"])

        self.transform_functions = {
            "create": self.create_transform,
            "add": self.add_transform,
            "union": self.union_transform,
            "remove": self.remove_transform
        }

    def gen_distractor(self, node, op: str) -> list:
        """ Calls the function associated with the op on the given node """
        return self.transform_functions[op](node)

    def literal_transform(self, node: ast.Set) -> list: pass

    def create_transform(self, node: ast.Assign) -> list:
        """[summary]

        Args:
            node (ast.Assign): 

        Returns:
            list: [description]
        """
        distractor_templates = self.distractors["Create"]

        kwargs = {
            "args": ast.unparse(node.value)[1:-1],
            "set_name": node.targets[0].id
        }

        return self.format_distractors(distractor_templates, **kwargs)

    def add_transform(self, node: ast.Expr) -> list:
        """[summary]

        Args:
            node (ast.Expr): 
                Expr(
                    value=Call(
                        func=Attribute(
                            value=Name(id='x', ctx=Load()),
                            attr='add',
                            ctx=Load()),
                        args=[
                            Constant(value=4)],
                        keywords=[]))

        Returns:
            list: 
        """

        distractor_templates = self.distractors["Add"]

        kwargs = {
            "set_name": ast.unparse(node.value.func.value),
            "args": ast.unparse(node.value.args[0])
        }

        return self.format_distractors(distractor_templates, **kwargs)

    def remove_transform(self, node) -> list:
        """[summary]

        Args:
            node (ast.Expr): 
            Expr(
                value=Call(
                    func=Attribute(
                        value=Name(id='x', ctx=Load()),
                        attr='remove',
                        ctx=Load()),
                    args=[
                        Name(id='y', ctx=Load())],
                    keywords=[]))

        Returns:
            list: [description]
        """

        distractor_templates = self.distractors["Remove"]

        kwargs = {
            "set_name": ast.unparse(node.value.func.value),
            "args": ast.unparse(node.value.args[0])
        }

        return self.format_distractors(distractor_templates, **kwargs)


    def union_transform(self, node) -> list:
        """[summary]

        Args:
            node (ast.Assign | ast.Expr): 

            ast.Assign -> Assign(
                            targets=[
                                Name(id='z', ctx=Store())],
                            value=Call(
                                func=Attribute(
                                    value=Name(id='x', ctx=Load()),
                                    attr='union',
                                    ctx=Load()),
                                args=[
                                    Name(id='y', ctx=Load())],
                                keywords=[]))

            ast.Expr -> Expr(
                            value=Call(
                                func=Attribute(
                                    value=Name(id='x', ctx=Load()),
                                    attr='union',
                                    ctx=Load()),
                                args=[
                                    Name(id='y', ctx=Load())],
                                keywords=[]))

        Returns:
            list: 
        """

        if type(node) is ast.Assign:
            distractor_templates = self.distractors["Union"]["Expr"]
            kwargs = {
                "set1": ast.unparse(node.value.func.value),
                "set2": ast.unparse(node.value.args[0]),
                "set3": ast.unparse(node.targets[0])
            }
        elif type(node) is ast.Expr:
            distractor_templates = self.distractors["Union"]["Assign"]
            kwargs = {
                "set1": ast.unparse(node.value.func.value),
                "set2": ast.unparse(node.value.args[0])
            }
        else:
            raise Exception("A union transformation should be either an assignment or an expression")

        return self.format_distractors(distractor_templates, **kwargs)