import secrets
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Activation:
    user: 'User'
    code: Optional[str] = field(default_factory=lambda: secrets.token_urlsafe(16))

    id: Optional[uuid.UUID] = None

    @property
    def user_id(self):
        return self.user.id
