from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email



class UserPanelEmailForm(FlaskForm):
    """
    This Form Uses in User Panel For Updating User Email Address
    """
    Email = StringField(
        validators=[
            Email(message="ایمیل وارد شده نامعتبر است"),
            DataRequired(
                message="ورود داده در این فیلد الزامی است"
            ),
            InputRequired(
                message="ورود داده در این فیلد الزامی است"
            )
        ],
        render_kw={
            "class": "form-control bg-muted",
            "placeholder":"Email Address",
            "dir": "ltr"
        }
    )

    Submit = SubmitField(
        render_kw={
            "value":"بروزرسانی",
            "class":"btn btn-success my-2 w-100"
        }
    )


class UserProfileForm(FlaskForm):
    username = StringField(render_kw={"disabled: true"})
    password = StringField()
    avatar = ""
    first_name = StringField()
    last_name = StringField()
    phone_number = StringField()
    national_code = StringField()
    employee_code = StringField()
    status = StringField()
    email_address = StringField()
    last_login_time = StringField()
    work_section = StringField()

