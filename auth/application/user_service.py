import uuid

from auth.application.exception import InvalidCredentials, UserNotActivated
from auth.domain.user import User
from auth.infrastructure.password import Password
from auth.infrastructure.token import Token
from auth.infrastructure.user_adapter import UserAdapter


class UserService:

    def __init__(self):
        self.__user_adapter = UserAdapter()
        self.__password = Password
        self.__token = Token()

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

    def refresh_session(self, refresh_token):
        return self.__user_adapter.refresh_session(refresh_token=refresh_token)

    def sign_out(self, access_token):
        decoded_token = self.__token.validate_token(access_token)
        self.__user_adapter.delete_session(session_id=decoded_token['session_id'])

    def create_reset_password_token(self, email):
        user = self.__user_adapter.fetch_by_email(email=email)
        updated_user = user.create_reset_password_token()

        return self.__user_adapter.update(updated_user)

    def reset_password(self, new_password, reset_password_token):
        hashed_password = self.__password.hash_password(new_password)
        user = self.__user_adapter.fetch_by_reset_password_token(reset_password_token)

        updated_user = user.reset_password(
            new_password=hashed_password,
            reset_password_token=reset_password_token
        )

        return self.__user_adapter.update(updated_user)

    def send_activation_email(self, user_id, activation_code):
        user = self.__user_adapter.fetch_by_id(user_id)

        self.__user_adapter.send_activation_email(user=user, activation_code=activation_code)

    def send_reset_password_email(self, user_id, reset_password_token):
        user = self.__user_adapter.fetch_by_id(user_id)

        self.__user_adapter.send_reset_password_email(
            user=user,
            reset_password_token=reset_password_token
        )
