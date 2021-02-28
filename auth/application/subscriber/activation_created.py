from auth.infrastructure.event_bus import bus
from auth.infrastructure.messaging.event.activation_created import ActivationCreated
from auth.infrastructure.messaging.event_publisher import EventPublisher
from auth.settings import ACTIVATION_QUEUE


@bus.subscribe('activation_created')
async def publish_event(activation):
    event = ActivationCreated(user_id=str(activation.user.id), code=activation.code)

    EventPublisher.publish(queue=ACTIVATION_QUEUE, event=event)
