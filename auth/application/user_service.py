from auth.domain.user import User
from auth.infrastructure.password import Password
from auth.infrastructure.user_adapter import UserAdapter


class UserService:

    def __init__(self):
        self.__user_adapter = UserAdapter()
        self.__password = Password

    def signup(self, full_name, email, password):
        hashed_password = Password.hash_password(password)
        user = User(
            full_name=full_name,
            email=email,
            password=hashed_password
        )
        return self.__user_adapter.create(user)

    def activate(self, code):
        user = self.__user_adapter.fetch_by_activation_code(code=code)

        return self.__user_adapter.update(user.activate(code=code))
