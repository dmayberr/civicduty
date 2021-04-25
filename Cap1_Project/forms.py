from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from data import us_state_abbrev
import geonamescache

gc = geonamescache.GeonamesCache()
states = gc.get_us_states()


class UserAddForm(FlaskForm):
    """Form for adding users to system."""

    username = StringField('username')
    password = PasswordField('New Password', 
        validators=[DataRequired(), Length(min=6), EqualTo('passwordConfirm', message='Passwords must match.')]) 
    passwordConfirm = PasswordField('Repeat Password')  
    email = StringField('Email', validators=[Email(), DataRequired()])
    residentState = SelectField(u'State', validators=[DataRequired()], choices=us_state_abbrev)
    residentCity = SelectField('City')
    residentStreetAddress = StringField('Street Address')
    

