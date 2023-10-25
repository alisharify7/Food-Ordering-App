# cli commands

import datetime
import getpass
import sys
from faker import Faker

import sqlalchemy
from flask.cli import AppGroup
from FoodyConfig.SuperUser import create_super_user
from email_validator import validate_email



create_commands = AppGroup("create", help="creation operation commands.")




@create_commands.command("superuser")
def createsuperuser():
    """
    use this command to create a superuser in app

        @params:
            username: str
            password: str
            password confirm: str
            email: str
            phone: str
    """
    def get_input(message):
        while True:
            x = input(message)
            if not x:
                print("invalid Input :(")
                continue
            else:
                if x.isidentifier():
                    return x
                else:
                    print("invalid Input :(")
                    continue


    def get_email(message):
        while True:
            x = input(message)
            try:
                validate_email(x)
            except Exception as e:
                print("Invalid email address")
            else:
                return x


    username = get_input("Enter Admin Username: ")
    password = getpass.getpass("Enter Admin Password: ")
    password_confirm = getpass.getpass("Enter Admin Password again: ")
    email = get_email("Enter admin Email Address: ")
    phonenumber = input('Enter Admin Phone Number: ')

    if not password or not password_confirm:
        raise ValueError("invalid data for passwords!")

    if password != password_confirm:
        raise ValueError("Passwords are not matched !")

    create_super_user(
        username=username,
        password=password,
        phonenumber=phonenumber,
        email=email
    )


@create_commands.command("init_setting")
def init_setting():
    """
        initialize days and sections in to database

        @params:
            None

    """
    from FoodyCore.extension import db
    from FoodyAuth.model import Section
    from FoodyConfig.StaticConfig.Sections import SECTIONS
    from FoodyConfig.config import ALL_DAYS
    from FoodyOrder.model import Day
    from sqlalchemy.exc import ProgrammingError

    # add section
    for each in SECTIONS:
        s = Section()
        try:
            s.SetPublicKey()
        except sqlalchemy.exc.ProgrammingError as e:
            print(e)
            sys.exit()

        s.Name = each["name"]
        s.Description = each["description"]
        try:
            db.session.add(s)
            db.session.commit()
        except sqlalchemy.exc.ProgrammingError as e:
            print(e)
            sys.exit()
        except Exception as e:
            db.session.rollback()
            print(f"[{datetime.datetime.utcnow()}] section {s.id} not added")
        else:
            print(f"[{datetime.datetime.utcnow()}] section {s.id} added")

    for each in ALL_DAYS:
        d = Day()
        try:
            d.SetPublicKey()
        except sqlalchemy.exc.ProgrammingError as e:
            # print(e)
            sys.exit()
        d.NameFa = each[0]
        d.NameEn = each[1]
        try:
            db.session.add(d)
            db.session.commit()
        except sqlalchemy.exc.ProgrammingError as e:
            print(e)
            sys.exit()
        except Exception as e:
            db.session.rollback()
            print(f"[{datetime.datetime.utcnow()}] day {d.NameEn} not added")
        else:
            print(f"[{datetime.datetime.utcnow()}] day {d.NameEn} added")



@create_commands.command("fakeuser")
def create_fake_user():
    """
        create fake users in db
        @params
            None

    """
    fakerManger = Faker(locale=["fa_IR"])
    import random
    from FoodyCore.extension import db
    from FoodyAuth.model import Section, User


    def get_number():
        """

        """
        while True:
            """
            return fake number
            """
            number = fakerManger.phone_number().replace(" ", "")
            if len(number) == 11:
                return number
            continue


    while True:
        x = input("This Command Create Fake Users in App. Are You Sure? [Y, N]: ").lower().strip()
        if x not in ["y", "n"]:
            continue
        else:
            if x == "y":
                break
            elif x == "n":
                sys.exit("Operation Aborted!")
            else:
                continue


    while True:
        x = input("Enter Number of users: ")
        if x.isdigit():
            x = int(x)
            break
        else:
            continue

    counter = 0
    try:
        sections = [each[0] for each in db.session.query(Section.id,).distinct().all()]
        if not sections:
            raise ValueError("sections are not included in database. use command flask create init_setting for adding setting into database ")
    except sqlalchemy.exc.ProgrammingError as e:
        print(e)
        sys.exit()

    while counter < x:
        user = User()
        user.SetPublicKey()
        user.SectionID = random.choice(sections)
        user.Active = 1 == random.randint(1, 2)
        user.SetUsername(f"{fakerManger.user_name()}")
        user.SetPassword(str(counter))
        user.NationalCode = random.randint(999_999_999, 999_999_999_9)
        user.PhoneNumber = get_number()
        user.EmployeeCode = random.randint(1, 9999)
        user.FirstName = f"{fakerManger.first_name()}"
        user.LastName = f"{fakerManger.last_name()}"
        user.SetEmailAddress(fakerManger.email())
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            # print(e)
            db.session.rollback()
        else:
            counter += 1
            print(f"[{datetime.datetime.utcnow()}][{counter}] user created")
