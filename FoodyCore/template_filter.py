import datetime
import khayyam

from flask import url_for
from FoodyAuth.model import Section
from FoodyCore import app
from FoodyCore.utils import TimeStamp
from FoodyOrder.model import FoodList, Day
from FoodyAuth.model import User
from FoodyAdmin.model import Admin

from FoodyConfig.config import STATUS




@app.template_filter("Serve")
def Serve(path):
    """
        this template filter generate media link base of Debug Mode (APP_DEBUG)

        if debug mode is on Flask app Serve Static files and generate a link to web.Serve View
        otherwise this view generate link for Nginx path /Media
    """
    if STATUS:
        return url_for("web.Serve", path=path) # flask serve
    else:
        return f'/Media/{path}'  # nginx serve
        # return app.config.get("DOMAIN", "")+f'/Media/{path}'  #nginx serve




@app.template_filter("Convert2Persian")
def Convert2Persian(dt: datetime.datetime) -> khayyam.JalaliDatetime:
    t = TimeStamp()
    t = t.convert_grg2_jalali_dt(dt)
    return f"{t.time()} - {t.year}/{t.month}/{t.day}"


@app.template_filter("SectionName")
def SectionName(SectionID: int) -> str:
    """This Filter Get a Section id and Return SectionName"""
    return Section.query.get(SectionID).Name or "NULL"


@app.template_filter("GetDayName")
def GetDayName(day: Day.id) -> str:
    """
    this Filter Take a Day_ID and return Day.Name
    """
    return Day.query.filter(Day.id == day).first().NameFa or "NULL"


@app.template_filter("GetFoodName")
def GetFoodName(food_id: int) -> str:
    """
    Get a Food_id and return food Name for db
    """
    return FoodList.query.filter(FoodList.id == food_id).first().Name or "NULL"


@app.template_filter("GetPersianDate")
def GetPersianDate(date: str) -> str:
    """
    convert an georgian time to jalali time
    """
    t = TimeStamp()
    d = t.convert_grg2_jalali_d(date)
    x = f" {str(d.isoformat())} - {d.strftime('%A')}"
    return x


@app.template_filter("GetUserName")
def GetUserName(userID: int) -> str:
    """
        get user id in db and return user's firstname + last name
    """
    name = User.query.filter(User.id == userID).first()
    if not name:
        return "NULL"
    return f"{name.FirstName} {name.LastName}"


@app.template_filter("GetSectionNameByUserID")
def GetSectionNameByUserID(userID: int) -> str:
    """
        return section name that user work via user id
    """
    user = User.query.filter(User.id == userID).first()
    if not user:
        return "NULL"
    return Section.query.filter(Section.id == user.SectionID).first().Name or "NULL"


@app.template_filter("UnixT2Date")
def UnixT2Date(unixtime: int) -> datetime.datetime:
    """
        convert a unix time stamp to a datetime
    """
    if not unixtime:
        return "NULL"
    time, date = datetime.datetime.fromtimestamp(unixtime).time(), datetime.datetime.fromtimestamp(unixtime).date()
    date = GetPersianDate(date)
    return f"{date}- {time}"


@app.template_filter("getAdmin")
def getAdmin(admin_id: int) -> Admin:
    """
        this filter get an admin primary key and return admin object
    """
    return Admin.query.get(admin_id) or "NULL"


print("[OK] All Template Filter checked By Flask App <FoodyCore>".title())
