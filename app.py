
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class MyForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()

    if form.validate_on_submit():
        # Access form data here (e.g., form.name.data, form.email.data)
        return "Form submitted with Name: {form.name.data}, Email: {form.email.data}"

    #return render_template('auth/index(redundant).html', form=form)

    return render_template('index.html', form=form)

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


if __name__ == '__main__':
    app.run(debug=True)