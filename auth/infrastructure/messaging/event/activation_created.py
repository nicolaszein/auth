from dataclasses import dataclass

from auth.infrastructure.messaging.event.event import Event


@dataclass
class ActivationCreated(Event):
    user_id: str
    code: str

    name = 'activation_created'
