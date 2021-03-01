import uuid
from unittest.mock import patch

from auth.domain.user import User as UserDomain
from auth.domain.user_status import UserStatus
from auth.infrastructure.entity.user import User
from auth.infrastructure.repository.user import UserRepository


def test_create(database):
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE.value
    )

    UserRepository().create(user)

    assert user.id
    assert user.created_at


def test_update(database):
    user = User(
        full_name='Foo Wrong',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE.value
    )
    UserRepository().create(user)
    user.full_name = 'Foo Bar'

    updated_user = UserRepository().update(user)

    assert updated_user.full_name == 'Foo Bar'


def test_fetch_by_id(database):
    entity = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE.value
    )
    UserRepository().create(entity)

    user = UserRepository().fetch_by_id(id=entity.id)

    assert user.id == entity.id


def test_fetch_by_id_not_found(database):
    user = UserRepository().fetch_by_id(id=uuid.uuid4())

    assert user is None


def test_fetch_by_email(database):
    email = 'foo.bar@email.com'
    entity = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE.value
    )
    UserRepository().create(entity)

    user = UserRepository().fetch_by_email(email=email)

    assert user.id == entity.id


def test_fetch_by_activation_code(database):
    domain = UserDomain(full_name='Foo Wrong', email='foo.bar@email.com', password='a-secret')
    domain.create_activation()
    code = domain.activations[0].code
    entity = User.from_domain(domain)
    UserRepository().create(entity)

    user = UserRepository().fetch_by_activation_code(code)

    assert user.id == entity.id


def test_fetch_by_reset_password_token(database):
    user = UserDomain(
        full_name='Foo Wrong',
        email='foo.bar@email.com',
        password='a-secret',
    )
    entity = User.from_domain(user.create_reset_password_token())
    UserRepository().create(entity)

    user = UserRepository().fetch_by_reset_password_token(entity.reset_password_token)

    assert user.id == entity.id


@patch('auth.infrastructure.repository.user.bus')
def test_emit_events(bus_mock, database):
    user = UserDomain(full_name='Foo Wrong', email='foo.bar@email.com', password='a-secret')
    user.add_user_created_event()
    entity = User.from_domain(user)

    UserRepository().create(entity)

    bus_mock.emit.assert_called_once_with('user_created', user=user)
