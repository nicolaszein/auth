from unittest.mock import patch

from auth.domain.event.user_created import UserCreated
from auth.domain.user import User as UserDomain
from auth.infrastructure.entity.user import User
from auth.infrastructure.repository.user import UserRepository


def test_create(database):
    user = User(full_name='Foo Bar', email='foo.bar@email.com', password='a-secret')

    UserRepository().create(user)

    assert user.id
    assert user.created_at


def test_update(database):
    user = User(full_name='Foo Wrong', email='foo.bar@email.com', password='a-secret')
    UserRepository().create(user)
    user.full_name = 'Foo Bar'

    updated_user = UserRepository().update(user)

    assert updated_user.full_name == 'Foo Bar'


def test_fetch_by_activation_code(database):
    domain = UserDomain(full_name='Foo Wrong', email='foo.bar@email.com', password='a-secret')
    domain.create_activation()
    code = domain.activations[0].code
    entity = User.from_domain(domain)
    UserRepository().create(entity)

    user = UserRepository().fetch_by_activation_code(code)

    assert user.id == entity.id


@patch('auth.infrastructure.repository.user.bus')
def test_emit_events(bus_mock, database):
    user = UserDomain(full_name='Foo Wrong', email='foo.bar@email.com', password='a-secret')
    event = UserCreated(user)
    entity = User(
        full_name='Foo Wrong',
        email='foo.bar@email.com',
        password='a-secret',
        events=[event]
    )

    UserRepository().create(entity)

    bus_mock.emit.assert_called_once_with(event.name, **event.to_dict())
