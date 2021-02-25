from auth.domain.session import Session as SessionDomain
from auth.infrastructure.entity.session import Session
from auth.infrastructure.entity.user import User
from auth.infrastructure.exception import UserNotFound
from auth.infrastructure.repository.session import SessionRepository
from auth.infrastructure.repository.user import UserRepository
from auth.infrastructure.token import Token


class UserAdapter:

    def __init__(self):
        self.__repository = UserRepository()
        self.__session_repository = SessionRepository()
        self.__token = Token()

    def fetch_by_id(self, id):
        user = self.__repository.fetch_by_id(id=id)

        if not user:
            raise UserNotFound(f'User with id {id} not found')

        return user.to_domain()

    def fetch_by_email(self, email):
        user = self.__repository.fetch_by_email(email=email)

        if not user:
            raise UserNotFound(f'User with id {email} not found')

        return user.to_domain()

    def fetch_by_activation_code(self, code):
        user = self.__repository.fetch_by_activation_code(code=code)

        if not user:
            raise UserNotFound(f'User with activation code {code} not found')

        return user.to_domain()

    def create(self, user):
        entity = User.from_domain(user)

        return self.__repository.create(entity).to_domain()

    def update(self, user):
        entity = User.from_domain(user)

        return self.__repository.update(entity).to_domain()

    def create_session(self, user):
        refresh_token = self.__token.generate_refresh_token(user_id=user.id)
        session = self.__session_repository.create(
            Session(
                user_id=user.id,
                refresh_token=refresh_token
            )
        )

        access_token = self.__token.generate_token(user_id=user.id, session_id=session.id)

        return SessionDomain(user=user, access_token=access_token, refresh_token=refresh_token)
