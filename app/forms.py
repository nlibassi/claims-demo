#forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
SubmitField, DateField, SelectField, FileField, DecimalField
#not using Required right now, look into it
from wtforms.validators import ValidationError, DataRequired, Email, \
EqualTo, InputRequired, Required, Optional
#3/10/18: not currently using QuerySelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Insured
from app.geography_lists import us_states, countries, currencies
#not sure if it's a good idea to import current_user here:
#from flask_login import current_user

"""
class RequiredIf(Required):
    # a validator which makes a field required if
    # another field is set and has a truthy value
    #https://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)
"""

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),
        EqualTo('password')])
    submit = SubmitField('Register')

    #comment out validate_username() and/or validate_email() functions to test error handling (or lack thereof)
    #changed 'user' to 'insured' here for consistency with routes.py
    def validate_username(self, username):
        insured = Insured.query.filter_by(username=username.data).first()
        if insured is not None:
            raise ValidationError('Please use a different username')
    

    def validate_email(self, email):
        insured =  Insured.query.filter_by(email=email.data).first()
        if insured is not None:
            raise ValidationError('Please use a different email address')
    
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    last_name = StringField('Last Name')
    #test = StringField('Test')
    gender = SelectField(label='Gender', choices=[(None, ''), ('f', 'Female'), ('m', 'Male')])
    date_of_birth = DateField('Date of Birth', format='%m/%d/%Y')
    air_id = StringField('Insured ID', validators=[DataRequired()])
    #############
    mailing_street = StringField('U.S. Mailing Street Address', validators=[DataRequired()])
    mailing_optional = StringField('Address 2 (Optional)')
    mailing_city = StringField('City', validators=[DataRequired()])
    mailing_state = SelectField(label='State', choices=us_states, validators=[DataRequired()])
    mailing_zip = StringField('Zip Code', validators=[DataRequired()])
    #the following three will be replaced
    #mailing_country = SelectField(label='Country (Mailing)', choices=countries)
    residence_country = SelectField(label='Country (Residence)', choices=countries, validators=[DataRequired()])
    foreign_currency_default = SelectField(label='Default Currency', choices=currencies, validators=[DataRequired()])
    """
    mailing_country = SelectField(label='Country (Mailing)', choices=countries)
    residence_country = SelectField(label='Country (Residence)', choices=countries)
    foreign_currency_default = SelectField(label='Default Currency', choices=currencies)
    """
    other_coverage = SelectField(label='Other Coverage?', choices=[(None, ''), ('n', 'No'), ('y', 'Yes')], validators=[DataRequired()])
    other_insurance_co = StringField('Other Insurance Company Name')
    other_plan_name = StringField('Other Insurance Plan Name')
    other_plan_id = StringField('Other Plan ID')
    medicare_part_a = SelectField(label='Coverage with Medicare Part A?', choices=[(None, ''), ('n', 'No'), ('y', 'Yes')], validators=[DataRequired()])
    medicare_part_b = SelectField(label='Coverage with Medicare Part B?', choices=[(None, ''), ('n', 'No'), ('y', 'Yes')], validators=[DataRequired()])
    #something like this could be done in routes (maybe) but not here
    #if medicare_part_a == 'Yes' or medicare_part_b == 'Yes':
        #medicare_id = StringField('Medicare ID', validators=[InputRequired()])
    #else:
    medicare_id = StringField('Medicare ID')
    #medicare_id = StringField('Medicare ID', validators=[RequiredIf('medicare_part_a')])
    full_time_student = SelectField(label='Full-time Student?', choices=[(None, ''), ('n', 'No'), ('y', 'Yes')], validators=[DataRequired()])
    #string_test = SelectField(label='String Test', choices=[('n', 'No'), ('y', 'Yes')])
    

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            insured = Insured.query.filter_by(username=self.username.data).first()
            if insured is not None:
                raise ValidationError('Please use a different username.')
    """
    # function below not working at all right now
    def validate(self):
        valid = True
        if not FlaskForm.validate(self):
            valid = False
        # can't even get an error with code below and  setting medicare_id equal to 1 in form
        if self.medicare_part_a == 'Yes' or self.medicare_part_b == 'Yes' and self.medicare_id == '1':
            self.email.medicare_id.append("Medicare ID is required")
            valid = False
        else:
            return valid
    """
    submit = SubmitField('Submit')   

class AddDependentForm(FlaskForm):
    first_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    last_name = StringField('Last Name')
    #relationship_to_insured = StringField('Relationship to Employee')
    #date_of_birth = DateField('Date of Birth')
    submit = SubmitField('Submit')  

class EditDependentProfileForm(FlaskForm):
    first_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    last_name = StringField('Last Name')
    #test = StringField('Test')
    gender = SelectField(label='Gender', choices=[(None, ''), ('f', 'Female'), ('m', 'Male')])
    date_of_birth = DateField('Date of Birth', format='%m/%d/%Y')
    relationship_to_insured = SelectField(label='Relationship to Employee', choices=[(None, ''), ('s', 'Spouse'), ('c', 'Child')])
    full_time_student = SelectField(label='Full-time Student?', choices=[(None, ''), ('n', 'No'), ('y', 'Yes')])
    #date_of_birth = DateField('Date of Birth')
    submit = SubmitField('Submit')         

class FileClaimForm(FlaskForm):
    diagnosis = StringField('Diagnosis or Type of Illness')
    accident_employment = SelectField(label='Was the service for an employment-related accident?', \
        choices=[('n', 'No'), ('y', 'Yes')], validators=[Optional()])
    accident_auto = SelectField(label='Was the service for an automobile accident?', \
        choices=[('n', 'No'), ('y', 'Yes')], validators=[Optional()])
    accident_other = SelectField(label='Was the service for any other accident or injury?', \
        choices=[('n', 'No'), ('y', 'Yes')], validators=[Optional()])
    accident_date = DateField(label='Accident Date', format='%m/%d/%Y', validators=[Optional()])
    accident_details = StringField('Details of Accident', validators=[Optional()])
    service_type = SelectField(label='Service Type', \
        choices=[('m', 'Medical'), ('d', 'Dental'), ('v', 'Vision'), ('h', 'Hearing'), ('r', 'Prescription')])
    service_details = StringField('Details of Service')
    service_date = DateField('Date of Service', format='%m/%d/%Y')
    #pre-populate
    service_currency = SelectField(label='Currency of Service', choices=currencies)
    #service_exchange_rate = DecimalField('Exchange Rate')
    service_provider = StringField('Service Provider')
    service_amount = StringField('Service Amount (in local currency - converted to USD automatically)')
    #service_receipt = FileField('Service Receipt')
    submit = SubmitField('Submit') 


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class ClaimSearchForm(FlaskForm):
    choices = [('First Name', 'First Name'),
                        ('Last Name', 'Last Name'),
                        ('Date of Service', 'Date of Service')]
    select = SelectField('Search for claim:', choices=choices)
    search = StringField('')