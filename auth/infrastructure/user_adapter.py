from auth.domain.session import Session as SessionDomain
from auth.infrastructure.entity.session import Session
from auth.infrastructure.entity.user import User
from auth.infrastructure.exception import SessionNotFound, UserNotFound
from auth.infrastructure.repository.session import SessionRepository
from auth.infrastructure.repository.user import UserRepository
from auth.infrastructure.sendgrid_client import SendgridClient
from auth.infrastructure.token import Token
from auth.settings import ACTIVATION_EMAIL_TEMPLATE_ID


class UserAdapter:

    def __init__(self):
        self.__repository = UserRepository()
        self.__session_repository = SessionRepository()
        self.__token = Token()
        self.__sendgrid_client = SendgridClient()

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
        refresh_token = self.__token.generate_refresh_token(user_id=str(user.id))
        session = self.__session_repository.create(
            Session(
                user_id=user.id,
                refresh_token=refresh_token
            )
        )

        access_token = self.__token.generate_token(user_id=str(user.id), session_id=str(session.id))

        return SessionDomain(user=user, access_token=access_token, refresh_token=refresh_token)

    def refresh_session(self, refresh_token):
        session = self.__session_repository.fetch_by_refresh_token(refresh_token=refresh_token)

        if not session:
            raise SessionNotFound('Session not found')

        access_token = self.__token.generate_token(
            user_id=str(session.user_id),
            session_id=str(session.id)
        )

        return SessionDomain(
            user=session.user,
            access_token=access_token,
            refresh_token=refresh_token
        )

    def send_activation_email(self, user, activation_code):
        subject = 'Por favor, confirme seu endereço de email'
        template_data = dict(first_name=user.first_name, code=activation_code)

        self.__sendgrid_client.send_template_message(
            to=user.email,
            subject=subject,
            template_id=ACTIVATION_EMAIL_TEMPLATE_ID,
            template_data=template_data
        )
