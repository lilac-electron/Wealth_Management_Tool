from flask import Flask, render_template
import pandas as pd
from flask import render_template

df = pd.read_excel('example.xlsx', sheet_name='Sheet1')
#print(df)
app = Flask(__name__)

@app.route('/test')
def hello_world():
   #return df.to_html(header="true", table_id="table")
   return render_template("auth/index.php")

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug = True)