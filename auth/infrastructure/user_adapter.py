from auth.infrastructure.entity.user import User
from auth.infrastructure.exception import UserNotFound
from auth.infrastructure.password import Password
from auth.infrastructure.repository.user import UserRepository


class UserAdapter:

    def __init__(self):
        self.__repository = UserRepository()
        self.__password = Password

    def fetch_by_activation_code(self, code):
        user = self.__repository.fetch_by_activation_code(code=code)

        if not user:
            raise UserNotFound(f'User with activation code {code} not found')

        return user

    def create(self, user):
        entity = User.from_domain(user)

        return self.__repository.create(entity).to_domain()

    def update(self, user):
        entity = User.from_domain(user)

        return self.__repository.update(entity).to_domain()
