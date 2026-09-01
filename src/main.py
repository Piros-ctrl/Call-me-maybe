import json
from llm_sdk.llm_sdk import Small_LLM_Model
from conver_to_list import read_functions, read_promts
from constrant_decoding import function_deffinition


def main():
    qwen = Small_LLM_Model()
    output_file = []
    input_file = 'data/input/function_calling_tests.json'
    function_defenation = "/home/p1rox/Documents/Call-me-maybe/data/input/functions_definition.json"
    function = read_functions(function_defenation)
    prompts_obj = read_promts(input_file)
    for prompt_obj in prompts_obj:
        constrant = function_deffinition(function, prompt_obj.prompt, qwen)
        request_respond = constrant.creat_single_request()
        output_file.append(request_respond)
    with open("output.json", "w") as output:
        json.dump(output_file, output, indent=4)

main()







# prompt_o = "What is the sum of 265 and 345?"
# qwen = Small_LLM_Model()
# function_defenation = "/home/p1rox/Documents/Call-me-maybe/data/input/functions_definition.json"
# function = read_functions(function_defenation)
# constrant = function_deffinition(function, prompt_o, qwen)
# request_respond = constrant.raw_data()
# print(request_respond)