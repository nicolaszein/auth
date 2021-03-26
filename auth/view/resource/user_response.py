from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str

    @classmethod
    def from_domain(cls, domain):
        return cls(
            id=str(domain.id),
            full_name=domain.full_name,
            email=domain.email,
        )
