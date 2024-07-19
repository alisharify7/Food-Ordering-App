"""
 * flask app factory function init flask app creation
 * author: @alisharify7
 * Copyleft 2023-2024. under GPL-3.0 license
 * https://github.com/alisharify7/Food-Ordering-App
"""

from flask import Flask, Blueprint
from flask_captcha2 import FlaskCaptcha
from werkzeug.middleware.proxy_fix import ProxyFix

from Config import Setting
from Auth.utils import load_user
from Core.urls import urlpatterns as ssr_urlpatterns
from Core.api_urls import urlpatterns as api_urlpatterns
from Core.extensions import (db, ServerSession, ServerMigrate, ServerMail,
                         csrf, SmsServer, FlaskLoginManager, Debugger, ApiManager)



def create_app(setting: Setting) -> Flask:
    """
        Factory Function For creating FlaskApp
    """
    app = Flask(
        __name__,
        template_folder="templates",
    )

    app.config.from_object(setting)

    # register extensions
    db.init_app(app=app)  # db
    csrf.init_app(app=app)  # csrf token
    ServerMail.init_app(app=app)  # mail
    ServerMigrate.init_app(db=db, app=app)  # migrate
    # celery = celery_init_app(app=app)  # celery
    ServerSession.init_app(app=app)  # session
    FlaskLoginManager.init_app(app=app)  # flask-login
    Debugger.init_app(app)  # flask_debugger tol
    app.extensions['sms'] = SmsServer

    apiBluePrint = Blueprint('api-blueprint', __name__)
    ApiManager.init_app(apiBluePrint)
    csrf.exempt(apiBluePrint)
    app.register_blueprint(apiBluePrint, url_prefix='')


    FlaskLoginManager.user_loader(load_user)
    FlaskLoginManager.login_message = "برای دسترسی به بخش مورد نظر  \
        ورود به حساب کاربری الزامی می باشد"
    FlaskLoginManager.login_message_category = "error"
    FlaskLoginManager.login_view = "auth.login_get"


    # captcha config
    ServerCaptchaMaster = FlaskCaptcha(app=app)
    ServerCaptcha2 = ServerCaptchaMaster.getGoogleCaptcha2(
        name='captcha2',
        conf=Setting.GOOGLE_CAPTCHA_V2_CONF)
    ServerCaptcha3 = ServerCaptchaMaster.getGoogleCaptcha3(
        name='captcha3',
        conf=Setting.GOOGLE_CAPTCHA_V3_CONF)
    app.extensions['master-captcha'] = ServerCaptchaMaster
    app.extensions['captcha2'] = ServerCaptcha2
    app.extensions['captcha3'] = ServerCaptcha3

    # Register apps:
    for each in ssr_urlpatterns:
        app.register_blueprint(each['obj'], url_prefix=each['prefix'])

    # Register apis:
    for each in api_urlpatterns:
        ApiManager.add_namespace(each['obj'], path=each['prefix'])

    # template filters and contexts
    from .template_filter import contexts, templatesFilters
    app.context_processor(contexts)

    for each in templatesFilters:
        app.add_template_filter(templatesFilters[each], name=each)

    app.wsgi_app = ProxyFix(  # tell flask in behind a reverse proxy
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    return app


app = create_app(Setting)

import Core.baseView
