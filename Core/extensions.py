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
ApiManager = Api(title='Food-web-app-api', description='Foody_web_app api docs', version='1.0.0', doc='/doc/')
FlaskLoginManager = LoginManager()
RedisServer = Setting.REDIS_DEFAULT_INTERFACE
ServerMail = Mail()
ServerSession = Session()
ServerMigrate = Migrate()
Debugger = DebugToolbarExtension()
SmsServer = SmsIr(
    api_key=Setting.SMS_API_KEY,
    linenumber=Setting.SMS_LINE_NUMBER
)
