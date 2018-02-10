from datetime import datetime
from app import db
#from app import login
#from sqlalchemy.dialects.postgresql import JSON
#from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import UserMixin

#add UserMixin back after BaseModel
class Insured(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #not a db field but high-level view of relationship 
    #between insureds and claims - a 'virtual field'
    claims = db.relationship('Claim', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    """
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    """

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('insured.id'))

    def __repr__(self):
        return '<Claim {}>'.format(self.body)
"""
@login.user_loader
def load_user(id):
    return Insured.query.get(int(id))
"""