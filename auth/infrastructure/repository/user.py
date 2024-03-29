from auth.infrastructure.database import db
from auth.infrastructure.entity.activation import Activation
from auth.infrastructure.entity.user import User
from auth.infrastructure.event_bus import bus


class UserRepository:

    def __init__(self):
        self.__entity = User

    def fetch_by_id(self, id):
        return db.session.query(self.__entity).filter_by(id=id).first()

    def fetch_by_email(self, email):
        return db.session.query(self.__entity).filter_by(email=email).first()

    def fetch_by_activation_code(self, code):
        activation = db.session.query(Activation).filter_by(code=code).first()

        if not activation:
            return None

        return activation.user

    def fetch_by_reset_password_token(self, reset_password_token):
        return db.session.query(self.__entity).filter_by(
            reset_password_token=reset_password_token
        ).first()

    def create(self, user):
        saved_user = self.__save(user)
        self.__emit_events(user.events)
        return saved_user

    def update(self, user):
        updated_user = db.session.merge(user)
        saved_user = self.__save(updated_user)
        self.__emit_events(user.events)
        return saved_user

    def __save(self, user):
        try:
            db.session.add(user)
            db.session.commit()
            db.session.flush()

            return user
        except Exception as e:
            db.session.rollback()

            raise e

    def __emit_events(self, events):
        for event in events:
            bus.emit(event.name, **event.to_dict())
