import khayyam
from flask import current_app
from flask_login import login_required
from flask_restx import Resource, abort

from Order import food_blp
from Order.model import Food as FoodModel, FoodReserveDay
from Order.schem import FoodScheme


@food_blp.route("<string:food_name>")
class SpecificFood(Resource):
    @login_required
    # @rate_limiter TODO:
    @food_blp.marshal_with(FoodScheme, code=200)
    def get(self, food_name: str):
        """get food base on the given food name """
        db = current_app.extensions['sqlalchemy']
        query = db.select(FoodModel).filter_by(name=food_name)
        result = db.session.execute(query).scalar_one_or_none()
        if not result:
            abort(message="غذایی با نام وارد شده یافت نشد", code=404)

        return result


@food_blp.route("/today/")
class TodayFoods(Resource):
    @login_required
    # @rate_limiter TODO:
    @food_blp.marshal_with(FoodScheme, code=200)
    def get(self):
        """return's today foods"""
        today = khayyam.JalaliDate.today().strftime("%A")
        db = current_app.extensions['sqlalchemy']
        query = db.select(FoodReserveDay).filter_by(dayFA=today)
        result = db.session.execute(query).scalar_one_or_none()
        if not result:
            abort(message="غذایی با نام وارد شده یافت نشد", code=404)
        return result.foods_list


@food_blp.route("/date/<string:day_string>")
class SpecificDayFood(Resource):
    @login_required
    # @rate_limiter TODO:
    @food_blp.marshal_with(FoodScheme, code=200)
    def get(self, day_string):
        """return's Specific Day foods"""
        db = current_app.extensions['sqlalchemy']
        query = db.select(FoodReserveDay).filter_by(dayFA=day_string)
        result = db.session.execute(query).scalar_one_or_none()
        if not result:
            abort(message="غذایی با نام وارد شده یافت نشد", code=404)
        return result.foods_list
