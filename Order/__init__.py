# from flask import Blueprint
#
# order = Blueprint(
#     name="order",
#     import_name=__name__,
#     static_folder="static/order",
#     template_folder="templates/order",
#     static_url_path="OrderStatic"
# )
#
# import Order.model
# import Order.views
#
from flask_restx import Namespace

food_blp = Namespace(name='food', description="Operation on foods", )
order_blp = Namespace(name='order',description="Operation on orders")

import Order.order_views
import Order.food_views
