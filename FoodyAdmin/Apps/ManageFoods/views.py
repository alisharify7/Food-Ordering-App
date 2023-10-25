import os.path
import pathlib
import uuid

from flask import render_template, flash, redirect, request
from FoodyAdmin import admin
from FoodyAdmin.views import admin_login_required
from FoodyOrder.model import FoodList, Day
from FoodyCore.extension import db

import FoodyAdmin.Apps.ManageFoods.utils as ManageFoodsUtils
import FoodyAdmin.Apps.ManageFoods.form as ManageFoodsForms

from werkzeug.utils import secure_filename
from FoodyConfig.config import FoodDir, VALID_IMAGE_EXTENSIONS

BASE_URL = "manage/ManageFoods/"
TEMPLATE_FOLDER = "admin/ManageFoods"


@admin.route(f"/{BASE_URL}/", methods=["GET"])
@admin_login_required
def manage_foods_all():
    """
    this view show all foods in app to admin
    """
    ctx = {
        "manage_foods": "show",
        "manage_foods_all": "item-active",
        "foods": FoodList.query.order_by(FoodList.id.desc()).all(),
    }
    return render_template(f'{TEMPLATE_FOLDER}/all_foods.html', ctx=ctx)


@admin.route(f"/{BASE_URL}/add/", methods=["GET"])
@admin_login_required
def add_new_food():
    """
    this view return template for adding new food to app
    """
    ctx = {
        "manage_foods": "show",
        "add_new_food": "item-active"
    }
    form = ManageFoodsForms.AddFoodForm()
    return render_template(f"{TEMPLATE_FOLDER}/add_new_food.html", ctx=ctx, form=form)


@admin.route(f"/{BASE_URL}/add/", methods=["POST"])
@admin_login_required
def add_new_food_post():
    """
    this view take a post request for addming new food to app
    """
    ctx = {
        "manage_foods": "show",
        "add_new_food": "item-active"
    }
    form = ManageFoodsForms.AddFoodForm()

    if not form.validate():
        flash("برخی موارد مقدار دهی اولیه نشده اند", "danger")
        return render_template(f"{TEMPLATE_FOLDER}/add_new_food.html", ctx=ctx, form=form)
    else:

        Food = FoodList()

        # check have image
        if form.Images.data:
            have_img = False

            for each in form.Images.data:
                if not each:
                    continue
                have_img = True

                name = str(uuid.uuid4()) + secure_filename(each.filename[:50])
                ex = pathlib.Path(each.filename).suffix
                if ex not in VALID_IMAGE_EXTENSIONS:
                    flash(
                        "عکس انتخابی دارای فرمت نامعتبر است" + "\nفرمت های پشتیبانی شده" + f"{''.join(VALID_IMAGE_EXTENSIONS)}",
                        "danger")
                    return render_template(f"{TEMPLATE_FOLDER}/add_new_food.html", ctx=ctx, form=form)
                each.filename = name
        # if have image save it in Media
        if have_img:
            for each in form.Images.data:
                try:
                    each.save(FoodDir / each.filename)
                except Exception as e:
                    print(e)
                    if (os.path.exists(FoodDir / each.filename)):
                        os.remove(FoodDir / each.filename)
                    flash("خطایی هنگام ذخیره تصصویر رخ داد", "danger")
                    return redirect(request.referrer)

            Food.SetImage([n.filename for n in form.Images.data])

        else:
            Food.SetImage(["default.png"])

        Food.SetPublicKey()
        Food.Name = form.Name.data
        Food.Description = form.Description.data
        for each in form.DayOfReserve.data:
            if (d := Day.query.filter_by(NameEn=each).first()):
                Food.DayOfReserve.append(d)
        Food.Active = True if form.Active.data == "active" else False

        try:
            db.session.add(Food)
            db.session.commit()
        except Exception as e:
            # if any error happen remove images for filesystem
            for each in Food.GetAllImages():
                if os.path.exists(FoodDir / each):
                    os.remove(FoodDir / each)

            print(e)
            db.session.rollback()
            flash(" خطایی رخ داد", "danger")
            return render_template(f"{TEMPLATE_FOLDER}/add_new_food.html", ctx=ctx, form=form)
        else:
            flash("عملیات با موفقیت انجام شد ", "danger")
            return redirect(request.referrer)

        return redirect(request.referrer)


@admin.route(f"/{BASE_URL}/edit/<uuid:FoodKey>", methods=["GET"])
@admin_login_required
def edit_food(FoodKey):
    """
        this view take a food PublicKey and check if its valid return a template for editing food
    """
    ctx = {
        "manage_foods": "show",
        "add_new_food": "item-active"
    }
    FoodKey = str(FoodKey)
    food_db = FoodList.query.filter_by(PublicKey=FoodKey).first()
    if not food_db:
        flash("غذایی با کلید مورد نظر یافت نشد", "danger")
        return redirect(request.referrer)

    form = ManageFoodsForms.AddFoodForm()
    form.Name.data = food_db.Name
    form.Description.data = food_db.Description
    form.DayOfReserve.data = [each.NameEn for each in food_db.DayOfReserve]
    form.Active.data = "active" if food_db.Active else "inactive"
    ctx["food"] = food_db
    ctx["images"] = food_db.GetAllImages()

    return render_template(f"{TEMPLATE_FOLDER}/edit_food.html", ctx=ctx, form=form)


@admin.route(f"/{BASE_URL}/edit/<uuid:FoodKey>", methods=["POST"])
@admin_login_required
def edit_food_post(FoodKey):
    """
        this view take a post request for edit a food in db
    """
    ctx = {
        "manage_foods": "show",
        "add_new_food": "item-active"
    }
    FoodKey = str(FoodKey)
    Food = FoodList.query.filter_by(PublicKey=FoodKey).first()
    if not Food:
        flash("غذایی با کلید مورد نظر یافت نشد", "danger")
        return redirect(request.referrer)

    form = ManageFoodsForms.AddFoodForm()

    global old_images
    old_images = False
    # check have image
    if form.Images.data:
        have_img = False

        for each in form.Images.data:
            if not each:
                continue
            have_img = True

            name = str(uuid.uuid4()) + secure_filename(each.filename[:50])
            ex = pathlib.Path(each.filename).suffix
            if ex not in VALID_IMAGE_EXTENSIONS:
                flash(
                    "عکس انتخابی دارای فرمت نامعتبر است" + "\nفرمت های پشتیبانی شده" + f"{''.join(VALID_IMAGE_EXTENSIONS)}",
                    "danger")
                return render_template(f"{TEMPLATE_FOLDER}/edit_food.html", ctx=ctx, form=form)
            each.filename = name

    # if have image save it in Media
    if have_img:
        for each in form.Images.data:
            try:
                each.save(FoodDir / each.filename)
            except Exception as e:
                print(e)
                if (os.path.exists(FoodDir / each.filename)):
                    os.remove(FoodDir / each.filename)
                flash("خطایی هنگام ذخیره تصصویر رخ داد", "danger")
                return redirect(request.referrer)

        old_images = False if Food.GetAllImages()[0] == "default.png" else Food.GetAllImages()
        Food.SetImage([n.filename for n in form.Images.data])

    if not Food.SetFoodName(form.Name.data):
        flash("نام غذا تکراری می باشد", "danger")
        return render_template(f"{TEMPLATE_FOLDER}/edit_food.html", ctx=ctx, form=form)

    Food.Description = form.Description.data

    Food.DayOfReserve = []
    for each in form.DayOfReserve.data:
        d = Day.query.filter_by(NameEn=each).first()
        if d and d not in Food.DayOfReserve:
            Food.DayOfReserve.append(d)

    # Food.DayOfReserve =
    Food.Active = True if form.Active.data == "active" else False

    try:
        db.session.add(Food)
        db.session.commit()
    except Exception as e:
        # if any error happen remove images for filesystem
        for each in Food.GetAllImages():
            if os.path.exists(FoodDir / each):
                os.remove(FoodDir / each)

        print(e)
        db.session.rollback()
        flash("خطایی رخ داد", "danger")
        return render_template(f"{TEMPLATE_FOLDER}/add_new_food.html", ctx=ctx, form=form)
    else:
        # remove old images
        if old_images:
            for each in old_images:
                if os.path.exists(FoodDir / each):
                    os.remove(FoodDir / each)

        flash("عملیات با موفقیت انجام شد", "danger")
        return redirect(request.referrer)

    return redirect(request.referrer)
