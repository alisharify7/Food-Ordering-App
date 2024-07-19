"""
 * main base abstract model for all other models
 * author: @alisharify7
 * Copyleft 2023-2024. under GPL-3.0 license
 * https://github.com/alisharify7/Food-Ordering-App
"""

import uuid
import datetime
from typing import Optional

import khayyam
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import current_app

from Config import Setting
from .utils import TimeStamp
from .extensions import db


class BaseModel(db.Model):
    """
    Base model class for all models
     ~~~~~~~~~~~~~~ abstract model ~~~~~~~~~~~~~~~

    """
    T = TimeStamp()

    __abstract__ = True
    # __table_args__ = {
    #     # 'mysql_engine': 'InnoDB',
    #     # 'mysql_charset': 'utf8',
    #     # 'mysql_collate': 'utf8_persian_ci'
    # }

    id: so.Mapped[int] = so.mapped_column(sa.INTEGER, primary_key=True)

    @staticmethod
    def SetTableName(name):
        """Use This Method For setting a table name"""
        name = name.replace("-", "_").replace(" ", "")
        return f"{Setting.DATABASE_TABLE_PREFIX_NAME}{name}".lower()

    def set_public_key(self):
        """ This Method Set a Unique PublicKey """
        while True:
            token = uuid.uuid4().hex
            if self.query.filter_by(public_key=token).first():
                continue
            else:
                self.public_key = token
                break

    def save(self, show_traceback: bool = True):
        """
         combination of two steps, add and commit session
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            if show_traceback:
                current_app.logger.exception(exc_info=e, msg=e)
            return False
        else:
            return True

    public_key: so.Mapped[str] = so.mapped_column(
        sa.String(36), nullable=False, unique=True, index=True)  # unique key for each element <usually used in frontend>
    created_time: so.Mapped[Optional[datetime.datetime]] = so.mapped_column(sa.DateTime,
                                                                            default=datetime.datetime.now)
    modified_time: so.Mapped[Optional[datetime.datetime]] = so.mapped_column(sa.DateTime,
                                                                             onupdate=datetime.datetime.now,
                                                                             default=datetime.datetime.now)

    @staticmethod
    def shamsi(obj):
        if isinstance(obj, datetime.datetime):
            c = khayyam.JalaliDatetime(obj)
            return f"{str(c.date())} {c.time()}"
        return obj


# class SettingAttributeType(enum.Enum):
#     json = 1
#     string = 2
#     integer = 3
#     float = 4
#
#
# class SettingAttribute(BaseModel):
#     __tablename__ = BaseModel.SetTableName("setting_attribute")
#
#     name: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False, unique=True)
#     value = so.relationship("SettingAttributeValue", backref="setting_attribute", lazy="dynamic")
#
#
# class SettingAttributesValue(BaseModel):
#     __tablename__ = BaseModel.SetTableName("setting_attribute_value")
#
#     value: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False, unique=False)
#     setting_attribute_id: so.Mapped[int] = so.mapped_column(sa.INTEGER, sa.ForeignKey(SettingAttribute.id, ondelete='SET NULL'), nullable=True, unique=True) # one to one
