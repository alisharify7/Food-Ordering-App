import os.path
import pathlib
import uuid

from flask import render_template, redirect, request, flash
from FoodyAdmin import admin
from FoodyAuth.AccessControl.decorators import admin_login_required
from FoodyAdmin.model import Admin, AdminLog
from FoodyCore.extension import db
from FoodyAdmin.model import SiteSetting
from FoodyConfig.config import Media, VALID_IMAGE_EXTENSIONS
from werkzeug.utils import secure_filename

import FoodyAdmin.Apps.Setting.form as SettingForms

BASE_URL = "manage/setting/"
TEMPLATE_FOLDER = "admin/Setting"


@admin.route(f"{BASE_URL}/admins/", methods=["GET"])
@admin_login_required
def manage_admin_index():
    """
        this view return All Admins in App
    """
    page = request.args.get(key="page", type=int, default=1)
    ctx = {
        "manage_admins": "show",
        "all_admins": "item-active",
        "current_page": page,
        "admins": Admin.query.order_by(Admin.id.desc()).paginate(page=page, per_page=15)
    }

    return render_template(f"{TEMPLATE_FOLDER}/all_admins.html", ctx=ctx)


@admin.route(f"{BASE_URL}/Add/Admin/", methods=["GET"])
@admin_login_required
def add_new_admin_get():
    """
        add new admin
    """
    ctx = {
        "manage_admins": "show",
        "add_new_admin": "item-active",
    }
    form = SettingForms.AddNewAdminForm()
    form.TryNumber.data = 0
    form.Active.data = "active"
    return render_template(f"{TEMPLATE_FOLDER}/add_new_admin.html", ctx=ctx, form=form)


@admin.route(f"{BASE_URL}/Add/Admin/", methods=["POST"])
@admin_login_required
def add_new_admin_post():
    """
        this view take a post request for adding new admin to the app
    """
    ctx = {
        "manage_admins": "show",
        "add_new_admin": "item-active",
    }
    form = SettingForms.AddNewAdminForm()
    if not form.validate():
        flash("برخی موارد مقدار دهی نشده اند", "danger")
        return render_template(f"{TEMPLATE_FOLDER}/add_new_admin.html", ctx=ctx, form=form)

    admin = Admin()
    if not admin.SetUsername(form.Username.data):
        flash("نام کاربری توسط ادمین دیگری گرفته شده است", "danger")
        return render_template(f"{TEMPLATE_FOLDER}/add_new_admin.html", ctx=ctx, form=form)

    if not admin.SetEmail(form.Email.data):
        flash("ایمیل توسط ادمین دیگری گرفته شده است", "danger")
        return render_template(f"{TEMPLATE_FOLDER}/add_new_admin.html", ctx=ctx, form=form)

    if not admin.SetPhone(form.PhoneNumber.data):
        flash("شماره تماس توسط ادمین دیگری گرفته شده است", "danger")
        return render_template(f"{TEMPLATE_FOLDER}/add_new_admin.html", ctx=ctx, form=form)

    admin.SetPassword(form.Password.data)
    admin.SetPublicKey()
    admin.Active = form.Active.data == "active"

    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        flash("خطایی رخ داد بعدا امتحان کنید", "danger")
        return render_template(f"{TEMPLATE_FOLDER}/add_new_admin.html", ctx=ctx, form=form)
    else:
        flash("عملیات با موفقیت انجام شد", "success")
        return redirect(request.referrer)


@admin.route(f"{BASE_URL}/edit/Admin/<uuid:adminKey>/", methods=["GET"])
@admin_login_required
def edit_admin_get(adminKey):
    """
        this view take a post request for adding new admin to the app
    """
    adminKey = str(adminKey)
    if not (adminDB := Admin.query.filter_by(PublicKey=adminKey).first()):
        flash("ادمینی با مشخصات وارد شده یافت نشد", "")
        return redirect(request.referrer)

    ctx = {
        "manage_admins": "show",
        "add_new_admin": "item-active",
        "admin": adminDB
    }

    form = SettingForms.AddNewAdminForm()
    form.PopPasswordValidator()

    form.TryNumber.data = adminDB.TryNumber
    form.Password.data = adminDB.Password
    form.PhoneNumber.data = adminDB.PhoneNumber
    form.Email.data = adminDB.Email
    form.Username.data = adminDB.Username
    form.Active.data = 'active' if adminDB.Active else 'inactive'
    form.Password.errors = ["به علت رمزنگاری گذرواژه ها امکان مشاهده وجود ندارد",
                            "صورتی که میخواهید گذرواژه را تغییر دهید صرفا این فیلد را پر کنید"]

    return render_template(f"{TEMPLATE_FOLDER}/edit_admin.html", ctx=ctx, form=form)


@admin.route(f"{BASE_URL}/edit/Admin/<uuid:adminKey>/", methods=["POST"])
@admin_login_required
def edit_admin_post(adminKey):
    """
        this view take a post request for adding new admin to the app
    """
    adminKey = str(adminKey)
    if not (adminDB := Admin.query.filter_by(PublicKey=adminKey).first()):
        flash("ادمینی با مشخصات وارد شده یافت نشد", "")
        return redirect(request.referrer)

    ctx = {
        "manage_admins": "show",
        "add_new_admin": "item-active",
    }

    form = SettingForms.AddNewAdminForm()
    if not form.validate():
        flash("برخی مادیر مقدار دهی نشده اند", "danger")
        return redirect(request.referrer)

    if adminDB.Username != form.Username.data:
        if not adminDB.SetUsername(form.Username.data):
            flash("نام کاربری توسط کاربر دیگری رزرو شده است", "danger")

    if adminDB.Password != form.Password.data:
        adminDB.SetPassword(form.Password.data)

    if adminDB.Email != form.Email.data:
        if not adminDB.SetEmail(form.Username.data):
            flash("ایمیل توسط کاربر دیگری رزرو شده است", "danger")

    if adminDB.PhoneNumber != form.PhoneNumber.data:
        if not adminDB.SetPhone(form.PhoneNumber.data):
            flash("تلفن توسط کاربر دیگری رزرو شده است", "danger")

    if adminDB.Active != (form.Active.data == "active"):
        adminDB.Active = form.Active.data == "active"

    try:
        adminDB.TryNumber = int(form.TryNumber.data)
    except ValueError:
        adminDB.TryNumber = 0


    try:
        db.session.add(adminDB)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        flash("خطایی رخ داد بعدا امتحان کنید", "danger")
    else:
        flash("عملیات با موفقیت انجام شد", "success")

    return redirect(request.referrer)


@admin.route(f"{BASE_URL}/", methods=["GET"])
@admin_login_required
def setting_get():
    """This view show to admin setting panel"""
    ctx = {
        "manage_admins": "show",
        "setting": "item-active",
    }
    Logoform = SettingForms.LogoSettingForm()
    Settingform = SettingForms.SiteSettingForm()

    if not (site := SiteSetting.query.filter(SiteSetting.tag == "setting").first()):
        site = SiteSetting()
        site.tag = "setting"
        site.SetPublicKey()
        try:
            db.session.add(site)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            flash("برخی موارد مقدار دهی نشده اند", "danger")
            return redirect(request.referrer)

    Settingform.Address.data = site.Address
    Settingform.Phone.data = site.Phone
    Settingform.Name.data = site.Name
    Settingform.Description.data = site.Description

    return render_template(
        f"{TEMPLATE_FOLDER}/setting.html",
        ctx=ctx,
        logoform=Logoform,
        settingform=Settingform
    )


@admin.route(f"{BASE_URL}/update/logo/", methods=["POST"])
@admin_login_required
def update_logo_image():
    """
    this view take a post request and update site logo
    """
    if not (site := SiteSetting.query.filter(SiteSetting.tag == "setting").first()):
        site = SiteSetting()
        site.tag = "setting"
        site.SetPublicKey()
        try:
            db.session.add(site)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            flash("برخی موارد مقدار دهی نشده اند", "danger")
            return redirect(request.referrer)

    old_logo = site.Logo

    form = SettingForms.LogoSettingForm()
    if not form.validate():
        flash("برهی مقادیر مقدار دهی اولیه نشده اند", "danger")
        return redirect(request.referrer)

    img = form.Image.data
    if not img:
        flash("تصویر در درخواست دریافت شده یافت نشد", "danger")
        return redirect(request.referrer)

    filename = pathlib.Path(img.filename)
    suffix = filename.suffix
    if suffix not in VALID_IMAGE_EXTENSIONS:
        flash(f"متاسفانه فرمت فایل انتخابی ساپورت نمی شود.\nفرمت های ساپورت شده {VALID_IMAGE_EXTENSIONS}"
              , "danger")
        return redirect(request.referrer)
    filenameToken = str(uuid.uuid4()) + secure_filename(str(filename))
    filenameToken = filenameToken[-50:]

    site.Logo = filenameToken
    img.filename = filenameToken
    try:
        img.save(Media / filenameToken)
    except Exception as e:
        print(e)
        flash("مشکلی در ذخیره تصویر رخ داد", "danger")
        return redirect(request.referrer)
    else:
        if old_logo:
            if os.path.exists(Media / old_logo):
                os.remove(Media / old_logo)
    try:
        db.session.add(site)
        db.session.commit()
    except Exception as e:
        print(e)
        if os.path.exists(Media / filenameToken):
            os.remove(Media / filenameToken)
        flash("خطایی هنگام ذخیره تغییرات در دیتابیس رخ داد", "danger")
    else:
        flash("بروزرسانی با موفقیت انجام شد", "success")

    return redirect(request.referrer)


@admin.route(f"{BASE_URL}/update/info/", methods=["POST"])
@admin_login_required
def update_app_description():
    """
    this view take a post request and update site information
    """
    if not (site := SiteSetting.query.filter(SiteSetting.tag == "setting").first()):
        site = SiteSetting()
        site.tag = "setting"
        site.SetPublicKey()
        try:
            db.session.add(site)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            flash("برخی موارد مقدار دهی نشده اند", "danger")
            return redirect(request.referrer)

    form = SettingForms.SiteSettingForm()
    if not form.validate():
        flash("برهی مقادیر مقدار دهی اولیه نشده اند", "danger")
        return redirect(request.referrer)

    site.Name = form.Name.data
    site.Address = form.Address.data
    site.Description = form.Description.data
    site.Phone = form.Phone.data

    try:
        db.session.add(site)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        flash("خطایی هنگام ذخیره اطلاعات رخ داد", "danger")
    else:
        flash("عملیات با موفقیت انجام شد", "success")

    return redirect(request.referrer)



@admin.route(f"{BASE_URL}/logs/", methods=["GET"])
@admin_login_required
def admin_logs_get():
    """
        this view return admin login logs
    """
    page = request.args.get(key="page", type=int, default=1)
    ctx = {
        "manage_admins": "show",
        "admin_logs": "item-active",
        "current_page": page,
    }
    ctx["data"] = AdminLog.query.order_by(AdminLog.CreatedTime.desc()).paginate(page=page, per_page=13)

    return render_template(f"{TEMPLATE_FOLDER}/admin_logs.html", ctx=ctx)



