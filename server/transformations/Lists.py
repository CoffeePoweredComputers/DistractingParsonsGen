import ast
import os
import yaml

from . import Transformer as st

class ListTransformer(st.Transformer):

    def __init__(self):

        super().__init__(["distractors", "list.yaml"])
        
        self.transform_functions = {
            "create": self.create_transform,
            "append": self.append_transform,
            "extend": self.extend_transform,
            "index": self.index_transform,
            "count": self.count_transform,
            "pop": self.pop_transform,
            "insert": self.insert_transform,
            "remove": self.remove_transform

        }

    def gen_distractor(self, node, op):
        """ Calls the function associated with the op on the given node """
        return self.transform_functions[op](node)

    def literal_transform(self, node: ast.List) -> list: pass

    def create_transform(self, node: ast.Assign) -> list:
        """[summary]

        Args:
            statement (ast.Node): [description]

        Returns:
            list: [description]
        """

        distractor_templates = self.distractors["Create"]

        kwargs = {
            "elems": ast.unparse(node.value)[1:-1],
            "lst_name": node.targets[0].id
        }

        return self.format_distractors(distractor_templates, **kwargs)

    def append_transform(self, node: ast.Expr) -> list:
        """[summary]

        Args:
            statement (str): [description]

        Returns:
            str: [description]
        """

        distractor_templates = self.distractors["Append"]

        kwargs = {
            "lst_name": node.value.func.value.id,
            "args": ast.unparse(node.value.args)
        } 

        return self.format_distractors(distractor_templates, **kwargs)


    def extend_transform(self, node: ast.Expr) -> str:
        """

        Args:
            statement (str): [description]

        Returns:
            str: [description]
        """

        distractor_templates = self.distractors["Extend"]

        kwargs = {
            "lst_name": node.value.func.value.id,
            "args": ast.unparse(node.value.args)
        }

        return self.format_distractors(distractor_templates, **kwargs)

    def index_transform(self, node: ast.Assign) -> list:
        """[summary]

        Args:
            statement (ast.Assign): [description]

        Returns:
            list: [description]
        """

        distractor_templates = self.distractors["Index"]

        kwargs = {
            "lst_name": node.value.func.value.id,
            "args": ast.unparse(node.value.args)
        }

        return self.format_distractors(distractor_templates, **kwargs)

    def count_transform(self, node: ast.Expr) -> list:
        """[summary]

        Args:
            statement (ast.Assign): 

            Literal Example:
            Assign(
                targets=[
                    Name(id='x', ctx=Store())],
                value=Call(
                    func=Attribute(
                        value=Name(id='y', ctx=Load()),
                        attr='count',
                        ctx=Load()),
                    args=[
                        Constant(value=5)],
                    keywords=[]))

           Var Example:
           Assign(
                targets=[
                    Name(id='x', ctx=Store())],
                value=Call(
                    func=Attribute(
                        value=Name(id='y', ctx=Load()),
                        attr='count',
                        ctx=Load()),
                    args=[
                        Name(id='z', ctx=Load())],
                    keywords=[])) 

        Returns:
            list: [description]
        """

        distractor_templates = self.distractors["Count"]

        kwargs = {
            "count_elem": node.targets[0].id,
            "lst_name": node.value.func.value.id,
            "elem": ast.unparse(node.value.args[0]),
        }

        return self.format_distractors(distractor_templates, **kwargs)

    def pop_transform(self, node) -> list:
        """[summary]

        Args:
            statement (ast.Assign or ast.Expr): 

            Assign:
                Assign(
                    targets=[
                        Name(id='x', ctx=Store())],
                    value=Call(
                        func=Attribute(
                            value=Name(id='y', ctx=Load()),
                            attr='pop',
                            ctx=Load()),
                        args=[
                            Constant(value=4)],
                        keywords=[]))

            Expr:
                Expr(
                    value=Call(
                        func=Attribute(
                            value=Name(id='y', ctx=Load()),
                            attr='pop',
                            ctx=Load()),
                        args=[
                            Constant(value=4)],
                        keywords=[]))

        Returns:
            list: [description]
        """

        if type(node) is ast.Assign:
            distractor_templates = self.distractors["Pop"]["Assign"]
            kwargs = {
                "count_var": node.targets[0].id,
                "list_name": node.value.func.value.id,
                "param": ast.unparse(node.value.args[0]),
            }
        elif type(node) is ast.Expr:
            distractor_templates = self.distractors["Pop"]["Expr"]
            kwargs = {
                "list_name": node.value.func.value.id,
                "param": ast.unparse(node.value.args[0]),
            }
        else:
            raise ValueError("")

        return self.format_distractors(distractor_templates, **kwargs)


    def insert_transform(self, node: ast.Expr) -> list:
        """[summary]

        Args:
            node (ast.Expr): 
            Expr(
                value=Call(
                    func=Attribute(
                        value=Name(id='x', ctx=Load()),
                        attr='insert',
                        ctx=Load()),
                    args=[
                        Constant(value=1),
                        Constant(value='hello')],
                    keywords=[]))

        Returns:
            list: [description]
        """

        distractor_templates = self.distractors["Insert"]

        kwargs = {
            "list_name": node.value.func.value.id,
            "pos": ast.unparse(node.value.args[0]),
            "val": ast.unparse(node.value.args[1]) 
        }

        return self.format_distractors(distractor_templates, **kwargs)

    def remove_transform(self, node: ast.Expr) -> str:
        """

        Args:
            statement (str): [description]

        Returns:
            str: [description]
        """

        distractor_templates = self.distractors["Remove"]

        kwargs = {
            "list_name": node.value.func.value.id,
            "args": ast.unparse(node.value.args)
        }

        return self.format_distractors(distractor_templates, **kwargs)

