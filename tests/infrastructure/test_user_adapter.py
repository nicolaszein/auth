import uuid
from unittest.mock import MagicMock, patch

from auth.domain.user import User
from auth.infrastructure.user_adapter import UserAdapter


@patch('auth.infrastructure.user_adapter.User')
@patch('auth.infrastructure.user_adapter.Password')
@patch('auth.infrastructure.user_adapter.UserRepository')
def test_create(user_repository_mock, password_mock, user_entity_mock):
    password = 'a-secret'
    password_mock.hash_password.return_value = 'hashed_password'
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )
    user_entity = MagicMock()
    user_repository_mock().create.return_value = user_entity
    user_entity.to_domain.return_value = user

    result = UserAdapter().create(full_name='Foo Bar', email='foo.bar@email.com', password=password)

    assert result == user
    user_entity_mock.assert_called_once_with(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )


@patch('auth.infrastructure.user_adapter.User')
@patch('auth.infrastructure.user_adapter.UserRepository')
def test_update(user_repository_mock, user_entity_mock):
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )
    user_entity = MagicMock()
    user_repository_mock().update.return_value = user_entity
    user_entity.to_domain.return_value = user

    result = UserAdapter().update(user=user)

    assert result == user
    user_entity_mock.from_domain.assert_called_once_with(user)
