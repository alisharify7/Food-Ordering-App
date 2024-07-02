from Auth import auth
import Auth.form as AuthForm
from flask import render_template




@auth.route("/login/", methods=["GET"])
def login_get() -> str:
    """render login page"""
    form = AuthForm.LoginForm()
    return render_template("login.html", form=form)



