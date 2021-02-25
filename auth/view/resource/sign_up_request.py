from pydantic import BaseModel, EmailStr, constr


class SignUpRequest(BaseModel):
    full_name: constr(min_length=3)
    email: EmailStr
    password: constr(min_length=4)
