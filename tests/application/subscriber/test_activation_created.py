import uuid
from unittest.mock import patch

import pytest
from auth.application.subscriber.activation_created import publish_event

from auth.domain.activation import Activation
from auth.domain.user import User
from auth.settings import ACTIVATION_QUEUE


@patch('auth.application.subscriber.activation_created.ActivationCreated')
@patch('auth.application.subscriber.activation_created.EventPublisher')
@pytest.mark.asyncio
async def test_publish_event(event_publisher_mock, activation_created_mock):
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret'
    )
    activation = Activation(user=user)
    activation_created_mock.return_value = 'event-instance'

    await publish_event(activation)

    event_publisher_mock.publish.assert_called_once_with(
        queue=ACTIVATION_QUEUE,
        event='event-instance'
    )
    activation_created_mock.assert_called_once_with(user_id=str(user.id), code=activation.code)
