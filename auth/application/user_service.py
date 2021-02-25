from auth.application.exception import InvalidCredentials, UserNotActivated
from auth.domain.user import User
from auth.infrastructure.password import Password
from auth.infrastructure.user_adapter import UserAdapter


class UserService:

    def __init__(self):
        self.__user_adapter = UserAdapter()
        self.__password = Password

    def signup(self, full_name, email, password):
        hashed_password = self.__password.hash_password(password)
        user = User(
            full_name=full_name,
            email=email,
            password=hashed_password
        )
        return self.__user_adapter.create(user)

    def signin(self, email, password):
        user = self.__user_adapter.fetch_by_email(email=email)

        if not self.__password.validate_password(password=password, hashed_password=user.password):
            raise InvalidCredentials('Invalid credentials')

        if not user.is_active:
            raise UserNotActivated(f'User with email {email} not activated!')

        return self.__user_adapter.create_session(user=user)

    def create_activation(self, user_id):
        user = self.__user_adapter.fetch_by_id(id=user_id)
        user.create_activation()

        return self.__user_adapter.update(user)

    def activate(self, code):
        user = self.__user_adapter.fetch_by_activation_code(code=code)

        return self.__user_adapter.update(user.activate(code=code))
