from dataclasses import dataclass

from auth.domain.event.event import Event


@dataclass(frozen=True)
class UserCreated(Event):
    user: 'User'

    name = 'user_created'
