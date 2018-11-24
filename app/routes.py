from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, \
EditDependentProfileForm, AddDependentForm, FileClaimForm, ClaimSearchForm
from flask_login import current_user, login_user, logout_user, login_required
#add Claim later
from app.models import Insured, Dependent, Claim
from werkzeug.urls import url_parse
from datetime import datetime
from werkzeug import secure_filename
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
import requests
from app.geography_dictionaries import currencies


def get_exchange_rate(date, foreign_currency):

    """
    INPUT:
        date: string in format '2008-11-04'
        currency: string in format 'TRY'
    OUTPUT:
        returns appropriate historical exchange rate as json (?)
    """

    api_key = 'f3c2a32e73c4784284b8ca33a4f30f95'
    print(foreign_currency)
    #returns 'TRY' from 'Turkish Lira' given as foreign_currency
    #foreign_currency_code = list(currencies.keys())[list(currencies.values()).index(foreign_currency)]

    params = {'access_key': api_key, 'date': date, 'currencies': foreign_currency, 'format': 1}

    # use 'live' in place of historical if desired
    r = requests.get('http://apilayer.net/api/historical', params = params)

    usd_to_foreign_currency = 'USD' + foreign_currency

    # is returned as float by default
    historical_quote = r.json()['quotes'][usd_to_foreign_currency]

    return historical_quote                                              


@app.route('/')
@app.route('/index')
@login_required
def index():
    insured = Insured.query.filter_by(username=current_user.username).first_or_404()
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

    dependents_list = list(Dependent.query.filter_by(insured_id=current_user.id))
    dependents  = []
    for d in dependents_list:
        dependents.append({'full_name': d})

    patients = [d for d in dependents]
    patients.append({'full_name': '{} {} {}'.format(insured.first_name, insured.middle_name, \
     insured.last_name)})

    search = ClaimSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
   
    return render_template('index.html', title='Home', posts=posts, patients=patients, form=search)
     

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
    dependents_list = list(Dependent.query.filter_by(insured_id=current_user.id))
    dependents  = []
    for d in dependents_list:
        dependents.append({'full_name': d})
    #print('Dependents: {}'.format(dependents_list))

    #patients = dependents
    patients = [d for d in dependents]
    patients.append({'full_name': '{} {} {}'.format(insured.first_name, insured.middle_name, \
     insured.last_name)})
    #print('Patients: {}'.format(patients))

    return render_template('insured.html', insured=insured, posts=posts, \
        dependents=dependents, patients=patients)

#def dependent(username_dependent_id)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()   

#why not /user/edit_profile?
@app.route('/edit_profile', methods=['GET', 'POST']) 
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.middle_name = form.middle_name.data
        current_user.last_name = form.last_name.data
        #current_user.test = form.test.data
        current_user.gender = form.gender.data
        current_user.date_of_birth = form.date_of_birth.data
        current_user.air_id = form.air_id.data
        current_user.mailing_street = form.mailing_street.data
        current_user.mailing_optional = form.mailing_optional.data
        current_user.mailing_city = form.mailing_city.data
        current_user.mailing_state = form.mailing_state.data
        current_user.mailing_zip = form.mailing_zip.data
        #current_user.mailing_country = form.mailing_country.data
        current_user.residence_country = form.residence_country.data
        current_user.foreign_currency_default = form.foreign_currency_default.data
        current_user.other_coverage = form.other_coverage.data
        current_user.other_insurance_co = form.other_insurance_co.data
        current_user.other_plan_name = form.other_plan_name.data
        current_user.other_plan_id = form.other_plan_id.data
        current_user.medicare_part_a = form.medicare_part_a.data
        current_user.medicare_part_b = form.medicare_part_b.data
        current_user.medicare_id = form.medicare_id.data
        current_user.full_time_student = form.full_time_student.data
        #current_user.string_test = form.string_test.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.middle_name.data = current_user.middle_name
        form.last_name.data = current_user.last_name
        #form.test.data = current_user.test
        form.gender.data = current_user.gender
        form.date_of_birth.data = current_user.date_of_birth
        form.air_id.data = current_user.air_id
        form.mailing_street.data = current_user.mailing_street
        form.mailing_optional.data = current_user.mailing_optional
        form.mailing_city.data = current_user.mailing_city
        form.mailing_state.data = current_user.mailing_state
        form.mailing_zip.data = current_user.mailing_zip
        #form.mailing_country.data = current_user.mailing_country
        form.residence_country.data = current_user.residence_country
        form.foreign_currency_default.data = current_user.foreign_currency_default
        form.other_coverage.data = current_user.other_coverage
        form.other_insurance_co.data = current_user.other_insurance_co
        form.other_plan_name.data = current_user.other_plan_name
        form.other_plan_id.data = current_user.other_plan_id
        form.medicare_part_a.data = current_user.medicare_part_a
        form.medicare_part_b.data = current_user.medicare_part_b
        form.medicare_id.data = current_user.medicare_id
        form.full_time_student.data = current_user.full_time_student
        #form.string_test.data = current_user.string_test
    return render_template('edit_profile.html', title='Edit Profile', form=form)

#@login_required
@app.route('/add_dependent', methods=['GET', 'POST'])
def add_dependent():
    #insured = Insured.query.filter_by(username=username).first_or_404()
    form = AddDependentForm()
    if form.validate_on_submit():
        dependent = Dependent(first_name=form.first_name.data, 
            middle_name=form.middle_name.data, last_name=form.last_name.data,
            insured_id=current_user.id)
        insured = Insured.query.filter_by(id=current_user.id).first_or_404()
        insured.has_dependent = 'y'
        db.session.add(dependent)
        db.session.commit()
        #current_user.has_dependent = True

        #flash('{} {}'.format(insured.has_dependent, insured.first_name))
        #flash('{} {} {}'.format(insured.has_dependent, insured.first_name, insured.last_name))
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
    # result of this query is just the repr containing first, middle, and last name unless we use .first()
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
        #dependent.test = form.test.data
        dependent.gender = form.gender.data
        dependent.date_of_birth = form.date_of_birth.data
        dependent.relationship_to_insured = form.relationship_to_insured.data
        dependent.full_time_student = form.full_time_student.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_dependent_profile', dependent_name=dependent_name))
    elif request.method == 'GET':
        form.first_name.data = dependent_name_first
        form.middle_name.data = dependent_name_middle
        form.last_name.data = dependent_name_last
        #form.test.data = dependent.test
        form.gender.data = dependent.gender
        form.date_of_birth.data = dependent.date_of_birth
        form.relationship_to_insured.data = dependent.relationship_to_insured
        form.full_time_student.data = dependent.full_time_student
    
    return render_template('edit_dependent_profile.html', title='Edit Dependent Profile', \
        form=form, dependent=dependent, dependent_name=dependent_name)


@app.route('/file_claim/<patient_name>', methods=['GET', 'POST']) 
def file_claim(patient_name):
    form = FileClaimForm()
    patient_name_first = patient_name.split(' ')[0]
    patient_name_middle = patient_name.split(' ')[1]
    patient_name_last = patient_name.split(' ')[2]
    try:
        patient = Dependent.query. \
                filter_by(first_name=patient_name_first, \
                    middle_name=patient_name_middle, \
                    last_name=patient_name_last).first()
        print('Patient id is {}'.format(patient.id))
        print(patient.insured_id)
        claim = Claim(insured_id=current_user.id, dependent_id=patient.id)
        claim_pre_reqs = [patient.gender, patient.date_of_birth, patient.relationship_to_insured, patient.full_time_student]
        #patient_type = 'dependent'
        #incomplete_profile_redirect = 'edit_dependent_profile' #finish
        if all(p is not None for p in claim_pre_reqs):
            db.session.add(claim)
        else:
            flash('Please complete profile for dependent before filing claim.')
            return redirect(url_for('edit_dependent_profile', dependent_name=patient_name))
    except:
        patient = Insured.query. \
            filter_by(first_name=patient_name_first, \
                middle_name=patient_name_middle, \
                last_name=patient_name_last).first()
        claim = Claim(insured_id=current_user.id)
        db.session.add(claim)
    
    #dependents_list = list(Dependent.query.filter(Dependent.insured_id==current_user.id))

    #query db using dependent argument and update db that way
    if form.validate_on_submit():
        claim.diagnosis = form.diagnosis.data
        claim.accident_employment = form.accident_employment.data
        claim.accident_auto = form.accident_auto.data
        claim.accident_other = form.accident_other.data
        claim.accident_date = form.accident_date.data
        claim.accident_details = form.accident_details.data
        claim.service_type = form.service_type.data
        claim.service_details = form.service_details.data
        claim.service_date = form.service_date.data
        claim.service_currency = form.service_currency.data
        claim.service_exchange_rate = get_exchange_rate(claim.service_date, claim.service_currency)
        claim.service_provider = form.service_provider.data
        claim.service_amount = form.service_amount.data
        #claim.service_receipt = form.service_receipt.data
        db.session.commit()

        """
        f = request.files['receipt']
        f.save(secure_filename(f.filename))
        """
        flash('Your claim information has been submitted. Please submit associated receipt.')
        #return redirect(url_for('file_claim',  patient_name=patient_name))
        return redirect(url_for('upload_receipt'))
    elif request.method == 'GET':
        form.diagnosis.data = claim.diagnosis
        form.accident_employment.data = claim.accident_employment
        form.accident_auto.data = claim.accident_auto
        form.accident_other.data = claim.accident_other
        form.accident_date.data = claim.accident_date
        form.accident_details.data = claim.accident_details
        form.service_type.data = claim.service_type
        form.service_details.data = claim.service_details
        form.service_date.data = claim.service_date
        form.service_currency.data = current_user.foreign_currency_default
        #if claim.service_exchange_rate: 
            #form.service_exchange_rate = claim.service_exchange_rate
        form.service_provider.data = claim.service_provider
        form.service_amount.data = claim.service_amount
        #form.service_receipt.data = claim.service_receipt
    
    return render_template('file_claim.html', title='File Claim', \
        form=form, patient=patient, patient_name=patient_name)

"""
#original "worked" per the front end only but didn't use /upload page
# actually, could have only added the receipt-related buttons to html as this wasn't doing anything
# never even tried going to /upload page
@app.route('/upload', methods=['POST'])
def upload_receipt():
    if request.method == 'POST':
        file = request.files['image']
        f = os.path.join('/home/nlibassi/claims-demo-uploads', file.filename)
        # add code to check that the uploaded file is not malicious
        file.save(f)

    return render_template('file_claim.html')    
"""

@app.route('/upload_receipt', methods=['GET', 'POST'])
def upload_receipt():
    if request.method == 'POST':
        f = request.files['receipt']
        f.save(secure_filename(f.filename))
        flash('Your claim has been submitted.')
        return redirect(url_for('index'))

    return render_template('upload_receipt.html')   


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        insured = Insured.query.filter_by(email=form.email.data).first()
        if insured:
            send_password_reset_email(insured)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)    

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    insured = Insured.verify_reset_password_token(token)
    if not insured:
        return redirect(url_for('index'))
    form = ResetPasswordForm
    if form.validate_on_submit():
        insured.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)   


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search.data['search'] == '':
        query = db_session.query(Claim)
        results = query.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=results)