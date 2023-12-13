# register all extensions


from redis import Redis
from flask_migrate import Migrate
from flask_session import Session
from flask_captcha2 import FlaskCaptcha2
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from FoodyConfig.config import REDIS_URI
from flask_mail import Mail
from sms_ir import SmsIr
from FoodyConfig.config import SMS_API, SMS_LINE



smsIR = SmsIr(
    api_key=SMS_API,
    linenumber=SMS_LINE,
)

db = SQLAlchemy()
ServerRedis = Redis().from_url(REDIS_URI)
ServerSession = Session()
ServerMigrate = Migrate()
ServerCsrf = CSRFProtect()
ServerCaptchaV2 = FlaskCaptcha2()
MailServer = Mail()
