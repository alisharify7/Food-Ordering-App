from flask import current_app, request
from flask_login import login_required
from flask_restx import Resource, abort

from Order import food_blp
from Order.model import Food as FoodModel
from Order.schem import FoodScheme


@food_blp.route("")
class Food(Resource):
    @login_required
    # @rate_limiter TODO:
    @food_blp.marshal_list_with(FoodScheme, code=200)
    def get(self):
        """returns all foods"""
        page = request.args.get('page', type=int, default=1)
        per_page = request.args.get('per_page', type=int, default=10)
        db = current_app.extensions['sqlalchemy']
        result = db.paginate(page=page, per_page=per_page, max_per_page=30, select=db.select(FoodModel))
        return result.items



@food_blp.route("<string:food_name>")
class SpecificFood(Resource):
    @login_required
    # @rate_limiter TODO:
    @food_blp.marshal_with(FoodScheme, code=200)
    def get(self, food_name: str):
        """return one food with given food name"""
        db = current_app.extensions['sqlalchemy']
        query = db.select(FoodModel).filter_by(name=food_name)
        result = db.session.execute(query).scalar_one_or_none()
        if not result:
            abort(message="غذایی با نام وارد شده یافت نشد", code=404)

        return result

