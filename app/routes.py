from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, \
EditDependentProfileForm, AddDependentForm
from flask_login import current_user, login_user, logout_user, login_required
#add Claim later
from app.models import Insured, Dependent
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    # below used as test before having traditional users and posts
    #user = {'username': 'Nick'}
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
    """
    #temporary test dependents
    dependents = [
        {
            'full_name' : 'John Bill Smith'
        }, 
        {
            'full_name' : 'Bo John Smith'
        }
    ]

    """
    dependents_list = list(Dependent.query.filter(Dependent.insured_id==current_user.id))
    dependents  = []
    for d in dependents_list:
        dependents.append({'full_name': d})
    
    return render_template('insured.html', insured=insured, posts=posts, dependents=dependents)

#def dependent(username_dependent_id)

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
        current_user.first_name = form.first_name.data
        current_user.middle_name = form.middle_name.data
        current_user.last_name = form.last_name.data
        current_user.test = form.test.data
        current_user.gender = form.gender.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.middle_name.data = current_user.middle_name
        form.last_name.data = current_user.last_name
        form.test.data = current_user.test
        form.gender.data = current_user.gender
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/add_dependent', methods=['GET', 'POST'])
def add_dependent():
    form = AddDependentForm()
    if form.validate_on_submit():
        dependent = Dependent(first_name=form.first_name.data, 
            middle_name=form.middle_name.data, last_name=form.last_name.data,
            insured_id = current_user.id)
        if current_user.has_dependent == 0:
            current_user.has_dependent = 1
        db.session.add(dependent)
        db.session.commit()
        flash('{} {} {} has been added as a dependent'.format(dependent.first_name, 
            dependent.middle_name, dependent.last_name))
        return redirect(url_for('add_dependent'))
        #return redirect(url_for('edit_dependent_profile'))
    return render_template('add_dependent.html', title='Add Dependent', form=form)


# needs to be rewritten
#may need to define variables using current_user.dependent<id>.first_name etc
@app.route('/edit_dependent_profile/<dependent_name>', methods=['GET', 'POST']) 
def edit_dependent_profile(dependent_name):
    form = EditDependentProfileForm()
    dependent_name_first = dependent_name.split(' ')[0]
    dependent_name_middle = dependent_name.split(' ')[1]
    dependent_name_last = dependent_name.split(' ')[2]
    # result of this query is just the repr containing first, middle, and last name; not accessing 
    # the db record in this way
    dependent = Dependent.query. \
        filter(Dependent.first_name==dependent_name_first and \
            Dependent.middle_name==dependent_name_middle and \
            Dependent.last_name==dependent_name_last).first()

    #dependents_list = list(Dependent.query.filter(Dependent.insured_id==current_user.id))

    #query db using dependent argument and update db that way
    if form.validate_on_submit():
        dependent.first_name = form.first_name.data
        dependent.middle_name = form.middle_name.data
        dependent.last_name = form.last_name.data
        dependent.test = form.test.data
        dependent.gender = form.gender.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_dependent_profile', dependent_name=dependent_name))
    elif request.method == 'GET':
        form.first_name.data = dependent_name_first
        form.middle_name.data = dependent_name_middle
        form.last_name.data = dependent_name_last
        form.test.data = dependent.test
        form.gender.data = dependent.gender
    
    return render_template('edit_dependent_profile.html', title='Edit Dependent Profile', \
        form=form, dependent=dependent, dependent_name=dependent_name)
  