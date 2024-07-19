from datetime import date

from flask import current_app
from flask.views import MethodView

from Order import order_blp
from Order.model import Food, FoodReserveDay

from flask_login import login_required
import Order.schem as schemes

# @order.route('/food/<string:string_date>', methods=['GET'])
# @login_required
# def get_foods_by_date(string_date: str):
#     """
#     Gets foods by daty
#     TODO: caching date for each food day ,
#         adding a new method for clearing cache each time a food edited or added in admin panel.
#
#     """
#     db = current_app.extensions['sqlalchemy']
#     query = db.select(FoodReserveDay).filter_by(dayFA=string_date)
#     if not (result := db.session.execute(query).scalar_one_or_none()):
#         return {"status": "failed", "message": "روز مورد نظر یافت نشد"}, 404
#
#
#     return ":HI"
