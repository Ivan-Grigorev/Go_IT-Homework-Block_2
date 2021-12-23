from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email
from models import AddressBook
from Module_11.app_folder import db


class AddContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Save')

    def validate_name(self, name):
        name = db.session.query(AddressBook).filter_by(name=name.title())
        if name is not None:
            raise ValidationError(f"Address book exist name {name}. Enter another name, please.")
        elif name is None:
            raise ValidationError("Enter the name, please!")

    def validate_phone(self, phone):
        if phone is None:
            phone += '-'

    def validate_email(self, email):
        if email is None:
            email += '-'

    def validate_address(self, address):
        if address is None:
            address += '-'
