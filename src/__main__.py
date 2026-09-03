import json
from llm_sdk.llm_sdk import Small_LLM_Model
from argparse import ArgumentParser
from conver_to_list import read_functions, read_promts
from constrant_decoding import function_deff


def main():
    qwen = Small_LLM_Model()
    output_fil = []
    input_file = 'data/input/function_calling_tests.json'
    function_definition = "data/input/functions_definition.json"
    output_file = 'data/output/function_calling_results.json'

    argpath = ArgumentParser()
    argpath.add_argument("--function_definition", default=function_definition)
    argpath.add_argument("--input", default=input_file)
    argpath.add_argument("--output", default=output_file)
    args = argpath.parse_args()

    function = read_functions(args.function_definition)
    prompts_obj = read_promts(args.input)
    for prompt_obj in prompts_obj:
        constrant = function_deff(function, prompt_obj.prompt, qwen)
        request_respond = constrant.creat_single_request()
        output_fil.append(request_respond)
    with open("data/input/function_calling_results.json", "w") as output:
        json.dump(output_fil, output, indent=4)

main()







# prompt_o = "What is the product of 3 and 5?"
# qwen = Small_LLM_Model()
# function_defenation = "/home/p1rox/Documents/Call-me-maybe/data/input/functions_definition.json"
# function = read_functions(function_defenation)
# constrant = function_deffinition(function, prompt_o, qwen)
# request_respond = constrant.creat_single_request()
# print(request_respond)