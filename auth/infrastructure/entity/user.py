import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    full_name: str
    email: str
    password: str
    is_active: Optional[bool] = False

    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
