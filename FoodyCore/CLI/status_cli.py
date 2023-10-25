import datetime

from FoodyAdmin.model import Admin
from FoodyAuth.model import User
from FoodyOrder.model import Order
from tabulate import tabulate

from flask.cli import AppGroup


status_cli = AppGroup("status", help="Show Status of Users and Database.")



@status_cli.command("users")
def show_users_status():
    """
    Show Users Status in App
    """
    all_users = User.query.count()
    active_users = User.query.filter(User.Active == True).count()

    headers = (
        "Time Stamp",
        "All Users",
        "Active Users"
    )
    table = [
        [datetime.datetime.utcnow(), all_users, active_users]
    ]


    print(tabulate(
        table,
        headers=headers,
        tablefmt="grid",
    ))


@status_cli.command("admins")
def show_users_status():
    """
    Show Admins Status in App
    """
    all_users = Admin.query.count()
    active_users = Admin.query.filter(Admin.Active == True).count()

    headers = (
        "Time Stamp",
        "All Admins",
        "Active Admins"
    )

    table = [
        [datetime.datetime.utcnow(), all_users, active_users]
    ]

    print(tabulate(
        table,
        headers=headers,
        tablefmt="grid",
    ))




@status_cli.command("orders")
def show_users_status():
    """
    Show Number os Today orders
    """
    today = datetime.date.today()
    today_orders = Order.query.filter(Order.OrderDate == today).count()
    all_orders = Order.query.count()

    headers = (
        "Time Stamp",
        "Today Orders",
        "All Orders",
    )
    table = [
        [datetime.datetime.utcnow(), today_orders, all_orders]
    ]

    print(tabulate(
        table,
        headers=headers,
        tablefmt="grid",
    ))


