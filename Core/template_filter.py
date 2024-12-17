"""
 * Food Ordering Application
 * core <global> template filter and ocntexts
 * author: github.com/alisharify7
 * email: alisharifyofficial@gmail.com
 * Copyleft 2023-2024. under GPL-3.0 license
 * https://github.com/alisharify7/Food-Ordering-App
"""

import datetime

from werkzeug.routing import BaseConverter, ValidationError
from flask import current_app, url_for, abort

import khayyam


def StorageUrl(path: str) -> str:
    """
    This template filter generate dynamic urls base of app.debug mode
    for serving statics via flask or nginx in production or development
    if debug mode is on this filter redirect users to flask.serve function
    but in production mode this filter redirect users to serve static via nginx

    :param path: path of the file
    :type path: str

    :return: static url path
    :rtype: str

    """
    if path[0] == "/":
        path = path[1:]

    if current_app.debug:
        return url_for("ServeStorageFiles", path=path, _external=True)  # flask serve
    else:
        return f"/Storage/{path}"  # Nginx Serve Files


def today(only_str=False, only_date=True, only_date_and_time=False):
    # TODO: refactor this function and make it a class with required methods
    now = khayyam.JalaliDatetime.now()
    if only_str:
        return now.strftime("%A")
    elif only_date:
        return str(now.date().today()).replace("-", "/")
    else:
        return str(now)




class ShamsiUrlDateConverter(BaseConverter):
    """
    Extracts a ISO8601 date from the path and validates it.
    https://stackoverflow.com/questions/31669864/date-in-flask-url
    """

    regex = r"\d{4}-\d{2}-\d{2}"

    def to_python(self, value):
        try:
            value = datetime.datetime.strptime(value, "%Y-%m-%d")
            return khayyam.JalaliDatetime(value).strftime("%A")
        except Exception:
            abort(404)

    def to_url(self, value):
        return value.strftime("%Y-%m-%d")



templatesFilters = {"StorageUrl": StorageUrl}
def contexts():
    ctx = {"current_app": current_app, "today": today}
    return ctx

