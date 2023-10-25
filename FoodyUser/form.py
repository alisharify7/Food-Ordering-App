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
