from pydantic import ValidationError
import json
from parsing import func_demonstration, prompts


def read_promts(file_path):
    try:
        with open(file_path, "r") as f:
            file = json.load(f)
            if not isinstance(file, list):
                raise ValueError("recheck you file data in this path :",file_path)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        exit(1)
    prompt_list = []
    try:
        for prompt_dict in file:
            prompt = prompts(**prompt_dict)
            prompt_list.append(prompt)
    except ValidationError:
        for error in e.errors():
            print(error["msg"])
    return prompt_list

def read_functions(file_path):
    try:
        with open(file_path, "r") as f:
            file = json.load(f)
            if not isinstance(file, list):
                raise ValueError("recheck you file data in this path :",file_path)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        exit(1)
    function_list = []
    try:
        for function in file:
            prompt = func_demonstration(**function)
            function_list.append(prompt)
    except ValidationError:
        for error in e.errors():
            print(error["msg"])
    return function_list
