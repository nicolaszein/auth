import uuid
from datetime import datetime

from auth.domain.activation import Activation as ActivationDomain
from auth.domain.user import User as UserDomain
from auth.domain.user_status import UserStatus
from auth.infrastructure.entity.activation import Activation
from auth.infrastructure.entity.user import User


def test_from_domain():
    reset_password_token_created_at = datetime.now()
    domain = UserDomain(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE,
        reset_password_token='123',
        reset_password_token_created_at=reset_password_token_created_at
    )
    domain.create_activation()

    user_entity = User.from_domain(domain)

    assert user_entity.id == domain.id
    assert user_entity.full_name == domain.full_name
    assert user_entity.email == domain.email
    assert user_entity.password == domain.password
    assert user_entity.status == UserStatus.ACTIVE.value
    assert user_entity.reset_password_token == '123'
    assert user_entity.reset_password_token_created_at == reset_password_token_created_at
    assert len(user_entity.activations) == 1
    assert isinstance(user_entity.activations[0], Activation)


def test_to_domain():
    reset_password_token_created_at = datetime.now()
    user_id = uuid.uuid4()
    activation = Activation(user_id=user_id, code='123')
    entity = User(
        id=user_id,
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE.value,
        reset_password_token='123',
        reset_password_token_created_at=reset_password_token_created_at,
        activations=[activation]
    )

    domain = entity.to_domain()

    assert domain.id == entity.id
    assert domain.full_name == entity.full_name
    assert domain.email == entity.email
    assert domain.password == entity.password
    assert domain.is_active
    assert domain.reset_password_token == '123'
    assert domain.reset_password_token_created_at == reset_password_token_created_at
    assert len(domain.activations) == 1
    assert isinstance(domain.activations[0], ActivationDomain)
