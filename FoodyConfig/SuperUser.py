from FoodyAdmin.model import Admin
from FoodyCore.extension import db
from email_validator import validate_email
from email_validator.syntax import EmailSyntaxError


def create_super_user(username: str, password: str, email: str, phonenumber: str):
    """Create a new Super User"""

    if check_super_user(username):
        print("[EXISTS] Super User exists in db ...")
        return True

    try:
        validate_email(email)
    except Exception as e:
        raise EmailSyntaxError("Admin Email is not a valid email address or Not Provided ...")

    admin = Admin()
    admin.SetPublicKey()
    admin.SetPassword(password)

    if not admin.SetUsername(username):
        return ValueError(f"An Admin With {username} username exists in db")

    admin.SetEmail(email)
    if not admin.SetPhone(phonenumber):
        return ValueError(f"An Admin With {phonenumber} phoneNumber exists in db")

    admin.Active = True

    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        print(e)
        print("[NOT CREATED] super User Cannot Created")
        return False
    else:
        print("[CREATED] super User Created Successfully")
        return True


def check_super_user(username: str):
    """Check Do Any Super User are in the database with provided username"""
    return True if Admin.query.filter_by(Username=username).first() else False


def check_have_any_super_user():
    """Check Does any superuser exists in database """
    return True if Admin.query.first() else False
