# Call Me Maybe - Function Calling with LLMs

*This project has been created as part of the 42 curriculum by oabderra.*

## Description

**Call Me Maybe** is a lightweight, fully local Function Calling system using the `Qwen/Qwen3-0.6B` language model.

The project converts natural-language requests into structured JSON function calls using **constrained decoding**. Instead of generating freely and fixing the output afterward, the system modifies the model's logits during generation to prevent invalid tokens.

## How It Works

The system works in two main steps:

### 1. Function Selection

Available functions are loaded from `functions_definition.json` and tokenized.

During generation, the model is only allowed to generate tokens that can form one of the defined function names.

```text
User prompt
    ↓
Qwen3-0.6B
    ↓
Logit masking
    ↓
Valid function
```

### 2. Parameter Generation

After selecting a function, the system generates its parameters while respecting their defined types.

* **String:** handles quotes and string boundaries.
* **Number:** restricts generation to valid numerical characters.
* **JSON structure:** braces, commas, and keys are controlled by the decoder.

This prevents malformed JSON from being generated.

## Constrained Decoding

At every generation step, invalid tokens are masked by setting their logits to `-inf`.

```text
Valid token   → normal logit
Invalid token → -inf
```

Therefore, invalid tokens cannot be selected by the model.

## Main Challenges

* Handling tokenizer behavior and multi-character tokens.
* Restricting function names to the available functions.
* Generating valid numbers and detecting their boundaries.
* Maintaining the correct JSON generation state.
* Preventing repetition and malformed context during generation.

## Technologies

* Python
* PyTorch
* Hugging Face Transformers
* Qwen3-0.6B
* Pydantic
* NumPy
* uv

## Installation

```bash
uv venv
source .venv/bin/activate
uv sync
```

## Usage

```bash
uv run python -m src.main \
    --functions_definition data/input/functions_definition.json \
    --input data/input/function_calling_tests.json \
    --output data/output/function_calling_results.json
```

## Testing

The generated results can be validated with `json.loads()` and checked against the function definitions to verify:

* Valid JSON
* Existing function names
* Correct parameter names
* Correct parameter types

## AI Usage

chatbot was used to understand concepts such as LLMs.
