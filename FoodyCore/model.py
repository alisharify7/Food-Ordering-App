import datetime
import uuid
from FoodyCore.extension import db
from sqlalchemy import String, DateTime, Integer, Column
from FoodyConfig.config import DATABASE_TABLE_PREFIX


class BaseModel(db.Model):
    """Base model class for all apps"""
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    @staticmethod
    def SetTableName(name):
        """Use This Method For setting a table name"""
        name = name.replace("-", "_")
        return f"{DATABASE_TABLE_PREFIX}{name}"

    def SetPublicKey(self):
        """This Method Set a Unique PublicKey For user """
        while True:
            token = str(uuid.uuid4())
            if self.query.filter(self.PublicKey == token).first():
                continue
            else:
                self.PublicKey = token
                break

    def GetPublicKey(self):
        return self.PublicKey

    PublicKey = Column(String(36), nullable=False, unique=True)
    CreatedTime = Column(DateTime, default=datetime.datetime.now)
    LastUpdateTime = Column(DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now)
