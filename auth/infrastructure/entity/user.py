import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, List, Optional

from auth.domain.event.event import Event
from auth.domain.user import User as UserDomain
from auth.infrastructure.entity.activation import Activation


@dataclass
class User:
    full_name: str
    email: str
    password: str
    is_active: Optional[bool] = False

    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    events: ClassVar[List[Event]] = field(default=[])
    activations: List[Activation] = field(default_factory=lambda: [])

    @classmethod
    def from_domain(cls, domain):
        return cls(
            id=domain.id,
            full_name=domain.full_name,
            email=domain.email,
            password=domain.password,
            is_active=domain.is_active,
            activations=[Activation.from_domain(activation) for activation in domain.activations],
            events=domain.events
        )

    def to_domain(self):
        return UserDomain(
            id=self.id,
            full_name=self.full_name,
            email=self.email,
            password=self.password,
            is_active=self.is_active,
            activations=[activation.to_domain() for activation in self.activations]
        )
