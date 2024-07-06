# framework

from flask import Blueprint, request, redirect, url_for, flash, session
from Config import Setting


blp = Blueprint('middlewares', __name__)

@blp.route("/set/language/<string:language>/", methods=["GET"])
def setUserLanguage(language):
    """
        this view select a language in users session
    """
    location = (request.referrer or url_for('web.index_get'))
    if language not in Setting.LANGUAGES:
        return redirect(location)
    else:
        flash('زبان با موفقیت تغییر کرد', "success")
        session["language"] = language
        return redirect(location)