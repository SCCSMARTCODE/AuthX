from db.engine import session_manager
from db.model.user import Users
from shared.services.pw_bcrypt import hash_pw, check_pw
from flask_auth import logging


def create_user(args):
    new_user = Users(
        email=args.get('email').strip().lower(),
        password_hash=hash_pw(args.get('password'))
    )
    try:
        with session_manager() as session:
            session.add(new_user)
            session.commit()
            logging.info(f"New User Created With ID: {new_user.get_id()}")
            return new_user
    except Exception as e:
        logging.info(f"New User Creation Failed with Error MSG: {e}")
        return None


def delete_user(user_id):
    try:
        with session_manager() as session:
            user = session.query(Users).filter_by(__id=user_id).first()
            if user:
                session.delete(user)
                logging.info(f"User Deleted With ID: {user.get_id()}")
                return True
    except Exception as e:
        logging.info(f"User Deletion Failed with Error MSG: {e}")
        return None


def get_user_by_email(email):
    try:
        with session_manager() as session:
            user = session.query(Users).filter_by(email=email.strip().lower()).first()
            logging.info(f"Get User By Email Fetched User: {user}")
            if user:
                return user
            else:
                return None
    except Exception as e:
        logging.info(f"Get User By Email Failed with Error MSG: {e}")
        return False
