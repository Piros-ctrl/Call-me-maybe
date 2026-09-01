import json

class function_deffinition:
    def __init__(self, functions, prompt, qwen):
        self.functions_obj = functions
        self.functions = [function.name for function in functions]
        self.prompt = prompt
        self.qwen = qwen
        self.index = 0
        self.function_name = self.elemenate_token()

    def _incress_index(self):
        self.index += 1

    def function_def(self):
        func_encoded = []
        for function in self.functions:
            tens_res = self.qwen.encode(function)
            dec_func = tens_res.tolist()[0]
            func_encoded.append(dec_func)
        return func_encoded

    def call_next(self):
        encoded_func = self.function_def()
        one_token_in_func = []
        for n in encoded_func:
            if self.index < len(n):
                one_token_in_func.append(n[self.index])
        self._incress_index()
        return one_token_in_func

    def given_prompt(self):
        return (
                "From the Given prompt pick the best Function.\n"
                "Return JUST the function name. No more no less.\n"
                "Those are the only Functions provided:\n"
                f"{self.functions}"
                "Examples:\n"
                "Input: Hello, can you greet me?\n"
                "Output: fn_greet\n\n"
                "Input: What is the capital of France?\n"
                "Output: non_seported\n\n"
                "Input: Calculate the sum of 10 and 20\n"
                "Output: fn_add_numbers\n\n"
                "Input: Find the square root of 16\n"
                "Output: fn_get_square_root\n\n"
                "Input: Reverse 'hello'\n"
                "Output: fn_reverse_string\n"
                f"Given prompt: {self.prompt}\n"
                "Output: "
                )

    def elemenate_token(self):
        self.index = 0
        function_name = ""
        encoded_promt = self.qwen.encode((self.given_prompt())).tolist()[0]
        while 1:
            allowed = self.call_next()
            logits = self.qwen.get_logits_from_input_ids(encoded_promt)
            for i in range(len(logits)):
                if i not in allowed:
                    logits[i] = float("-inf")
            final_token = logits.index(max(logits))
            encoded_promt.append(final_token)
            function_name += self.qwen.decode([final_token])
            if function_name in self.functions:
                break
        self.function_name = function_name
        return function_name

    def get_function_obj(self):
        function_name = self.function_name
        for function in  self.functions_obj:
            if function.name == function_name:
                return function
        return False

    def get_function_params(self):
        parameters = self.get_function_obj().parameters
        return parameters

    def extract_params(self):
        param_dict = {}
        raw_params = self.get_function_params()
        for key, value in raw_params.items():
            param_dict[key] = value.type
        return param_dict

    def _allowed_parameter_tokens(self):
        encoded_params = self.qwen.encode(self.prompt).tolist()[0]
        return encoded_params

    def parameter_prompt(self):
        return (
            "Extract the parameters for the function from the user request.\n"
            f"Function: {self.function_name}\n"
            f"Parameters: {self.extract_params()}\n"
            f"User: {self.prompt}\n\n"
            "Return ONLY valid JSON in this format: "
            '{"parameters": {...}}\n'
            "Use only defined parameters."
            "Numbers must be floats.\n\n"
            "Make sure that the outpput is VALID JSON"

            "Examples:\n"

            "Function: fn_add_numbers\n"
            'Parameters: {"a": float, "b": float}\n'
            "User: what is the sum of 2 and 4\n"
            'Assistant: {"parameters": {"a": 2.0, "b": 4.0}}'

            "\nFunction: fn_get_square_root\n"
            'Parameters: {"a": float}\n'
            "User: Calculate the square root of 144\n"
            'Assistant: {"parameters": {"a": 144.0}}'

            "\nFunction: fn_greet\n"
            'Parameters: {"s": str}\n'
            "User: Greet fred\n"
            'Assistant: {"parameters": {"s": "fred"}}'

            "\nFunction: fn_substitute_string_with_regex\n"
            'Parameters: {"source_string":"string","regex":"string","replacement":"string"}\n'
            'User: Replace all numbers in "Hello 34 I\'m 233 years old" with NUMBERS\n'
            'Assistant: {"parameters": {"source_string": "Hello 34 I\'m 233 years old", "regex": "[0-9]+", "replacement": "NUMBERS"}}'

            f"\nFunction: {self.function_name}\n"
            f"User: {self.prompt}\n"
            'Assistant: {"parameters": '
        )

    def raw_data(self):
        encoded = self.qwen.encode(self.parameter_prompt()).tolist()[0]
        generated_tokens = []
        i = 0
        while i < 50:
            logits = self.qwen.get_logits_from_input_ids(encoded)

            token = logits.index(max(logits))

            encoded.append(token)
            generated_tokens.append(token)

            text = self.qwen.decode(generated_tokens)
            i+=1

            if "}" in text:
                break
        raw_str = self.qwen.decode(generated_tokens)
        result = raw_str.split("}")
        net_value = result[0] + "}"
        return net_value.strip()

    def creat_single_request(self):
        parsed_data = json.loads(self.raw_data())

        request_dict = {
            "prompt": self.prompt,
            "name": self.function_name,
            "parameters": parsed_data
        }

        return request_dict
            
