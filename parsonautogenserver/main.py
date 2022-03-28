import ast
from sys import argv
import yaml
import os, shutil
import uuid
import json

from transformations import Lists
from transformations import FunctionDef
from transformations import ForLoop
from transformations import Dicts
from transformations import Sets

class DistractorGen():

    def __init__(self):

        this.transformer_functions = {
            "set": Sets.SetTransformer(),
            "list": Lists.ListTransformer(),
            "dict": Dicts.DictTransformer(),
            "function": FunctionDef.FunctionTransformer(),
            "forloop": ForLoop.ForLoopTransformer() 
        }

    def gen_distractor_block(self, node: str, t, op):

        try:
            distractors = this.transformer_functions[t].gen_distractor(node, op)
        except Exception as e:
            print("An exception occured: ", e)
            exit(-1)

        return json.dumps([
            {"block": distractor}
            for distractor in distractors
        ]).encode("utf-8")


    def gen_correct_blocks(self, py_source: str) -> list:

        # remove all empty lines from file
        py_source = list(filter(lambda x: len(x.strip()) > 0 , py_source))

        pl_lines = []
        for pos, line in enumerate(py_source, start=1):

            line = line.split("#")[0].rstrip()
            s_line = line.lstrip()
            indent = (len(line) - len(s_line)) // 4
            pl_lines.append({
                "indent": indent,
                "block": s_line,
                "ranking": pos
            })

        return pl_lines

    def gen_grading_server(self, qid: str) -> None:
            shutil.copyfile(
                os.path.join("pl-question-template", "server.py"),
                os.path.join(argv[2], qid, "server.py")
                )
            
    def gen_problem_yaml(correct: list, incorrect: list, prompt: str, outdir: str, qid: str, i: int) -> None:

        try:
            os.makedirs(os.path.join(outdir, qid, "question_contents"), exist_ok=True)
        except OSError as error:
            print("Error making question contents directory: ", error)
            exit(-1)

        all_blocks = {
                "Correct": correct, 
                "Incorrect": incorrect, 
                "Prompt": prompt
                }
        with open(os.path.join(outdir, qid, "question_contents", f"func{i}.yaml"), "w") as outstream:
            yaml.dump(all_blocks, outstream)

    def main():

        # 1) Initial Setup
        qid = "parsons" + argv[1].split(os.path.sep)[-1]
        try:
            os.makedirs(os.path.join(argv[2], qid), exist_ok = True)
        except OSError as error:
            print(f"Directory {qid} cannot be created: {error}")
            exit(-1)

        gen_info_json(argv[2], qid)

        # 2) Generate Parsons
        for i, f in enumerate(os.listdir(argv[1])):

            if not f.endswith(".py"): continue

            with open(os.path.join(argv[1], f)) as instream:
                py_source = instream.readlines()

            start_i, end_i = [idx for idx, s in enumerate(py_source) if '"""' in s][:2]
            prompt = " ".join(py_source[start_i + 1: end_i])
            correct_blocks = gen_correct_blocks(py_source[end_i + 1:])

            incorrect_blocks = []
            for line in py_source:

                # Only create distractors for lines with comments
                if "#" not in line:
                    continue

                line, comment = line.split("#")
                t, op = comment.split()


                # add pass here to make valid lines of the following
                if t in ["function", "forloop", "whileloop", "if", "elif", "else"]:
                    line += " pass"
                    #print(ast.parse(line.strip()).body[0])

                try:
                    line = ast.parse(line.strip()).body[0]
                    distractors = gen_distractor_blocks(line, t, op)
                    incorrect_blocks.extend(distractors)
                except Exception as e:
                    print(e)
                    continue
        
            gen_problem_yaml(correct_blocks, incorrect_blocks, prompt, argv[2], qid, i)

        shutil.copyfile(
            os.path.join("pl-question-template", "question.html"),
            os.path.join(argv[2], qid, "question.html")
            )
        gen_grading_server(qid)



if __name__ == "__main__":
    main()
