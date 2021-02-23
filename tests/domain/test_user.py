import uuid

import pytest

from auth.domain.activation import Activation
from auth.domain.event.user_created import UserCreated
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


def test_init_append_user_created_event():
    email = 'foo.bar@email.com'

    user = User(full_name='Foo Bar', email=email, password='a-secret')

    assert len(user.events) == 1
    assert isinstance(user.events[0], UserCreated)


def test_init_does_not_append_user_created_event():
    email = 'foo.bar@email.com'

    user = User(id=uuid.uuid4(), full_name='Foo Bar', email=email, password='a-secret')

    assert len(user.events) == 0


def test_create_activation():
    email = 'foo.bar@email.com'
    user = User(id=uuid.uuid4(), full_name='Foo Bar', email=email, password='a-secret')

    user.create_activation()

    assert len(user.activations) == 1
    assert isinstance(user.activations[0], Activation)
