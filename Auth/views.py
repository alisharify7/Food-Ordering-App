from flask import render_template, request, flash, redirect, url_for, current_app, get_flashed_messages, make_response

import Auth.form as AuthForm
from Auth import auth
from Auth.model import User
from Auth.utils import login_user


@auth.route("/notifications/", methods=["GET"])
def notifications() -> str:
    """Notification Messages view
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This view return user all flash messages in a json


    arguments:
        None -- clear

    return:
        return all flash messages in a json format


    - add no cacheing response of this view
    """
    flashes = []
    messages = get_flashed_messages(with_categories=True)

    for category, message in messages:
        temp = {"message": message, "type": category}
        flashes.append(temp)

    response = make_response(flashes)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@auth.route("/user/logout/", methods=["GET"])
def logout_user() -> str:
    """logout user view"""
    logout_user(request.user_object)
    return redirect(url_for('web.index_view'))


@auth.route("/login/", methods=["GET"])
def login_get() -> str:
    """render login page"""
    form = AuthForm.LoginForm()
    return render_template("login.html", form=form)


@auth.route("/login/", methods=["POST"])
def login_post() -> str:
    """login page -> post"""

    form = AuthForm.LoginForm()
    if not current_app.extensions['captcha3'].is_verify():
        flash(message="اعتبار سنجی کپچا نادرست می باشد", category="error")
        return render_template("login.html", form=form)

    if not form.validate():
        flash(message="اعتبار سنجی درخواست نادرست می باشد", category='error')
        return render_template("login.html", form=form)

    db = current_app.extensions['sqlalchemy']
    username, password = form.username.data, form.password.data

    query = db.session.select(User).filter(username=username)
    user_result = db.session.execute(statement=query).scalar_one_or_none()

    if not user_result:
        flash(message="اعتبار سنجی نادرست می باشد", category='error')
        return render_template("login.html", form=form)

    if not user_result.check_password(password):
        flash(message="اعتبار سنجی نادرست می باشد", category='error')
        return render_template("login.html", form=form)

    login_user(user_object=request.user_object)

    flash(message=f" خوش آمدید {user_result.full_name()}کاربر گرامی ", category='success')
    return f"Welcome Back {user_result.username}"



@auth.route("/reset-password/", methods=["GET"])
def reset_password_get() -> str:
    """render login page"""
    form = AuthForm.ResetPasswordForm()
    return render_template("reset_password.html", form=form)
