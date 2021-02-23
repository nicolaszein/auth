import uuid

from auth.domain.activation import Activation as ActivationDomain
from auth.domain.user import User as UserDomain
from auth.infrastructure.entity.activation import Activation
from auth.infrastructure.entity.user import User


def test_from_domain():
    domain = UserDomain(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        is_active=True
    )
    domain.create_activation()

    user_entity = User.from_domain(domain)

    assert user_entity.id == domain.id
    assert user_entity.full_name == domain.full_name
    assert user_entity.email == domain.email
    assert user_entity.password == domain.password
    assert user_entity.is_active
    assert len(user_entity.activations) == 1
    assert isinstance(user_entity.activations[0], Activation)


def test_to_domain():
    user_id = uuid.uuid4()
    activation = Activation(user_id=user_id, code='123')
    entity = User(
        id=user_id,
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        is_active=True,
        activations=[activation]
    )

    domain = entity.to_domain()

    assert domain.id == entity.id
    assert domain.full_name == entity.full_name
    assert domain.email == entity.email
    assert domain.password == entity.password
    assert domain.is_active
    assert len(domain.activations) == 1
    assert isinstance(domain.activations[0], ActivationDomain)
