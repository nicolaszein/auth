import secrets
import uuid
from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import List, Optional

from email_validator import EmailNotValidError, validate_email

from auth.domain.activation import Activation
from auth.domain.event.activation_created import ActivationCreated
from auth.domain.event.event import Event
from auth.domain.event.reset_password_token_created import ResetPasswordTokenCreated
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
    reset_password_token: Optional[str] = None
    reset_password_token_created_at: Optional[datetime] = None

    events: List[Event] = field(init=False, default_factory=lambda: [])

    activations: List[Activation] = field(default_factory=lambda: [])

    def __post_init__(self):
        try:
            validate_email(self.email)
        except EmailNotValidError:
            raise UserWithInvalidEmail(f'{self.email} is invalid.')

    @property
    def is_active(self):
        return self.status == UserStatus.ACTIVE

    @property
    def first_name(self):
        return self.full_name.split()[0]

    def add_user_created_event(self):
        self.events.append(UserCreated(user=self))

    def create_reset_password_token(self):
        token = secrets.token_urlsafe(24)
        now = datetime.now()

        user = replace(self, reset_password_token=token, reset_password_token_created_at=now)
        user.events.append(ResetPasswordTokenCreated(user=self))

        return user

    def create_activation(self):
        activation = Activation(user=self)
        self.activations.append(activation)
        self.events.append(ActivationCreated(activation=activation))

    def activate(self, code):
        filter_activation = filter(lambda activation: activation.code == code, self.activations)
        activation = next(filter_activation, None)

        if not activation:
            raise ActivationNotFound(f'Activation with code {code} not found')

        if activation.is_expired:
            raise ActivationExpired(f'Activation with code {code} expired')

        self.activations.remove(activation)
        return replace(self, status=UserStatus.ACTIVE)
