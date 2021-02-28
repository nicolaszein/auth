from pydantic import BaseModel


class SessionResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

    @classmethod
    def from_domain(cls, domain):
        return cls(
            access_token=domain.access_token,
            refresh_token=domain.refresh_token,
            token_type=domain.token_type,
            expires_in=domain.expires_in
        )
