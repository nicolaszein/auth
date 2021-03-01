from auth.infrastructure.database import db
from auth.infrastructure.entity.session import Session


class SessionRepository:

    def __init__(self):
        self.__entity = Session

    def fetch_by_id(self, id):
        return db.session.query(self.__entity).filter_by(id=id).first()

    def fetch_by_refresh_token(self, refresh_token):
        return db.session.query(self.__entity).filter_by(refresh_token=refresh_token).first()

    def create(self, session):
        try:
            db.session.add(session)
            db.session.commit()
            db.session.flush()

            return session
        except Exception as e:
            db.session.rollback()

            raise e

    def delete(self, session):
        try:
            db.session.delete(session)
            db.session.commit()
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            raise e
