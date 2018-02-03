from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hi, not from the template"
    #return render_template('index.html')