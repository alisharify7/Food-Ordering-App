import datetime

import khayyam
from flask import render_template, flash, redirect, request
from FoodyAdmin import admin
from FoodyAdmin.views import admin_login_required
from FoodyCore.extensions import db
from FoodyOrder.model import Order
from FoodyAuth.model import Section, User
from FoodyCore.utils import TimeStamp

import FoodyAdmin.Apps.Accounting.form as AccountingForms
import FoodyAdmin.Apps.Accounting.utils as AccountingUtils

BASE_URL = "manage/Accounting"
TEMPLATE_FOLDER = "admin/Accounting"


def sort_orders(X: Order):
    return User.query.get(X.UserID).SectionID


@admin.route(f"{BASE_URL}/Report/", methods=["GET"])
@admin_login_required
def report_today_get():
    """
    Rport today orders
    """
    today = datetime.date.today()

    # today_orders = Order.query.filter(Order.OrderDate == today).all()
    all_sections = db.session.query(Section.id, Section.Name).distinct().all()

    # try:  # sort order by Sections
    #     today_orders = sorted(today_orders, key=lambda order: User.query.get(order.UserID).SectionID, reverse=False)
    # except Exception as e:
    #     print(e)

    total_orders = 0
    sections_order = {}
    for each in all_sections:
        # section = Section.query.get(each[0])
        Specified_section_today_orders = Order.query\
            .join(User, Order.UserID == User.id) \
            .filter(User.SectionID == each[0]) \
            .filter(Order.OrderDate == today)\
            .all()
        total_orders += len(Specified_section_today_orders)

        if Specified_section_today_orders:
            sections_order[each[1]] = Specified_section_today_orders


    ctx = {
        "report_today": "item-active",
        "accounting": "show",
        "total_orders": total_orders,
        "sections_order": sections_order
    }

    return render_template(f"{TEMPLATE_FOLDER}/report_today.html", ctx=ctx)


@admin.route(f"{BASE_URL}/Report/Section/", methods=["GET"])
@admin_login_required
def report_section_get():
    """
    render query by sections in orders
    """
    form = AccountingForms.SearchBySectionsForm()
    form.Sections.choices = AccountingUtils.get_all_unique_sections_wtf_select()

    ctx = {
        "accounting": "show",
        "report_section": "item-active",
        "all_sections": db.session.query(Section.Name).distinct().all(),
    }

    return render_template(f"{TEMPLATE_FOLDER}/report_section.html", ctx=ctx, form=form)


@admin.route(f"{BASE_URL}/Report/Section/", methods=["POST"])
@admin_login_required
def report_section_post():
    """
    take a post request and query in db (with section)
    """

    ctx = {
        "accounting": "show",
        "report_section": "item-active",
    }

    form = AccountingForms.SearchBySectionsForm()
    form.Sections.choices = AccountingUtils.get_all_unique_sections_wtf_select()

    if not form.validate():
        return redirect(request.referrer)

    if not form.validate_dates():
        flash("تاریخ به درستی وارد نشده است", "danger")
        return redirect(request.referrer)

    startDate, endDate = form.GetGeorgianDates()

    if startDate > endDate:
        flash("تاریخ شروع نمی تواند از تاریخ انتهایی بزرگتر باشد", "danger")
        return redirect(request.referrer)

    if form.Sections.data != "all":
        SectionDb = Section.query.filter_by(PublicKey=form.Sections.data).first()
        if not SectionDb:
            flash("بخش مورد نظر به درستی وارد نشده است", "danger")
            return redirect(request.referrer)
        ctx["section"] = SectionDb.Name

        Orders = Order.query\
            .order_by(Order.UserID.desc()) \
            .join(User, Order.UserID == User.id) \
            .filter(User.SectionID == SectionDb.id) \
            .filter(Order.OrderDate >= startDate) \
            .filter(Order.OrderDate <= endDate) \
            .all()

    else:
        Orders = Order.query\
            .order_by(Order.OrderDate.desc())\
            .join(User, Order.UserID == User.id)\
            .filter(Order.OrderDate >= startDate) \
            .filter(Order.OrderDate <= endDate)\
            .all()
        ctx["section"] = "تمام بخش ها"

    ctx["orders"] = Orders
    ctx["total_orders"] = len(Orders)
    ctx["from"] = form.StartDate.data
    ctx["end"] = form.EndDate.data

    return render_template(f"{TEMPLATE_FOLDER}/report_section_result.html", ctx=ctx, form=form)



@admin.route(f"{BASE_URL}/Report/User/", methods=["GET"])
@admin_login_required
def report_user_get():
    ctx = {
        "user_report": "item-active",
        "accounting": "show",
    }
    form = AccountingForms.ReportUserForm()
    return render_template(f"{TEMPLATE_FOLDER}/user_report.html", ctx=ctx, form=form)



@admin.route(f"{BASE_URL}/Report/User/", methods=["POST"])
@admin_login_required
def report_user_post():
    ctx = {
        "user_report": "item-active",
        "accounting": "show",
    }
    form = AccountingForms.ReportUserForm()
    if not form.validate():
        flash("برخی موارد مقدار دهی اولیه نشده اند", "danger")
        return redirect(request.referrer)

    EmployeeDb = User.query.filter_by(EmployeeCode=form.EmployeeCode.data).first()
    if not EmployeeDb:
        flash("کاربری با کد کارمندی وارد شده یافت نشد", "danger")
        return redirect(request.referrer)

    if not form.validate_dates():
        flash("تاریخ به درستی وارد نشده است", "danger")
        return redirect(request.referrer)

    startDate, endDate = form.GetGeorgianDates()

    Orders = Order.query.order_by(Order.OrderDate.desc()).join(User, Order.UserID == EmployeeDb.id).filter(
        Order.OrderDate >= startDate) \
        .filter(Order.OrderDate <= endDate).all()

    ctx["total_orders"] = len(Orders)
    ctx["orders"] = Orders
    ctx["user"] = EmployeeDb
    ctx["from"] = startDate
    ctx["end"] = endDate

    return render_template(f"{TEMPLATE_FOLDER}/user_report_result.html", ctx=ctx, form=form)



@admin.route(f"{BASE_URL}/Report/User/this_month/<uuid:userKey>/", methods=["GET"])
@admin_login_required
def user_this_month_order(userKey):
    ctx = {
        "user_report": "item-active",
        "accounting": "show",
    }
    userKey = str(userKey)
    if not (UserDb := User.query.filter_by(PublicKey=userKey).first()):
        flash("کاربری با مشخصات وارد شده یافت نشد", "danger")
        return redirect(request.referrer)

    today = khayyam.JalaliDate.today()
    startMonth = khayyam.JalaliDate(day=1, month=today.month, year=today.year)
    endMonth = khayyam.JalaliDate(day=today.daysinmonth, month=today.month, year=today.year)
    ctx["from"] = startMonth
    ctx["to"] = endMonth

    t = TimeStamp()
    startMonth = t.convert_jlj2_georgian_d(startMonth)
    endMonth = t.convert_jlj2_georgian_d(endMonth)

    ctx["this_month_orders"] = Order.query.filter(Order.OrderDate >= startMonth).filter(
        Order.OrderDate <= endMonth).filter(Order.UserID == UserDb.id).all()
    ctx["user"] = UserDb
    ctx["total_orders_len"] = len(ctx["this_month_orders"])

    return render_template(f"{TEMPLATE_FOLDER}/user_this_month_order.html", ctx=ctx)
