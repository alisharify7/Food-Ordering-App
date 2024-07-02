import datetime
import os.path

from flask import render_template, send_from_directory
from FoodyAdmin import admin
from FoodyAuth.AccessControl.decorators import admin_login_required
from FoodyConfig.config import Admin_Static
from FoodyOrder.model import Order
from FoodyAuth.model import User


@admin.route("/AdminPrivateStatic/<path:filename>/")
@admin_login_required
def AdminStatic(filename):
    """Serve Static Files only To Admin accounts"""
    if os.path.exists(Admin_Static / filename):
        return send_from_directory(Admin_Static, filename)
    else:
        return "File Not Found!", 404


@admin.route("/")
@admin_login_required
def index():
    ctx = {
        "all_orders": Order.query.count(),
        "today_orders": Order.query.filter(Order.OrderDate == datetime.date.today()).count(),
        "all_users": User.query.count(),
        "active_users": User.query.filter(User.Active == True).count(),
    }
    return render_template("admin/index.html", ctx=ctx)
