import datetime
import json
import uuid

from auth.domain.user_status import UserStatus
from auth.infrastructure.entity.user import User
from auth.infrastructure.repository.user import UserRepository
from auth.view.function.create_activation import handle


def test_create_activation(database):
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE.value
    )
    UserRepository().create(user)
    body = {
        'id': str(uuid.uuid4()),
        'name': 'user_created',
        'produced_at': datetime.datetime.now().isoformat(),
        'payload': {
            'user_id': str(user.id)
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

    assert len(user.activations) == 1
