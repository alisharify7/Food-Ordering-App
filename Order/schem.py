"""
 * input and output models for api's
 * author: @alisharify7
 * Copyleft 2023-2024. under GPL-3.0 license
 * https://github.com/alisharify7/Food-Ordering-App
"""

from Order import food_blp
from flask_restx import fields




FoodReserveDayScheme = food_blp.model("FoodReserveDayScheme", {
    "dayFA": fields.String(),
    "dayEN": fields.String(),
})

FoodScheme = food_blp.model("FoodScheme", {
    "name": fields.String(),
    "images": fields.String(),
    "description": fields.String(),
    "reserve_days": fields.List(fields.Nested(FoodReserveDayScheme))
})
