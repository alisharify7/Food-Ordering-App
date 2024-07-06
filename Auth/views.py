from flask import render_template, request, flash, redirect, url_for, get_flashed_messages, make_response, current_app

import sqlalchemy as sa
from flask_login import login_user as login_user_flask_login, logout_user as logout_user_flask_login

from Auth import auth
import Auth.form as AuthForm
from Auth.model import User
from Core.extensions import db


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


@auth.route("/logout/", methods=["GET"])
def logout_user() -> str:
    """logout user view"""
    logout_user_flask_login()
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
        flash(message="اعتبار سنجی درخواست نادرست می باشد", category='error') # TODO: add form errors to html
        return render_template("login.html", form=form)

    username, password = form.username.data, form.password.data

    query = db.select(User).filter_by(username=username)
    user_result:User = db.session.execute(query).scalar_one_or_none()

    if not user_result:
        flash(message="اعتبار سنجی نادرست می باشد", category='error')
        return render_template("login.html", form=form)

    if not user_result.check_password(password):
        flash(message="اعتبار سنجی نادرست می باشد", category='error')
        return render_template("login.html", form=form)

    flash(message=f" خوش آمدید {user_result.full_name()}کاربر گرامی ", category='success')
    login_user_flask_login(user=user_result)

    return redirect(url_for("user.index_get"))


@auth.route("/reset-password/", methods=["GET"])
def reset_password_get() -> str:
    """render login page"""
    form = AuthForm.ResetPasswordForm()
    ctx = {'message': False}
    return render_template("reset_password.html", form=form)


@auth.route("/reset-password/", methods=["POST"])
def reset_password_post() -> str:
    """render login page"""
    ctx = {'message': False}
    form = AuthForm.ResetPasswordForm()

    if not current_app.extensions['captcha3'].is_verify():
        flash(message="اعتبار سنجی کپچا نادرست می باشد", category="error")
        return render_template("reset_password.html", form=form, ctx=ctx)

    if not form.validate():
        flash(message="اعتبار سنجی درخواست نادرست می باشد", category='error')
        return render_template("reset_password.html", form=form, ctx=ctx)

    field_data = form.username.data

    db = current_app.extensions['sqlalchemy']
    query = db.session.select(User).filter(sa.or_(username=field_data, email_address=field_data, national_code=field_data, phone_number=field_data))

    user_result = db.session.execute(statement=query).scalar_one_or_none()

    ctx["message"] = "در صورتی که کاربری با مشخصات وارد شما در سیستم ثبت شده باشد <br> پیامک بازنشانی گذرواژه برای حساب مورد ارسال خواهد شد"
    flash(message=ctx["message"], category='success')

    if not user_result:
        return render_template("reset_password.html", form=form, ctx=ctx)



    return render_template("reset_password.html", form=form, ctx=ctx)



    return render_template("reset_password.html", form=form)
