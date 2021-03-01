from dataclasses import dataclass

from auth.domain.event.event import Event


@dataclass(frozen=True)
class ResetPasswordTokenCreated(Event):
    user: 'User'

    name = 'reset_password_token_created'
