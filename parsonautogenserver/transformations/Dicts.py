import ast
import os
import yaml

from . import Transformer as st

class DictTransformer(st.Transformer):

    def __init__(self):

        super().__init__(["distractors", "dict.yaml"])

        self.transform_functions = {
            "create": self.create_transform,
            "delete": self.delete_transform,
            "addchangepair": self.addchangepair_transform,
            "update": self.update_transform
        }

    def gen_distractor(self, node: ast.For, op: str) -> list:
        """ Calls the function associated with the op on the given node """
        return self.transform_functions[op](node)

    def literal_transform(self, node: ast.Expr): pass


    def create_transform(self, node: ast.Assign):
        """[summary]

        Args:
            node (ast.Assign):
            Assign(
                targets=[
                    Name(id='x', ctx=Store())],
                value=Dict(
                    keys=[
                        Constant(value='hi'),
                        Constant(value='world')],
                    values=[
                        Constant(value=5),
                        Constant(value=10)]))
        """

        distractor_templates = self.distractors["Create"]

        var_name = node.targets[0].id
        keys = [ ast.unparse(key) for key in node.value.keys ]
        values = [ str(ast.unparse(value)) for value in node.value.values ]
        pairs = list(zip(keys, values))

        if len(pairs) == 0:
            return self.format_distractors(distractor_templates["Empty"], var_name=var_name)
        else:
            return [
                distractor_template.format(var_name=var_name, args=", ".join(list(map(lambda x: sep.join(x), pairs))))
                for sep, distractor_template in distractor_templates["NonEmpty"]
            ]

    def delete_transform(self, node: ast.Delete):
        """[summary]

        Args:
            node (ast.Delete): [description]

        Returns:
            node: Delete(
                    targets=[
                        Subscript(
                            value=Name(id='x', ctx=Load()),
                            slice=Constant(value='hi'),
                            ctx=Del())])
        """

        distractor_templates = self.distractors["Delete"]

        kwargs = {
            "var_name" : node.targets[0].value.id,
            "key" : ast.unparse(node.targets[0].slice)
        }

        return self.format_distractors(distractor_templates, **kwargs)


    def addchangepair_transform(self, node: ast.Assign):
        """[summary]

        Args:
            node (ast.Assign): 
            Assign(
                targets=[
                    Subscript(
                        value=Name(id='x', ctx=Load()),
                        slice=Constant(value=0),
                        ctx=Store())],
                value=Constant(value=5))
        """


        distractor_templates = self.distractors["AddChangePair"]

        kwargs = {
            "var_name" : node.targets[0].value.id,
            "key" : ast.unparse(node.targets[0].slice),
            "value" : ast.unparse(node.value)
        }

        return self.format_distractors(distractor_templates, **kwargs)

    def update_transform(self, node: ast.Expr):
        """[summary]

        Args:
            node (ast.Expr): 

            structure for literal:
            Expr(
                value=Call(
                    func=Attribute(
                        value=Name(id='x', ctx=Load()),
                        attr='update',
                        ctx=Load()),
                    args=[
                        Dict(
                            keys=[
                                Constant(value='hi')],
                            values=[
                                Constant(value=4)])],
                    keywords=[]))

            structure for value:
            Expr(
                value=Call(
                    func=Attribute(
                        value=Name(id='x', ctx=Load()),
                        attr='update',
                        ctx=Load()),
                    args=[
                        Name(id='y', ctx=Load())],
                    keywords=[]))
        """

        distractor_templates = self.distractors["Update"]

        var_name = node.value.func.value.id

        if type(node.value.args[0]) is ast.Dict:

            keys = [ ast.unparse(key) for key in node.value.args[0].keys ]
            values = [ str(ast.unparse(value)) for value in node.value.args[0].values ]
            pairs = list(zip(keys, values))

            return [
                distractor_template.format(var_name=var_name, args=", ".join(list(map(lambda x: sep.join(x), pairs))))
                for sep, distractor_template in distractor_templates
            ]

        elif type(node.value.args[0]) is ast.Name:

            kwargs = {
                "var_name": var_name,
                "args": ast.unparse(node.value.args[0])
            }

            # filter to just get the templates since we're updating a dictionary
            # with a variable rather and a literal. This will get erased later
            # once we add support for literal distractors for each class
            distractor_templates = [ t[1] for t in distractor_templates ]

            return self.format_distractors(distractor_templates, **kwargs)

        else:
            raise Exception("Invalid structure for dictionary method 'update'")
