import uuid
from dataclasses import replace
from unittest.mock import MagicMock, patch

from auth.domain.user import User
from auth.infrastructure.user_adapter import UserAdapter


@patch('auth.infrastructure.user_adapter.User')
@patch('auth.infrastructure.user_adapter.UserRepository')
def test_create(user_repository_mock, user_entity_mock):
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )
    persisted_user = replace(user, id=uuid.uuid4())
    user_entity = MagicMock()
    user_repository_mock().create.return_value = user_entity
    user_entity.to_domain.return_value = persisted_user

    result = UserAdapter().create(user)

    assert result == persisted_user
    user_entity_mock.from_domain.assert_called_once_with(user)


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