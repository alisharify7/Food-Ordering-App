import json
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as so

from Core.model import BaseModel


Food2ReserveDay = sa.Table(
  "food_2_day_reserve",
           BaseModel.metadata,
      sa.Column( "food_menu" + "_id", sa.Integer, sa.ForeignKey(BaseModel.SetTableName("food_menu") + ".id"), nullable=False),
            sa.Column( "food_reserve_day" + "_id", sa.Integer, sa.ForeignKey(BaseModel.SetTableName("food_reserve_day") + ".id"), nullable=False),
)

class FoodReserveDay(BaseModel):
    __tablename__ = BaseModel.SetTableName("food_reserve_day")

    dayFA: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False, unique=True)
    dayEN: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False, unique=True)

    # backreference for getting foods = foods_list

class Food(BaseModel):
    __tablename__ = BaseModel.SetTableName("food_menu")

    name: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False, unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(1024), nullable=False, unique=False)
    images: so.Mapped[sa.JSON] = so.mapped_column(sa.JSON, default=json.dumps([]), nullable=False, unique=False)
    price: so.Mapped[sa.Integer] = so.mapped_column(sa.Integer, nullable=False, unique=False)

    reserve_days: so.Mapped[List[FoodReserveDay]] = so.relationship(FoodReserveDay, secondary=Food2ReserveDay, backref="foods_list", lazy="dynamic")
