import pytest

from auth.domain.exception import UserWithInvalidEmailError
from auth.domain.user import User


def test_valid_email():
    email = 'foo.bar@email.com'

    user = User(full_name='Foo Bar', email=email, password='a-secret')

    assert user.email == email


def test_invalid_email():
    email = 'invalid-email'

    with pytest.raises(UserWithInvalidEmailError):
        User(full_name='Foo Bar', email=email, password='a-secret')
