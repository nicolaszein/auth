from dataclasses import dataclass
from typing import Optional

from auth.domain.user import User
from auth.settings import TOKEN_EXPIRATION_TIME


@dataclass(frozen=True)
class Session:
    user: User
    access_token: str
    refresh_token: str

    token_type: Optional[str] = 'bearer'
    expires_in: Optional[int] = TOKEN_EXPIRATION_TIME
