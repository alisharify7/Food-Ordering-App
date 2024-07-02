# framework

from flask import Blueprint, request, redirect, url_for, flash, session, current_app
from sqlalchemy.exc import SQLAlchemyError
# current app
from Auth.model import User
from Config import Setting

# app
from .extensions import db

blp = Blueprint('middlewares', __name__)



@blp.before_app_request
def set_user_statue():
    """
    Set useful attributes on request before processing the view.

    Attributes:
        request.user_object (User): The User object from the database if authenticated.
        request.current_language (str): The user's current language.
        request.is_authenticated (bool): Whether the user is authenticated.


    """
    if any(ext in request.path for ext in ('.js', '.css', '.mp4', '.png', '.jpg', '.jpeg', '.gif')):

        request.remote_addr = request.headers.get('X-Real-Ip', request.remote_addr)
        request.is_authenticated = session.get("login", False)
        try:
            request.user_object = db.session.execute(
                db.select(User).filter_by(id=session.get("account-id", None))).scalar_one_or_none()
        except SQLAlchemyError as e:
            request.user_object = None


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