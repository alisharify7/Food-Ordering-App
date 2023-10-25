from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length
from FoodyCore.utils import TimeStamp


class SendSingleSMS(FlaskForm):
    """Send Single SmS to SomeOne"""
    targetMobile = StringField(
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=11, max=11)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "شماره تلفن گیرنده"
        }
    )
    Text = TextAreaField(
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=1, max=128)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "متن پیام",
            "rows": "16"
        }
    )

    Submit = SubmitField(
        render_kw={
            "class": "form-control btn btn-success",
            "placeholder": "ثبت",
            "value": "ارسال"
        }
    )


class ReportSMSPeriodTime(FlaskForm):
    """
    this form uses for report between to dates in sms panel api
    """
    FromDate = StringField(
        validators=[
            DataRequired(),
            InputRequired(),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "تاریخ به صورت  YYYY/MM/DDوارد شود"
        }
    )
    EndDate = StringField(
        validators=[
            DataRequired(),
            InputRequired(),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "تاریخ به صورت  YYYY/MM/DDوارد شود"
        }
    )

    Submit = SubmitField(
        render_kw={
            "class": "form-control btn btn-success",
            "placeholder": "جستجو",
            "value": "جستجو"
        }
    )

    def validate_dates(self):
        """
        Validate Both Start And End Date for Persian Date
        """
        date1 = self.FromDate.data
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
        date1 = self.FromDate.data
        date2 = self.EndDate.data

        t = TimeStamp()

        return [t.convert_string_jalali2_dateD(date1), t.convert_string_jalali2_dateD(date2)]


class SendToAllSMS(FlaskForm):
    """
    Send to All SMS
    """
    sections = SelectField(
        choices=[],
        validators=[
            DataRequired(),
            InputRequired(),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "شماره تلفن گیرنده"
        }
    )

    Text = TextAreaField(
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=1, max=128)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "متن پیام",
            "rows": "16"
        }
    )
    Submit = SubmitField(
        render_kw={
            "class": "form-control btn btn-success",
            "placeholder": "ثبت",
            "value": "ارسال"
        }
    )
