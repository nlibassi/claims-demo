from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
SubmitField, DateField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, \
EqualTo
#3/10/18: not currently using QuerySelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Insured

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
    first_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    last_name = StringField('Last Name')
    test = StringField('Test')
    gender = SelectField(label='Gender', choices=[('f', 'Female'), ('m', 'Male'), ('o', 'Other')])
    date_of_birth = DateField('Date of Birth', format='%m/%d/%Y')
    air_id = StringField('AIR ID')
    #############
    mailing_street = StringField('Street Address')
    mailing_optional = StringField('Building (optional)')
    mailing_city = StringField('City')
    mailing_state = StringField('State')
    mailing_zip = StringField('Zip Code')
    #the following three will be replaced
    mailing_country = StringField('Country (Mailing)')
    residence_country = StringField('Country (Residence)')
    foreign_currency_default = StringField('Default Currency')
    """
    mailing_country = SelectField(label='Country (Mailing)', choices=countries)
    residence_country = SelectField(label='Country (Residence)', choices=countries)
    foreign_currency_default = SelectField(label='Default Currency', choices=currencies)
    """
    other_coverage = SelectField(label='Other Coverage?', choices=[('n', 'No'), ('y', 'Yes')])
    other_insurance_co = StringField('Other Insurance Company Name')
    other_plan_name = StringField('Other Insurance Plan Name')
    other_plan_id = StringField('Other Plan ID')
    medicare_part_a = SelectField(label='Coverage with Medicare Part A?', choices=[('n', 'No'), ('y', 'Yes')])
    medicare_part_b = SelectField(label='Coverage with Medicare Part B?', choices=[('n', 'No'), ('y', 'Yes')])
    medicare_id = StringField('Medicare ID')
    full_time_student = SelectField(label='Full-time Student?', choices=[('n', 'No'), ('y', 'Yes')])
    string_test = SelectField(label='String Test', choices=[('n', 'No'), ('y', 'Yes')])
    ##############
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
    test = StringField('Test')
    gender = StringField('Gender')
    #relationship_to_insured = StringField('Relationship to Employee')
    #date_of_birth = DateField('Date of Birth')
    submit = SubmitField('Submit')         

class FileClaimForm(FlaskForm):
    body = StringField('Claim Details')
    #relationship_to_insured = StringField('Relationship to Employee')
    #date_of_birth = DateField('Date of Birth')
    submit = SubmitField('Submit') 