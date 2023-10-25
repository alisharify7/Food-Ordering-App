
from FoodyCore.model import BaseModel
from sqlalchemy import String, Boolean, Column, ForeignKey, Integer
from werkzeug.security import generate_password_hash, check_password_hash
from FoodyCore.extension import db


class User(BaseModel):
    """
        User Table in db
    """

    __tablename__ = BaseModel.SetTableName("users")

    Username = Column(String(64), nullable=False, unique=True)
    Password = Column(String(102), nullable=False, unique=False)

    FirstName = Column(String(256), nullable=False, unique=False)
    LastName = Column(String(265), nullable=False, unique=False)

    NationalCode = Column(String(11), nullable=False, unique=True)
    PhoneNumber = Column(String(11), nullable=False, unique=True)
    SectionID = Column(Integer, ForeignKey(BaseModel.SetTableName("sections") + ".id"), nullable=False, unique=False)
    Active = Column(Boolean, default=False)
    EmployeeCode = Column(String(64), nullable=False, unique=True)
    Email = Column(String(255), nullable=True, unique=False)

    Orders = db.relationship("Order", cascade="all,delete", backref="GetUser")

    def GetUserName(self) -> str:
        return f"{self.FirstName} {self.LastName}"

    def SetPassword(self, password: str) -> None:
        """ Set Hashed Password for user """
        self.Password = generate_password_hash(password)

    def CheckPassword(self, password: str) -> bool:
        """ Check Password with Hashed password """
        return check_password_hash(self.Password, password)

    def Is_Active(self) -> bool:
        """ check account is active """
        return self.Active

    def SetActive(self) -> None:
        """Change user status  to active"""
        self.Active = True

    def SetUsername(self, username: str) -> bool:
        """Set Unique Username For user"""
        if self.query.filter_by(Username=username).first():
            return False
        else:
            self.Username = username
            return True

    def SetNationalCode(self, nationalcode: str) -> bool:
        """Set Unique National code For USer"""
        if self.query.filter_by(NationalCode=nationalcode).first():
            return False
        else:
            self.NationalCode = nationalcode
            return True

    def SetPhoneNumber(self, phone: str) -> bool:
        """Set Unique Phone Number For USer"""
        if self.query.filter_by(PhoneNumber=phone).first():
            return False
        else:
            self.PhoneNumber = phone
            return True

    def SetEmploeeCode(self, code: str) -> bool:
        """Set Unique Employee Code For User"""
        if self.query.filter_by(EmployeeCode=code).first():
            return False
        else:
            self.EmployeeCode = code
            return True

    def SetEmailAddress(self, email: str) -> bool:
        """Set Email Address For User"""
        # if self.query.filter_by(Email=email).first():
        #     return False
        # else:
        #     self.Email = email
        #     return True
        self.Email = email
        return True


class Section(BaseModel):
    """This table Hold Sections"""
    __tablename__ = BaseModel.SetTableName("sections")

    Name = Column(String(64), nullable=False, unique=True)
    Description = Column(String(512), nullable=False, unique=False)

    users = db.relationship("User", backref='GetSection')
