from auth.infrastructure.database import db
from auth.infrastructure.entity.user import User


class UserRepository:

    def __init__(self):
        self.__entity = User

    def create(self, user):
        try:
            db.session.add(user)
            db.session.commit()
            db.session.flush()
        except Exception as e:
            db.session.rollback()

            raise e
