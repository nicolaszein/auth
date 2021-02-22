from auth.infrastructure.entity.user import User
from auth.infrastructure.password import Password
from auth.infrastructure.repository.user import UserRepository


class UserAdapter:

    def __init__(self):
        self.__repository = UserRepository()
        self.__password = Password

    def create(self, full_name, email, password):
        hashed_password = self.__password.hash_password(password)
        entity = User(
            full_name=full_name,
            email=email,
            password=hashed_password
        )

        return self.__repository.create(entity).to_domain()

    def update(self, user):
        entity = User.from_domain(user)

        return self.__repository.update(entity).to_domain()
