from flask import current_app, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from email_validator import validate_email as email_validator_func
from email_validator.exceptions_types import EmailNotValidError

class UserProfileForm(FlaskForm):

    @staticmethod
    def validate_email(email: str) -> bool:
        try:
            email_validator_func(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False

    @property
    def action(self):
        return url_for('user.profile_post')

    def fill_with(self, obj):
        default = ""
        placeholder = {'placeholder': "تنظیم نشده است"}
        self.username.data = obj.username or default

        self.first_name.data = obj.first_name or default
        self.first_name.render_kw.update(placeholder if not obj.first_name else {})

        self.last_name.data = obj.last_name or default
        self.last_name.render_kw.update(placeholder if not obj.last_name else {})

        self.email_address.data = obj.email_address or default
        self.phone_number.data = obj.phone_number or default
        self.national_code.data = obj.national_code or default
        self.employee_code.data = obj.employee_code or default
        self.status.data = 'فعال' if obj.status else 'غیرفعال'
        self.work_section.data = obj.work_section.name or default

    username = StringField(validators=[], render_kw={"class": "form-control", "disabled": "true",})
    first_name = StringField(validators=[], render_kw={"class": "form-control"})
    last_name = StringField(validators=[], render_kw={"class": "form-control"})
    email_address = EmailField(validators=[], render_kw={"class": "form-control"})
    phone_number = StringField(validators=[], render_kw={"disabled": "true", "class": "form-control"})
    national_code = StringField(validators=[], render_kw={"disabled": "true", "class": "form-control"})
    employee_code = StringField(validators=[], render_kw={"disabled": "true", "class": "form-control"})
    status = StringField(validators=[], render_kw={"disabled": "true", "class": "form-control"})
    work_section = StringField(validators=[], render_kw={"disabled": "true", "class": "form-control"})
