from pydantic import BaseModel, constr


class RefreshSessionRequest(BaseModel):
    refresh_token: constr(min_length=1)
