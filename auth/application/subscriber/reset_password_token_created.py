from auth.infrastructure.event_bus import bus
from auth.infrastructure.messaging.event.reset_password_token_created import \
    ResetPasswordTokenCreated
from auth.infrastructure.messaging.event_publisher import EventPublisher
from auth.settings import RESET_PASSWORD_QUEUE


@bus.subscribe('reset_password_token_created')
async def publish_event(user):
    event = ResetPasswordTokenCreated(
        user_id=str(user.id),
        user_name=user.first_name,
        user_email=user.email,
        token=user.reset_password_token
    )

    EventPublisher.publish(queue=RESET_PASSWORD_QUEUE, event=event)
