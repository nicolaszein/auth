import uuid
from dataclasses import replace
from unittest.mock import MagicMock, patch

import pytest

from auth.domain.user import User
from auth.infrastructure.exception import UserNotFound
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


@patch('auth.infrastructure.user_adapter.UserRepository')
def test_fetch_by_id(user_repository_mock):
    id = uuid.uuid4()
    user = User(
        id=id,
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )
    user_entity = MagicMock()
    user_repository_mock().fetch_by_id.return_value = user_entity
    user_entity.to_domain.return_value = user

    result = UserAdapter().fetch_by_id(id=id)

    assert result == user


@patch('auth.infrastructure.user_adapter.UserRepository')
def test_fetch_by_id_with_user_not_found(user_repository_mock):
    user_repository_mock().fetch_by_id.return_value = None

    with pytest.raises(UserNotFound):
        UserAdapter().fetch_by_id(id=uuid.uuid4())


@patch('auth.infrastructure.user_adapter.UserRepository')
def test_fetch_by_email(user_repository_mock):
    id = uuid.uuid4()
    email = 'foo.bar@email.com'
    user = User(
        id=id,
        full_name='Foo Bar',
        email=email,
        password='hashed_password'
    )
    user_entity = MagicMock()
    user_repository_mock().fetch_by_email.return_value = user_entity
    user_entity.to_domain.return_value = user

    result = UserAdapter().fetch_by_email(email=email)

    assert result == user


@patch('auth.infrastructure.user_adapter.UserRepository')
def test_fetch_by_email_with_user_not_found(user_repository_mock):
    user_repository_mock().fetch_by_email.return_value = None

    with pytest.raises(UserNotFound):
        UserAdapter().fetch_by_email(email='foo.bar@email.com')


@patch('auth.infrastructure.user_adapter.UserRepository')
def test_fetch_by_activation_code(user_repository_mock):
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )
    user_entity = MagicMock()
    user_repository_mock().fetch_by_activation_code.return_value = user_entity
    user_entity.to_domain.return_value = user
    code = '123'

    result = UserAdapter().fetch_by_activation_code(code=code)

    assert result == user


@patch('auth.infrastructure.user_adapter.UserRepository')
def test_fetch_by_activation_code_with_user_not_found(user_repository_mock):
    code = '123'
    user_repository_mock().fetch_by_activation_code.return_value = None

    with pytest.raises(UserNotFound):
        UserAdapter().fetch_by_activation_code(code=code)
