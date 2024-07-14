from flask import render_template, flash
from flask_login import login_required, current_user

from User import user
from User.form import UserProfileForm


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
    form = UserProfileForm()
    form.fill_with(current_user)
    return render_template("user/profile.html", form=form)


@user.route("/profile", methods=["POST"])
@login_required
def profile_post():
    form = UserProfileForm()
    if not form.validate():
        flash('خطایی هنگام ارسال درخواست رخ داد', 'error')
        print(form.errors)

    return render_template("user/profile.html", form=form)
