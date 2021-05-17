import os
from flask import Flask, jsonify, request, render_template, url_for, session, Blueprint, make_response, flash, redirect, g 
from models import User, connect_db, db
from forms import UserAddForm, LoginForm
from sqlalchemy.exc import IntegrityError
import requests
import jsonify
import geonamescache
from uszipcode import SearchEngine, SimpleZipcode
from dotenv import load_dotenv, dotenv_values
from data import api_key

CURR_USER_KEY = "curr_user"
API_URL = "https://www.googleapis.com/civicinfo/v2/representatives/"
# key = load_dotenv()
key = api_key
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///civicduty'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

#####  User registration/login/logout #####

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""
    
    session[CURR_USER_KEY] = user.id
    


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If there is already a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()        

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                residentState=form.residentState.data,
                residentCity=form.residentCity.data,
                residentStreetAddress=form.residentStreetAddress.data,
                residentZipCode=form.residentZipCode.data
            )
            db.session.commit()
            db.session.flush()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/users/")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    id = g.user.id
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:            
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect(f"/users/{id}")

        flash("Invalid credentials.", 'danger')    
    
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    
    session.pop('USERNAME', None)    
    flash("You have been successfully logged out.")
    return redirect("/login")

##### Routes #####

@app.route('/')
def index():
    form = UserAddForm()
    return render_template("/index.html", form=form)

@app.route('/users/<int:id>', methods=["GET", "POST"])
def user_homepage(id):
    """Show a page with info on a specific user."""
    
    user = User.query.get(id)    
    address = user.residentStreetAddress

    user_pres = {'key': key, 'address': address, 'includeOffices': True, 'levels': "country", 'roles': "headOfState"}
    req = request.get_json()
    r = requests.get(API_URL, params=user_pres).json()
    name_pres = r['officials'][0]['name']
    office_pres = r['offices'][0]['name']
    party_pres = r['officials'][0]['party']

    user_senators = {'key': key, 'address': address, 'includeOffices': True, 'levels': "country", 'roles': "legislatorUpperBody"}
    req = request.get_json()
    r = requests.get(API_URL, params=user_pres).json()
    name_sen1 = r['officials'][0]['name']
    office_sen1 = r['offices'][0]['name']
    party_sen1 = r['officials'][0]['party']
    
    
    return render_template('/users/home.html', user=user, name_pres=name_pres, office_pres=office_pres, party_pres=party_pres,
        name_sen1=name_sen1, office_sen1=office_sen1, party_sen1=party_sen1)

##### API Requests #####

def requestSenators(address):

    user = User.query.get_or_404(id)   


    userInfo = {'key': key, 'address': address, 'includeOffices': True, 'levels': "country", 'roles': "legislatorLowerBody"}
    r = requests.get(API_URL, params=userInfo)

    data = r.json()
    
    
    return jsonify(data)
