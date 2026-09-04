from pydantic import BaseModel


class prompts(BaseModel):
    """A single prompt entry consisting of the raw prompt text."""
    prompt: str


class defin_type(BaseModel):
    """A simple type descriptor, e.g. used for parameter or return types."""
    type: str


class func_demonstration(BaseModel):
    """A function definition demonstration: its name, description, parameter types, and return type."""
    name: str
    description: str
    parameters: dict[str, defin_type]
    returns: defin_type
