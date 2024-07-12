from Auth.model import User
from Core.extensions import db


def load_user(user_id: str):
    try:
        user_id = int(user_id)
    except ValueError:
        user_id = None

    return db.session.get(User, user_id)
