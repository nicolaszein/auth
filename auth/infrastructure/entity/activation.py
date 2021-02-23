import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from auth.domain.activation import Activation as ActivationDomain


@dataclass
class Activation:
    user_id: uuid.UUID
    code: str

    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None

    user: 'User' = field(init=False)

    @classmethod
    def from_domain(cls, domain):
        return cls(
            id=domain.id,
            user_id=domain.user_id,
            code=domain.code,
        )

    def to_domain(self):
        return ActivationDomain(
            id=self.id,
            user=self.user,
            code=self.code
        )
