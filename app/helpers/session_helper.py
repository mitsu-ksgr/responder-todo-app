#
# Session Helper
#
import bcrypt

from app.models.user import User


def hash_password(password):
    """Return a password hash.

    Args:
        password (str): the user's plain text password.

    Returns:
        str: Returns the hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password, password_hash):
    """Verifies that the given hash matches the given password.

    Args:
        password (str): the user's plain text password.
        password_hash (str): the user's password hash.

    Returns:
        bool: Returns the verification result.
    """
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def login(resp, user_id):
    resp.session["user_id"] = user_id


def logout(resp):
    if "user_id" in resp.session:
        del resp.session["user_id"]


def current_user(resp, db_session):
    if "user_id" not in resp.session:
        return None
    return db_session.query(User).get(resp.session["user_id"])
