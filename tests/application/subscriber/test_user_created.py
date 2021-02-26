import uuid
from unittest.mock import patch

import pytest

from auth.application.subscriber.user_created import publish_event
from auth.domain.user import User
from auth.settings import USER_QUEUE


@patch('auth.application.subscriber.user_created.UserCreated')
@patch('auth.application.subscriber.user_created.EventPublisher')
@pytest.mark.asyncio
async def test_publish_event(event_publisher_mock, user_created_mock):
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret'
    )
    user_created_mock.return_value = 'event-instance'

    await publish_event(user)

    event_publisher_mock.publish.assert_called_once_with(queue=USER_QUEUE, event='event-instance')
    user_created_mock.assert_called_once_with(user_id=str(user.id))
