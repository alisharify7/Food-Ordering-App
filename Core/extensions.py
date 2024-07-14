# flask extensions

from flask_babel import Babel
from flask_mail import Mail
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sms_ir import SmsIr
from Config import Setting


login_manager = LoginManager()
RedisServer = Setting.REDIS_DEFAULT_INTERFACE
babel = Babel()
db = SQLAlchemy()
ServerMail = Mail()
csrf = CSRFProtect()
ServerSession = Session()
ServerMigrate = Migrate()
debugger = DebugToolbarExtension()
SmsServer = SmsIr(
    api_key=Setting.SMS_API_KEY,
    linenumber=Setting.SMS_LINE_NUMBER
)
