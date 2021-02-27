import datetime
import uuid

from auth.domain.activation import Activation as ActivationDomain
from auth.domain.user import User as UserDomain
from auth.domain.user_status import UserStatus
from auth.infrastructure.entity.activation import Activation
from auth.infrastructure.entity.user import User


def test_from_domain():
    created_at = datetime.datetime.now()
    user = UserDomain(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE
    )
    domain = ActivationDomain(user=user, created_at=created_at)

    activation = Activation.from_domain(domain)

    assert activation.user_id == user.id
    assert activation.code == domain.code
    assert activation.created_at == created_at


def test_to_domain():
    created_at = datetime.datetime.now()
    code = '123456'
    activation_id = uuid.uuid4()
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE
    )
    activation = Activation(id=activation_id, user_id=user.id, code=code, created_at=created_at)
    activation.user = user

    domain = activation.to_domain()

    assert domain.id == activation_id
    assert domain.code == code
    assert domain.user == user
    assert domain.created_at == created_at
