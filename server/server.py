from sys import argv
import ast
import json
import os, shutil
import random
import time
import uuid
import yaml

from flask import Flask, request
from flask_cors import CORS, cross_origin

from transformations import Lists
from transformations import FunctionDef
from transformations import ForLoop
from transformations import Dicts
from transformations import Sets

transformer_functions = {
    "set": Sets.SetTransformer(),
    "list": Lists.ListTransformer(),
    "dict": Dicts.DictTransformer(),
    "function": FunctionDef.FunctionTransformer(),
    "forloop": ForLoop.ForLoopTransformer() 
}

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/get_distractors")
@cross_origin(methods=["GET"])
def get_distractors():

    r_text = request.args.get("text")
    r_type = request.args.get("type")
    r_op = request.args.get("operation")

    print(r_text, r_type, r_op)

    try:
        node = ast.parse(r_text.strip()).body[0]
        distractors = transformer_functions[r_type].gen_distractor(node, r_op)
    except Exception as e:
        print("An exception occured: ", e)
        return None

    return json.dumps([
        {"text": distractor}
        for distractor in distractors
        ]).encode("utf-8")

@app.route("/match_distractor")
@cross_origin(methods=["GET"])
def match_distractor():
    r_text = request.args.get("text")
    return {"matchFound": "append" in r_text}


if __name__ == "__main__":
    app.run(port=8000, debug=True)
