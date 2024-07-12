import json

import sqlalchemy as sa
import sqlalchemy.orm as so

from Auth.model import User
from Core.model import BaseModel

Food2ReserveDay = sa.Table(
    BaseModel.SetTableName("food_2_day_reserve"),
    BaseModel.metadata,
    sa.Column("food_menu_id", sa.INTEGER, sa.ForeignKey(BaseModel.SetTableName("food_menu") + ".id"), nullable=False),
    sa.Column("food_reserve_day_id", sa.INTEGER, sa.ForeignKey(BaseModel.SetTableName("food_reserve_day") + ".id"),
              nullable=False),
)


class FoodReserveDay(BaseModel):
    __tablename__ = BaseModel.SetTableName("food_reserve_day")

    dayFA: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False, unique=True)
    dayEN: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False, unique=True)

    # backreference for getting foods = foods_list


class FoodType(BaseModel):
    __tablename__ = BaseModel.SetTableName("food_menu_type")
    name: so.Mapped[str] = so.mapped_column(sa.String(256), unique=True, nullable=False)

    def __str__(self):
        return f"<FoodType {self.id} - {self.name}>"


class Food(BaseModel):
    __tablename__ = BaseModel.SetTableName("food_menu")

    name: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False, unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(2048), nullable=False, unique=False)
    images: so.Mapped[sa.JSON] = so.mapped_column(sa.JSON, default=json.dumps([]), nullable=False, unique=False)
    food_type: so.Mapped[int] = so.mapped_column(sa.INTEGER, sa.ForeignKey(FoodType.id), unique=False)

    reserve_days = so.relationship(FoodReserveDay, secondary=Food2ReserveDay, backref="foods_list", lazy="dynamic")
    prices = so.relationship("FoodPrice", backref="food", lazy="dynamic")

    @property
    def price(self):
        latest_price = self.prices.order_by(FoodPrice.id.desc()).limit(1).first()
        return latest_price.price if latest_price else 0

    def __str__(self):
        return f"<FoodType {self.id} - {self.name}>"


class FoodPrice(BaseModel):
    __tablename__ = BaseModel.SetTableName("menu_prices")
    price: so.Mapped[int] = so.mapped_column(sa.BIGINT, unique=False, nullable=False)
    food_id: so.Mapped[int] = so.mapped_column(sa.INTEGER, sa.ForeignKey(Food.id), nullable=False)

    def __str__(self):
        return f"<FoodPrice {self.id} - {self.price}>"


Order2FoodPrice = sa.Table(
    BaseModel.SetTableName("order-2-food-price"),
    BaseModel.metadata,
    sa.Column("food_menu_id", sa.INTEGER, sa.ForeignKey(Food.id), nullable=False),
    sa.Column("food_price_id", sa.INTEGER, sa.ForeignKey(FoodPrice.id), nullable=False),
    sa.Column("order_id", sa.INTEGER, sa.ForeignKey(BaseModel.SetTableName("orders") + ".id"), nullable=False)
)


class Order(BaseModel):
    __tablename__ = BaseModel.SetTableName("orders")
    user_id: so.Mapped[int] = so.mapped_column(sa.INTEGER, sa.ForeignKey(User.id, ondelete='SET NULL'), nullable=False)

    foods = so.relationship(Food, secondary=Order2FoodPrice, backref="orders", lazy="dynamic")

    def __str__(self):
        return f"<Order {self.id} - {self.food_id}>"
