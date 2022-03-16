import ast
import os
import yaml

from . import Transformer as st

class ForLoopTransformer(st.Transformer):

    def __init__(self):

        super().__init__(["distractors", "forloop.yaml"])

        self.transform_functions = {
            "collection": self.transform_collection,
            "range": self.transform_range,
            "enumerate": self.transform_enumerate,
            "dict-items": self.transform_dict_items,
            "dict-values": self.transform_dict_values,
            "dict-keys": self.transform_dict_keys
        }

    def gen_distractor(self, node: ast.For, op: str) -> list:
        """ Calls the function associated with the op on the given node """
        return self.transform_functions[op](node)

    def transform_collection(self, node: ast.For) -> list:
        """[summary]

        Args:
            node (ast.For): 

            Literal:

            #TODO: This needs to be altered to permute the collections
            if they are iterating over a literal. This may result in just
            defining a "literal morph" function or class that morphs whenever
            the value is a data structure rather than a name that's being
            loaded.... As for generation of valid/invalid structures, just make
            this a boolean that defaults to false and turns to true in 
            *very* specific circumstances.

            For(
                target=Name(id='item', ctx=Store()),
                iter=List(
                    elts=[
                        Constant(value=1),
                        Constant(value=2),
                        Constant(value=3)],
                    ctx=Load()),
                body=[
                    Pass()],
                orelse=[])

            Variable:
            For(
                target=Name(id='item', ctx=Store()),
                iter=Name(id='collection', ctx=Load()),
                body=[
                    Pass()],
                orelse=[])

        Returns:
            list: [description]
        """

        distractor_templates = self.distractors["Collection"]

        kwargs = {
            "iter_var": node.target.id,
            "collection": ast.unparse(node.iter)
        }

        return self.format_distractors(distractor_templates, **kwargs)


    def transform_range(self, node: ast.For) -> list:
        """[summary]

        Args:
            node (ast.For): 
                For(
                    target=Name(id='item', ctx=Store()),
                    iter=Call(
                        func=Name(id='range', ctx=Load()),
                        args=[
                            Constant(value=10)],
                        keywords=[]),
                    body=[
                        Pass()],
                    orelse=[])

            This can have up 2 three args and still be considered
            valid.

        Returns:
            list: a list of formatted distractor strings lines
        """

        kwargs = {
            "iter_var": node.target.id
        }

        if len(node.iter.args) == 1:
            distractor_templates = self.distractors["Range"]["OneArg"]
            kwargs["end"] = ast.unparse(node.iter.args[0])
        elif len(node.iter.args) == 2:
            distractor_templates = self.distractors["Range"]["TwoArgs"]
            kwargs.update({
                "start": ast.unparse(node.iter.args[0]),
                "end": ast.unparse(node.iter.args[1])
            })
        elif len(node.iter.args) == 3:
            distractor_templates = self.distractors["Range"]["ThreeArgs"]
            kwargs.update({
                "start": ast.unparse(node.iter.args[0]),
                "end": ast.unparse(node.iter.args[1]),
                "inc": ast.unparse(node.iter.args[2])
            })
        else:
            raise ValueError("The range function, as used in a for loop, should take 1-3 args")

        return self.format_distractors(distractor_templates, **kwargs)
    
    def transform_enumerate(self, node: ast.For) -> list:
        """[summary]

        Args:
            node (ast.For): 

                Varaible Param:
                For(
                    target=Tuple(
                        elts=[
                            Name(id='i', ctx=Store()),
                            Name(id='item', ctx=Store())],
                        ctx=Store()),
                    iter=Call(
                        func=Name(id='enumerate', ctx=Load()),
                        args=[
                            Name(id='y', ctx=Load())],
                        keywords=[]),
                    body=[
                        Pass()],
                    orelse=[])

                Literal:
                For(
                    target=Tuple(
                        elts=[
                            Name(id='i', ctx=Store()),
                            Name(id='item', ctx=Store())],
                        ctx=Store()),
                    iter=Call(
                        func=Name(id='enumerate', ctx=Load()),
                        args=[
                            List(
                                elts=[
                                    Constant(value='hi'),
                                    Constant(value='hello')],
                                ctx=Load())],
                        keywords=[]),
                    body=[
                        Pass()],
                    orelse=[])


        Returns:
            list: [description]
        """

        distractor_templates = self.distractors["Enumerate"]

        if type(node.target) is not ast.Tuple:
            raise Exception("Enumerate is expected to be used in a loop with two iteration variables: index and value")


        kwargs = {
            "index": node.target.elts[0].id,
            "value": node.target.elts[1].id,
            "args": ast.unparse(node.iter.args[0])
        }

        return self.format_distractors(distractor_templates, **kwargs)

    def transform_dict_items(self, node: ast.For) -> list:
        """[summary]

        Args:
            node (ast.For): 

                Literal:
                    For(
                        target=Name(id='item', ctx=Store()),
                        iter=Call(
                            func=Attribute(
                                value=Dict(
                                    keys=[
                                        Constant(value='hi'),
                                        Constant(value='hello')],
                                    values=[
                                        Constant(value=4),
                                        Constant(value=5)]),
                                attr='values',
                                ctx=Load()),
                            args=[],
                            keywords=[]),
                        body=[
                            Pass()],
                        orelse=[])

                Var:            
                    For(
                        target=Name(id='item', ctx=Store()),
                        iter=Call(
                            func=Attribute(
                                value=Name(id='x', ctx=Load()),
                                attr='items',
                                ctx=Load()),
                            args=[],
                            keywords=[]),
                        body=[
                            Pass()],
                        orelse=[])

        Returns:
            list: [description]
        """

        if type(node.target) is not ast.Tuple:
            raise Exception("dict.items() is expected to be used in a loop with two iteration variables: index and value")

        distractor_templates = self.distractors["DictItems"]

        kwargs = {
            "iter_var1": node.target.elts[0].id,
            "iter_var2": node.target.elts[1].id,
            "dict": ast.unparse(node.iter.func.value)
        }

        return self.format_distractors(distractor_templates, **kwargs)

    def transform_dict_values(self, node: ast.For) -> list:
        """[summary]

        Args:
            node (ast.For):

            Literal:
                For(
                    target=Name(id='item', ctx=Store()),
                    iter=Call(
                        func=Attribute(
                            value=Dict(
                                keys=[
                                    Constant(value='hi'),
                                    Constant(value='hello')],
                                values=[
                                    Constant(value=4),
                                    Constant(value=5)]),
                            attr='values',
                            ctx=Load()),
                        args=[],
                        keywords=[]),
                    body=[
                        Pass()],
                    orelse=[])

            Var:            
                For(
                    target=Name(id='item', ctx=Store()),
                    iter=Call(
                        func=Attribute(
                            value=Name(id='x', ctx=Load()),
                            attr='values',
                            ctx=Load()),
                        args=[],
                        keywords=[]),
                    body=[
                        Pass()],
                    orelse=[])

        Returns:
            list: [description]
        """

        distractor_templates = self.distractors["DictValues"]

        kwargs = {
            "iter_var": node.target.id,
            "dict": ast.unparse(node.iter.func.value)
        }

        return self.format_distractors(distractor_templates, **kwargs)

    def transform_dict_keys(self, node: ast.For) -> list:
        """[summary]

        Args:
            node (ast.For): 
                Literal:
                    For(
                        target=Name(id='item', ctx=Store()),
                        iter=Call(
                            func=Attribute(
                                value=Dict(
                                    keys=[
                                        Constant(value='hi'),
                                        Constant(value='hello')],
                                    keys=[
                                        Constant(value=4),
                                        Constant(value=5)]),
                                attr='keys',
                                ctx=Load()),
                            args=[],
                            keywords=[]),
                        body=[
                            Pass()],
                        orelse=[])

                Var:            
                    For(
                        target=Name(id='item', ctx=Store()),
                        iter=Call(
                            func=Attribute(
                                value=Name(id='x', ctx=Load()),
                                attr='keys',
                                ctx=Load()),
                            args=[],
                            keywords=[]),
                        body=[
                            Pass()],
                        orelse=[])


        Returns:
            list: 
        """

        distractor_templates = self.distractors["DictKeys"]

        kwargs = {
            "iter_var": node.target.id,
            "dict": ast.unparse(node.iter.value)
        }

        return self.format_distractors(distractor_templates, **kwargs)
