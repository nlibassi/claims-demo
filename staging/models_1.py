from datetime import datetime
from app import db
#from app import login
#from sqlalchemy.dialects.postgresql import JSON
#from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import UserMixin

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        #used for querying database
        return self.__dict__

#add UserMixin back after BaseModel
class Insured(BaseModel, db.Model):
    __tablename__ = 'insureds'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    #skipping this as defined in base model (see real python tutorial)
    """
    def __repr__(self):
        return '<User {}>'.format(self.username)
    """
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #necessary for inserting records locally using python but try modify __init__() in 
    #BaseModel in future to avoid this (why is it not in M.G.'s tutorial?)
    def __init__(self,  id, username, email, *args):
      self.id = id
      self.username = username
      self.email = email
      #self.password_hash = password_hash

class Claim(BaseModel, db.Model):
    __tablename__ = 'claims'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('insureds.id'))

"""
@login.user_loader
def load_user(id):
    return Insured.query.get(int(id))
"""