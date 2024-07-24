from flask_restx import Resource, abort

from Order import order_blp
from Order.model import Food, Order, FoodPrice
from flask_login import login_required



@order_blp.route("")
class Order(Resource):
    pass