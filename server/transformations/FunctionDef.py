import ast
import os
import yaml

from . import Transformer as st

class FunctionTransformer(st.Transformer):

    def __init__(self):

        super().__init__(["distractors", "functiondef.yaml"])

        self.transform_functions = {
            "def": self.def_transform
        }


        
    def gen_distractor(self, node: ast.FunctionDef, op: str) -> list:
        """ Calls the function associated with the op on the given node """
        if op == "all":
            return [
                func(node)
                for func in self.transform_functions.values()
                ]

        else:
            return self.transform_functions[op](node)

    def extract_args(self, node: ast.FunctionDef) -> tuple:

        kwarb = "**"  + ast.unparse(node.args.kwarg)
        arb = "*" +  ast.unparse(node.args.vararg)

        defaults_values = node.args.defaults
        args = node.args.args
        default_args = [
            "{}={}".format(ast.unparse(a), ast.unparse(b))
            for a, b in zip(args[-len(defaults_values):], defaults_values)
        ]
        non_default_args = [
            ast.unparse(a)
            for a in args[:len(defaults_values)]
        ]

        return non_default_args, default_args, arb, kwarb


    def def_transform(self, node: ast.FunctionDef) -> str:

        distractor_templates = self.distractors["Def"]

        func_name = node.name
        args = ast.unparse(node.args)

        return [
            distractor_template.format(func_name=func_name, args=args)
            for distractor_template in distractor_templates
        ]


    #def args_transform(self, node: ast.FunctionDef) -> str:
    #    #TODO: This one still needs some work

    #    distractor_templates = self.distractors["Args"]

    #    func_name = node.name

    #    non_default, default, arb, kwarb = self.extract_args(node)

    #    return [
    #        distractor_template.format(
    #            func_name=func_name,
    #            non_default_args=", ".join(non_default_args) if len(non_default_args) > 0 else "",
    #            default_args=", ".join(default_args) if len(default_args) > 0 else "",
    #            kwarb= ", " + kwarb if len(kwarb) > 0 else "",
    #            arb= ", " + arb if len(arb) > 0 else "" 
    #            )
    #        for distractor_template in distractor_templates
    #    ]