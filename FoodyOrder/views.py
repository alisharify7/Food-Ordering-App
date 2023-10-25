import datetime
import khayyam
from flask import jsonify, request, redirect, flash

from FoodyOrder import order
from FoodyCore.utils import TimeStamp
from FoodyAuth.model import User
from FoodyOrder.model import Day, FoodList, Order
from FoodyConfig.config import VALID_DAYS_PERSIAN, MAX_ORDER_TIMEOUT_DAY
from FoodyAuth.AccessControl.decorators import login_required, admin_login_required, admin_and_users_allowed
from FoodyCore.extension import ServerCsrf
from FoodyCore.extension import db


@order.route("/GetMenuDays/", methods=["GET"])
@login_required
def GetMenuDays():
    """
        this view return Valid Days for registering order
        from now() time to 7 days ahead

        like:
        {
            "date-shamsi": 1400/10/21,
            "date-shamsi-farsi": "شنبه"
         }

    """
    today = khayyam.JalaliDatetime.now()
    week = []

    # move 7 days from this day
    for each in range(0, MAX_ORDER_TIMEOUT_DAY):
        d = today + datetime.timedelta(days=each)  # target day
        p = d.strftime("%A")  # in persian string date

        if p not in VALID_DAYS_PERSIAN:  # if day is not allowed skip it
            continue

        info = {
            "date-shamsi": str(d.date()),
            "date-shamsi-farsi": str(p)
        }

        week.append(info)

    return jsonify(week), 200


@order.route("/", methods=["POST"])
@login_required
def Register_New_Order_Post():
    """
        this view register new orders for each user
        params:
            food key(Public Key:uuid)
            target day (a persian date: 1400-10-21)

    """
    day = request.form.get("day", None, type=str)
    if not day:
        return jsonify({"status": "failed", "error": "برخی مقادیر به نظر گم شده اند، لطفا دوباره امتحان کنید"}), 400

    key = request.form.get("food", None, type=str)
    if not day:
        return jsonify({"status": "failed", "error": "برخی مقادیر به نظر گم شده اند، لطفا دوباره امتحان کنید"}), 400

    try:  # check target date is valid
        day = khayyam.JalaliDate(*day.split("/"))
    except:
        return jsonify({"status": "failed", "error": "تاریخ وارد شده معتبر نمی باشد"}), 400

    # check da is not less than today
    today = khayyam.JalaliDate.today()
    if day < today:
        return jsonify({"status": "failed", "error": "امکان سفارش برای تاریخ های گذشته وجود ندارد"}), 400

    if day > today + datetime.timedelta(days=MAX_ORDER_TIMEOUT_DAY):
        return jsonify({"status": "failed", "error": "محمدوده سفارشات غذا باید بین امروز تا 7 روز آینده باشد"}), 400

    if not (DayDb := Day.query.filter_by(NameFa=day.strftime("%A")).first()):  # getting food object
        return jsonify({"status": "failed", "error": "تاریخی با مشخصات وارد شده یافت نشد"}), 400

    if today == day and khayyam.JalaliDatetime.now().time() > datetime.time(9, 0, 0):
        return jsonify({"status": "failed", "error": "امکان سفارش برای امروز بعد از ساعت 9 صبح، غیرفعال می باشد"}), 400

    foodDb = FoodList.query.filter_by(PublicKey=key).first()  # check food key exists
    if not foodDb:
        return jsonify({"status": "failed", "error": "غذایی با مشخصات وارد شده یافت نشد"}), 400
    if not foodDb.Active:
        return jsonify({"status": "failed", "error": "غذا مورد نظر توسط مدیر سیستم غیرفعال شده است"}), 400

    if (DayDb not in foodDb.DayOfReserve):
        return jsonify({"status": "failed", "error": "غذا و روز انتخابی موجود نیست!"}), 400

    t = TimeStamp()
    OrderDateGeorgian = t.convert_jlj2_georgian_d(value=day)  # convert jalali to georgian
    IsUSerOrdered = Order.query.filter(Order.OrderDate == OrderDateGeorgian).filter(
        Order.UserID == request.user_object.id).first()

    if IsUSerOrdered:
        return jsonify({'status': 'failed', 'error': ' کاربر برای روز انتخابی غذایی از قبل رزرو دارد'}), 400

    NewOrder = Order()
    NewOrder.SetPublicKey()
    NewOrder.OrderDate = OrderDateGeorgian
    NewOrder.DayID = DayDb.id
    NewOrder.FoodID = foodDb.id
    NewOrder.SetPublicKey()
    NewOrder.UserID = request.user_object.id

    try:
        db.session.add(NewOrder)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'status': 'failed', 'error': 'error in db'}), 400

    return jsonify({'status': 'success', 'message': 'سفارش با موفقیت انجام شد'}), 200


@order.route("/GetDayFood/", methods=["POST"])
@admin_and_users_allowed  # both admin and users can request this view
def GetDayFood():
    """
        this  view take a persian string date and return all foods that related to that day
        params: formdata('day'):a jalali calendar date
    """
    day = request.form.get("day", None, type=str)
    if not day:
        return jsonify({"status": "failed", "error": "invalid params"}), 400

    try:
        day = khayyam.JalaliDate(*day.split("/"))
    except:
        return jsonify({"status": "failed", "error": "invalid day, day format YYYY-DD-MM"}), 400

    if not (DayDb := Day.query.filter_by(NameFa=day.strftime("%A")).first()):
        return jsonify({"status": "failed", "error": "invalid day"}), 400

    Foods = FoodList.query.filter(FoodList.DayOfReserve.contains(DayDb)).filter(FoodList.Active == True).all()
    foodJson = []
    t = TimeStamp()
    for each in Foods:
        OrderDateGeorgian = t.convert_jlj2_georgian_d(value=day)  # convert jalali to georgian
        temp = {}
        temp["images"] = each.GetAllImages()
        temp["name"] = each.Name
        temp["caption"] = each.Description
        temp["food-key"] = each.GetPublicKey()

        if request.user_object:  # if user is requesting
            ordered = Order.query.filter(Order.OrderDate == OrderDateGeorgian).filter(
                Order.UserID == request.user_object.id).filter(Order.FoodID == each.id).first()

            temp["is_ordered"] = True if ordered else False
        else:  # if admin is requesting
            temp["is_ordered"] = False

        foodJson.append(temp)

    return jsonify({"status": "success", "data": foodJson}), 200


@order.route("/cancel/", methods=["POST"])
@login_required
def cancel_order_post():
    """
        this view cancel an order if its cancelable

    """
    OrderKey = request.form.get("orderKey", type=str, default=None)
    if not OrderKey:
        return jsonify({'status': 'failed', 'error': 'سفارشی یافت نشد'}), 400

    if not (order_db := Order.query.filter_by(PublicKey=OrderKey).first()):
        return jsonify({'status': 'failed', 'error': 'سفارشی یافت نشد'}), 400

    if not order_db.IsCancelAble():
        return jsonify({'status': 'failed',
                        'error': 'امکان لغو سفارش مورد نظر وجود ندارد / سفارشات تنها تا ساعت 9 آن روز قابل لغو هستند'}), 400

    else:
        try:
            db.session.delete(order_db)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'failed', 'error': 'خطایی هنگام لغو سفارش رخ داد'}), 400
        else:
            return jsonify({'status': 'success', 'message': 'سفارش با موفقیت لغو گردید'}), 200


@order.route("/delete/<uuid:orderKey>", methods=["GET"])
@admin_login_required
def delete_order_post(orderKey):
    """
        this view take order Key and delete that order from db
    """
    orderKey = str(orderKey)
    if not (order_db := Order.query.filter_by(PublicKey=orderKey).first()):
        flash("سفارشی با مشخصات وارد شده یافت نشد", "danger")
        return redirect(request.referrer)

    try:
        db.session.delete(order_db)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        flash("خطایی هنگام حذف سفارش رخ داد", "danger")
    else:
        flash("عملیات با موفقیت انجام شد", "success")

    return redirect(request.referrer)


@order.route("/haveOrder/", methods=["POST"])
@admin_login_required
@ServerCsrf.exempt
def haveAnyOrder():
    """
        this view take an employee code and check that employee have any order in specified date
    """
    TargetDate, employeeCode = request.form.get("date"), request.form.get("employeeCode")
    if not TargetDate or not employeeCode:
        return jsonify(
            {
                "status": "failed",
                "error": "برخی مقادیر به درستی ارسال نشده اند"
            }), 404

    t = TimeStamp()
    if t.is_persian_date(TargetDate):
        TargetDate = t.convert_string_jalali2_dateD(TargetDate)

    if not (user_db := User.query.filter_by(EmployeeCode=employeeCode).first()):
        return jsonify(
            {
                "status": "failed",
                "error": "کارمندی با شماره کارمندی وارد شده یافت نشد"
            }), 404

    if Order.query.filter(Order.UserID == user_db.id).filter(Order.OrderDate == TargetDate).first():
        return jsonify({
            "status": "failed",
            "error": "کاربر برای روز انتخابی غذایی رزرو دارد"
        }), 400

    else:
        return jsonify({
            "status": "success",
            "message": f"کاربر {user_db.GetUserName()} برای روز انتخابی غذایی رزرو ندارد"
        }), 200


@order.route("/register/food/", methods=["POST"])
@admin_login_required
@ServerCsrf.exempt  # ignore csrf token
def Register_food_user_Post():
    """
        this view register food for given employeeCode
        uses by admin :
    """
    employeeCode, foodKey, order_date = request.form.get('employeeCode'), request.form.get('foodKey'), request.form.get(
        'order_date')
    if not employeeCode or not foodKey or not order_date:
        return jsonify({"status": "failed", "error": "برخی موارد به درستی ارسال نشده است"}), 400

    t = TimeStamp()
    if not t.is_persian_date(order_date):
        return jsonify({"status": "failed", "error": "تاریخ به درستی وارد نشده است"}), 400

    order_date = t.convert_string_jalali2_dateD(order_date)  # georgian date
    day = t.convert_grg2_jalali_d(order_date)  # jalali date

    if not (user_db := User.query.filter(User.EmployeeCode == employeeCode).first()):
        return jsonify({"status": "failed", "error": "کاربری با کد کارمندی وارد شده یافت نشد"}), 404

    if not (food_db := FoodList.query.filter(FoodList.PublicKey == foodKey).first()):
        return jsonify({"status": "failed", "error": "غذایی با مشخصات وارد شده یافت نشد"}), 404

    if not (DayDb := Day.query.filter_by(NameFa=day.strftime("%A")).first()):  # getting food object
        return jsonify({"status": "failed", "error": "تاریخی با مشخصات وارد شده یافت نشد"}), 400

    if (DayDb not in food_db.DayOfReserve):
        return jsonify({"status": "failed", "error": "غذا و روز انتخابی موجود نیست!"}), 400

    if (Order.query.filter(Order.OrderDate == order_date).filter(Order.UserID == user_db.id).first()):
        return jsonify({"status": "failed", "error": "کاربر در روز انتخابی غذایی از قبل رزرو دارد"}), 400

    order = Order()
    order.SetPublicKey()
    order.UserID = user_db.id
    order.FoodID = food_db.id
    order.OrderDate = order_date
    order.DayID = DayDb.id

    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"status": "failed", "error": "خطایی هنگا ذخیره سازی رخ داد"}), 400
    else:
        return jsonify({"status": "success", "message": "سفارش با موفقیت ثبت گردید"}), 200
