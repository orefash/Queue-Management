from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db#, login_manager


class Customer(UserMixin, db.Model):
    """
    Create a Role table
    """
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    age = db.Column(db.Integer, index=True)
    phone_no = db.Column(db.String(16), index=True, unique=True)
    is_done = db.Column(db.Boolean, default=False) #note this
    is_current = db.Column(db.Boolean, default=False) #note this
    t_date = db.Column(db.DateTime, nullable = False)


    def __repr__(self):
        return '<Customer: {}>'.format(self.name)

class Customerstore(UserMixin, db.Model):
    """
    Create a Role table
    """
    __tablename__ = 'customerstore'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    age = db.Column(db.Integer, index=True)
    phone_no = db.Column(db.String(16), index=True, unique=True)
    t_date = db.Column(db.DateTime, nullable = False)


    def __repr__(self):
        return '<Customer: {}>'.format(self.name)

# Set up user_loader
#@login_manager.user_loader
#def load_user(user_id):
#    return Customer.query.get(int(user_id))

class CurrentId(db.Model):
    __tablename__ = 'currentid'
    id = db.Column(db.Integer, primary_key=True)
    current = db.Column(db.Integer, index=True)


    def __repr__(self):
        return '<CurrentId: {}>'.format(self.current)

class Removed(db.Model):
    __tablename__ = 'removed'
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, index=True)


    def __repr__(self):
        return '<Removed: {}>'.format(self.position)      