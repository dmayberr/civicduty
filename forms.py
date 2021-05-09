from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from data import us_state_abbrev
import geonamescache
from uszipcode import SearchEngine, SimpleZipcode

search = SearchEngine()

gc = geonamescache.GeonamesCache()
states = gc.get_us_states()
cities = gc.get_cities()

class UserAddForm(FlaskForm):
    """Form for adding users to system."""

    username = StringField('username')
    password = PasswordField('New Password', 
        validators=[DataRequired(), Length(min=6), EqualTo('passwordConfirm', message='Passwords must match.')]) 
    passwordConfirm = PasswordField('Repeat Password')  
    email = StringField('Email', validators=[Email(), DataRequired()])    
    residentState = SelectField(u'State', validators=[DataRequired()], choices=us_state_abbrev)
    residentCity = StringField('City', validators=[DataRequired()])
    residentStreetAddress = StringField('Street Address')
    residentZipCode = IntegerField('Zip Code', validators=[NumberRange(min=1001, max=99950, message="Invalid zip code")])
    
class LoginForm(FlaskForm):
    """Form to login existing users"""

    username = StringField('username')
    password = PasswordField('password')

