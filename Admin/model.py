import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so

from werkzeug.security import generate_password_hash, check_password_hash
from Core.model import BaseModel

class AdminRole(BaseModel):
    __tablename__ = BaseModel.SetTableName("admin_roles")

    name: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False, unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(512), nullable=False, unique=False)

    admins_list = so.relationship("Admin", backref="roles_list", lazy="dynamic")


class Admin(BaseModel):
    __tablename__ = BaseModel.SetTableName("admins")

    USERNAME_LENGTH = 256
    EMAIL_ADDRESS_LENGTH = 320
    PHONE_NUMBER_LENGTH = 11

    username: so.Mapped[str] = so.mapped_column(sa.String(USERNAME_LENGTH), unique=True, nullable=False)
    password: so.Mapped[str] = so.mapped_column(sa.String(162), unique=True, nullable=False)
    role_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(AdminRole.id, ondelete="SET NULL"))
    phone_number: so.Mapped[str] = so.mapped_column(sa.String(PHONE_NUMBER_LENGTH), unique=True, nullable=False)
    email_address: so.Mapped[str] = so.mapped_column(sa.String(EMAIL_ADDRESS_LENGTH), unique=True, nullable=False)
    status: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, nullable=False, unique=False)
    max_try_number: so.Mapped[int] = so.mapped_column(sa.Integer, default=10, unique=False, nullable=False)
    try_number: so.Mapped[int] = so.mapped_column(sa.Integer, default=0, unique=False, nullable=False)

    last_login_time: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow)

    @so.validates("username")
    def validate_username(self, key: str, value: str):
        if len(value) > self.USERNAME_LENGTH:
            raise ValueError("username is to long, valid length is %d" % self.USERNAME_LENGTH)
        return value

    def set_username(self, username:str) -> bool:
        """ Set Unique Username for admin """

        if self.query.filter_by(username=username).first():
            return False
        else:
            try: # check validator well
                self.username = username
            except Exception as e:
                return False

            return True


    def set_password(self, password:str) -> None:
        """Set Hash Password For admin"""
        self.password = generate_password_hash(password)


    def check_password(self, password:str) -> None:
        """Check Password with Hashed Password in db"""
        return check_password_hash(self.Password, password)


    @so.validates("email_address")
    def validate_email_address(self, key: str, value: str):
        if len(value) > self.EMAIL_LENGTH:
            raise ValueError("email address is to long, valid length is %d" % self.EMAIL_LENGTH)
        return value

    def set_email_address(self, email:str) -> None:
        """Set Unique Email for admin"""
        if self.query.filter_by(email_address=email).first():
            return False
        else:
            try: # check validator well
                self.email_address = email
            except Exception as e:
                return False

            return True


    @so.validates("phone_number")
    def validate_phone_number(self, key: str, value: str):
        if len(value) > self.PHONE_NUMBER_LENGTH:
            raise ValueError("phone number is to long, valid length is %d" % self.PHONE_NUMBER_LENGTH)
        return value

    def set_phone_number(self, phone:str) -> None:
        """ Set Unique Phone For admin  """
        if self.query.filter_by(phone_number=phone).first():
            return False
        else:
            try:
                self.phone_number = phone
            except Exception as e:
                return False
            return True

    def has_login_access(self) -> bool:
        """check user can logged in or not"""
        return self.try_number < self.max_try_number

    def set_last_login(self):
        self.last_login_time = datetime.datetime.utcnow()

    logs = so.relationship("AdminLog", backref='admin', lazy='dynamic')


class AdminLog(BaseModel):
    __tablename__ = BaseModel.SetTableName("admins_log")

    ip_address: so.Mapped[str] = so.mapped_column(sa.String(15), nullable=False, unique=False)
    action: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False, unique=False)
    admin_id: so.Mapped[int] = so.mapped_column(sa.INTEGER, sa.ForeignKey(Admin.id, ondelete="SET NULL"), nullable=False, unique=False)


