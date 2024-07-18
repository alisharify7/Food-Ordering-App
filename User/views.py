from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from User import user
from User.form import UserProfileForm

@user.route("", methods=["GET"])
@login_required
def index_get():
    return render_template("user/index.html")


class food:
    name = ""
    image = ""
    description = ""

def get_fake_food(n):
    import random
    f = []
    for i in range(n):
        ff = food()
        ff.name = random.choice(['برگر امریکایی', 'لازانیا', 'پیتزا'])
        ff.image = random.choice(['https://www.foodandwine.com/thmb/DI29Houjc_ccAtFKly0BbVsusHc=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/crispy-comte-cheesburgers-FT-RECIPE0921-6166c6552b7148e8a8561f7765ddf20b.jpg', 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/640px-Eq_it-na_pizza-margherita_sep2005_sml.jpg', 'https://s3.amazonaws.com/shecodesio-production/uploads/files/000/054/181/original/lazania.jpg?1668632642'])
        ff.description = "300 گرم گوشت مرغ همراه با دوغ و نوشابه به همراه نون و نمک"
        f.append(ff)
    return f

@user.route("/order", methods=["GET"])
@login_required
def order_get():
    foods = get_fake_food(100)
    return render_template("user/order.html", foods=foods)


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

