import datetime
import json
import uuid
from unittest.mock import patch

from auth.domain.user_status import UserStatus
from auth.infrastructure.entity.user import User
from auth.infrastructure.repository.user import UserRepository
from auth.view.function.send_reset_password_email import handle


@patch('auth.view.function.send_reset_password_email.UserService')
def test_send_reset_password_email(user_service_mock, database):
    reset_password_token = 'reset-password-token'
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE.value,
        reset_password_token='reset-password-token'
    )
    UserRepository().create(user)
    body = {
        'id': str(uuid.uuid4()),
        'name': 'reset_password_token_created',
        'produced_at': datetime.datetime.now().isoformat(),
        'payload': {
            'user_id': str(user.id),
            'user_name': 'Foo',
            'user_email': user.email,
            'token': str(reset_password_token)
        }
    }
    event = {
        'Records': [
            {
                'body': json.dumps(body),
            }
        ],
    }

    handle(event, None)

    user_service_mock().send_reset_password_email.assert_called_once_with(
        user_id=str(user.id),
        reset_password_token=reset_password_token
    )
