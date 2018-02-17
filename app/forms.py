from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, \
EqualTo
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
    first_name = StringField('First name')
    middle_name = StringField('Middle name')
    last_name = StringField('Last name')
    submit = SubmitField('Submit')            