from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired
from FoodyCore.utils import TimeStamp


class TimeStartEndUtils:
    def validate_dates(self):
        """
        Validate Both Start And End Date for Persian Date
        """
        date1 = self.StartDate.data
        date2 = self.EndDate.data

        t = TimeStamp()

        if not t.is_persian_date(date1):
            return False
        if not t.is_persian_date(date2):
            return False

        return True

    def GetGeorgianDates(self):
        """
            This Method convert Both Start and End Dates to Georgian Date
            remember don't call this method Before self.validate_dates Method
            first call self.validate_dates and then for getting Clean Dates call this method
        """
        date1 = self.StartDate.data
        date2 = self.EndDate.data

        t = TimeStamp()

        return [t.convert_string_jalali2_dateD(date1), t.convert_string_jalali2_dateD(date2)]


class SearchBySectionsForm(FlaskForm, TimeStartEndUtils):
    """ Base Flask Form For Searching in Sections """

    Sections = SelectField(
        choices=[],
        validators=[
            DataRequired(),
            InputRequired()
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "بخش مورد نظر"
        }
    )
    date_filed_placeholder_info = """| تاریخ به صورت YYYY/MM/DD وارد شود"""

    StartDate = StringField(
        validators=[
            DataRequired(),
            InputRequired()
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "تاریخ شروع " + date_filed_placeholder_info
        }
    )

    EndDate = StringField(
        validators=[
            DataRequired(),
            InputRequired()
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "تاریخ پایان " + date_filed_placeholder_info
        }
    )

    Submit = SubmitField(
        render_kw={
            "class": "btn btn-success w-100 my-3",
            "value": "جستجو"
        }
    )


class ReportUserForm(FlaskForm, TimeStartEndUtils):
    """
        this form uses for Report Each User order
    """

    EmployeeCode = StringField(
        validators=[
            DataRequired(),
            InputRequired()
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "کد کارمندی"
        }
    )
    date_filed_placeholder_info = """| تاریخ به صورت YYYY/MM/DD وارد شود"""

    StartDate = StringField(
        validators=[
            DataRequired(),
            InputRequired()
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "تاریخ شروع " + date_filed_placeholder_info
        }
    )

    EndDate = StringField(
        validators=[
            DataRequired(),
            InputRequired()
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "تاریخ پایان " + date_filed_placeholder_info
        }
    )

    Submit = SubmitField(
        render_kw={
            "class": "btn btn-success w-100 my-3",
            "value": "جستجو"
        }
    )
