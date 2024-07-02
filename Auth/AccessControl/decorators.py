from functools import wraps
from flask import abort, session, request, redirect, url_for
from Core.extensions import db
from Auth.model import User
from Admin.model import Admin

def admin_login_required(f):
    """
    Base Decorator For Login admin to their accounts
    """
    @wraps(f)
    def inner_decorator(*args, **kwargs):

        if not session.get("login"):
            session.clear()
            abort(401)

        if not (account_id := session.get("account-id")):
            session.clear()
            abort(401)

        previous_ip_address = session.get("ip_address", "")
        if not (request.remote_addr == previous_ip_address):
            session.clear()
            abort(401)

        # Getting user by primary key
        if not (admin_object := db.session.get(Admin, account_id)):
            session.clear()
            abort(401)

        if not admin_object.status:
            session.clear()
            abort(401)

        # check hashed passwords
        if session.get("password", "null") != admin_object.password:
            session.clear()
            abort(401)

        return f(*args, **kwargs)
    return inner_decorator



def login_required(f):
    """
    Base Decorator For Login Users to their accounts
    """
    @wraps(f)
    def inner_decorator(*args, **kwargs):

        if not session.get("login"):
            session.clear()
            abort(401)

        if not (account_id := session.get("account-id")):
            session.clear()
            abort(401)

        # Getting user by primary key
        user_db = User.query.get(account_id)
        if not (user_object := db.session.get(User, account_id)):
            session.clear()
            abort(401)

        previous_ip_address = session.get("ip_address", "")
        if not (request.remote_addr == previous_ip_address):
            session.clear()
            abort(401)

        if not user_object.status:
            session.clear()
            abort(401)

        if not session.get("password", "null") == user_object.password:
            session.clear()
            abort(401)

        return f(*args, **kwargs)

    return inner_decorator


def admin_and_users_allowed(f):
    """
      this decorator give permission to both admin
          and users to visit a special view or endpoint
    """
    @wraps(f)
    def inner_decorator(*args, **kwargs):
        # if admin requested
        if session.get("admin", None):
            return admin_login_required(f)(*args, **kwargs)
        else: # if user requested
            return login_required(f)(*args, **kwargs)

        return f(*args, **kwargs)
    return inner_decorator


def change_password_only(f):
    """
    This decorator let only users that their account is inactive to activate their account and change their password
        [0] - Check rest password token is session
        [1] - Check referer address is redirected from login page
    """
    @wraps(f)
    def inner_decorator(*args, **kwargs):
        """Inner decorator"""
        reset_token = session.get("reset-token", False)
        if not reset_token:
            session.clear()
            abort(401)
        if not (ServerRedis.get(name=reset_token)):
            session.clear()
            abort(401)

        return f(*args, **kwargs)
    return inner_decorator

