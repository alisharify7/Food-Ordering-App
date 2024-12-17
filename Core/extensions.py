# flask extensions
from flask_babel import Babel
from flask_mail import Mail
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_restx import Api
from sms_ir import SmsIr
from Config import Setting


db = SQLAlchemy()
csrf = CSRFProtect()
babel = Babel()

api_manager = Api(
    title="Food-web-app-api",
    description="Foody_web_app api docs",
    version="1.0.0",
    doc="/docs/",
    terms_url="/terms/",
    contact="example@yahoo.com",
    license="all rights reserved for github.com/alisharify7 OSS",
)
flask_login_manager = LoginManager()
redis_server = Setting.REDIS_DEFAULT_INTERFACE
server_mail = Mail()
server_session = Session()
server_migrate = Migrate()
flask_debugger_tool_bar = DebugToolbarExtension()
sms_server = SmsIr(api_key=Setting.SMS_API_KEY, linenumber=Setting.SMS_LINE_NUMBER)
