from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo
from flask_wtf import RecaptchaField, Recaptcha


class LoginForm(FlaskForm):
    username = StringField(
        validators = [
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            DataRequired(message="وارد کردن داده در این فیلد الزامی است "),
        ]
    )

    password = PasswordField(
        validators = [
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            DataRequired(message="وارد کردن داده در این فیلد الزامی است "),
        ]
    )

    submit = SubmitField()



class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        validators = [
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            DataRequired(message="وارد کردن داده در این فیلد الزامی است "),
            Length(min=6, max=64, message="حداقل طول گذرواژه باید 6 کاراکتر باشدو حداکثر 64 کاراکتر")
        ]
    )
    password_repeat = PasswordField(
        validators = [
            InputRequired(message="وارد کردن داده در این فیلد الزامی است    "),
            DataRequired(message="وارد کردن داده در این فیلد الزامی است "),
            Length(min=6, max=64, message="حداقل طول گذرواژه باید 6 کاراکتر باشدو حداکثر 64 کاراکتر"),
            EqualTo("password", message="گذرواژه ها یکسان نیستند")
        ]
    )

    # reset_token = HiddenField(validators=[
    #     DataRequired(),
    #     InputRequired(),
    # ])
    submit = SubmitField()
