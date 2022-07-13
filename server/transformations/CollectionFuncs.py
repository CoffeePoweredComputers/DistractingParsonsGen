import ast
import os
import yaml

from . import Transformer as st

class CollectionFuncsTransformations(st.Transformer):

    def __init__(self):

        super().__init__(["distractors", "collection_func.yaml"])

        self.transform_functions = {

            # Set
            "setcreate": self.set_create_transform,
            "add": self.add_transform,
            "union": self.union_transform,

            # Dict
            "dictcreate": self.dict_create_transform,
            "delete": self.delete_transform,
            "addchangepair": self.addchangepair_transform,

            #
            "listcreate": self.list_create_transform,
            "update": self.update_transform,
            "append": self.append_transform,
            "extend": self.extend_transform,
            "index": self.index_transform,
            "count": self.count_transform,
            "pop": self.pop_transform,
            "insert": self.insert_transform,
            "remove": self.remove_transform

        }

    def gen_distractor(self, node, op: str) -> list:
        """ Calls the function associated with the op on the given node """
        return self.transform_functions[op](node)


    def list_create_transform(self, node: ast.Assign) -> list:
        """[summary]

        Args:
            statement (ast.Node): [description]

        Returns:
            list: [description]
        """

        distractor_templates = self.distractors["ListCreate"]

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
            "val": ast.unparse(node.value.args)
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
            "val": ast.unparse(node.value.args)
        }

        return self.format_distractors(distractor_templates, **kwargs)

    def index_transform(self, node: ast.Assign) -> list:
        """[summary]

        Args:
            statement (ast.Assign): [description]

        Returns:
            list: [description]
        """

        distractor_templates = self.distractors["Index"]["Assign"]

        if type(node) is ast.Assign:
            kwargs = {
                "var": node.targets[0].id,
                "collection_name": ast.unparse(node.value.func.value),
                "val": ast.unparse(node.value.args[0]),
            }

        return self.format_distractors(distractor_templates, **kwargs)

    def count_transform(self, node: ast.Expr | ast.Assign) -> list:
        """[summary]

        Args:
        Returns:
            list: [description]
        """

        if type(node) is ast.Assign:
            distractor_templates = self.distractors["Count"]["Assign"]
            kwargs = {
                "var": node.targets[0].id,
                "collection_name": node.value.func.value.id,
                "val": ast.unparse(node.value.args[0]),
            }
        elif type(node) is ast.Expr:
            distractor_templates = self.distractors["Count"]["Expr"]
            kwargs = {
                "collection_name": node.value.func.value.id,
                "val": ast.unparse(node.value.args[0]),
            }


        return self.format_distractors(distractor_templates, **kwargs)

    def pop_transform(self, node) -> list:
        """[summary]

        Args:

        Returns:
            list: [description]
        """

        if type(node) is ast.Assign:
            distractor_templates = self.distractors["Pop"]["Assign"]
            kwargs = {
                "elem": node.targets[0].id,
                "collection_name": node.value.func.value.id,
                "key": ast.unparse(node.value.args[0]),
            }
        elif type(node) is ast.Expr:
            distractor_templates = self.distractors["Pop"]["Expr"]
            kwargs = {
                "collection_name": node.value.func.value.id,
                "key": ast.unparse(node.value.args[0]),
            }
        else:
            raise ValueError("{ast.unparse(node)} is not a valid formation of the pop statement/expression")

        return self.format_distractors(distractor_templates, **kwargs)


    def insert_transform(self, node: ast.Expr) -> list:
        """[summary]

        Args:

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
            "collection_name": node.value.func.value.id,
            "val": ast.unparse(node.value.args)
        }

        return self.format_distractors(distractor_templates, **kwargs)


    def dict_create_transform(self, node: ast.Assign):
        """[summary]

        Args:
        """

        distractor_templates = self.distractors["DictCreate"]

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

    def set_create_transform(self, node: ast.Assign) -> list:
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

        Returns:
            list: 
        """

        distractor_templates = self.distractors["Add"]

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

    def set_create_transform(self, node: ast.Assign) -> list:
        """[summary]

        Args:
            node (ast.Assign): 

        Returns:
            list: [description]
        """
        distractor_templates = self.distractors["SetCreate"]

        kwargs = {
            "args": ast.unparse(node.value)[1:-1],
            "set_name": node.targets[0].id
        }

        return self.format_distractors(distractor_templates, **kwargs)

    def add_transform(self, node: ast.Expr) -> list:
        """[summary]

        Args:
            node (ast.Expr): 

        Returns:
            list: 
        """

        distractor_templates = self.distractors["Add"]

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
    
