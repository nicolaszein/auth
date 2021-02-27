import uuid

from auth.domain.user_status import UserStatus
from auth.infrastructure.entity.session import Session
from auth.infrastructure.entity.user import User
from auth.infrastructure.repository.session import SessionRepository
from auth.infrastructure.repository.user import UserRepository


def test_create(database):
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE.value
    )
    UserRepository().create(user)
    session = Session(user_id=user.id, refresh_token=str(uuid.uuid4()))

    SessionRepository().create(session)

    assert user.id
    assert user.created_at
