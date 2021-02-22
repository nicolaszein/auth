from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from auth.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        self.__metadata = MetaData()
        self.__engine = engine
        self.__session = Session

    @property
    def metadata(self):
        return self.__metadata

    @property
    def session(self):
        return self.__session

    @property
    def engine(self):
        return self.__engine
