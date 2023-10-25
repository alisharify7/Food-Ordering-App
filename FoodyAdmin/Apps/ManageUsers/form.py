from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, RadioField
from wtforms.validators import Length, DataRequired, InputRequired
from FoodyAuth.utils import get_all_section_wtf_select


class AddNewUserForm(FlaskForm):
    """
    Base Class For Adding new user to web app
    This form uses for adding new user or edit a user as well
    """

    def PopPasswordValidator(self):
        self.Password.validators = []

    FirstName = StringField(
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
            Length(min=1, max=256, message="حداقل و حداکثر طول ورودی این فیلد  1 و 265 کاراکتر است"),
        ],
    )

    LastName = StringField(
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
            Length(min=1, max=256, message="حداقل و حداکثر طول ورودی این فیلد  1 و 265 کاراکتر است"),
        ],
    )

    Username = StringField(
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
            Length(min=1, max=64, message="حداقل و حداکثر طول ورودی این فیلد  1 و 64 کاراکتر است"),
        ],
    )

    Password = StringField(
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
            Length(min=1, max=102, message="حداقل و حداکثر طول ورودی این فیلد 1 و 102 کاراکتر است"),
        ]
    )

    NationalCode = StringField(
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
            Length(min=10, max=10, message="حداقل و حداکثر طول ورودی این فیلد 10 و 10 کاراکتر است"),
        ]
    )

    PhoneNumber = StringField(
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
            Length(min=11, max=11, message="حداقل و حداکثر طول ورودی این فیلد 11 و 11 کاراکتر است"),
        ]
    )

    SectionID = SelectField(
        choices=get_all_section_wtf_select,
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
        ]
    )

    Active = RadioField(
        choices=[("inactive", "غیرفعال"), ("active", "فعال")],
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
        ]
    )

    EmployeeCode = StringField(
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
            Length(min=1, max=64, message="حداقل و حداکثر طول ورودی این فیلد 1 و 64 کاراکتر است"),
        ]
    )

    Email = StringField(
        validators=[
        ]
    )

    Submit = SubmitField()


class SearchInUsers(FlaskForm):
    """Use This Form For Searching in Users"""
    SearchOption = SelectField(
        choices=[
            ('NationalCode', 'کد ملی'),
            ('PhoneNumber', 'شماره تماس'),
            ('EmployeeCode', 'کد کارمندی'),
        ],
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
        ]
    )

    SearchBox = StringField(
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
        ]
    )

    submit = SubmitField()
