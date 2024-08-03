from flask_restx import Resource, abort

from Order import order_blp
from Order.model import Food, Order, FoodPrice
from flask_login import login_required

from Order.schem import MakeFoodOrderSchem, FoodOrderResponse


@order_blp.route("")
class Order(Resource):

    @login_required
    @order_blp.expect(MakeFoodOrderSchem)
    @order_blp.marshal_with(FoodOrderResponse)
    def post(self):
        """register an order for a user"""
        payload = order_blp.payload
        food_key = payload.get('food_key')

        return "IJ"