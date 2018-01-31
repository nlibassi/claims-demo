from app import db
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        #used for querying database
        return self.__dict__

class Insured(BaseModel, db.Model):
    __tablename__ = 'insureds'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #necessary for inserting records locally using python
    def __init__(self,  id, first_name, last_name, email, *args):
      self.id = id
      self.first_name = first_name
      self.last_name = last_name
      self.email = email
      #self.password = password