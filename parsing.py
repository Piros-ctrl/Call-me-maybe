from pydantic import BaseModel, ValidationError

class func_demonstration(BaseModel):
    name : str
    description : str
    parameter : dict[str, str]
    returns : dict[str, str]


class 
