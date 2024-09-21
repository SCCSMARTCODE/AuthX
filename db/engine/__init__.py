from .engine import DBEngine, logging
from contextlib import contextmanager


engine = DBEngine()
Session = engine.load()


@contextmanager
def session_manager():
    session = Session()
    try:
        yield session
    except Exception as e:
        logging.error(msg=e)
        session.rollback()
    finally:
        session.close()
