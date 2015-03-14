"""This module contains the RegistrationForm Class."""
from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):

    """Form for handling registration form validation."""

    username = StringField(
        'username',
        [validators.required(),
         validators.Length(min=1, max=25)]
    )
    password = PasswordField(
        'password',
        [validators.required(),
         validators.Length(min=6, max=35),
         validators.EqualTo('confirm')]
    )
    confirm = PasswordField('confirm')
