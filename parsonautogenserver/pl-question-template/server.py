import random, copy, json, yaml, os
from pythonHelper import *

questions = []
for f in os.listdir("question_contents/"):
    if f.endswith(".yaml"):
        with open(os.path.join("question_contents", f)) as instream:
            try:
                questions.append(yaml.safe_load(instream))
            except yaml.YAMLError as exc:
                print(exc)


def generate(data):

    randblocks = random.choice(questions) 

    data['params']['correct_blocks'] = randblocks["Correct"]
    data['params']['incorrect_blocks'] = randblocks["Incorrect"]
    data['params']['prompt'] = randblocks['Prompt']