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

    def create(self, user):
        return self.__save(user)

    def update(self, user):
        user_updated = db.session.merge(user)
        return self.__save(user_updated)

    def __save(self, user):
        try:
            db.session.add(user)
            db.session.commit()
            db.session.flush()

            for event in user.events:
                bus.emit(event.name, **event.to_dict())

            return user
        except Exception as e:
            db.session.rollback()

            raise e
