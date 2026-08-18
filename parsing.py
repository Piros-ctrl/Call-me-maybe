from pydantic import BaseModel


class type_defin(BaseModel):
    type: str


class func_demonstration(BaseModel):
    name: str
    description: str
    parameters: dict[str, type_defin]
    returns: type_defin
