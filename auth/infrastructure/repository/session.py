from auth.infrastructure.database import db


class SessionRepository:

    def create(self, session):
        try:
            db.session.add(session)
            db.session.commit()
            db.session.flush()

            return session
        except Exception as e:
            db.session.rollback()

            raise e
