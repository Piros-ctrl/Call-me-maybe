from llm_sdk.llm_sdk import Small_LLM_Model

class function_deffinition:
    def __init__(self, functions, prompt):
        self.functions = [function.name for function in functions]
        self.prompt = prompt
        self.qwen = Small_LLM_Model()
        self.index = 0

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
        return function_name

    def prompt_json(self):
        # We leave the final bracket off so the LLM knows it needs to finish the JSON
        return (
            "Create a JSON object exactly like this.\n"
            "Example:\n"
            "{\n"
            '   "prompt": "What is the sum of 2 and 3",\n'
            '   "name": "fn_add_numbers"\n'
            "}\n"
            "Now complete this one:\n"
            "{\n"
            f'   "prompt": "{self.prompt}",\n'
            f'   "name": "{self.elemenate_token()}"\n'
        )

    def result(self):
        tokens = []
        # Encode the prompt into a flat list of IDs
        encoded_res = self.qwen.encode(self.prompt_json()).tolist()[0]
        
        for n in range(54):
            # 1. Ask the model for the next token scores
            logits = self.qwen.get_logits_from_input_ids(encoded_res)
            
            # 2. Find the winning token ID
            winer_token = logits.index(max(logits))
            
            # 3. Append the winning ID to the prompt so the model sees it on the next loop
            encoded_res.append(winer_token)
            
            # 4. Save the token to our results list
            tokens.append(winer_token)
            
        # 5. Decode only the newly generated tokens into a text string once the loop is done
        tk = self.qwen.decode(tokens)
        return tk