import uuid

from auth.application.exception import InvalidCredentials, UserNotActivated
from auth.domain.user import User
from auth.infrastructure.password import Password
from auth.infrastructure.user_adapter import UserAdapter


class UserService:

    def __init__(self):
        self.__user_adapter = UserAdapter()
        self.__password = Password

    def sign_up(self, full_name, email, password):
        hashed_password = self.__password.hash_password(password)
        user = User(
            id=uuid.uuid4(),
            full_name=full_name,
            email=email,
            password=hashed_password
        )
        user.add_user_created_event()
        return self.__user_adapter.create(user)

    def sign_in(self, email, password):
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

    def send_activation_email(self, user_id, activation_code):
        user = self.__user_adapter.fetch_by_id(user_id)

        self.__user_adapter.send_activation_email(user=user, activation_code=activation_code)
