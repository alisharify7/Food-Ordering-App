from User import user
from flask import render_template, g
from User import form as UserForm
from flask_login import login_required

@user.route("", methods=["GET"])
@login_required
def index_get():
    return render_template("user/index.html")



@user.route("/order", methods=["GET"])
@login_required
def order_get():
    return render_template("user/order.html")



@user.route("/history", methods=["GET"])
@login_required
def history_get():
    return render_template("user/order.html")



@user.route("/profile", methods=["GET"])
@login_required
def profile_get():
    return render_template("user/profile.html")


