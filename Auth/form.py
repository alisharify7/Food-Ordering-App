import flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()




class LoginForm(FlaskForm):

    @property
    def action(self):
        return flask.url_for('auth.login_get')

    username = StringField(
        label="نام کاربری",
        validators=[
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            DataRequired(message="وارد کردن داده در این فیلد الزامی است "),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "username",
            "dir": "ltr"
        }
    )

    password = PasswordField(
        label="گذرواژه",
        validators=[
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            DataRequired(message="وارد کردن داده در این فیلد الزامی است "),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "password",
            "dir": "ltr"
        }
    )

    remember_me = MultiCheckboxField(choices=['مرا به خاطر داشته باش'], render_kw={"class": "list-unstyled m-0 text-muted"})

    submit = SubmitField(
                         render_kw={
                             "class": "btn btn-primary w-100 fs-5 ",
                             "value": "ورود"
                         })



class ResetPasswordForm(FlaskForm):

    @property
    def action(self):
        return flask.url_for('auth.reset_password_get')

    username = StringField(
        label="نام کاربری یا کد ملی یا شماره تماس یا ایمیل",
        validators=[
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            DataRequired(message="وارد کردن داده در این فیلد الزامی است "),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "username or email address or national code or phone number",
            "dir": "ltr"
        }
    )

    submit = SubmitField(validators=[InputRequired()],
                         render_kw={
                             "class": "btn btn-primary w-100 fs-5 my-3",
                             "value": "بازنشانی گذرواژه"
                         })


