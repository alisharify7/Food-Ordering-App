"""
 * input and output models for api's
 * author: @alisharify7
 * Copyleft 2023-2024. under GPL-3.0 license
 * https://github.com/alisharify7/Food-Ordering-App
"""

from Order import food_blp, order_blp
from flask_restx import fields




FoodReserveDayScheme = food_blp.model("FoodReserveDayScheme", {
    "dayFA": fields.String(),
    "dayEN": fields.String(),
})


FoodScheme = food_blp.model("FoodScheme", {
    "name": fields.String(),
    "images": fields.List(fields.String()),
    "description": fields.String(),
    "reserve_days": fields.List(fields.Nested(FoodReserveDayScheme)),
    "public_key": fields.String(data_key="a"),
})


MakeFoodOrderSchem = order_blp.model("MakeFoodOrderSchem", {
    "food_key": fields.String()
})
FoodOrderResponse = order_blp.model("FoodOrderResponse", {
    "order_id": fields.String(),
    "status": fields.Boolean()
})