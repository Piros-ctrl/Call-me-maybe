from llm_sdk.llm_sdk import Small_LLM_Model

class function_deffinition:
    def __init__(self, functions, prompt):
        self.functions = functions
        self.prompt = prompt
        self.qwen = Small_LLM_Model()
        self.index = 0

    def _incress_index(self):
        self.index += 1

    def function_def(self):
        func_encoded = []
        for function in self.functions:
            tens_res = self.qwen.encode(function.name)
            dec_func = tens_res.tolist()[0]
            func_encoded.append(dec_func)
        return func_encoded

    def call_next(self):
        encoded_func = self.function_def()
        one_token_in_func = []
        for n in encoded_func:
            one_token_in_func.append(n[self.index])
        self._incress_index()
        return one_token_in_func

    def _allowed_tokens(self):
        all_tokens = self.function_def()
        filtred_tokens = []
        for tokens in all_tokens:
            for token in tokens:
                filtred_tokens.append(token)
        return set(filtred_tokens)

    def given_prompt(self):
        return (
                "You are a function-calling assistant."
                "Match the User Request to the best Function Name.\n"
                "Return ONLY the function name. No explanation.\n\n"
                "Available Functions:\n"
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
                f"User Request: {self.prompt}\n"
                "Output: "
                )

    def elemenate_token(self):
        function_name = ""
        allowed = self._allowed_tokens()
        encoded_promt = self.qwen.encode(self.given_prompt()).tolist()[0]
        
        # Make a quick list of just the text names so we can exit the loop later
        valid_function_names = [f.name for f in self.functions]
        
        while True:
            # 1. Ask for predictions INSIDE the loop so they update every step
            logits = self.qwen.get_logits_from_input_ids(encoded_promt)
            
            # 2. Apply the mask
            for i in range(len(logits)):
                # FIX: Check if the index 'i' is allowed, not the score 'logits[i]'
                if i not in allowed:
                    logits[i] = float("-inf")
            
            # 3. Find the winner and append it
            final_token = logits.index(max(logits))
            encoded_promt.append(final_token)
            
            # 4. FIX: Add brackets to the decode function
            function_name += self.qwen.decode([final_token])
            
            # 5. FIX: Check against the list of names, not objects
            if function_name in valid_function_names:
                break
                
        return function_name
