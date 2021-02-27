import re
import uuid
from dataclasses import dataclass, field, replace
from typing import List, Optional

from auth.domain.activation import Activation
from auth.domain.event.event import Event
from auth.domain.event.user_created import UserCreated
from auth.domain.exception import ActivationExpired, ActivationNotFound, UserWithInvalidEmail
from auth.domain.user_status import UserStatus


@dataclass(frozen=True)
class User:
    full_name: str
    email: str
    password: str

    id: Optional[uuid.UUID] = None
    status: Optional[UserStatus] = UserStatus.INACTIVE

    events: List[Event] = field(init=False, default_factory=lambda: [])

    activations: List[Activation] = field(default_factory=lambda: [])

    def __post_init__(self):
        email_regex = re.compile(r'^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
        if not email_regex.match(self.email):
            raise UserWithInvalidEmail(f'{self.email} is invalid.')

    @property
    def is_active(self):
        return self.status == UserStatus.ACTIVE

    def add_user_created_event(self):
        self.events.append(UserCreated(user=self))

    def create_activation(self):
        self.activations.append(Activation(user=self))

    def activate(self, code):
        filter_activation = filter(lambda activation: activation.code == code, self.activations)
        activation = next(filter_activation, None)

        if not activation:
            raise ActivationNotFound(f'Activation with code {code} not found')

        if activation.is_expired:
            raise ActivationExpired(f'Activation with code {code} expired')

        self.activations.remove(activation)
        return replace(self, status=UserStatus.ACTIVE)
