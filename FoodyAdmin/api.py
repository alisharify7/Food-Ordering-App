import datetime

from flask import request, jsonify
from sqlalchemy import func

from FoodyAdmin import admin
from FoodyAuth.AccessControl.decorators import admin_login_required
from FoodyAuth.model import Section, User
from FoodyCore.extension import db
from FoodyCore.utils import TimeStamp
from FoodyOrder.model import Order


@admin.route("/api/AllOrders/", methods=["GET"])
@admin_login_required
def All_Orders_API():
    """
        this api view take 2 get arguments
            from: a date for starting time
            to: a date for ending time

        and return all Orders from date to end date
    """
    Ftime = request.args.get("from", type=str, default=None)
    Etime = request.args.get("end", type=str, default=None)

    if not Ftime or not Etime:
        return jsonify({}), 400

    try:
        f = datetime.datetime.strptime(Ftime, "%Y-%m-%dT%H:%M:%S.%fZ")
        e = datetime.datetime.strptime(Etime, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return jsonify({"status": "failed", "error": "invalid date format"}), 400
    except Exception as e:
        print(e)
        return jsonify({"status": "failed", "error": "invalid date format"}), 400

    f = f.date()
    e = e.date()
    timeHandler = TimeStamp()

    data = []
    for each in range(0, (f - e).days):
        time = f - datetime.timedelta(days=each)
        temp = {}
        query = Order.query.filter(Order.OrderDate == time).count()

        time = timeHandler.convert_grg2_jalali_d(time)
        temp["date"] = f"{str(time)} {time.strftime('%A')}"
        temp["order_count"] = query
        data.append(temp)


    data.reverse()
    return jsonify({"status": "success", "data": data}), 200


@admin.route("/api/AllOrders/Sections/", methods=["GET"])
@admin_login_required
def All_Orders_Sections_API():
    """
    this view take two ISO format date and return all Orders(filtered by SectionsName) that
    are between these two dates
    """
    Ftime = request.args.get("from", type=str, default=None)
    Etime = request.args.get("end", type=str, default=None)

    if not Ftime or not Etime:
        return jsonify({"status": "failed", "error": "invalid params"}), 400

    try:
        f = datetime.datetime.strptime(Ftime, "%Y-%m-%dT%H:%M:%S.%fZ")
        e = datetime.datetime.strptime(Etime, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return jsonify({"status": "failed", "error": "invalid date format"}), 400
    except Exception as e:
        print(e)
        return jsonify({"status": "failed", "error": "invalid date format"}), 400

    f = f.date()  # from date
    e = e.date()  # end date

    AllSections = [section for section in db.session.query(Section.id, Section.Name).distinct().all()]

    data = []
    for sectionID, sectionName in AllSections:
        all_section_orders = Order.query.join(User, Order.UserID == User.id) \
            .filter(User.SectionID == sectionID) \
            .filter(Order.OrderDate <= f) \
            .filter(Order.OrderDate >= e) \
            .count()

        temp = {}
        temp["section_name"] = str(sectionName)
        temp["orders_count"] = all_section_orders
        data.append(temp)

    return jsonify({"status": "success", "data": data}), 200


@admin.route("/api/All/Users/", methods=["GET"])
@admin_login_required
def All_Users_Info_API():
    """
    this view return an info about all user and how many user each section have
    """

    AllSections = db.session.query(Section.id, Section.Name).distinct().all()

    data = []
    for sectionID, sectionName in AllSections:
        temp = {}
        sectionCount = User.query.filter_by(SectionID=sectionID).count()
        temp["section_name"] = sectionName
        temp["section_users"] = sectionCount
        data.append(temp)

    if len(data) == 0:
        for i in range(5):
            temp = {}
            temp["section_name"] = "تعریف نشده است"
            temp["section_users"] = 0
            data.append(temp)

    return jsonify({"status": "success", "data": data}), 200


@admin.route("/api/Top/User/Order/", methods=["GET"])
@admin_login_required
def Top_Five_User_Order_API():
    """
        this view return top 5 user with most ordered food in last month
    """
    today = datetime.date.today()
    last_month = today + datetime.timedelta(days=-31)

    TopFiveUsers = db.session.query(Order.UserID, db.func.count(Order.UserID).label('order_count')) \
        .group_by(Order.UserID) \
        .order_by(func.count(Order.UserID).desc()) \
        .filter(Order.OrderDate >= last_month) \
        .filter(Order.OrderDate <= today) \
        .limit(5) \
        .all()

    if len(TopFiveUsers) == 1:
        if TopFiveUsers[0][0] == None and TopFiveUsers[0][1] == 0:
            TopFiveUsers = []
    try:
        TopFiveUsers = [
            (User.query.get(each[0]), each[1]) for each in TopFiveUsers
        ]
    except Exception as e:
        print(e)
        TopFiveUsers = []

    data = []
    for each in TopFiveUsers:
        user, count = each[0].GetUserName(), each[1]

        temp = {
            "user_name": user + f"-{Section.query.get(each[0].SectionID).Name or '' }",
            "order_count": count
        }
        data.append(temp)

    if len(data) == 0:
        data.extend(
            [{"user_name": "وجود ندارد","order_count": 0}] * (5)
        )

    if len(data) < 5:
        data.extend(
            [{"user_name": "وجود ندارد","order_count": 0}] * (5-len(data))
        )

    return jsonify({"status": "success", "data": data}), 200
