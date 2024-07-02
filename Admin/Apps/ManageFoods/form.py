from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField, TextAreaField, RadioField, \
    SubmitField, SelectMultipleField
from wtforms.validators import Length, DataRequired, InputRequired
from FoodyConfig.config import VALID_DAYS

from wtforms.widgets import ListWidget, CheckboxInput


class CheckBoxField(SelectMultipleField):
    """Check Box Form"""
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class AddFoodForm(FlaskForm):
    """Use This Class For adding new food to app"""

    Name = StringField(
        validators=[
            InputRequired(message="ورود داده در این فیلد الزامی است"),
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            Length(min=2, max=64, message='حداکثر طول این فیلد 64 و حداقل 2 کاراکتر است')
        ],
        render_kw={
            "id": "Name",
            "class": "form-control",
            "placeholder": "نام غذا را وارد نمایید"
        }
    )

    Description = TextAreaField(
        validators=[
            InputRequired(message="ورود داده در این فیلد الزامی است"),
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            Length(min=2, max=255, message='حداکثر طول این فیلد 255 و حداقل 2 کاراکتر است')
        ],
        render_kw={
            "id": "Description",
            "class": "form-control",
            "placeholder": "توضیحات غذا را وارد نمایید",
            "rows":10
        }
    )

    DayOfReserve = CheckBoxField(
        choices=[(each[1], each[0],) for each in VALID_DAYS],
        validators=[
        ],

    )

    Active = RadioField(
        choices=[('active', 'فعال'), ('inactive', 'غیرفعال')],
        validators=[
            InputRequired(message="ورود داده در این فیلد الزامی است"),
            DataRequired(message="ورود داده در این فیلد الزامی است"),
        ]
    )

    Images = MultipleFileField(
        render_kw={
            'multiple': True,
            "id": "Images",
            "class": "form-control"
        }
    )

    Submit = SubmitField(
        render_kw={
            "class": "w-100 btn btn-success",
            "value": "ثبت"
        }
    )
