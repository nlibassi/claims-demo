#from flask import Flask
from flask import Flask, flash, redirect, render_template, \
    request, session, abort
from flask.ext.sqlalchemy import SQLAlchemy
"""
#have not yet installed these
from flask.ext.security import current_user, login_required, \
    RoleMixin, Security, SQLAlchemyUserDatastore, UserMixin, \
    utils

from flask_mail import Mail
from flask.ext.admin import Admin
from flask.ext.admin.contrib import sqla

from wtforms.fields import PasswordField
"""
import os

app = Flask(__name__)
#ensure use of correct environment variables depending on where the app is run from
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#mail = Mail(app)
db = SQLAlchemy(app)

from models import BaseModel, Insured

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

#@app.route('/register', methods=['POST'])
#def 

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()

"""
@app.route('/')
def hello():
    return "Hey!"

@app.route('/<name>')
def hello_name(name):
    return "Hey {}!".format(name)
"""
#print(os.environ['APP_SETTINGS'])

if __name__ == '__main__':
    app.run()