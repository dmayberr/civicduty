import os
from flask import Flask, jsonify, request, render_template, url_for, session, Blueprint, make_response, flash, redirect, g 
from models import User, connect_db, db
from forms import UserAddForm, LoginForm
from sqlalchemy.exc import IntegrityError
import requests
from uszipcode import SearchEngine, SimpleZipcode
from dotenv import load_dotenv, dotenv_values
from data import api_key

CURR_USER_KEY = "curr_user"
API_URL = "https://www.googleapis.com/civicinfo/v2/representatives/"
# key = load_dotenv()
key = api_key
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

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
    
    r = requests.get(API_URL, params=user_pres).json()
    name_pres = r['officials'][0]['name']
    office_pres = r['offices'][0]['name']
    party_pres = r['officials'][0]['party']

    user_vp = {'key': key, 'address': address, 'includeOffices': True, 'levels': "country", 'roles': "deputyHeadOfGovernment"}
    
    r = requests.get(API_URL, params=user_vp).json()
    name_vp = r['officials'][0]['name']
    lastname_vp = getLastName(name_vp)
    office_vp = r['offices'][0]['name']
    party_vp = r['officials'][0]['party']

    user_senators = {'key': key, 'address': address, 'includeOffices': True, 'levels': "country", 'roles': "legislatorUpperBody"}
    
    r = requests.get(API_URL, params=user_senators).json()
    name_sen1 = r['officials'][0]['name']
    lastname_sen1 = getLastName(name_sen1)
    office_sen1 = r['offices'][0]['name']
    party_sen1 = r['officials'][0]['party']

    r = requests.get(API_URL, params=user_senators).json()
    name_sen2 = r['officials'][1]['name']
    lastname_sen2 = getLastName(name_sen2)
    office_sen2 = r['offices'][0]['name']
    party_sen2 = r['officials'][0]['party']

    user_rep = {'key': key, 'address': address, 'includeOffices': True, 'levels': "country", 'roles': "legislatorLowerBody"}

    r = requests.get(API_URL, params=user_rep).json()
    name_rep = r['officials'][0]['name']
    lastname_rep = getLastName(name_rep)
    office_rep = r['offices'][0]['name']
    party_rep = r['officials'][0]['party']
    
    
    return render_template('/users/home.html', user=user, 
        name_pres=name_pres, office_pres=office_pres, party_pres=party_pres,
        name_vp=name_vp, office_vp=office_vp, party_vp=party_vp, lastname_vp=lastname_vp,
        name_sen1=name_sen1, office_sen1=office_sen1, party_sen1=party_sen1, lastname_sen1=lastname_sen1,
        name_sen2=name_sen2, office_sen2=office_sen2, party_sen2=party_sen2, lastname_sen2=lastname_sen2,
        name_rep=name_rep, office_rep=office_rep, party_rep=party_rep, lastname_rep=lastname_rep)

##### API Requests #####

# def requestSenators(address):

#     user = User.query.get_or_404(id)   


#     userInfo = {'key': key, 'address': address, 'includeOffices': True, 'levels': "country", 'roles': "legislatorLowerBody"}
#     r = requests.get(API_URL, params=userInfo)

#     data = r.json()
    
    
#     return jsonify(data)

def getLastName(string):
    li = list(string.split(" "))
    lastname = li[-01].lower()
    return lastname
