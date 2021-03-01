import datetime
import uuid

import pytest

from auth.domain.activation import Activation
from auth.domain.event.activation_created import ActivationCreated
from auth.domain.event.user_created import UserCreated
from auth.domain.exception import ActivationExpired, ActivationNotFound, UserWithInvalidEmail
from auth.domain.user import User
from auth.domain.user_status import UserStatus


def test_valid_email():
    email = 'foo.bar@email.com'

    user = User(full_name='Foo Bar', email=email, password='a-secret')

    assert user.email == email


def test_invalid_email():
    email = 'invalid-email'

    with pytest.raises(UserWithInvalidEmail):
        User(full_name='Foo Bar', email=email, password='a-secret')


def test_is_valid_true():
    email = 'foo.bar@email.com'

    user = User(full_name='Foo Bar', email=email, password='a-secret', status=UserStatus.ACTIVE)

    assert user.is_active


def test_is_valid_false():
    email = 'foo.bar@email.com'

    user = User(full_name='Foo Bar', email=email, password='a-secret', status=UserStatus.INACTIVE)

    assert not user.is_active


def test_add_user_created_event():
    email = 'foo.bar@email.com'
    user = User(full_name='Foo Bar', email=email, password='a-secret')

    user.add_user_created_event()

    assert len(user.events) == 1
    assert isinstance(user.events[0], UserCreated)


def test_create_activation():
    email = 'foo.bar@email.com'
    user = User(id=uuid.uuid4(), full_name='Foo Bar', email=email, password='a-secret')

    user.create_activation()

    assert len(user.activations) == 1
    assert isinstance(user.activations[0], Activation)
    assert len(user.events) == 1
    assert isinstance(user.events[0], ActivationCreated)


def test_activate():
    created_at = datetime.datetime.now()
    activation = Activation(user=None, created_at=created_at)
    email = 'foo.bar@email.com'
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email=email,
        password='a-secret',
        activations=[activation]
    )

    activated_user = user.activate(code=activation.code)

    assert len(activated_user.activations) == 0
    assert activated_user.is_active


def test_activate_with_code_not_found():
    created_at = datetime.datetime.now()
    activation = Activation(user=None, created_at=created_at)
    email = 'foo.bar@email.com'
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email=email,
        password='a-secret',
        activations=[activation]
    )

    with pytest.raises(ActivationNotFound):
        user.activate(code='not_found')


def test_activate_with_expired_code():
    created_at = datetime.datetime(2019, 1, 1)
    activation = Activation(user=None, created_at=created_at)
    email = 'foo.bar@email.com'
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email=email,
        password='a-secret',
        activations=[activation]
    )

    with pytest.raises(ActivationExpired):
        user.activate(code=activation.code)


def test_first_name():
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
    )

    assert user.first_name == 'Foo'


def test_first_name():
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
    )

    assert user.first_name == 'Foo'


def test_create_reset_password_token():
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
    )

    updated_user = user.create_reset_password_token()

    assert updated_user.reset_password_token
    assert updated_user.reset_password_token_created_at
    assert len(updated_user.events) == 1
