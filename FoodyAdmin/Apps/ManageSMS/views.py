from FoodyAdmin import admin
from flask import request, flash, render_template, redirect
from FoodyAuth.AccessControl.decorators import admin_login_required
from FoodyAuth.model import Section, User

import FoodyAdmin.Apps.ManageSMS.utils as ManageSMSutils
import FoodyAdmin.Apps.ManageSMS.form as ManageSMSform
from FoodyAuth.utils import get_all_section_wtf_select
from FoodyCore.extension import smsIR

BASE_URL = "Manage/SMS"
TEMPLATE_FOLDER = "admin/ManageSMS"


@admin.route(f"/{BASE_URL}/Send/", methods=["GET"])
@admin_login_required
def send_sms_get():
    """
        Send SMS to One Person
    """
    ctx = {
        "manage_sms": "show",
        "send_sms": "item-active",
    }
    form = ManageSMSform.SendSingleSMS()
    return render_template(f'{TEMPLATE_FOLDER}/send_sms.html', ctx=ctx, form=form)


@admin.route(f"/{BASE_URL}/Send/", methods=["POST"])
@admin_login_required
def send_sms_post():
    """
        Send SMS to One Person
    """
    ctx = {
        "manage_sms": "show",
        "send_sms": "item-active",
    }
    form = ManageSMSform.SendSingleSMS()
    if not form.validate():
        flash("برخی موارد مقدار دهی نشده اند", "danger")
        return redirect(request.referrer)

    result = smsIR.send_sms(number=form.targetMobile.data, message=form.Text.data)
    if result.status_code == 200:
        data = {}
        result = result.json()
        data["cost"] = result['data']["cost"]
        data["receiver_number"] = form.targetMobile.data
        data["message"] = form.Text.data
        data["status"] = "موفق"
        data["sender_number"] = smsIR._linenumber
        ctx["data"] = data
    else:
        data = {}
        data["cost"] = 0
        data["receiver_number"] = form.targetMobile.data
        data["message"] = form.Text.data
        data["status"] = "ناموفق"
        data["sender_number"] = smsIR._linenumber
        ctx["data"] = data

    return render_template(f'{TEMPLATE_FOLDER}/send_sms.html', ctx=ctx)


@admin.route(f"/{BASE_URL}/Report/", methods=["GET"])
@admin_login_required
def report_sms_today_get():
    """
        receiver all sms's that sends today
    """
    ctx = {
        "manage_sms": "show",
        "report_today_send": "item-active",
    }

    result = smsIR.report_today(page_size=1000)
    ctx["credit"] = smsIR.get_credit().json()["data"]
    try:
        ctx["data"] = result.json()
        ctx["data"] = ctx["data"]["data"][::-1]
        ctx["total_sms"] = len(ctx["data"])
    except Exception as e:
        print(e)
        ctx["data"] = None

    return render_template(f'{TEMPLATE_FOLDER}/report_today_sends.html', ctx=ctx)


@admin.route(f"/{BASE_URL}/Report/Between-date/", methods=["GET"])
@admin_login_required
def report_sms_between_get():
    """
        report sms between to days
    """
    ctx = {
        "manage_sms": "show",
        "report_between_date": "item-active",
    }
    form = ManageSMSform.ReportSMSPeriodTime()
    return render_template(f'{TEMPLATE_FOLDER}/report_period_time.html', ctx=ctx, form=form)


@admin.route(f"/{BASE_URL}/Report/Between-date/", methods=["POST"])
@admin_login_required
def report_sms_between_post():
    """

    """
    ctx = {
        "manage_sms": "show",
        "report_between_date": "item-active",
    }
    form = ManageSMSform.ReportSMSPeriodTime()
    if not form.validate():
        flash("برخی موارد مقدار دهی نشده اند", "danger")
        return redirect(request.referrer)

    if not form.validate_dates():
        flash("تاریخ به درستی وارد نشده است", "danger")
        return redirect(request.referrer)

    fromDate, toDate = form.GetGeorgianDates()

    result = smsIR.report_archived(from_date=str(fromDate), to_date=str(toDate), page_size=1000)

    if result.status_code == 200:
        data = result.json()["data"][::-1]
        ctx["data"] = data
        ctx["total_sms"] = len(data)
    else:
        ctx["data"] = []

    return render_template(f'{TEMPLATE_FOLDER}/report_period_time.html', ctx=ctx, form=form)


@admin.route(f"/{BASE_URL}/Send/To/All/", methods=["GET"])
@admin_login_required
def send_to_all_sms_get():
    """
        send sms to section's users or even all users
    """
    ctx = {
        "manage_sms": "show",
        "send_to_all": "item-active",
    }
    form = ManageSMSform.SendToAllSMS()
    form.sections.choices = get_all_section_wtf_select() + [('all', "همه بخش ها")]

    return render_template(f'{TEMPLATE_FOLDER}/send_to_all.html', ctx=ctx, form=form)


@admin.route(f"/{BASE_URL}/Send/To/All/", methods=["POST"])
@admin_login_required
def send_to_all_sms_post():
    """
        send sms to section's users or even all users
    """
    ctx = {
        "manage_sms": "show",
        "send_to_all": "item-active",
        "data": []
    }
    form = ManageSMSform.SendToAllSMS()
    form.sections.choices = get_all_section_wtf_select() + [('all', "همه بخش ها")]

    if not form.validate():
        flash("برخی موارد مقدار دهی نشده اند", "danger")
        return redirect(request.referrer)

    text = form.Text.data
    section = form.sections.data

    if section == "all":
        numbers = User.query.join(Section, User.SectionID == Section.id) \
            .with_entities(User.PhoneNumber) \
            .all()
        numbers = [str(each[0]) for each in numbers]
        total_round = len(numbers) // 100

        for each in range(1, total_round + 1):
            n = numbers[:100]
            numbers = numbers[100:]

            result = smsIR.send_bulk_sms(
                numbers=n,
                message=text
            )

            if result.status_code == 200:
                ctx["data"].append(result)

        if numbers:
            result = smsIR.send_bulk_sms(
                numbers=numbers,
                message=text
            )
            if result.status_code == 200:
                ctx["data"].append(result)

        flash(f"پیامک با {'موفقیت' if len(ctx['data']) else 'خطا'} برای کاربران ارسال شد", "success")
        return redirect(request.referrer)

    else:
        SectionDB = Section.query.filter_by(PublicKey=section).first()
        if not SectionDB:
            flash("برخی موارد مقدار دهی نده اند", "danger")
            return redirect(request.referrer)
        numbers = User.query.join(Section, User.SectionID == Section.id) \
            .filter(User.SectionID == SectionDB.id) \
            .with_entities(User.PhoneNumber) \
            .all()

        numbers = [str(each[0]) for each in numbers]
        total_round = len(numbers) // 100

        for each in range(1, total_round + 1):
            n = numbers[:100]
            numbers = numbers[100:]

            result = smsIR.send_bulk_sms(
                numbers=n,
                message=text
            )
            if result.status_code == 200:
                ctx["data"].append(result)

        if numbers:
            result = smsIR.send_bulk_sms(
                numbers=numbers,
                message=text
            )
            if result.status_code == 200:
                ctx["data"].append(result)

        flash(f"پیامک با {'موفقیت' if len(ctx['data']) else 'خطا'} برای کاربران ارسال شد", "success")
        return redirect(request.referrer)
