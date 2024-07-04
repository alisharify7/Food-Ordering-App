from flask import render_template, request, flash, redirect, url_for, current_app


import Auth.form as AuthForm
from Auth import auth
from Auth.model import User
from Auth.utils import login_user


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
    if not current_app.extensions['captcha2'].is_verify():
        return render_template("login.html", form=form)

    if not form.validate():
        flash("اعتبار سنجی درخواست نادرست می باشد")
        return render_template("login.html", form=form)

    db = current_app.extensions['sqlalchemy']
    username, password = form.username.data, form.password.data

    query = db.session.select(User).filter(username=username)
    user_result = db.session.execute(statement=query).scalar_one_or_none()

    if not user_result:
        flash("اعتبار سنجی نادرست می باشد")
        return render_template("login.html", form=form)

    if not user_result.check_password(password):
        flash("اعتبار سنجی نادرست می باشد")
        return render_template("login.html", form=form)

    login_user(user_object=request.user_object)

    return f"Welcome Back {user_result.username}"

