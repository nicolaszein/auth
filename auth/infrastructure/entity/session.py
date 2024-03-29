import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from auth.infrastructure.entity.user import User


@dataclass
class Session:
    user_id: uuid.UUID
    refresh_token: str

    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None

    user: User = field(init=False)
