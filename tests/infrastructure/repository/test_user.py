from auth.infrastructure.entity.user import User
from auth.infrastructure.repository.user import UserRepository


def test_create(database):
    user = User(full_name='Foo Bar', email='foo.bar@email.com', password='a-secret')

    UserRepository().create(user)

    assert user.id
    assert user.created_at


def test_update(database):
    user = User(full_name='Foo Wrong', email='foo.bar@email.com', password='a-secret')
    UserRepository().create(user)
    user.full_name = 'Foo Bar'

    updated_user = UserRepository().update(user)

    assert updated_user.full_name == 'Foo Bar'
