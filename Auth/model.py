# build in
import datetime

# lib
import sqlalchemy as sa
import sqlalchemy.orm as so

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# application
from Core.model import BaseModel


class WorkSection(BaseModel):
    __tablename__ = BaseModel.SetTableName("work_section")

    name: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False, unique=False)
    description: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True, unique=False)

    # default work station for site admin is admin_website



class UserRole(BaseModel):
    __tablename__ = BaseModel.SetTableName("user_roles")
    USER = 1
    ADMIN = 2
    ROLES_CHOICES = (
        (USER, "USER"),
        (ADMIN, "ADMIN"),
    )

    name: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False, unique=True)

    @classmethod
    def init_roles(cls):
        db = current_app.extensions['sqlalchemy']
        for role_id, role_name in cls.ROLES_CHOICES:
            query = db.session.select(UserRole).filter_by(id=role_id)
            if not (db.session.execute(query).scalar_one_or_none()):
                t = cls(name=role_name, id=role_id)
                t.set_public_key()
                db.session.add(t)

        db.session.commit()

    def __str__(self):
        return f"<UserRole {self.id} - {self.name}>"



User2Role = sa.Table(
        BaseModel.SetTableName("users_2_roles"),
        BaseModel.metadata,
  sa.Column("role_id", sa.Integer, sa.ForeignKey(BaseModel.SetTableName("user_roles")+".id", ondelete="CASCADE"), unique=False, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey(BaseModel.SetTableName("users")+".id", ondelete="CASCADE"), unique=False, nullable=False),
)


class User(BaseModel, UserMixin):
    __tablename__ = BaseModel.SetTableName("users")
    USERNAME_LENGTH = 256
    PHONE_NUMBER_LENGTH = 11
    EMAIL_LENGTH = 320

    username: so.Mapped[str] = so.mapped_column(sa.String(USERNAME_LENGTH), unique=True, nullable=False)
    password: so.Mapped[str] = so.mapped_column(sa.String(162), unique=True, nullable=False)

    first_name: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True, unique=False)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True, unique=False)
    phone_number: so.Mapped[str] = so.mapped_column(sa.String(11), unique=True, nullable=True)

    national_code: so.Mapped[str] = so.mapped_column(sa.String(PHONE_NUMBER_LENGTH), unique=True, nullable=True)
    employee_code: so.Mapped[int] = so.mapped_column(sa.INTEGER, unique=True, nullable=False)

    status: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, nullable=False, unique=False)
    email_address: so.Mapped[str] = so.mapped_column(sa.String(EMAIL_LENGTH), nullable=True, unique=False)
    max_try_number: so.Mapped[int] = so.mapped_column(sa.Integer, default=10, unique=False, nullable=False)
    try_number: so.Mapped[int] = so.mapped_column(sa.Integer, default=0, unique=False, nullable=False)
    roles = so.relationship(UserRole, secondary=User2Role, backref="users")

    last_login_time: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, onupdate=datetime.datetime.utcnow,
                                                               default=datetime.datetime.utcnow)
    work_section_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(WorkSection.id, ondelete='SET NULL'),
                                                       nullable=False, unique=False)

    logs = so.relationship("UserLog", backref='user', lazy='dynamic')


    def to_dict(self):
        return {
            "username": self.username,
            "FirstName": self.first_name or "NULL",
            "LastName": self.last_name or "NULL",
            "Email": self.email_address,
            "Status": "Active" if self.status else "inactive",
            "CreatedTime": self.created_time
        }

    def full_name(self):
        """concat first name and last name"""
        return f"{self.first_name} {self.last_name}"


    def set_username(self, username: str) -> bool:
        """ Set Unique Username for admin """

        if self.query.filter_by(username=username).first():
            return False
        else:
            try: # check validator well
                self.username = username
            except Exception as e:
                return False

            return True
    def set_password(self, password: str) -> None:
        """Set Hash Password For admin"""
        self.password = generate_password_hash(password)


    def check_password(self, password: str) -> None:
        """Check Password with Hashed Password in db"""
        return check_password_hash(self.password, password)


    def set_email_address(self, email: str) -> None:
        """Set Unique Email for admin"""
        if self.query.filter_by(email_address=email).first():
            return False
        else:
            try: # check validator well
                self.email_address = email
            except Exception as e:
                return False

            return True

    def set_phone_number(self, phone: str) -> None:
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

    def __str__(self):
        return f"<User {self.id}-{self.username}-{self.full_name()}>"




class UserLog(BaseModel):
    __tablename__ = BaseModel.SetTableName("users_log")

    ip_address: so.Mapped[str] = so.mapped_column(sa.String(15), nullable=False, unique=False)
    action: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False, unique=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.INTEGER, sa.ForeignKey(User.id, ondelete="SET NULL"), nullable=False, unique=False)


