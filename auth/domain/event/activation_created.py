from dataclasses import dataclass

from auth.domain.activation import Activation
from auth.domain.event.event import Event


@dataclass(frozen=True)
class ActivationCreated(Event):
    activation: Activation

    name = 'activation_created'
