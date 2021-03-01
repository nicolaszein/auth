from dataclasses import dataclass

from auth.infrastructure.messaging.event.event import Event


@dataclass
class ResetPasswordTokenCreated(Event):
    user_id: str
    user_email: str
    user_name: str
    token: str

    name = 'reset_password_token_created'
