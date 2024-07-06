# flask extensions

from flask_babel import Babel
from flask_mail import Mail
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sms_ir import SmsIr
from Config import Setting


login_manager = LoginManager()
SmsServer = SmsIr(api_key=Setting.SMS_API_KEY, linenumber=Setting.SMS_LINE_NUMBER)
RedisServer = Setting.REDIS_DEFAULT_INTERFACE
db = SQLAlchemy()
babel = Babel()
csrf = CSRFProtect()
ServerSession = Session()
ServerMigrate = Migrate()
ServerMail = Mail()