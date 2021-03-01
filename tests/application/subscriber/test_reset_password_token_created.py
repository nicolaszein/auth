import uuid
from unittest.mock import patch

import pytest

from auth.application.subscriber.reset_password_token_created import publish_event
from auth.domain.user import User
from auth.settings import RESET_PASSWORD_QUEUE


@patch('auth.application.subscriber.reset_password_token_created.ResetPasswordTokenCreated')
@patch('auth.application.subscriber.reset_password_token_created.EventPublisher')
@pytest.mark.asyncio
async def test_publish_event(event_publisher_mock, reset_password_token_created_mock):
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        reset_password_token='token'
    )
    reset_password_token_created_mock.return_value = 'event-instance'

    await publish_event(user)

    event_publisher_mock.publish.assert_called_once_with(
        queue=RESET_PASSWORD_QUEUE,
        event='event-instance'
    )
    reset_password_token_created_mock.assert_called_once_with(
        user_id=str(user.id),
        user_name=user.first_name,
        user_email=user.email,
        token=user.reset_password_token
    )
