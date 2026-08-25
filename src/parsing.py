from pydantic import BaseModel


class prom(BaseModel):
    prompt : str


class defin_type(BaseModel):
    type: str


class func_demonstration(BaseModel):
    name : str
    description : str
    parameters : dict[str, defin_type]
    returns : defin_type
