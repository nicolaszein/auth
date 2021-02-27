from pydantic import BaseModel, constr


class ActivateRequest(BaseModel):
    code: constr(min_length=1)
