from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class UserAddForm(FlaskForm):
    """Form for adding users to system."""

    username = StringField('username')
    password = PasswordField('New Password', 
        validators=[DataRequired(), Length(min=6), EqualTo('passwordConfirm', message='Passwords must match.')]) 
    passwordConfirm = PasswordField('Repeat Password')  
    email = StringField('Email', validators=[Email(), DataRequired()])
    residentState = SelectField('States')
    residentCity = SelectField('Cities')
    residentStreetAddress = SelectField('Street Address')
    

