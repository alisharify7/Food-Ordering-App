from functools import wraps
from FoodyAuth.model import User
from flask import session, abort
from FoodyCore.extension import ServerRedis



def admin_login_required(f):
    from FoodyAdmin.model import Admin
    """
    Base Decorator For Login admin to their accounts
    """
    @wraps(f)
    def inner_decorator(*args, **kwargs):
        """Inner decorator"""

        if not session.get("login"):
            session.clear()
            abort(401)

        if not (account_id := session.get("account-id")):
            session.clear()
            abort(401)

        # Getting user by primary key
        admin_db = Admin.query.get(account_id)
        if not admin_db:
            session.clear()
            abort(401)

        if not admin_db.Is_Active():
            session.clear()
            abort(401)

        # check hashed passwords
        if session['password'] != admin_db.Password:
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
        """Inner decorator"""

        if not session.get("login"):
            session.clear()
            abort(401)

        if not (account_id := session.get("account-id")):
            session.clear()
            abort(401)

        # Getting user by primary key
        user_db = User.query.get(account_id)
        if not user_db:
            session.clear()
            abort(401)

        if not user_db.Is_Active():
            session.clear()
            abort(401)

        if not user_db.Password == session.get("account-password", 'NULL'):
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

