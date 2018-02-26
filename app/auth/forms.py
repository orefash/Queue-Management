# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired#, Email, EqualTo

from flask.ext.wtf import Form
from wtforms import validators
from wtforms.widgets import Input


from ..models import Customer

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    phone_no = StringField('Phone No.', validators=[DataRequired()])
    #submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    phone_no = StringField('Phone No.', validators=[DataRequired()], render_kw={"placeholder": "Phone No."})
    #submit = SubmitField('Login')