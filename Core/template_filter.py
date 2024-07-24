import datetime

from werkzeug.routing import BaseConverter, ValidationError
from flask import current_app, url_for, abort

import khayyam

def StorageUrl(path: str):
    """
    This template filter generate dynamic urls base of app.debug mode
    for serving statics via flask or nginx in production or development
    if debug mode is on this filter redirect users to flask.serve function
    but in production mode this filter redirect users to serve static via nginx
    """
    if path[0] == "/":
        path = path[1:]

    if current_app.debug:
        # flask serve
        return url_for("ServeStorageFiles", path=path, _external=True)
    else:
        return f"/Storage/{path}"  # Nginx Serve Files


templatesFilters = {
    "StorageUrl": StorageUrl
}


def today(only_str=False, only_date=True, only_date_and_time=False):
    #TODO: refactor this function and make it a class with required methods
    now = khayyam.JalaliDatetime.now()
    if (only_str):
        return now.strftime("%A")
    elif only_date:
        return str(now.date().today()).replace('-', '/')
    else:
        return str(now)

def contexts():
    ctx = {
        "current_app": current_app,
        "today": today
    }

    return ctx



# base url convertor

class ShamsiUrlDateConverter(BaseConverter):
    """
    Extracts a ISO8601 date from the path and validates it.
    https://stackoverflow.com/questions/31669864/date-in-flask-url
    """
    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        try:
            value = datetime.datetime.strptime(value, "%Y-%m-%d")
            return khayyam.JalaliDatetime(value).strftime("%A")
        except Exception:
            abort(404)
    def to_url(self, value):
        return value.strftime('%Y-%m-%d')