from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import StringField, PasswordField, SubmitField, validators, BooleanField
from wtforms.validators import InputRequired, Email, Length
import email_validator
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import base64

app = Flask(__name__)

bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['WTF_CSRF_SECRET_KEY'] = 'a_random_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PythonDB.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Enter Username', validators=[InputRequired(), Length(min=3, max = 15)])
    password = PasswordField('Enter Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class RegistrationForm(FlaskForm):
    email = StringField('Enter Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
    username = StringField('Enter Username', validators=[InputRequired(), Length(min=3, max = 15)])
    password = PasswordField('Enter Password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('auth/index.html')#, form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('pages/dashboard.html', name=current_user.username)

@app.route('/credits')
@login_required
def credits():
    return render_template('pages/credits.html', name=current_user.username)
@app.route('/simulatedGrowth')
@login_required
def simulatedGrowth():
    return render_template('pages/simulatedGrowth.html', name=current_user.username)
@app.route('/assetValue')
@login_required
def assetValue():
    return render_template('pages/currentAssetValue.html', name=current_user.username)
@app.route('/updateFinances')
@login_required
def updateFinances():
    return render_template('pages/updateFinancialDetails.html', name=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid Username or Password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return  render_template('login/login.html',form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user Created</h1>'
        #return '<h1>' + form.email.data + ' ' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login/register.html',form=form)




@app.route('/graph')
def graph():
    df = pd.read_excel('example.xlsx')
    cols = df[['rank', 'total_assets_us_b']]

    out = cols.to_numpy().tolist()
    out = [tuple(elt) for elt in out]
    out = [("sdiufnd", 23213),
    ("wksdfsdf", 123123),
    ("iwe", 2312)]

    labels = [row[0] for row in out]
    values = [row[1] for row in out]
    # Render the HTML template with the base64-encoded image
    #table_html = df.to_html(classes='table table-striped', index=False)
    return render_template('viewData/graph.html', labels=labels, values=values)

with app.app_context():
    db.drop_all()
    db.create_all()
    users = User.query.all()
    #print("Print Statement")
    #print(users)
    #print("End print statement")

if __name__ == '__main__':
    app.run(debug=True)