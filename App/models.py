from sqlalchemy.orm import backref
from App import db, login_manager
from App import bcrypt
from flask_login import UserMixin
from datetime import datetime
import random
import string

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    ID = db.Column(db.Integer(), nullable=False, primary_key=True)
    Username = db.Column(db.String(length=30), nullable=False, unique=True)
    Email = db.Column(db.String(length=50), nullable=False, unique=True)
    Password = db.Column(db.String(length=60), nullable=False)

    """ @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.Password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.Password, attempted_password)  """

    def get_id(self):
           return (self.ID)


class Report(db.Model):
    No = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    ID = db.Column(db.String())
    Description = db.Column(db.String(), nullable=False)
    Date = db.Column(db.String(), nullable=False)
    Category = db.Column(db.String(), nullable=False)
    Area = db.Column(db.String(), nullable=False)
    Status = db.Column(db.String(), nullable=False)

class Final(db.Model):
    No = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    ID = db.Column(db.String())
    Description = db.Column(db.String(), nullable=False)
    Date = db.Column(db.String(), nullable=False)
    Category = db.Column(db.String(), nullable=False)
    Area = db.Column(db.String(), nullable=False)
    Status = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'Item {self.ID}'