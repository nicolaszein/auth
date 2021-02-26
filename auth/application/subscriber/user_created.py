from auth.infrastructure.event_bus import bus
from auth.infrastructure.messaging.event.user_created import UserCreated
from auth.infrastructure.messaging.event_publisher import EventPublisher
from auth.settings import USER_QUEUE


@bus.subscribe('user_created')
async def publish_event(user):
    event = UserCreated(user_id=str(user.id))

    EventPublisher.publish(queue=USER_QUEUE, event=event)
