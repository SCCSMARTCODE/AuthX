from bcrypt import gensalt, hashpw, checkpw
import base64


def hash_pw(password: str) -> str:
    """
    Hashes a password using bcrypt and returns it as a base64 encoded string.

    :param password: The plaintext password to hash.
    :return: The hashed password as a base64 encoded string.
    """
    password = password.encode('utf-8')
    salt = gensalt()
    hash_ = hashpw(password, salt)
    return base64.b64encode(hash_).decode('utf-8')


def check_pw(password: str, stored_hash: str) -> bool:
    """
    Checks if the provided password matches the stored hashed password.

    :param password: The plaintext password to check.
    :param stored_hash: The base64 encoded hashed password to compare against.
    :return: True if the password matches, False otherwise.
    """
    password = password.encode('utf-8')
    hash_ = base64.b64decode(stored_hash)
    return checkpw(password, hash_)
