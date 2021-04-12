from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users to system."""

    username = StringField('username'
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('pwConfirmation', message='Passwords must match')

    ])
    pwConfirmation = PasswordField('Repeat Password')
    email = StringField('Email', validators=[Email()])
    residentState = 