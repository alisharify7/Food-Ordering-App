import datetime
import json
from FoodyCore.model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Column, JSON, ForeignKey, Date, Boolean
from FoodyCore.extension import db
from FoodyCore.utils import TimeStamp

FoodsDay = db.Table(
    BaseModel.SetTableName("food_days"),
    Column("food_id", Integer, ForeignKey(BaseModel.SetTableName("foods") + ".id")),
    Column("day_id", Integer, ForeignKey(BaseModel.SetTableName("days") + ".id")),
)


class FoodList(BaseModel):
    """This Table Hold Foods List Name"""
    __tablename__ = BaseModel.SetTableName("foods")
    Images = Column(JSON, nullable=False, unique=False, default=json.dumps(["default.png"]))
    Name = Column(String(64), nullable=False, unique=False)
    Description = Column(String(255), nullable=False, unique=False)
    DayOfReserve = relationship('Day', secondary=FoodsDay, backref='GetFood')
    Active = Column(Boolean(), default=False, unique=False, nullable=False)
    Orders = db.relationship("Order", backref='GetFood')

    def SetFoodName(self, name):
        if name == self.Name:
            return True
        else:
            if self.query.filter_by(Name=name).first():
                return False
            else:
                self.Name = name
                return True

    def SetImage(self, imgARR: list):
        self.Images = json.dumps(imgARR)

    def GetAllImages(self) -> list:
        return json.loads(self.Images)

    def GetImage(self, loc: int) -> str:
        imgs = self.GetAllImages()
        try:
            return imgs[loc]
        except:
            return imgs[-1] or "NON"

    def GetAllDays(self):
        d = []
        days = self.DayOfReserve
        days.sort(key=lambda x: x.id)
        for each in days:
            d.append(each.NameFa)

        return d

    def __str__(self):
        return f"<FoodList {self.id}> {self.PublicKey}"


class Day(BaseModel):
    """This Table hold days for each food"""
    __tablename__ = BaseModel.SetTableName("days")
    NameFa = Column(String(64), nullable=False, unique=True)
    NameEn = Column(String(64), nullable=False, unique=True)

    def __str__(self):
        return f"<Day {self.id}> {self.NameEn}"

    def __repr__(self):
        return f"<Day {self.id}> {self.NameEn}"

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id


class Order(BaseModel):
    """This table Keep All Orders information"""
    __tablename__ = BaseModel.SetTableName("orders")
    UserID = Column(Integer, ForeignKey(BaseModel.SetTableName('users') + ".id"))
    FoodID = Column(Integer, ForeignKey(BaseModel.SetTableName('foods') + ".id"))
    DayID = Column(Integer, ForeignKey(BaseModel.SetTableName("days") + ".id"))
    OrderDate = Column(Date, nullable=False, unique=False)

    def __str__(self):
        return f"<Order {self.id} - {self.PublicKey}>"

    def GetJalaliDate(self):
        """
        this method Return jalali version of OrderDate
        """
        t = TimeStamp()
        return t.convert_grg2_jalali_d(self.OrderDate)

    def GetFoodName(self):
        """
        return Food Name
        """
        return FoodList.query.get(self.FoodID).Name

    def IsCancelAble(self):
        """
        this method check this order can be canceled by user or not
            each order only can cancel with below conditions:
                - if order date is same as today user only cancel order before 09:00 AM

                - if order date is less than today user can cancel order

                - if order date is grater than today user can't cancel order
        """
        todayDate = datetime.date.today()
        BorderTime = datetime.time(9, 0, 0)

        if self.OrderDate > todayDate:
            return True
        elif self.OrderDate < todayDate:
            return False
        else:
            if datetime.datetime.now().time() < BorderTime:
                return True
            else:
                return False

        return False
