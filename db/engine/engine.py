from sqlalchemy import create_engine, URL
from sqlalchemy.orm import scoped_session, sessionmaker
from db.model.basemodel import Base
from db.model.user import Users
import os
from shared.services.logger import AuthXLogger


logging = AuthXLogger(name='AuthXEngine', set_channels=['file']).logger


class DBEngine(object):
    """
    This class manages DataBase connection
    """
    __engine = None
    __session = None
    __url = None

    def __init__(self):
        self.__url = URL(
            drivername=os.getenv('DB_DRIVER', ""),
            username=os.getenv('DB_USERNAME', ""),
            password=os.getenv('DB_PASSWORD', ""),
            host=os.getenv('DB_HOST', ""),
            port=os.getenv('DB_PORT', -1),
            database=os.getenv('DB_NAME', ""),
            query={'application_name': 'AuthX'}
        )

        logging.info(f"Engine Configured URL: [{self.__url}]")

        self.__engine = create_engine(self.__url, echo=True)
        if not self.__engine:
            logging.error(msg="Issue With Creating Engine")
        os.environ['DB_URL'] = str(self.__engine.url)

    def load(self):
        if self.__engine:
            Base.metadata.create_all(self.__engine)
            maker = sessionmaker(bind=self.__engine, expire_on_commit=False)
            Session = scoped_session(maker)
            return Session
        return None
