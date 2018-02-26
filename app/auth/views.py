 # -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from datetime import datetime
from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Customer, Customerstore
import requests
import unicodedata

def send_msg(number, id):
    msg = "Your token number is Z"+str(id)+" . There are 2 customers in line before you . We will let you know as soon as its your turn . Meantime you can use our free wifi as our small way of thanking your patience .\n"
    mal = u'താങ്കളുടെ ടോക്കൺ നമ്പർ Z'.encode("utf-8")
    i = str(id)
    mal2 = u' ആണ്. താങ്കൾക്ക് മുമ്പിൽ രണ്ട് പേർ അവസരം കാത്തിരിപ്പുണ്ട്. താങ്കളുടെ ഊഴം വരുമ്പോൾ ഞങ്ങൾ അറിയിക്കുന്നതായിരിക്കും. താങ്കളുടെ ക്ഷമയ്ക്ക് കൃതജ്ഞത രേഖപ്പെടുത്തുന്നതോടൊപ്പം ഞങ്ങളുടെ ചെറിയ ഒരു ഉപഹാരമായി സൗജന്യ വൈഫൈ താങ്കൾക്ക് ഉപയോഗിക്കാവുന്നതാണ്.'.encode("utf-8")
    mal = mal + i + mal2
    msg = msg + mal
    #print(msg, file=sys.stderr)
    mobile = number
    sid = "ZugoTL"
    ura = "http://smshorizon.co.in/api/sendsms.php?user=zugo&apikey=G6gNVWxbBr4E5bsNd6fX&mobile="+mobile+"&message="+msg+"&senderid="+sid+"&type=uni"
    resp = requests.get(ura)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    
    if form.validate_on_submit():
        
        customer = Customer(
                            name=form.name.data,
                            age=form.age.data,
                            phone_no=form.phone_no.data,
                            t_date=datetime.now())
        customerstore = Customerstore(
                            name=form.name.data,
                            age=form.age.data,
                            phone_no=form.phone_no.data,
                            t_date=datetime.now())
        """if Customerstore.query.filter_by(phone_no = str(form.phone_no.data)) != None:
            print("customer exists!!", file=sys.stderr)
        else:
            print("customer not exists!!", file=sys.stderr)
            db.session.add(customerstore)
            db.session.commit()"""
        count = Customerstore.query.filter_by(phone_no = str(form.phone_no.data)).count()
        if count > 0:
            print("customer exists!!", file=sys.stderr)
        else:
            print("customer not exists!!", file=sys.stderr)
            db.session.add(customerstore)
            db.session.commit()
       
        # add employee to the database        
        try:
            db.session.add(customer)
            db.session.commit()
            try:
                employee = Customer.query.filter_by(phone_no=str(form.phone_no.data)).first()
                send_msg(str(form.phone_no.data), str(employee.id))
            except:
                print("msg not sent", file=sys.stderr)
            return redirect("http://google.co.in")
        except:
            db.session.rollback()            
            flash('Phone Number already exists!!!')
        
    # load registration template
    return render_template('auth/reg2.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        customer = Customer.query.filter_by(phone_no=form.phone_no.data).first()

        if customer is not None:
            # log employee in
            login_user(customer)
            #flash("logged in successfully")
            # redirect to the dashboard page after login
            return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid phone number.')

    # load login template
    return render_template('auth/login1.html', form=form, title='Login')




@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))