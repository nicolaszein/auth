from auth.infrastructure.database import db
from auth.infrastructure.entity.user import User
from auth.infrastructure.event_bus import bus


class UserRepository:

    def __init__(self):
        self.__entity = User

    def create(self, user):
        return self.__save(user)

    def update(self, user):
        return self.__save(user)

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
