import datetime
import uuid

from auth.domain.activation import Activation
from auth.domain.user import User
from auth.settings import ACTIVATION_EXPIRE_TIME


def test_user_id():
    email = 'foo.bar@email.com'
    user = User(id=uuid.uuid4(), full_name='Foo Bar', email=email, password='a-secret')

    activation = Activation(user=user)

    assert activation.user_id == user.id


def test_expire_date():
    created_at = datetime.datetime.now()
    expected_expire_date = created_at + datetime.timedelta(seconds=ACTIVATION_EXPIRE_TIME)
    email = 'foo.bar@email.com'
    user = User(id=uuid.uuid4(), full_name='Foo Bar', email=email, password='a-secret')
    activation = Activation(user=user, created_at=created_at)

    assert activation.expire_date == expected_expire_date


def test_is_expired_false():
    created_at = datetime.datetime.now()
    email = 'foo.bar@email.com'
    user = User(id=uuid.uuid4(), full_name='Foo Bar', email=email, password='a-secret')
    activation = Activation(user=user, created_at=created_at)

    assert not activation.is_expired


def test_is_expired_false():
    created_at = datetime.datetime(2019, 1, 1)
    email = 'foo.bar@email.com'
    user = User(id=uuid.uuid4(), full_name='Foo Bar', email=email, password='a-secret')
    activation = Activation(user=user, created_at=created_at)

    assert activation.is_expired
