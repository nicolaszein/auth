import uuid

from auth.domain.activation import Activation as ActivationDomain
from auth.domain.user import User as UserDomain
from auth.infrastructure.entity.activation import Activation
from auth.infrastructure.entity.user import User


def test_from_domain():
    user = UserDomain(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        is_active=True
    )
    domain = ActivationDomain(user=user)

    activation = Activation.from_domain(domain)

    assert activation.user_id == user.id
    assert activation.code == domain.code


def test_to_domain():
    code = '123456'
    activation_id = uuid.uuid4()
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        is_active=True
    )
    activation = Activation(id=activation_id, user_id=user.id, code=code)
    activation.user = user

    domain = activation.to_domain()

    assert domain.id == activation_id
    assert domain.code == code
    assert domain.user == user
