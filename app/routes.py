from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Insured
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Nick'}
    posts = [
        {
            'author' : {'username': 'John'},
            'body' : 'Beautiful day in Portland!'
        }, 
        {
            'author' : {'username' : 'Susan'},
            'body' : 'Testing another body'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        insured = Insured.query.filter_by(username=form.username.data).first()
        if insured is None or not insured.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(insured, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        insured = Insured(username=form.username.data, 
            email=form.email.data)
        insured.set_password(form.password.data)
        db.session.add(insured)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def insured(username):
    insured = Insured.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': insured, 'body': 'Test post #1'},
        {'author': insured, 'body': 'Test post #2'}
    ]
    return render_template('insured.html', insured=insured, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()   

#why not /user/edit_profile?
@app.route('/edit_profile', methods=['GET', 'POST']) 
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    #if form is being requested for the first time:
    elif request.method == 'GET':
        form.username.data = current_user.username
    #in case of validation error (in case of error in form data): (?)
    return render_template('edit_profile.html', title='Edit Profile', form=form)