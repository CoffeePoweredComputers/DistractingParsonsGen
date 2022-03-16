import ast
import os
import yaml

from . import Transformer as st

class BuiltinTransformer(st.Transformer):

    def __init__(self):

        super().__init__(["distractors", "dict.yaml"])

        self.transform_functions = {
            "input": self.transform_input,
            "print": self.transformer_print
        }

    def gen_distractor(self, node: ast.For, op: str) -> list:
        """ Calls the function associated with the op on the given node """
        return self.transform_functions[op](node)

    def transform_input(self, node: ast.Call) -> list:
        distractor_templates = self.distractors["Input"]

    def transformer_print(self, node: ast.Call) -> list:
        distractor_templates = self.distractors["Input"]
        
