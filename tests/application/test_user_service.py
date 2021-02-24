import uuid
from datetime import datetime
from unittest.mock import patch

from auth.application.user_service import UserService
from auth.domain.activation import Activation
from auth.domain.user import User


@patch('auth.application.user_service.Password')
@patch('auth.application.user_service.UserAdapter')
def test_signup(user_adapter_mock, password_mock):
    password_mock.hash_password.return_value = 'hashed-password'
    user = User(
        full_name='Foo Bar',
        email='foo@email.com',
        password='hashed-password'
    )
    user_adapter_mock().create.return_value = user

    persisted_user = UserService().signup(
        full_name='Foo Bar',
        email='foo@email.com',
        password='a-secret'
    )

    assert persisted_user == user


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
