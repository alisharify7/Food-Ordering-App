from flask import render_template, flash, redirect, url_for
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
        return redirect(url_for('user.profile_get'))

    data = form.data
    data.pop("csrf_token")
    current_user.update_fields(kwdata=data, fields=['first_name', 'last_name'])

    if form.email_address.data:
        if not UserProfileForm.validate_email(form.email_address.data):
            flash("آدرس ایمیل وارد شده صحیح نمی باشد", "error")
        else:
            if form.email_address.data != current_user.email_address:
                current_user.email_address = form.email_address.data
    else:
        current_user.email_address = form.email_address.data

    current_user.save()
    return redirect(url_for('user.profile_get'))

