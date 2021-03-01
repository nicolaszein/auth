from pydantic import BaseModel, EmailStr


class CreateResetPasswordRequest(BaseModel):
    email: EmailStr
