# build in
import os.path
import khayyam

from FoodyUser import user
from flask import render_template, send_from_directory, request, flash, redirect, url_for

from FoodyCore.extensions import db
from FoodyAuth.AccessControl.decorators import login_required
from FoodyConfig.config import User_Static
from FoodyOrder.model import FoodList, Order
from FoodyCore.utils import TimeStamp
from FoodyUser.form import UserPanelEmailForm



@user.route("/UserStatic/<path:filename>")
@login_required
def UserStatic(filename:str):
    """Serve static files to users that authenticated."""
    if os.path.exists(User_Static / filename):
        return send_from_directory(User_Static, filename)
    else:
        return "File Not Found!", 404



@user.route("/", methods=['GET'])
@login_required
def index_view() -> str:
    """return user index page """
    return render_template("user/index.html")


@user.route("/menu/", methods=["GET"])
@login_required
def get_menu() -> str:
    """return food menu page"""
    ctx = {}
    ctx["foods"] = FoodList.query.filter_by(Active=True).all()
    return render_template("user/menu.html", ctx=ctx)


@user.route("/order/", methods=["GET"])
@login_required
def order_get() -> str:
    """return ordering page """
    return render_template("user/order.html")


@user.route("/history/", methods=["GET"])
@login_required
def history_get() -> str:
    """return orders history """
    page = request.args.get("page", type=int, default=1)
    ctx = {"current_page":page}

    ctx["orders"] = Order.query.order_by(Order.OrderDate.desc()) \
         .filter_by(UserID=request.user_object.id) \
         .paginate(per_page=15, page=page)

    return render_template("user/history.html", ctx=ctx)


@user.route("/panel/", methods=["GET"])
@login_required
def panel_get() -> str:
    """return users panel page"""
    Today = khayyam.JalaliDate.today()
    t = TimeStamp()

    startofMonth = t.convert_jlj2_georgian_d(khayyam.JalaliDate(year=Today.year, month=Today.month, day=1))
    endofMonth = t.convert_jlj2_georgian_d(khayyam.JalaliDate(year=Today.year, month=Today.month, day=Today.daysinmonth))

    user = request.user_object # get user object

    form = UserPanelEmailForm()
    form.Email.data = user.Email or ""

    ctx = {
        "user": request.user_object,
        "this_month_orders": Order.query.filter(Order.UserID == user.id).filter(Order.OrderDate >= startofMonth).filter(Order.OrderDate <= endofMonth).count()
    }
    return render_template("user/panel.html", ctx=ctx, form=form)



@user.route("/panel/", methods=["POST"])
@login_required
def panel_post():
    """updating users information in their panel"""

    user = request.user_object # get user object

    form = UserPanelEmailForm()
    if not form.validate():
        flash("برخی موارد به درستی مقدار دهی نشده اند", "danger")
        error = "\n".join([form.errors[err][-1] for err in form.errors])
        if error:
            flash(error, "danger")
        return redirect(url_for('user.panel_get'))

    if not user.SetEmailAddress(form.Email.data):
        flash("آدرس ایمیل وارد شده توسط کاربر دیگری در سیستم گرفته شده است \nلطفا آدرس دیگری را وارد کنید", "danger")
        return redirect(url_for('user.panel_get'))

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash("خطایی هنگام ذخیره سازی رخ داد بعدا امتحان کند", "danger")
    else:
        flash("عملیات با موفقیت انجام شد\nآدرس ایمیل با موفقیت بروزرسانی گردید", "danger")

    return redirect(url_for('user.panel_get'))

