from flask import session, request
from Auth.model import User
from flask import current_app

def load_user(user_id: str):
    try:
        user_id = int(user_id)
    except ValueError:
        user_id = None
    db = current_app.extensions['sqlalchemy']
    query = db.session.select(User).filter_by(id=user_id)
    return db.session.execute(query).scalar_one_or_none()



def login_user(user_object):
    session['username'] = user_object.username
    session['account-id'] = user_object.id
    session['password-hash'] = user_object.password
    session['login'] = True
    session['role'] = 'user'

def logout_user():
    session.pop('username')
    session.pop('account-id')
    session.pop('password-hash')
    session.pop('login')
    session.pop('role')

def login_admin():
    ...

def logout_admin():
    ...

