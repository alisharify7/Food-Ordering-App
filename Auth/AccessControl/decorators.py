from functools import wraps

from flask import redirect, url_for, request
from flask_login import current_user, logout_user


def admin_login_required(f):  # TODO: replace it with a general method like @login(roles=[])
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if current_user.is_anonymous:
            logout_user()
            return redirect(url_for('auth.login_get', next=request.path))

        if 'admin' not in current_user.get_roles():
            logout_user()
            return redirect(url_for('auth.login_get', next=request.path))

        return f(*args, **kwargs)

    return decorated_function
