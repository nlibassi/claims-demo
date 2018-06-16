from datetime import datetime
from app import db
from app import login
#from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt
from app import app

#add UserMixin back after BaseModel
class Insured(UserMixin, db.Model):
    #make id serial next time? but still populates itself this way
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    first_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    #test = db.Column(db.String(15))
    #tried to change gender to integer but it didn't change upon migration? try again later
    gender = db.Column(db.String(1))
    date_of_birth = db.Column(db.Date)
    air_id = db.Column(db.String(20))
    mailing_street = db.Column(db.String(64))
    mailing_optional = db.Column(db.String(64))
    mailing_city = db.Column(db.String(64))
    mailing_state = db.Column(db.String(15))
    mailing_zip = db.Column(db.String(10))
    mailing_country = db.Column(db.String(30))
    residence_country = db.Column(db.String(30))
    foreign_currency_default = db.Column(db.String(30))
    other_coverage = db.Column(db.String(1))
    other_insurance_co = db.Column(db.String(64))
    other_plan_name = db.Column(db.String(64))
    other_plan_id = db.Column(db.String(64))
    medicare_part_a = db.Column(db.String(1))
    medicare_part_b = db.Column(db.String(1))
    medicare_id = db.Column(db.String(64))
    full_time_student = db.Column(db.String(1))
    has_dependent = db.Column(db.String(1))
    #string_test = db.Column(db.String(1))
    #gender should be integer with lookup later, had issue with Integer
    #not a db field but high-level view of relationship 
    #between insureds and claims - a 'virtual field'
    claims = db.relationship('Claim', backref='author', lazy='dynamic')
    dependents = db.relationship('Dependent', backref='employee', lazy='dynamic')


    def __repr__(self):
        return '<Username {}>'.format(self.username)

    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], 
                algorithms=['HS256'])['reset_password']
        except:
            return
        return Insured.query.get(id)

        
class Dependent(db.Model):
    #make id serial next time? but still populates itself this way
    id = db.Column(db.Integer, primary_key=True)
    # will eventually add 'nullable=False' as another argument to Column
    insured_id = db.Column(db.Integer, db.ForeignKey('insured.id'), nullable=False)
    first_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    UniqueConstraint('insured_id', 'first_name', 'middle_name', 
        'last_name', name='unique_dependent_name_constraint')
    #test = db.Column(db.String(15))
    gender = db.Column(db.String(1))
    date_of_birth = db.Column(db.Date)
    relationship_to_insured = db.Column(db.String(1))
    full_time_student = db.Column(db.String(1))
    #gender should be integer with lookup later, had issue with Integer
    #not a db field but high-level view of relationship 
    #between insureds and claims - a 'virtual field'
    claims = db.relationship('Claim', backref='patient', lazy='dynamic')

    def __repr__(self):
        return '{} {} {}'.format(self.first_name, self.middle_name, self.last_name)


class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    insured_id = db.Column(db.Integer, db.ForeignKey('insured.id'), nullable=False)
    dependent_id = db.Column(db.Integer, db.ForeignKey('dependent.id'))
    diagnosis = db.Column(db.String(64))
    accident_employment = db.Column(db.String(1))
    accident_auto = db.Column(db.String(1))
    accident_other = db.Column(db.String(1))
    accident_date = db.Column(db.Date)
    accident_details = db.Column(db.String(64))
    service_type = db.Column(db.String(1))
    service_details = db.Column(db.String(64))
    service_date = db.Column(db.Date)
    service_currency = db.Column(db.String(30))
    # exch rate will be automatically populated based on selected date and currency
    service_exchange_rate = db.Column(db.Float())
    service_provider = db.Column(db.String(30))
    service_amount = db.Column(db.Float())
    # the image may need to be uploaded to the server rather than stored in the db
    #service_receipt = ??

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #change to insured_id here and elsewhere
    #user_id = db.Column(db.Integer, db.ForeignKey('insured.id'))

    def __repr__(self):
        return '<Claim {}>'.format(self.body)

# since login extension can't communicate with the 
# database (?) the application has to load a user
@login.user_loader
def load_user(id):
    # id that Flask-Login passes to the function is a string
    return Insured.query.get(int(id))
