from dataclasses import dataclass

from auth.infrastructure.messaging.event.event import Event


@dataclass
class UserCreated(Event):
    user_id: str

    name = 'user_created'
