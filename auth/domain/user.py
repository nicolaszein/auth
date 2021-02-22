import re
import uuid
from dataclasses import dataclass
from typing import Optional

from auth.domain.exception import UserWithInvalidEmailError


@dataclass(frozen=True)
class User:
    full_name: str
    email: str
    password: str

    id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = False

    def __post_init__(self):
        email_regex = re.compile(r'^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
        if not email_regex.match(self.email):
            raise UserWithInvalidEmailError(f'{self.email} is invalid.')
