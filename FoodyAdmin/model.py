import datetime
from sqlalchemy.orm import relationship
from FoodyCore.model import BaseModel
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(BaseModel):
    """
        Base Model For Admin Table
    """
    __tablename__ = BaseModel.SetTableName("admins")

    Username = Column(String(64), nullable=False, unique=True)
    Password = Column(String(102), nullable=False, unique=True)

    PhoneNumber = Column(String(11), nullable=False, unique=True)
    TryNumber = Column(Integer, default=0, nullable=False, unique=False)
    Active = Column(Boolean, default=False, nullable=False, unique=False)
    Email = Column(String(256), nullable=False, unique=True)


    def SetLoginLog(self, message:str, ip:str) -> bool:
        """
        This Method register a log for admin in log table
        """
        from FoodyCore.extensions import db

        a = AdminLog()
        a.AdminID = self.id
        a.SetPublicKey()
        a.Action = message
        a.IpAddress = ip

        try:
            db.session.add(a)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
        else:
            return True


    def SetAdminLogin(self, message:str, ip:str) -> None:
        """Set Admin Last Login date in db and set a log to"""
        self.LastLogin = datetime.datetime.now()
        self.SetLoginLog(message, ip)


    def Is_TryNumber_Check(self):
        """ Check Admin Pass Try Number """
        return self.TryNumber >= 5


    def Is_Active(self):
        """  Check Account is active or not """
        return self.Active


    def SetUsername(self, username:str) -> bool:
        """ Set Unique Username for admin """
        if self.query.filter_by(Username=username).first():
            return False
        else:
            self.Username = username
            return True


    def SetPassword(self, password:str) -> None:
        """Set Hash Password For admin"""
        self.Password = generate_password_hash(password, method="pbkdf2")


    def CheckPassword(self, password:str) -> None:
        """Check Password with Hashed Password in db"""
        return check_password_hash(self.Password, password)


    def SetLastLogin(self):
        self.LastLoginDate = datetime.datetime.now()


    def ResetTryNUmber(self):
        self.TryNumber = 0

    def SetEmail(self, email:str) -> None:
        """Set Unique Email for admin"""
        if self.query.filter_by(Email=email).first():
            return False
        else:
            self.Email = email
            return True


    def SetPhone(self, phone:str) -> None:
        """ Set Unique Phone For admin  """
        if self.query.filter_by(PhoneNumber=phone).first():
            return False
        else:
            self.PhoneNumber = phone
            return True

    LastLoginDate = Column(DateTime, default=None, nullable=True, unique=False)
    Logs = relationship('AdminLog', backref='GetAdmin')


class AdminLog(BaseModel):
    """Admin Log Table"""
    __tablename__ = BaseModel.SetTableName("log_admins")

    AdminID = Column(Integer, ForeignKey(BaseModel.SetTableName("admins")+".id"))
    Action = Column(String(512), nullable=False, unique=False)
    IpAddress = Column(String(15), nullable=True, unique=False, default="0.0.0.0")



class SiteSetting(BaseModel):
    """
        All Site Setting info
    """
    __tablename__ = BaseModel.SetTableName("settings")
    Name = Column(String(255), unique=True)
    Description = Column(String(512), unique=True)
    Logo = Column(String(512), unique=True)
    Address = Column(String(512), unique=True)
    Phone = Column(String(512), unique=True)
    tag = Column(String(64), default="setting", unique=True, nullable=False)



