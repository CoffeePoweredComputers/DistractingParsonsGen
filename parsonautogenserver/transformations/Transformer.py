import os
import yaml
#from Matcher import Matcher

class Transformer:

    def __init__(self, path_elems: list):

        with open(os.path.join(*path_elems)) as instream:
            try:
                self.distractors = yaml.safe_load(instream)
            except yaml.YAMLError as exec:
                print(exec)
                exit(-1)

    def format_distractors(self, distractor_templates, **kwargs):

        return [
            distractor_template.format(**kwargs)
            for distractor_template in distractor_templates
        ]

