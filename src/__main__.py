import json
import os
from llm_sdk.llm_sdk import Small_LLM_Model
from argparse import ArgumentParser
from conver_to_list import read_functions, read_promts
from constrant_decoding import function_deff


def main() -> None:
    """Run function-calling tests against the LLM and write results to a JSON output file."""
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
    os.mkdir("data/output")
    with open(args.output, "w") as output:
        json.dump(output_fil, output, indent=4)


main()