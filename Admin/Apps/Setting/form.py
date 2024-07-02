from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField, EmailField, FileField, TextAreaField
from wtforms.validators import Length, DataRequired, InputRequired, Email


class AddNewAdminForm(FlaskForm):
    """
        use this form for adding new admin to app
        also for editing admins as well
    """

    def PopPasswordValidator(self):
        self.Password.validators = []

    Username = StringField(
        validators=[
            DataRequired(message="ورود داده در این فیلد الرامی است"),
            InputRequired(message="ورود داده در این فیلد الرامی است"),
            Length(min=3, max=64, message="حداقل و حداکثر طول این فیلد 3 - 64 کاراکتر است")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "نام کاربری"
        }
    )

    Password = StringField(
        validators=[
            DataRequired(message="ورود داده در این فیلد الرامی است"),
            InputRequired(message="ورود داده در این فیلد الرامی است"),
            Length(min=5, max=256, message="حداقل و حداکثر طول این فیلد 5 - 256 کاراکتر است")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "گدرواژه حساب کاربری"
        }
    )

    PhoneNumber = StringField(
        validators=[
            DataRequired(message="ورود داده در این فیلد الرامی است"),
            InputRequired(message="ورود داده در این فیلد الرامی است"),
            Length(min=11, max=11, message="حداقل و حداکثر طول این فیلد 11 - 11 کاراکتر است")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "شماره تلفن ادمین"
        }
    )

    TryNumber = IntegerField(
        validators=[
            # DataRequired(message="ورود داده در این فیلد الرامی است"),
            InputRequired(message="ورود داده در این فیلد الرامی است"),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "0",
        }
    )

    Email = EmailField(
        validators=[
            Email(message="ایمیل وارد شده نامعتبر می باشد"),
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
        ],
        render_kw={
            'class': "form-control",
            'placeholder': "Email Address",
        }
    )

    Active = RadioField(
        choices=[("inactive", "غیرفعال"), ("active", "فعال")],
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
        ]
    )

    Submit = SubmitField(
        render_kw={
            'class': "btn btn-primary w-100 my-2",
            'value': "ثبت"
        }
    )


class LogoSettingForm(FlaskForm):
    """
    Logo Setting in App
    """

    Image = FileField(
        validators=[
            DataRequired(),
            InputRequired()
        ],
        render_kw={
            "class": "form-control",
        }
    )

    Submit = SubmitField(
        render_kw={
            "class": "btn btn-primary w-100 my-2",
            "value": "بروزرسانی"
        }
    )


class SiteSettingForm(FlaskForm):
    """
    Site Setting Form
    """

    Name = StringField(
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=1, max=255)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "نام شرکت"
        }
    )
    Description = TextAreaField(
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=1, max=512)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "توضیح کوتاهی راجب شرکت",
            "rows":10
        }
    )
    Address = TextAreaField(
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=1, max=512)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "آدرس شرکت",
            "rows":10
        }
    )
    Phone = StringField(
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=1, max=512)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "شماره تلفن شرکت"
        }
    )

    Submit = SubmitField(
        render_kw={
            "class": "btn btn-primary w-100 my-2",
            "value": "بروزرسانی"
        }
    )
