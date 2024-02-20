from flask import (
    Flask, render_template, jsonify, request, redirect, url_for, flash, session
)
import itsdangerous
import wtforms
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, IntegerField, PasswordField, BooleanField, SelectMultipleField
)
from wtforms.validators import (
    InputRequired, Email, Length, NumberRange#, validators
)

from wtforms import MultipleFileField
import email_validator
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required, logout_user, current_user
)
import datetime
import pandas_datareader.data as pdr
import yfinance as yfin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import base64
import csv 
import numpy as np
import requests

np.random.seed(seed=8)
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

#class MultipleFileUploadForm(FlaskForm):
#    files = MultipleFileField('Upload Files', validators=[FileAllowed(['csv', 'xls', 'xlsx'], 'Only CSV and Excel files are allowed.')])

class DeleteFileForm(FlaskForm):
    files_to_delete = SelectMultipleField('Files to Delete', coerce=str)
    submit = SubmitField('Delete Selected Files')

class DynamicForm(FlaskForm):
    pass
class DynamicForm2(FlaskForm):
    pass
def clearAttribute():
    DynamicForm = [attr for attr in DynamicForm if  not(attr.startswith('field_'))]

def CreditsForm(inputs_list):
    for item in inputs_list:
        setattr(DynamicForm, f'field_{item}', IntegerField(f'Enter monthly payment for {item}'))
        #print(item)
    #DynamicForm.submit = SubmitField('Submit')   

def AssetForm(inputs_list):
    for item in inputs_list:
        setattr(DynamicForm2, f'field_{item}', IntegerField(f'Enter asset value for {item}'))
        #print(item)   

def list_files(directory):
    file_names = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return file_names

def create_csv_file(file_path, column_names, data_dict):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=column_names)
        writer.writeheader()
        writer.writerow(data_dict)

def read_csv_file(file_path):
    data_dict = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_dict.update(row)
    return data_dict

def write_csv_file(upload_folder_path, data):
    # Ensure the folder exists (create it if it doesn't)
    #os.makedirs(upload_folder_path, exist_ok=True)

    column_names = list(data.keys())
    print("THESE ARE COLUMN NAMES")
    print(column_names)
    print(type(data))

    # Open the CSV file for writing
    with open(upload_folder_path, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row (keys)
        writer.writerow(data.keys())

        # Write the data row (values)
        writer.writerow(data.values())

def read_user_data(username, upload_folder_path):
    # Create asset and credit file paths
    csv_asset_upload_folder_path = os.path.join(upload_folder_path, f'{username}_assetValue.csv')
    csv_credit_upload_folder_path = os.path.join(upload_folder_path, f'{username}_credits.csv')

    # Read values from asset and credit CSV files
    asset_data = read_csv_file(csv_asset_upload_folder_path)
    credit_data = read_csv_file(csv_credit_upload_folder_path)

    # Create dictionaries for assets and credits
    #assets_dict = {'assets': asset_data}
    #credits_dict = {'credits': credit_data}

    return asset_data, credit_data

def fetch_stock_data(ticker, start_date, end_date):
    yfin.pdr_override()
    #data = pdr.DataReader(ticker, 'yahoo', start_date, end_date).loc[:, 'Adj Close']
    sp = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)
    sp_html = sp.to_html()
    return sp_html, sp

def check_credits():
    try:
        credits = app.config['CREDITS']
    except KeyError:
        return False
    return True

def check_assets():
    try:
        credits = app.config['ASSETS']
    except KeyError:
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('auth/index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if not check_credits() or not check_assets():
        return redirect(url_for('login'))
    else:
        totalCredits = 0
        for value in app.config['CREDITS'].values():
            totalCredits += int(value)
        totalAssets = 0
        for value in app.config['ASSETS'].values():
            totalAssets += int(value)

        #labels = [
        #    '2015','2016','2017','2018','2019','2020','2021', '2022','2023'
        #]
        numYears = 10
        labels = []
        labels.append(totalAssets)
        print (numYears*12)
        for i in range(1,((numYears*12)+1)):
            labels.append(i)
        print(len(labels))
        data = []
        assetStart=totalAssets
        #ticker = 'AAPL'  # Example ticker
        ticker = '^SP500TR'
        start_date = datetime.date(2000, 1, 1).strftime("%Y-%m-%d")
        end_date = datetime.date(2023, 1, 1).strftime("%Y-%m-%d")

        stock_data_html, stock_data = fetch_stock_data(ticker, start_date, end_date)
        var1=stock_data.resample('M').last().pct_change().mean().values[0]
        var2=stock_data.resample('M').last().pct_change().std().values[0]
        #print(var1)
        #print(var2)
        np.random.seed(seed=25)
        data.append(assetStart)
        for month in labels:
            market_return = np.random.normal(var1, var2,1)[0]
            assetStart = assetStart * (1+ market_return)
            #print(assetStart)
            data.append(assetStart)
            #print( market_return)
        #print(data)
        
        #data = [0, 10, 15, 8, 22, 18, 25]

        return render_template('pages/dashboard.html', name=current_user.username, total_credits=totalCredits, total_assets=totalAssets, data=data, Labels=labels)

@app.route('/credits', methods=['GET', 'POST'])
@login_required
def credits():
    #input_list = ['value1', 'value2', 'value3']  # Replace with your list
    input_list = app.config['CREDITS'].keys()
    form = DynamicForm()
    upload_folder_path = os.path.join('upload_folder', f'{current_user.username}/{current_user.username}_credits.csv')
    print(upload_folder_path)
    if request.method == 'POST' and form.validate_on_submit():
        entered_data = {key.lstrip('field_'): value for key, value in request.form.items() if key.startswith('field_')}
        print("Entered data:", entered_data)
        app.config['CREDITS'] = entered_data
        write_csv_file(upload_folder_path, entered_data)
        ##print("Entered data:", entered_data)
        flash("Data entered successfully", "success")
        #clearAttribute()

    if request.method == 'POST' and not form.validate_on_submit():
        flash('There was an issue uploading your data, please try again', 'danger')

    CreditsForm(input_list)
    total_credits = 0
    for key in input_list:
        total_credits += int(app.config['CREDITS'][key])
    return render_template('pages/credits.html', name=current_user.username, form=form, credits_data = app.config['CREDITS'], total_credits=total_credits)

@app.route('/simulatedGrowth')
@login_required
def simulatedGrowth():
    # Define the ticker and date range
    #ticker = 'AAPL'  # Example ticker
    ticker = '^SP500TR'
    start_date = datetime.date(2020, 1, 1).strftime("%Y-%m-%d")
    print(start_date)
    end_date = datetime.date(2023, 1, 1).strftime("%Y-%m-%d")
    print(end_date)
    # Fetch historical stock data for the specified ticker
    stock_data_html, stock_data = fetch_stock_data(ticker, start_date, end_date)
    var1=stock_data.resample('M').last().pct_change().mean().values[0]
    var2=stock_data.resample('M').last().pct_change().std().values[0]
    for i in range (0,1000):
        market_return = np.random.normal(var1, var2,1)[0]
        print(market_return)
    #print(stock_data)
    
    # Convert DataFrame to HTML table
    #stock_table_html = stock_data.to_frame().to_html()
    
    #return render_template('index.html', stock_table_html=stock_table_html)
    return render_template('pages/simulatedGrowth.html', name=current_user.username, stock_table = stock_data_html)
@app.route('/assetValue', methods=['GET', 'POST'])
@login_required
def assetValue():
    #input_list = ['value1', 'value2', 'value3']  # Replace with your list
    input_list = app.config['ASSETS'].keys()
    form =  DynamicForm2()
    upload_folder_path = os.path.join('upload_folder', f'{current_user.username}/{current_user.username}_assetValue.csv')
    print(upload_folder_path)
    if request.method == 'POST' and form.validate_on_submit():
        print("test 1")
        entered_data = {key.lstrip('field_'): value for key, value in request.form.items() if key.startswith('field_')}
        print("test 1")
        app.config['ASSETS'] = entered_data
        print("test 1")
        write_csv_file(upload_folder_path, entered_data)
        print("test 1")
        #print("Entered data:", entered_data)
        flash("Data entered successfully", "success")

    if request.method == 'POST' and not form.validate_on_submit():
        flash('There was an issue uploading your data, please try again', 'danger')

    AssetForm(input_list)
    total_assets = 0
    for key in input_list:
        total_assets += int(app.config['ASSETS'][key])
    return render_template('pages/currentAssetValue.html', name=current_user.username, form=form, assets_data=app.config['ASSETS'], total_assets=total_assets)
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
                assets, credits = read_user_data(username, upload_folder_path)
                app.config['ASSETS'] = assets
                app.config['CREDITS'] = credits
                #print(assets)
                #print(credits)
                flash("Welcome "+ str(current_user.username)+", you have been logged in.")
                return redirect(url_for('dashboard'))

        flash("Incorrect Username or Password", "danger")
        #return '<h1>Invalid Username or Password</h1>'
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
        #with open(csv_asset_upload_folder_path, 'w', newline='') as file:
        #    writer = csv.writer(file)
        #    writer.writerow(['House', 'Car', 'Investments', 'Checking Account', 'Stocks', 'Savings', 'Retirement Accounts'])
        #    writer.writerow([])

        #with open(csv_credit_upload_folder_path, 'w', newline='') as file:
        #    writer = csv.writer(file)
        #    writer.writerow(['Rent', 'Mortgage', 'Utilities', 'Food and Groceries','Car Payments', 'Student loan Payments', 'Pension','Streaming Subscriptions', 'Music Subscriptions', 'Misc Subscriptions', 'Health Insurance', 'House Insurance', 'Other Insurance'])
        #    writer.writerow([20, 400])

        # Define column names for asset and credit files
        asset_column_names = ['House', 'Car', 'Investments', 'Checking Account', 'Stocks', 'Savings', 'Retirement Accounts']
        credit_column_names = ['Rent', 'Mortgage', 'Utilities', 'Food and Groceries', 'Car Payments', 'Student loan Payments', 'Pension', 'Subscriptions', 'Health Insurance', 'House Insurance', 'Other Insurance']

        # Create dictionaries with column names as keys and 0 as values
        asset_data_dict = dict.fromkeys(asset_column_names, 0)
        credit_data_dict = dict.fromkeys(credit_column_names, 0)

        # Create asset and credit files with dictionaries
        create_csv_file(csv_asset_upload_folder_path, asset_column_names, asset_data_dict)
        create_csv_file(csv_credit_upload_folder_path, credit_column_names, credit_data_dict)
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
@login_required
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

#@app.route('/monzo_test')
#def monzo():
#    return render_template('pages/monzo_test.html')

@app.route('/capitalOne', methods=['GET', 'POST'])
def capitalOne():
    # Define the endpoint and request body
    api_url = 'https://api-sandbox.capitalone.com/oauth2/token'
    request_body = {
        'client_id': '9c08b0d10faec81a311401d34e99ccf7',
        'client_secret': '48af6fca7486763d5982ee1e5ff7bb99',
        'grant_type': 'client_credentials'
    }

    # Make the POST request
    response = requests.post(api_url, data=request_body, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    # Check if the request was successful
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        print('Access Token:', access_token)
    else:
        print('Error:', response.text)
    

    api_url = 'https://api-sandbox.capitalone.com/deposits/products/~/search'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json;v=5',
        'Accept': 'application/json;v=5'
    }
    body = {
        'isCollapseRate': True
    }
    response = requests.post(api_url, headers=headers, json=body)
    if response.status_code == 200:
        print('Request successful')
        print(response.json())
    else:
        print('Error:', response.text)


    return(redirect(url_for('dashboard')))


@app.route('/monzo', methods=['GET', 'POST'])
def monzo():
    client_id = 'oauth2client_0000AdfM5AeMUPFJkXTHnt'
    redirect_uri = 'http://localhost'
    state_token = 'your_state_token'

    url = f"https://auth.monzo.com/?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state={state_token}"
    
    return(redirect(url))

@app.route('/oauth/callback')
def oauth_callback():
    # Get the authorization code and state token from the URL parameters
    #authorization_code = request.args.get('code')
    #state_token = request.args.get('state')

    # Check if state_token matches the one you provided earlier
    #expected_state_token = 'your_state_token'

    #if state_token != expected_state_token:
    #    return 'Invalid state token', 400

    # Process the authorization code, exchange it for an access token, etc.
    # You will need to implement this part according to Monzo's documentation

    # For now, let's just print out the received authorization code
    #print(f'Received authorization code: {authorization_code}')

    # You can also redirect the user to another page if needed
    # return redirect('/success')

    # Return a success message
    #return 'Authorization successful'
    authorization_code = 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6InZmWEl1VkZxSzkrSktIR3Y0WXlrIiwianRpIjoiYXV0aHpjb2RlXzAwMDBBZXdraFlDSjhUZGdEdmdKWE4iLCJ0eXAiOiJhemMiLCJ2IjoiNiJ9.5rWu7Vr4aZ8qaGvsVAHeNRV5PvsKndDueIGb6kaaf4yi0BNzcCYTI27ntpbHW3c9R1XnKqQz3XEyxxi4gJhciw'

    access_token(authorization_code)
    return(redirect(url_for('login')))

def access_token(authorization_code):
    

    # Parameters for the request
    params = {
        'grant_type': 'authorization_code',
        'client_id': 'oauth2client_0000AdfM5AeMUPFJkXTHnt',
        'client_secret': 'mnzconf.libMV5WRpToEiz+Q64aUwZCWMLUcr110p4OSgvEY5TwSxT+SoX0xcsM7fC0fciBUrBYZIkCFLj4akwpF2qpkwQ==',
        'redirect_uri': 'http://localhost',
        'code': authorization_code
    }
    print('before')
    # Make the POST request to exchange the authorization code for an access token
    response = requests.post("https://api.monzo.com/oauth2/token", data=params)
    print('after')
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the access token
        print("Access token:", response.json()['access_token'])
        response = requests.get(f"https://api.monzo.com/balance?account_id=user_00009hPDVBoQ6BJJXislbV", headers={"Authorization": f"Bearer {response.json()['access_token']}"})

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the balance as JSON
            return jsonify(response.json())
        else:
            # Return the error message if the request was not successful
            return jsonify({"error": response.text}), response.status_code
    else:
        # Print the error message if the request was not successful
        print("Error:", response.text)
    

with app.app_context():
    #db.drop_all()
    db.create_all()
    #sample_user = User(username="test", email="test@test.com", password=generate_password_hash("password"))
    #db.session.add(sample_user)
    #db.session.commit()
    
    #users = User.query.all()
    #print("Print Statement")
    #print(users)
    #print("End print statement")

if __name__ == '__main__':
    app.run(debug=True)