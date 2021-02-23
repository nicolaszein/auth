import re
import uuid
from dataclasses import dataclass, field
from typing import List, Optional

from auth.domain.activation import Activation
from auth.domain.event.event import Event
from auth.domain.event.user_created import UserCreated
from auth.domain.exception import UserWithInvalidEmailError


@dataclass(frozen=True)
class User:
    full_name: str
    email: str
    password: str

    id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = False

    events: List[Event] = field(init=False, default_factory=lambda: [])

    activations: List[Activation] = field(default_factory=lambda: [])

    def __post_init__(self):
        email_regex = re.compile(r'^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
        if not email_regex.match(self.email):
            raise UserWithInvalidEmailError(f'{self.email} is invalid.')

        if not self.id:
            self.events.append(UserCreated(user=self))

    def create_activation(self):
        self.activations.append(Activation(user=self))
