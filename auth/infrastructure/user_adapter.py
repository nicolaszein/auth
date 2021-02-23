from auth.infrastructure.entity.user import User
from auth.infrastructure.password import Password
from auth.infrastructure.repository.user import UserRepository


class UserAdapter:

    def __init__(self):
        self.__repository = UserRepository()
        self.__password = Password

    def create(self, user):
        entity = User.from_domain(user)

        return self.__repository.create(entity).to_domain()

    def update(self, user):
        entity = User.from_domain(user)

        return self.__repository.update(entity).to_domain()
