import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from auth.domain.user import User as UserDomain


@dataclass
class User:
    full_name: str
    email: str
    password: str
    is_active: Optional[bool] = False

    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_domain(cls, domain):
        return cls(
            id=domain.id,
            full_name=domain.full_name,
            email=domain.email,
            password=domain.password,
            is_active=domain.is_active
        )

    def to_domain(self):
        return UserDomain(
            id=self.id,
            full_name=self.full_name,
            email=self.email,
            password=self.password,
            is_active=self.is_active
        )
