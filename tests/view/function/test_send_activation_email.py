import datetime
import json
import uuid
from unittest.mock import patch

from auth.domain.user_status import UserStatus
from auth.infrastructure.entity.user import User
from auth.infrastructure.repository.user import UserRepository
from auth.view.function.send_activation_email import handle


@patch('auth.view.function.send_activation_email.UserService')
def test_send_activation_email(user_service_mock, database):
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE.value
    )
    UserRepository().create(user)
    code = uuid.uuid4()
    body = {
        'id': str(uuid.uuid4()),
        'name': 'activation_created',
        'produced_at': datetime.datetime.now().isoformat(),
        'payload': {
            'user_id': str(user.id),
            'code': str(code)
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

    user_service_mock().send_activation_email.assert_called_once_with(
        user_id=str(user.id),
        activation_code=str(code)
    )
