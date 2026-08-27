from llm_sdk.llm_sdk import Small_LLM_Model

            
modul = Small_LLM_Model()

text = "the sky has"
text1 = modul.encode(text)
input_encoded = text1.tolist()[0]

for _ in range(5):
    expetetion_result = modul.get_logits_from_input_ids(input_encoded)
    winning_token = expetetion_result.index(max(expetetion_result))
    input_encoded.append(winning_token)


text2 = modul.decode(input_encoded)
print(text2)
