from flask import (
    Flask, render_template, jsonify, request, redirect, url_for, flash, session
)
import itsdangerous
import wtforms
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, IntegerField, PasswordField, BooleanField, SelectMultipleField,FileField
)
from wtforms.validators import (
    InputRequired, Email, Length, NumberRange, DataRequired, Optional, EqualTo, ValidationError#, validators
)
import email_validator

from wtforms import MultipleFileField, DecimalField
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required, logout_user, current_user
)
from openpyxl import Workbook, load_workbook
from passlib.hash import sha256_crypt
import datetime
#from datetime import datetime
import pandas_datareader.data as pdr
import yfinance as yfin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
#import matplotlib.pyplot as plt
import os
import io
import base64
import csv 
import re
import numpy as np
import requests
import json
from PythonGenerators.generateAccounts import FinanceDataGenerator
from PythonGenerators.generateCreditCardAccounts import CreditCardDataGenerator
from decimal import Decimal

#FinsFintechFYP

np.random.seed(seed=8)
app = Flask(__name__)

bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['WTF_CSRF_SECRET_KEY'] = 'a_random_key' 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PythonDB.db'
app.config['UPLOAD_FOLDER'] = 'upload_folder'

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Finnnnnn1",
    password="FinsFintechFYP",
    hostname="Finnnnnn1.mysql.pythonanywhere-services.com",
    databasename="Finnnnnn1$users",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = "users"
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

class UploadForm(FlaskForm):
    file = FileField('Upload File', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Transaction:
    def __init__(self, transaction_id, date, amount, description, category, balance, merchant=None):
        self.transaction_id = transaction_id
        self.date = date
        self.amount = amount
        self.description = description
        self.category = category
        self.merchant = merchant
        self.balance = balance

    def to_dict(self):
        transaction_dict = {
            "transaction_id": self.transaction_id,
            "date": self.date,
            "amount": self.amount,
            "description": self.description,
            "category": self.category,
            "balance": self.balance
        }
        if self.merchant:
            transaction_dict["merchant"] = self.merchant
        return transaction_dict

class Account:
    def __init__(self, account_number, sort_code, balance, currency, account_holder, transactions):
        self.account_number = account_number
        self.sort_code = sort_code
        self.balance = balance
        self.currency = currency
        self.account_holder = account_holder
        self.transactions = transactions
        self.account_total_in = 0
        self.account_total_out = 0 
        self.merchant_count = {}
        self.salary = 0
        for transaction in self.transactions:
            if transaction.amount > 0 :
                self.account_total_in += transaction.amount
            else:
                self.account_total_out += transaction.amount
                self.merchant_count[transaction.merchant['category']] = self.merchant_count.get(transaction.merchant['category'], 0)+1
            if transaction.description == "Salary Deposit":
                self.salary = float(transaction.amount)
        self.top_merchant = max(self.merchant_count, key=self.merchant_count.get)
        self.account_total_in = round(float(self.account_total_in), 2)
        self.account_total_out = round(float(self.account_total_out), 2)

    def to_dict(self):
        account_dict = {
            "account_number": self.account_number,
            "sort_code": self.sort_code,
            "balance": self.balance,
            "currency": self.currency,
            "account_holder": self.account_holder,
            "transactions": [txn.to_dict() for txn in self.transactions],
            "total_in": self.account_total_in,
            "total_out": self.account_total_out,
            "top_merchant": self.top_merchant,
            "salary": self.salary
        }
        return account_dict

class CreditCard:
    def __init__(self, card_number, expiry_date, card_holder, credit_limit, currency, transactions):
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.card_holder = card_holder
        self.credit_limit = credit_limit
        self.currency = currency
        self.transactions = transactions
        self.credit_total_in = 0
        self.credit_total_out = 0 
        self.merchant_count = {}
        for transaction in self.transactions:
            if transaction.amount > 0 :
                self.credit_total_in += transaction.amount
            else:
                self.credit_total_out += transaction.amount
                self.merchant_count[transaction.merchant['category']] = self.merchant_count.get(transaction.merchant['category'], 0)+1
        self.top_merchant = max(self.merchant_count, key=self.merchant_count.get)
        self.credit_total_in = round(float(self.credit_total_in), 2)
        self.credit_total_out = round(float(self.credit_total_out), 2)
    

    def to_dict(self):
        credit_card_dict = {
            "card_number": self.card_number,
            "expiry_date": self.expiry_date,
            "card_holder": self.card_holder,
            "credit_limit": self.credit_limit,
            "currency": self.currency,
            "transactions": [txn.to_dict() for txn in self.transactions],
            "total_in": self.credit_total_in,
            "total_out": self.credit_total_out,
            "top_merchant": self.top_merchant
        }
        return credit_card_dict

class Form1(FlaskForm):
    field1 = StringField('Field 1', validators=[InputRequired()])

class Form2(FlaskForm):
    field2 = StringField('Field 2', validators=[InputRequired()])

class SavingsCalculatorYear(FlaskForm):
    savings_goal = DecimalField('Savings Goal', validators=[InputRequired(), NumberRange(min=0)])
    current_held_savings = DecimalField('Current Savings', validators=[InputRequired(), NumberRange(min=0)])
    annual_interest_rate = DecimalField('Annual Interest Rate (%)', default=10, validators=[NumberRange(min=0)])
    saving_per_month = DecimalField('Monthly Savings', validators=[InputRequired(), NumberRange(min=0)])

class SavingsCalculatorAmount(FlaskForm):
    savings_goal = DecimalField('Savings Goal', validators=[InputRequired(), NumberRange(min=0)])
    current_held_savings = DecimalField('Current Savings', validators=[InputRequired(), NumberRange(min=0)])
    annual_interest_rate = DecimalField('Annual Interest Rate (%)', default=10, validators=[InputRequired(), NumberRange(min=0)])
    years_to_save = IntegerField('Years to Save', validators=[NumberRange(min=0)], default=None)

class Retirement(FlaskForm):
    current_age = IntegerField('Current Age', validators=[InputRequired()])
    desired_retirement_age = IntegerField('Desired Retirement Age', validators=[InputRequired()])
    current_savings = IntegerField('Current Retirement Savings', validators=[InputRequired()])
    expected_annual_return = IntegerField('Expected Annual Return (%). This is suggested to be a value between 2 and 7', validators=[InputRequired()])
    desired_annual_income = IntegerField('Desired Annual Retirement Income', validators=[InputRequired()])

class UKTaxCalculatorForm(FlaskForm):
    yearly_earnings = DecimalField('Yearly Earnings (£)', validators=[InputRequired(), NumberRange(min=0)])
    over_state_pension_age = BooleanField('Are you over the State Pension Age?')
    blind = BooleanField('Do you receive blind persons allowance?')

class CapitalGainsCalculator(FlaskForm):
    purchase_price = DecimalField('Purchase Price', validators=[InputRequired()])
    sale_price = DecimalField('Sale Price', validators=[InputRequired()])
    holding_period = IntegerField('Holding Period (Years)', validators=[InputRequired()])
    cost_of_improvements = DecimalField('Cost of Improvements')
    used_as_business = BooleanField('Was a room used for a desk for business or a lodger in a single room?')
    sq_metres = BooleanField('Is the property 0ver 5000 metres, including the buildings?')

def validate_category(form, field):
    if not re.match(r'^[A-Za-z\s.!]+$', field.data):
        raise ValidationError('Category must contain only letters, spaces, ".", or "!"')

class BudgetForm(FlaskForm):
    category = StringField('Category for the expense', validators=[InputRequired(), validate_category])
    amount = DecimalField('Amount paid', validators=[InputRequired(), NumberRange(min=0.01)])
    clear_table = BooleanField('Select if you want to clear the table.')

class MortgageForm(FlaskForm):
    loan_amount = DecimalField('Loan Amount (£)', validators=[DataRequired(), NumberRange(min=0.01)])
    down_payment = DecimalField('Down Payment (£)', validators=[Optional(), NumberRange(min=0)])
    interest_rate = DecimalField('Interest Rate (%)', validators=[DataRequired(), NumberRange(min=0.01)])
    loan_term = IntegerField('Loan Term (years)', validators=[DataRequired(), NumberRange(min=1, max=100)])

class MortgageAffordabilityForm(FlaskForm):
    annual_income = DecimalField('Annual Income (£)', validators=[DataRequired(), NumberRange(min=0.01)])
    monthly_debt = DecimalField('Monthly Debt (£)', validators=[DataRequired(), NumberRange(min=0.01)])
    interest_rate = DecimalField('Interest Rate (%)', validators=[Optional()])
    loan_term = DecimalField('Loan Term (years)', validators=[DataRequired(), NumberRange(min=1)])

def clearAttribute():
    DynamicForm = [attr for attr in DynamicForm if  not(attr.startswith('field_'))]


def list_files(directory):
    file_names = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return file_names

def create_excel_file(file_path, sheet_data):
    # Create a Pandas Excel writer using ExcelWriter as the engine
    writer = pd.ExcelWriter(file_path)
    
    # Iterate through the sheet data
    for sheet_name, column_names in sheet_data.items():
        # Create a DataFrame with column names
        df = pd.DataFrame(columns=column_names)
        
        # Fill the DataFrame with zeros below the column names
        for col in column_names:
            df[col] = [0]
        
        # Write the DataFrame to the Excel file
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    # Save the Excel file
    writer.save()

def excel_to_dict(file_path):
    # Read the Excel file
    xls = pd.ExcelFile(file_path)
    
    # Initialize an empty dictionary to store sheet data
    excel_dict = {}
    
    # Iterate through each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(xls, sheet_name)
        
        # Convert the DataFrame to a dictionary and add it to the excel_dict
        excel_dict[sheet_name] = df.to_dict(orient='records')
    
    return excel_dict

def write_dict_to_excel(file_path, sheet_name, data_dict):
    # Load the workbook or create a new one if it doesn't exist
    try:
        wb = load_workbook(file_path)
    except FileNotFoundError:
        wb = Workbook()
    
    # Select the worksheet or create a new one if it doesn't exist
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(title=sheet_name)

    # Write the keys in the first row
    keys = list(data_dict.keys())
    for col, key in enumerate(keys, start=1):
        ws.cell(row=1, column=col, value=key)

    # Write the values in the second row
    values = list(data_dict.values())
    for col, value in enumerate(values, start=1):
        ws.cell(row=2, column=col, value=value)

    # Save the workbook
    wb.save(file_path)


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
    totalCredits = 0
    totalAssets = 0
    if not check_credits() or not check_assets():
        return redirect(url_for('login'))
    else:
        #totalCredits = 0
        for value in app.config['CREDITS'].values():
            totalCredits += int(value)
        #totalAssets = 0
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
        # Create datetime objects for start and end dates
        #start_date = datetime.datetime(2000, 1, 1)

        #end_date = datetime.datetime(2023, 1, 1)
        # Format datetime objects as strings and assign to original variable names
       # start_date = start_date.strftime("%Y-%m-%d")
        #end_date = end_date.strftime("%Y-%m-%d")
        from dateutil import parser

        # Parse date strings into datetime objects
        start_date = parser.parse("2000-01-01")
        end_date = parser.parse("2023-01-01")

        # Format datetime objects as strings
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")


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

def generate_credits_form(input_list):
    class CreditsForm(DynamicForm):
        pass
    
    for index, field_name in enumerate(input_list):
        initial_value = 0
        field = IntegerField(field_name, validators=[Optional(), NumberRange(min=0)], default=initial_value)
        setattr(CreditsForm, f'field_{index}', field)

    return CreditsForm()

@app.route('/credits', methods=['GET', 'POST'])
@login_required
def credits():
    #input_list = ['value1', 'value2', 'value3']  # Replace with your list
    input_list = app.config['CREDITS'].keys()
    form = generate_credits_form(input_list=input_list)
    #upload_folder_path = os.path.join('Wealth_Managment_Tool/upload_folder', f'{current_user.username}/{current_user.username}_credits.csv')
    #print(upload_folder_path)
    if request.method == 'POST' and form.validate_on_submit():
        old_vals = list(app.config['CREDITS'].values())
        entered_data_list = [value if value != '' else '-1' for value in request.form.values()]
        counter = 0
        for val in entered_data_list:
            if val == '-1' and int(old_vals[counter]) != 0:
                entered_data_list[counter] = old_vals[counter]
            elif val == '-1':
                entered_data_list[counter] = '0'
            counter += 1
        entered_data = {list(input_list)[i]:entered_data_list[i] for i in range(len(input_list))}
        #print("Entered data:", entered_data)
        app.config['CREDITS'] = entered_data
        #write_csv_file(upload_folder_path, entered_data)
        write_dict_to_excel(app.config['UPLOAD_FOLDER'], 'credits', entered_data)
        ##print("Entered data:", entered_data)
        flash("Data entered successfully", "success")
        #clearAttribute()

    if request.method == 'POST' and not form.validate_on_submit():
        flash('There was an issue uploading your data, please try again', 'danger')
    
    total_credits = 0
    for key in app.config['CREDITS'].keys():
        total_credits += int(app.config['CREDITS'][key])
    return render_template('pages/credits.html', name=current_user.username, form=form, credits_data = app.config['CREDITS'], total_credits=total_credits)

def generate_assets_form(input_list):
    class AssetsForm(DynamicForm2):
        pass
    
    for index, field_name in enumerate(input_list):
        initial_value = 0
        field = IntegerField(field_name, validators=[Optional(), NumberRange(min=0)], default=initial_value)
        setattr(AssetsForm, f'field_{index}', field)

    return AssetsForm()

@app.route('/assetValue', methods=['GET', 'POST'])
@login_required
def assetValue():
    #input_list = ['value1', 'value2', 'value3']  # Replace with your list
    input_list = app.config['ASSETS'].keys()
    form = generate_assets_form(input_list=input_list)
    #upload_folder_path = os.path.join('Wealth_Managment_Tool/upload_folder', f'{current_user.username}/{current_user.username}_assetValue.csv')
    #print(upload_folder_path)
    if request.method == 'POST' and form.validate_on_submit():
        #print("test 1")
        old_vals = list(app.config['ASSETS'].values())
        entered_data_list = [value if value != '' else '-1' for value in request.form.values()]
        counter = 0
        for val in entered_data_list:
            if val == '-1' and int(old_vals[counter]) != 0:
                entered_data_list[counter] = old_vals[counter]
            elif val == '-1':
                entered_data_list[counter] = '0'
            counter += 1
        entered_data = {list(input_list)[i]:entered_data_list[i] for i in range(len(input_list))}
        #print("test 1")
        app.config['ASSETS'] = entered_data
        #print("test 1")
        #write_csv_file(upload_folder_path, entered_data)
        write_dict_to_excel(app.config['UPLOAD_FOLDER'], 'assets', entered_data)
        #print("test 1")
        #print("Entered data:", entered_data)
        flash("Data entered successfully", "success")

    if request.method == 'POST' and not form.validate_on_submit():
        flash('There was an issue uploading your data, please try again', 'danger')

    total_assets = 0
    for key in input_list:
        total_assets += int(app.config['ASSETS'][key])
    return render_template('pages/currentAssetValue.html', name=current_user.username, form=form, assets_data=app.config['ASSETS'], total_assets=total_assets)

@app.route('/simulatedGrowth')
@login_required
def simulatedGrowth():
    totalAssets = 0
    for value in app.config['ASSETS'].values():
            totalAssets += int(value)

    numYears = 10
    labels = []
    labels.append(totalAssets)
    print (numYears*12)
    for i in range(1,((numYears*12)+1)):
        labels.append(i)
    print(len(labels))
    SPdata = [] #S+P500 data
    Sdata = [] #savings data
    LRdata =[] #Low risk managed
    HRdata =[] #Hish Risk managed
    MSdata = [] #Modified savings data

    assetStart=totalAssets
    #ticker = 'AAPL'  # Example ticker
    ticker = '^SP500TR'
    from dateutil import parser

    # Parse date strings into datetime objects
    start_date = parser.parse("2000-01-01")
    end_date = parser.parse("2023-01-01")

    # Format datetime objects as strings
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")


    stock_data_html, stock_data = fetch_stock_data(ticker, start_date, end_date)
    var1=stock_data.resample('M').last().pct_change().mean().values[0]
    var2=stock_data.resample('M').last().pct_change().std().values[0]
    np.random.seed(seed=25)
    SPdata.append(assetStart)
    LRdata.append(assetStart)
    Sdata.append(assetStart)
    HRdata.append(assetStart)
    MSdata.append(assetStart)
    SP_asset_val = assetStart
    LR_asset_val = assetStart
    S_asset_val = assetStart
    HR_asset_val = assetStart
    MS_asset_val = assetStart
    for i in  range(len(labels)):
        market_return = np.random.normal(var1, var2,1)[0]
        #SPreturn = assetStart * (1+ market_return)
        SP_asset_val *= (1+ market_return)
        SPdata.append(SP_asset_val)
        LR_asset_val *= (1 + ((np.random.normal(0.65, 0.35,1)[0]/12)/100))
        LRdata.append(LR_asset_val)
        if i < 12:
            S_asset_val *= (1 + ((np.random.normal(7, 4,1)[0]/12)/100))
        else:
            S_asset_val *= (1 + ((np.random.normal(2, 2,1)[0]/12)/100))
        Sdata.append(S_asset_val)
        HR_asset_val *= (1+ ((np.random.normal(7, 20,1)[0]/12)/100))
        HRdata.append(HR_asset_val)
        MS_asset_val *= (1+ ((np.random.normal(7, 7,1)[0]/12)/100))
        MSdata.append(MS_asset_val)
    return render_template('pages/simulatedGrowth.html', name=current_user.username, stock_table = stock_data_html, labels=labels, SPdata=SPdata, Sdata=Sdata, LRdata=LRdata, HRdata=HRdata, MSdata=MSdata)

def toolsCardContent():
    #This function will return all the card contents that are available. 

    print("add function")


@app.route('/double_form', methods=['GET', 'POST'])
@login_required
def double_form():
    form1 = Form1(request.form)
    form2 = Form2(request.form)
    card_content1 = None
    card_content2 = None

    if request.method == 'POST':
        if form1.validate():
            field1_value = form1.field1.data
            card_content1 = f'New savings goal: {field1_value}'
            app.config['RETIREMENT']['Retirement Age'] = field1_value
            write_dict_to_excel(app.config['UPLOAD_FOLDER'], 'retirement', app.config['RETIREMENT'])
            old_savings = app.config['SAVINGS']['Saving Goal']
            card_content2 = f'Previous savings goal: {old_savings}'
        elif form2.validate():
            field2_value = form2.field2.data
            card_content2 = f'New desired retirement age: {field2_value}'
            app.config['SAVINGS']['Saving Goal'] = field2_value
            write_dict_to_excel(app.config['UPLOAD_FOLDER'], 'savings', app.config['SAVINGS'])
            old_retirement = app.config['RETIREMENT']['Retirement Age']
            card_content1 = f'Previous retirement goal: {old_retirement}'

    
    return render_template('pages/doubleForm.html', form1=form1, form2=form2, card_content1=card_content1, card_content2=card_content2)

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
            if sha256_crypt.verify(form.password.data, user.password):
                login_user(user, remember=form.remember.data)
                username = current_user.username
                upload_folder_path = os.path.join('Wealth_Managment_Tool/upload_folder', username, f'{username}_values.xlsx')
                # Set the UPLOAD_FOLDER configuration
                app.config['UPLOAD_FOLDER'] = upload_folder_path
                listOfDictionaries = excel_to_dict(app.config['UPLOAD_FOLDER'])
                app.config['ASSETS'] = listOfDictionaries['assets'][0]
                app.config['CREDITS'] = listOfDictionaries['credits'][0]
                """app.config['RETIREMENT'] = listOfDictionaries['retirement'][0]
                app.config['SAVINGS'] = listOfDictionaries['savings'][0]"""
                app.config['FINANCE_PATH'] = os.path.join('Wealth_Managment_Tool/SimulatedFinanceData/', username)
                app.config['BUDGET'] = []
                #print(assets)
                #print(credits)
                flash("Welcome "+ str(current_user.username)+", you have been logged in.", 'success')
                return redirect(url_for('dashboard'))

        flash("Incorrect Username or Password", "danger")
        #return '<h1>Invalid Username or Password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return  render_template('login/login.html',form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = sha256_crypt.hash(form.password.data)
        print(hashed_password)
        username = form.username.data
        email = form.email.data
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already in use, please try again', 'danger')
        else:
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            username = form.username.data
            upload_folder_path = os.path.join('Wealth_Managment_Tool/upload_folder', username)
            

            # Ensure the folder exists (create it if it doesn't)
            os.makedirs(upload_folder_path, exist_ok=True)
            upload_folder_path = os.path.join(upload_folder_path, f'{username}_values.xlsx')
            # Set the UPLOAD_FOLDER configuration
            app.config['UPLOAD_FOLDER'] = upload_folder_path
            asset_column_names = ['House', 'Car', 'Investments', 'Checking Account', 'Stocks', 'Savings', 'Retirement Accounts']
            credit_column_names = ['Rent', 'Mortgage', 'Utilities', 'Food and Groceries', 'Car Payments', 'Student loan Payments', 'Pension', 'Subscriptions', 'Health Insurance', 'House Insurance', 'Other Insurance']

            sheet_data = {
                'credits': credit_column_names,  # List for 'credits' sheet
                'assets': asset_column_names,      # List for 'assets' sheet
            }

            
            create_excel_file(app.config['UPLOAD_FOLDER'], sheet_data=sheet_data)
            finance_path = 'Wealth_Managment_Tool/SimulatedFinanceData/' + username
            os.makedirs(finance_path, exist_ok=True)

            generator = FinanceDataGenerator()
            generator.generate_and_save_json(finance_path + '/current_account_transactions.json')

            generator = CreditCardDataGenerator()
            generator.generate_and_save_json(finance_path + '/credit_card_transactions.json')
            app.config['FINANCE_PATH'] = finance_path

            flash('New User Created', 'success')
            return redirect(url_for('login'))
            #return '<h1>' + form.email.data + ' ' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login/register.html',form=form)

@app.route('/upload',  methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = file.filename
        file.save('Wealth_Managment_Tool/upload_folder', current_user.username, 'banking_data' + filename)
        flash('File uploaded successfully', 'success')
        return redirect('/upload')  # Redirect to the same page after successful upload
    return render_template('pages/uploadForm.html', form=form)

@app.route('/transactions')
@login_required
def transactions():
    # Read data from JSON files for both account and credit card

    accounts_path = os.path.join(app.config['FINANCE_PATH'],'current_account_transactions.json')
    print (accounts_path)
    credits_path = os.path.join(app.config['FINANCE_PATH'], 'credit_card_transactions.json')
    print (credits_path)

    with open(accounts_path, 'r') as f:
        account_data = json.load(f)

    with open(credits_path, 'r') as f:
        credit_card_data = json.load(f)

    
    account_info = account_data['account']
    account_transactions_data = account_data['transactions']

    
    credit_card_info = credit_card_data['account']
    credit_card_transactions_data = credit_card_data['transactions']

    
    account = Account(
        account_number=account_info['account_number'],
        sort_code=account_info['sort_code'],
        balance=account_info['balance'],
        currency=account_info['currency'],
        account_holder=account_info['account_holder'],
        transactions=[Transaction(**txn_data) for txn_data in account_transactions_data],
    )

    
    credit_card = CreditCard(
        card_number=credit_card_info['card_number'],
        expiry_date=credit_card_info['expiry_date'],
        card_holder=credit_card_info['card_holder'],
        credit_limit=credit_card_info['credit_limit'],
        currency=credit_card_info['currency'],
        transactions=[Transaction(**txn_data) for txn_data in credit_card_transactions_data],
    )


    account_dict = account.to_dict()
    credit_card_dict = credit_card.to_dict()
    account_balances = [transaction.balance for transaction in account.transactions] 
    #print(account_balances)
    balances_labels = []
    counter = 1
    for transaction in account_balances:
        balances_labels.append(counter)
        counter += 1
    credit_balances = [transaction.balance for transaction in credit_card.transactions]
    #print(credit_balances)
    

    # Render HTML template with both account and credit card information
    return render_template('pages/transactions.html', current_account=account_dict, credit_card=credit_card_dict, name=current_user.username, account_balances=account_balances, credit_balances=credit_balances, balances_labels=balances_labels)

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

"""@app.route('/capitalOne', methods=['GET', 'POST'])
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
    params = {
        'grant_type': 'authorization_code',
        'client_id': 'oauth2client_0000AdfM5AeMUPFJkXTHnt',
        'client_secret': 'mnzconf.libMV5WRpToEiz+Q64aUwZCWMLUcr110p4OSgvEY5TwSxT+SoX0xcsM7fC0fciBUrBYZIkCFLj4akwpF2qpkwQ==',
        'redirect_uri': 'http://localhost',
        'code': authorization_code
    }
    try:
        response = requests.post("https://api.monzo.com/oauth2/token", data=params)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        access_token = response.json().get('access_token')
        if access_token:
            response = requests.get("https://api.monzo.com/balance?account_id=user_00009hPDVBoQ6BJJXislbV", headers={"Authorization": f"Bearer {access_token}"})
            response.raise_for_status()  # Raise an exception for non-200 status codes
            return jsonify(response.json())
        else:
            return jsonify({"error": "Access token not found"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/testApi', methods=['GET', 'POST'])
@login_required
def testCPIAPI():
    import requests

    country = 'Germany'
    api_url = 'https://api.api-ninjas.com/v1/inflation?country={}'.format(country)
    response = requests.get(api_url, headers={'X-Api-Key': 'baNTxUroHJT09t2ktLHXdg==u72J9wP5Y5WKyduy'})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)

    return redirect(url_for('dashboard'))"""


@app.route('/savingsForm', methods=['GET', 'POST'])
@login_required
def savingsForm():
    savings_form_year = SavingsCalculatorYear(request.form)
    savings_form_amount = SavingsCalculatorAmount(request.form)
    year_content_card = None
    amount_content_card = None
    if request.method == "POST": 
        if savings_form_year.validate_on_submit():
            savings_goal = savings_form_year.savings_goal.data
            current_savings = savings_form_year.current_held_savings.data
            annual_interest_rate = savings_form_year.annual_interest_rate.data
            savings_per_month = savings_form_year.saving_per_month.data

            num_months = 0
            while current_savings < savings_goal:
                num_months += 1
                current_savings += savings_per_month
                current_savings *= (((annual_interest_rate/12)/100)+1)
            #print(num_months)
            num_months = int(num_months)
            year_content_card = "The number of months it would take to save £{:.2f}, saving £{:.2f} per month, would be {} month/s.".format(savings_goal, savings_per_month, num_months)
        elif savings_form_amount.validate_on_submit():
            savings_goal = savings_form_amount.savings_goal.data
            current_savings = savings_form_amount.current_held_savings.data
            annual_interest_rate = savings_form_amount.annual_interest_rate.data
            years_to_save = savings_form_amount.years_to_save.data

            savings_goal -= current_savings
            months_to_save = years_to_save * 12
            amount_per_month = (savings_goal/months_to_save) * (1-(annual_interest_rate/100))
            #print(amount_per_month)
            amount_content_card = "The amount you would need to save each month to reach your goal of £{:.2f}, in {} years is: £{:.2f} per month".format(savings_goal, years_to_save, amount_per_month)
    return render_template('pages/savingsForm.html', savings_form_amount=savings_form_amount, savings_form_year=savings_form_year, year_content_card=year_content_card, amount_content_card=amount_content_card,name=current_user.username)

def calculate_monthly_contribution(current_age, desired_retirement_age, current_savings, expected_annual_return, desired_annual_income):
    # Calculate the number of years until retirement
    years_until_retirement = desired_retirement_age - current_age
    #print(years_until_retirement)
    
    # Convert the expected annual return to a decimal
    expected_annual_return_decimal = expected_annual_return / 100
    #print(expected_annual_return_decimal)
    
    # Calculate the future value of the retirement savings
    future_value = desired_annual_income / expected_annual_return_decimal
    #print(future_value)
    
    
    #how much needed to save
    monthly_contribution = (((future_value/(years_until_retirement*(expected_annual_return_decimal+1)**years_until_retirement))-current_savings)/12)
    
    return monthly_contribution

@app.route('/retirementForm', methods=['GET', 'POST'])
@login_required
def retirementForm():
    retirement_form = Retirement(request.form)
    retirement_content = None
    totalCredits = None
    if request.method == "POST":
        if retirement_form.validate_on_submit():
            current_age = retirement_form.current_age.data
            desired_retirement_age = retirement_form.desired_retirement_age.data
            current_savings = retirement_form.current_savings.data
            expected_annual_return = retirement_form.expected_annual_return.data
            desired_annual_income = retirement_form.desired_annual_income.data

            monthly_contribution = calculate_monthly_contribution(current_age, desired_retirement_age, current_savings, expected_annual_return, desired_annual_income)

            #print("You need to save approximately {:.2f} per month to reach your desired annual income in retirement of {:.2f}.".format(monthly_contribution, desired_annual_income))
            retirement_content = "You need to save approximately £{:.2f} per month to reach your desired annual income in retirement of £{:.2f}.".format(monthly_contribution, desired_annual_income)
            totalCredits = 0
            #print(app.config['CREDITS'])
            for key in app.config['CREDITS'].keys():
                if key != "Rent" and key != "Mortgage":
                    totalCredits += int(app.config['CREDITS'][key])
    return render_template('pages/retirementForm.html', retirement_form=retirement_form, name=current_user.username, retirement_content=retirement_content, totalCredits=totalCredits)

def calculate_tax(yearly_income, over_state_pension_age, blind):
    PA = 12570 #Basic personal allowance 2023/24
    yearly_income = float(yearly_income)
    if blind:
        #2023/24, blind add 2870 to PA
        PA += 2870
    if yearly_income > 125140:
        PA = 0
    elif yearly_income>= 100000 and yearly_income<=125140:
        #For every 2 pounds earnt over 100000 and less than 125140, £1 taken off PA
        incomeOverHundredThousand = yearly_income-100000
        incomeOverHundredThousand /= 2
        PA -= incomeOverHundredThousand
    
    tax = 0
    # Basic rate
    basic_rate_threshold = 50270  # £50,270
    basic_rate = 0.2

    # Higher rate
    higher_rate_threshold = 125140  # £125,140
    higher_rate = 0.4

    # Additional rate
    additional_rate = 0.45

    print ("PA: "+str(PA))
    if yearly_income <= PA:
        tax = 0
    elif PA < yearly_income <= basic_rate_threshold:
        tax = (yearly_income - PA) * basic_rate
    elif basic_rate_threshold < yearly_income <= higher_rate_threshold:
        basic_tax = (basic_rate_threshold - PA) * basic_rate
        tax = basic_tax + ((yearly_income - basic_rate_threshold) * higher_rate)
    else:
        basic_tax = (basic_rate_threshold - PA) * basic_rate
        higher_tax = (higher_rate_threshold - basic_rate_threshold) * higher_rate
        tax = basic_tax + higher_tax + (yearly_income - higher_rate_threshold) * additional_rate

    return Decimal(tax)

def calculate_national_insurance(yearly_earnings, state_pension_age):
    income = float(yearly_earnings)
    weekly_earnings = income/52
    print("weekly earnings"+str(weekly_earnings))
    NI = 0
    if weekly_earnings < 242:
        NI = 0
    elif 242 < weekly_earnings < 967:
        lowerRate = (weekly_earnings - 242) * 0.08
        NI = lowerRate
    else:
        lowerRate = (967-242.01) * 0.1
        higherRate = (weekly_earnings-967) * 0.02
        NI = lowerRate + higherRate
    NI *= 52
    if state_pension_age:
        NI = 0
    return Decimal(NI)

@app.route('/incomeTaxCalculator', methods=['GET', 'POST'])
@login_required
def incomeTaxCalculator():
    UK_income_tax_calculator_form = UKTaxCalculatorForm(request.form)
    tax_content = None
    user_finances = None
    if request.method=="POST":
        if UK_income_tax_calculator_form.validate_on_submit():
            yearly_earnings = Decimal(UK_income_tax_calculator_form.yearly_earnings.data)
            over_state_pension_age = UK_income_tax_calculator_form.over_state_pension_age.data
            blind = UK_income_tax_calculator_form.blind.data
            tax_amount = calculate_tax(yearly_income=yearly_earnings, over_state_pension_age=over_state_pension_age, blind=blind)
            national_insurance = calculate_national_insurance(yearly_earnings=yearly_earnings, state_pension_age=over_state_pension_age)
            user_finances = [tax_amount, national_insurance, (yearly_earnings-(tax_amount+national_insurance))]
            print("For a yearly income of £{:.2f}, you need to pay £{:.2f}, in income tax a year. You will also pay £{:.2f} in national insurance".format(yearly_earnings, tax_amount, national_insurance))
            tax_content = "For a yearly income of £{:.2f}, you need to pay £{:.2f}, in income tax a year. You will also pay £{:.2f} in national insurance".format(yearly_earnings, tax_amount, national_insurance)
            #scottish_tax_payer = UK_income_tax_calculator_form.scottish_tax_payer.data

    return render_template('pages/incomeTaxForm.html', UK_income_tax_calculator_form=UK_income_tax_calculator_form, tax_content=tax_content,name=current_user.username, user_finances=user_finances)

def calculateCapitalGains(purchase_price, sale_price, holding_period, cost_of_improvements, used_as_business, sq_metres):
    gain = sale_price-purchase_price
    tax_able_gain = gain - cost_of_improvements
    if gain <= 0:
        return "Because you sold your asset for the same or less than what you bought it for, there are ways you can offset the taxes you need to pay on other gains of the same type."
    if used_as_business or sq_metres:
        return "You may be subject to less relief on your gains, due to either having used the property as a business asset or it being too large. Visit the gov website for more detailed information"
    else:
        return "The taxable gain on the property is £{:.2f}, the amount of tax you pay will be determined by: holding period, your income and a few other factors. Visit the gov website for more detailed information".format(tax_able_gain)

@app.route('/capitalGainsForm', methods=['GET', 'POST'])
@login_required
def capitalGainsForm():
    capital_gains_calculator_form = CapitalGainsCalculator(request.form)
    capital_gains_content = None
    if request.method == "POST":
        if capital_gains_calculator_form.validate_on_submit():
            purchase_price = capital_gains_calculator_form.purchase_price.data
            sale_price = capital_gains_calculator_form.sale_price.data
            holding_period = capital_gains_calculator_form.holding_period.data
            cost_of_improvements = capital_gains_calculator_form.cost_of_improvements.data
            used_as_business = capital_gains_calculator_form.used_as_business.data
            sq_metres = capital_gains_calculator_form.sq_metres.data
            print(calculateCapitalGains(purchase_price=purchase_price, sale_price=sale_price, holding_period=holding_period, cost_of_improvements=cost_of_improvements, used_as_business=used_as_business, sq_metres=sq_metres))
            capital_gains_content = calculateCapitalGains(purchase_price=purchase_price, sale_price=sale_price, holding_period=holding_period, cost_of_improvements=cost_of_improvements, used_as_business=used_as_business, sq_metres=sq_metres)

    return render_template('pages/capitalGainsForm.html', capital_gains_calculator_form=capital_gains_calculator_form, capital_gains_content=capital_gains_content, name=current_user.username)

@app.route('/budgetPlanner', methods=['GET', 'POST'])
@login_required
def budgetPlanner():
    form = BudgetForm(request.form)
    total = 0
    if request.method == "POST":
        if form.validate_on_submit():
            if form.clear_table.data:
                app.config['BUDGET'] = []
            else:
                app.config['BUDGET'].append({'category': form.category.data, 'amount': form.amount.data})

    # Calculate total from budget data
    for item in app.config['BUDGET']:
        total += item['amount']
    for value in app.config['CREDITS'].values():
        total += value
        print(value)
    return render_template('pages/budgetPlanner.html', form=form, budget_data=app.config['BUDGET'], user_credit_keys=app.config['CREDITS'].keys(), user_credit=app.config['CREDITS'], total=total, name=current_user.username)

def mortgageRepaymentCalculator(loan_amount, interest_rate, loan_term, down_payment):
    principal = loan_amount - down_payment
    monthly_interest_rate = interest_rate / 100 / 12
    num_payments = loan_term * 12
    monthly_payment = (principal * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)
    return monthly_payment



@app.route('/mortgageRepayment', methods=['GET', 'POST'])
@login_required
def mortgageCalculator():
    form = MortgageForm(request.form)
    monthly_payment = None
    if request.method == "POST":
        if form.validate_on_submit():
            loan_amount = form.loan_amount.data
            #print(loan_amount)
            down_payment = form.down_payment.data
            if down_payment == None:
                down_payment = 0
            #print(down_payment)
            interest_rate = form.interest_rate.data
            #print(interest_rate)
            loan_term = form.loan_term.data
            #print(loan_term)
            monthly_payment = round(mortgageRepaymentCalculator(loan_amount, interest_rate, loan_term, down_payment), 2)
            #print(monthly_payment)

    return render_template('pages/mortgageRepayment.html', form=form, monthly_payment=monthly_payment, name=current_user.username)

def calculate_affordability(annual_income, monthly_debt, interest_rate, loan_term):
    monthly_income = annual_income / 12
    monthly_debt += 1  # Don;'t divide by 0
    max_mortgage = (monthly_income - monthly_debt) * (1 - (1 + interest_rate / 12) ** (-loan_term * 12)) / (interest_rate / 12)
    return max_mortgage

@app.route('/mortgageAffordability', methods=['GET', 'POST'])
@login_required
def mortgageAffordability():
    form = MortgageAffordabilityForm(request.form)
    max_mortgage = None
    if request.method == "POST":
        if form.validate_on_submit():
            annual_income = form.annual_income.data
            monthly_debt = form.monthly_debt.data
            interest_rate = form.interest_rate.data 
            if interest_rate == None:
                interest_rate = 3.6
            interest_rate /= 100
            loan_term = form.loan_term.data
            max_mortgage = calculate_affordability(annual_income, monthly_debt, interest_rate, loan_term)
    return render_template('pages/mortgageAffordability.html', form=form, max_mortgage=max_mortgage, name=current_user.username)

@app.route('/feedbackForm')
@login_required
def feedbackForm():
    return render_template('pages/feedbackFormPage.html', name=current_user.username)

@app.route('/tools')
@login_required
def tools():
    return render_template('pages/tools.html', name=current_user.username)
#with app.app_context():
    #db.drop_all()
    #db.create_all()
    #sample_user = User(username="test", email="test@test.com", password=generate_password_hash("password"))
    #db.session.add(sample_user)
    #db.session.commit()
    
    #users = User.query.all()
    #print("Print Statement")
    #print(users)
    #print("End print statement")

if __name__ == '__main__':
    app.run(debug=True)