from unittest.mock import patch

from auth.application.user_service import UserService
from auth.domain.user import User


@patch('auth.application.user_service.UserAdapter')
def test_signup(user_adapter_mock):
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

    user_adapter_mock().create.assert_called_once_with(
        full_name='Foo Bar',
        email='foo@email.com',
        password='a-secret'
    )
    assert persisted_user == user
