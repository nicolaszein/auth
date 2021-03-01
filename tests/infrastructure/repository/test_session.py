import uuid

from auth.domain.user_status import UserStatus
from auth.infrastructure.entity.session import Session
from auth.infrastructure.entity.user import User
from auth.infrastructure.repository.session import SessionRepository
from auth.infrastructure.repository.user import UserRepository


def test_fetch_by_id(database):
    refresh_token = str(uuid.uuid4())
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE.value
    )
    UserRepository().create(user)
    session = Session(user_id=user.id, refresh_token=refresh_token)
    SessionRepository().create(session)

    result = SessionRepository().fetch_by_id(id=session.id)

    assert result.id == session.id


def test_fetch_by_refresh_token(database):
    refresh_token = str(uuid.uuid4())
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE.value
    )
    UserRepository().create(user)
    session = Session(user_id=user.id, refresh_token=refresh_token)
    SessionRepository().create(session)

    result = SessionRepository().fetch_by_refresh_token(refresh_token=refresh_token)

    assert result.id == session.id


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


def test_delete(database):
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE.value
    )
    UserRepository().create(user)
    session = Session(user_id=user.id, refresh_token=str(uuid.uuid4()))
    SessionRepository().create(session)

    SessionRepository().delete(session)

    assert not SessionRepository().fetch_by_id(session.id)
