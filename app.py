from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import StringField, PasswordField, SubmitField, validators, BooleanField, SelectMultipleField
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms.validators import InputRequired, Email, Length
import email_validator
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import base64
import csv 

app = Flask(__name__)

bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['WTF_CSRF_SECRET_KEY'] = 'a_random_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PythonDB.db'
app.config['UPLOAD_FOLDER'] = 'upload_folder'

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

class MultipleFileUploadForm(FlaskForm):
    files = MultipleFileField('Upload Files', validators=[FileAllowed(['csv', 'xls', 'xlsx'], 'Only CSV and Excel files are allowed.')])

class DeleteFileForm(FlaskForm):
    files_to_delete = SelectMultipleField('Files to Delete', coerce=str)
    submit = SubmitField('Delete Selected Files')

def list_files(directory):
    file_names = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return file_names

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('auth/index.html')

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
                username = current_user.username
                upload_folder_path = os.path.join('upload_folder', username)

                # Set the UPLOAD_FOLDER configuration
                app.config['UPLOAD_FOLDER'] = upload_folder_path
                flash("Welcome "+ str(current_user.username)+", you have been logged in.")
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
        username = form.username.data
        upload_folder_path = os.path.join('upload_folder', username)
        csv_asset_upload_folder_path = os.path.join(upload_folder_path, f'{username}_assetValue.csv')
        csv_credit_upload_folder_path = os.path.join(upload_folder_path, f'{username}_credits.csv')

        # Ensure the folder exists (create it if it doesn't)
        os.makedirs(upload_folder_path, exist_ok=True)

        # Set the UPLOAD_FOLDER configuration
        app.config['UPLOAD_FOLDER'] = upload_folder_path
        #Create a user csv which will store their asset values
        with open(csv_asset_upload_folder_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['House', 'Car', 'Investments', 'Checking Account', 'Stocks', 'Savings', 'Retirement Accounts'])
            writer.writerow([])

        with open(csv_asset_upload_folder_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Rent', 'Mortgage', 'Utilities', 'Food and Groceries','Car Payments', 'Student loan Payments', 'Pension','Streaming Subscriptions', 'Music Subscriptions', 'Misc Subscriptions', 'Health Insurance', 'House Insurance', 'Other Insurance'])
            writer.writerow([20, 400])

        flash('New User Created', 'success')
        return redirect (url_for('login'))
        #return '<h1>' + form.email.data + ' ' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login/register.html',form=form)

@app.route('/uploadMultiple', methods=['GET', 'POST'])
@login_required
def uploadMultiple():
    form = MultipleFileUploadForm()

    if form.validate_on_submit():
        uploaded_files = form.files.data
        
        for uploaded_file in uploaded_files:
            # Securely save each file to a folder on the server
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)

            # Process each file or perform additional actions
            # Example: Read the contents of a CSV file
            #df = pd.read_csv(file_path)
            # Perform analysis on df...
            return "<h1>File uploaded</h1>"
        # Redirect to a success page or perform other actions
        return redirect(url_for('dashboard'))

    return render_template('pages/upload_multiple.html', form=form)

@app.route('/delete_files', methods=['GET', 'POST'])
def delete_files():
    form = DeleteFileForm()

    # Specify the directory path you want to iterate through
    directory_path = app.config['UPLOAD_FOLDER']

    file_names = list_files(directory_path)

    # Populate choices for the SelectMultipleField
    form.files_to_delete.choices = [(file, file) for file in file_names]

    if form.validate_on_submit():
        # Get the selected file names and perform deletion logic
        selected_files = form.files_to_delete.data
        for file in selected_files:
            file_path = os.path.join(directory_path, file)
            # Add logic to delete the file or perform any other actions
            try:
                os.remove(file_path)
            except OSError as e:
                file_path = ''

        return redirect(url_for('dashboard'))

    return render_template('pages/deleteFiles.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))




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