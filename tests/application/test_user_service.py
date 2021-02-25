import uuid
from datetime import datetime
from unittest.mock import patch

import pytest

from auth.application.exception import InvalidCredentials, UserNotActivated
from auth.application.user_service import UserService
from auth.domain.activation import Activation
from auth.domain.user import User


@patch('auth.application.user_service.Password')
@patch('auth.application.user_service.UserAdapter')
def test_sign_up(user_adapter_mock, password_mock):
    password_mock.hash_password.return_value = 'hashed-password'
    user = User(
        full_name='Foo Bar',
        email='foo@email.com',
        password='hashed-password'
    )
    user_adapter_mock().create.return_value = user

    persisted_user = UserService().sign_up(
        full_name='Foo Bar',
        email='foo@email.com',
        password='a-secret'
    )

    assert persisted_user == user


@patch('auth.application.user_service.Password')
@patch('auth.application.user_service.UserAdapter')
def test_sign_in(user_adapter_mock, password_mock):
    email = 'foo@email.com'
    password = 'a-secret'
    password_mock.validate_password.return_value = True
    user = User(
        full_name='Foo Bar',
        email='foo@email.com',
        password='hashed-password',
        is_active=True
    )
    user_adapter_mock().fetch_by_email.return_value = user
    user_adapter_mock().create_session.return_value = 'Session'

    result = UserService().sign_in(
        email=email,
        password=password
    )

    assert result == 'Session'
    user_adapter_mock().fetch_by_email.assert_called_once_with(email=email)
    user_adapter_mock().create_session.assert_called_once_with(user=user)
    password_mock.validate_password.assert_called_once_with(
        password=password,
        hashed_password='hashed-password'
    )


@patch('auth.application.user_service.Password')
@patch('auth.application.user_service.UserAdapter')
def test_sign_in_with_password_invalid(user_adapter_mock, password_mock):
    email = 'foo@email.com'
    password = 'invalid-password'
    user = User(
        full_name='Foo Bar',
        email='foo@email.com',
        password='hashed-password'
    )
    password_mock.validate_password.return_value = False
    user_adapter_mock().fetch_by_email.return_value = user

    with pytest.raises(InvalidCredentials):
        UserService().sign_in(
            email=email,
            password=password
        )


@patch('auth.application.user_service.Password')
@patch('auth.application.user_service.UserAdapter')
def test_sign_in_with_user_not_activated(user_adapter_mock, password_mock):
    email = 'foo@email.com'
    password = 'invalid-password'
    user = User(
        full_name='Foo Bar',
        email='foo@email.com',
        password='hashed-password',
        is_active=False
    )
    password_mock.validate_password.return_value = True
    user_adapter_mock().fetch_by_email.return_value = user

    with pytest.raises(UserNotActivated):
        UserService().sign_in(
            email=email,
            password=password
        )


@patch('auth.application.user_service.UserAdapter')
def test_create_activation(user_adapter_mock):
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        full_name='Foo Bar',
        email='foo@email.com',
        password='hashed-password'
    )
    user_adapter_mock().fetch_by_id.return_value = user
    user_adapter_mock().update.side_effect = lambda x: x

    persisted_user = UserService().create_activation(user_id=user_id)

    assert len(persisted_user.activations) == 1


@patch('auth.application.user_service.UserAdapter')
def test_activate(user_adapter_mock):
    activation = Activation(user=None, created_at=datetime.now())
    user = User(
        full_name='Foo Bar',
        email='foo@email.com',
        password='hashed-password',
        activations=[activation]
    )
    user_adapter_mock().fetch_by_activation_code.return_value = user
    user_adapter_mock().update.side_effect = lambda x: x

    persisted_user = UserService().activate(code=activation.code)

    assert len(persisted_user.activations) == 0
    assert persisted_user.is_active
