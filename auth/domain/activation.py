import secrets
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from auth.settings import ACTIVATION_EXPIRE_TIME


@dataclass(frozen=True)
class Activation:
    user: 'User'
    code: Optional[str] = field(default_factory=lambda: secrets.token_urlsafe(16))

    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None

    @property
    def user_id(self):
        return self.user.id

    @property
    def expire_date(self):
        return self.created_at + timedelta(seconds=ACTIVATION_EXPIRE_TIME)

    @property
    def is_expired(self):
        return datetime.now() > self.expire_date
