import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError
from wtforms.fields import TextAreaField
from wtforms.fields.html5 import EmailField, SearchField, DateTimeLocalField
from wtforms.validators import InputRequired, DataRequired, Length, Email, Optional


def validate_email(form, field) -> bool:
    regex = r"^[a-z0-9]+[\._+]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if re.search(regex, field.data):
        return True
    else:
        raise ValidationError("E-mail must follow this format: username@example.com")


class ShippingAddressForm(FlaskForm):
    name = StringField(
            "Full Name", validators=[InputRequired(), DataRequired(), Length(min=2, max=25)]
    )
    phone = StringField(
            "Phone Number",
            validators=[InputRequired(), DataRequired(), Length(min=9, max=12)],
    )
    contact_email = EmailField(
            "Contact E-mail", validators=[InputRequired(), validate_email]
    )
    company_name = StringField("Company Name", validators=[Length(min=1, max=25)])
    address_line_1 = StringField(
            "Address Line 1",
            validators=[InputRequired(), DataRequired(), Length(min=2, max=60)],
    )
    address_line_2 = StringField("Address Line 2", validators=[Optional(), Length(max=60)])
    address_line_3 = StringField("Address Line 3", validators=[Optional(), Length(max=60)])
    city_locality = StringField(
            "City", validators=[InputRequired(), DataRequired(), Length(min=2, max=50)]
    )
    state_province = StringField(
            "State (2 character abbreviation)",
            validators=[InputRequired(), DataRequired(), Length(max=2)],
    )
    postal_code = StringField(
            "Postal Code",
            validators=[InputRequired(), DataRequired(), Length(min=1, max=15)],
    )
    country_code = StringField(
            "Country (2 character abbreviation)",
            validators=[InputRequired(), DataRequired(), Length(max=2)],
    )
    address_residential_indicator = SelectField(
            "Address Residential Indicator", choices=["unknown", "yes", "no"]
    )
    create_return_label = SubmitField('Create Return Label')


class SchedulePickupForm(FlaskForm):
    label_id = StringField("Label ID", validators=[InputRequired(), DataRequired()])
    contact_name = StringField(
            "Full Name", validators=[InputRequired(), DataRequired()]
    )
    contact_email = EmailField(
            "E-mail", validators=[InputRequired(), DataRequired(), Email()]
    )
    contact_phone = StringField(
            "Phone Number", validators=[InputRequired(), DataRequired()]
    )
    pickup_window_start_at = DateTimeLocalField(
            "Pickup Window: Start - Begin at 9 AM", validators=[InputRequired(), DataRequired()]
    )
    pickup_window_end_at = DateTimeLocalField(
            "Pickup Window: End - Ends at 5 PM", validators=[InputRequired(), DataRequired()]
    )
    pickup_notes = TextAreaField(
            "Pickup Notes", validators=[Optional()]
    )
    schedule_pickup = SubmitField("Schedule Pickup")


class SearchBar(FlaskForm):
    search = SearchField()


class EmailLabelForm(FlaskForm):
    contactEmail = EmailField(
            "E-mail", validators=[InputRequired(), DataRequired(), Email()]
    )
