import sys
from parsing import func_demonstration, prompts
from functions import read_functions, read_promts
import json
from constrant_decoding import function_deffinition


input_file = 'data/input/function_calling_tests.json'
function_defenation = "/home/p1rox/Documents/Call-me-maybe/data/input/functions_definition.json"
function = read_functions(function_defenation)

prompt = "greet yassin"

constrant = function_deffinition(function, prompt)
var = constrant.elemenate_token()
# var = constrant.call_next()
print(var)


# def test():
#     file = sys.argv[-1]
#     with open(file, "r") as f:
#         jfile = json.load(f)
#         for data in jfile:
#             func_demonstration(**data)
#     file1 = sys.argv[-2]
#     with open(file1, "r") as f1:
#         jsfile = json.load(f1)
#         for line in jsfile:
#             prompts(**line)


# test()
