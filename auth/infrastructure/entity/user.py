import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from auth.domain.event.event import Event
from auth.domain.user import User as UserDomain
from auth.domain.user_status import UserStatus
from auth.infrastructure.entity.activation import Activation


@dataclass
class User:
    full_name: str
    email: str
    password: str
    status: str

    id: Optional[uuid.UUID] = None
    reset_password_token: Optional[str] = None
    reset_password_token_created_at: Optional[datetime] = None

    _events: Optional[List[Event]] = field(init=False, default=None)
    activations: List[Activation] = field(default_factory=lambda: [])

    @property
    def events(self):
        return self._events or []

    @classmethod
    def from_domain(cls, domain):
        user = cls(
            id=domain.id,
            full_name=domain.full_name,
            email=domain.email,
            password=domain.password,
            status=domain.status.value,
            reset_password_token=domain.reset_password_token,
            reset_password_token_created_at=domain.reset_password_token_created_at,
            activations=[Activation.from_domain(activation) for activation in domain.activations],
        )
        user.__set_events(domain.events)
        return user

    def to_domain(self):
        return UserDomain(
            id=self.id,
            full_name=self.full_name,
            email=self.email,
            password=self.password,
            status=UserStatus(self.status),
            reset_password_token=self.reset_password_token,
            reset_password_token_created_at=self.reset_password_token_created_at,
            activations=[activation.to_domain() for activation in self.activations]
        )

    def __set_events(self, events):
        self._events = events
