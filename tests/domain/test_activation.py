import uuid

from auth.domain.activation import Activation
from auth.domain.user import User


def test_user_id():
    email = 'foo.bar@email.com'
    user = User(id=uuid.uuid4(), full_name='Foo Bar', email=email, password='a-secret')

    activation = Activation(user=user)

    assert activation.user_id == user.id
