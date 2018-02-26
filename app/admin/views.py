# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
import app
import datetime
from . import admin
from forms import LoginForm, RegistrationForm
from .. import db
from .admin_model import Employee
from ..models import Customer, CurrentId, Customerstore, Removed
import requests
from sqlalchemy import text
from flask import session


@admin.route("/customers/push/<int:a>", methods=['GET', 'POST'])
def pushqueue(a):
    print("Pushed!! "+str(a), file=sys.stderr)
    try:
        #current_id.current = current_id.current + 1
        current_id1 = CurrentId.query.get_or_404(1)
        current_idp = CurrentId.query.get_or_404(2)
        if (current_idp.current != a):
            customer1 = Customer.query.get_or_404(current_idp.current)
            customer1.is_done=1
            db.session.commit()
        if (current_id1.current):
            customer1 = Customer.query.get_or_404(current_id1.current)
            customer1.is_done=1
            db.session.commit()
        customer = Customer.query.get_or_404(a)
        customer.is_current = 1
        customer.is_done = 1
        name = customer.name
        print("In pushq name: "+name, file=sys.stderr)
        no = customer.phone_no

        current_id = CurrentId.query.get_or_404(2)
        current_id.current = a
        db.session.commit()
    except:
        flash("Error in queue")
        return redirect(url_for('admin.list_customers'))
    #print("After exec", file=sys.stderr)
    try:
        send_msg(name, no, a)
        flash(" Sent to customer: "+str(a))
    except:
        print("Msg not sent", file=sys.stderr)

    return redirect(url_for('admin.list_customers'))


@admin.route("/charts")
def chart():
    labels = ["January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8]
    return render_template('admin/info.html', values=values, labels=labels)

@admin.route("/chartdemo")
def chartdemo():
    labels = ["January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8]
    return render_template('admin/chart.html', values=values, labels=labels)

@admin.route("/charts/trial")
def trial():
    print('Trial done!', file=sys.stderr)
    a = datetime.datetime.today().date()
    today = a.weekday()
    print(today, file=sys.stderr)
    numdays = today
    dateList = []
    for x in range (0, numdays):
        dateList.append(a - datetime.timedelta(days = x))
    print(dateList, file=sys.stderr)
    
    #query = "TRUNCATE TABLE customers"
    #sql = text(query)
    #result = db.engine.execute(sql)
    h = datetime.date(2017, 10, 17)
    v = datetime.date(year=2017,month=10,day=17)
    dat = h
    #dat = datetime.date.today()
    print (dat, file=sys.stderr)
    try:
        #query = 'select * from customerstore where date(t_date)=%s' %dat
        posts = Customerstore.query.filter(Customerstore.t_date <= dat)
        #print (query, file=sys.stderr)
        #sql = text(query)
        #result = db.engine.execute(sql).fetchall()
        print ("Query worked:", file=sys.stderr)
        print (posts , file=sys.stderr)
        for row in posts:
            print (row , file=sys.stderr)
    except:
        print("Didn't work", file=sys.stderr)
    return redirect(url_for('admin.chart'))

@admin.route("/charts/trialday")
def daytrial():
    print('Day Trial done!', file=sys.stderr)
    a = datetime.datetime.today().date()
    today = a.weekday()
    print(today, file=sys.stderr)
    numdays = today
    dateList = []
    for x in range (0, numdays):
        dateList.append(a - datetime.timedelta(days = x))
    print(dateList, file=sys.stderr)
    return redirect(url_for('admin.chart'))


@admin.route('/' )
def homepage():
    """
    Render the homepage template on the / route
    """
    if session.get('logged_in') == True:
        return redirect(url_for('admin.dashboard'))
    else:
        form = LoginForm()
        return render_template('admin/login1.html', form=form, title='Login')
    return render_template('admin/dashboard.html', title="Welcome")

@admin.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        #return redirect(url_for('admin.login'))
        return redirect(url_for('admin.login'))

    # load registration template
    return render_template('admin/reg2.html', form=form, title='Register')

@admin.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            # log employee in
            session['logged_in'] = True
            login_user(employee)
            

            # redirect to the dashboard page after login
            return redirect(url_for('admin.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('admin/login1.html', form=form, title='Login')

@admin.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('admin.login'))

@admin.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('admin/dashboard.html', title="Dashboard")

@admin.route('/customers', methods=['GET', 'POST'])
@login_required
def list_customers():
    """
    List all customer
    """
    #logger.warning('A warning message is sent.')
    #logger.error('An error message is sent.')
    print('Hello world!', file=sys.stderr)
    customers = Customer.query.all()
    return render_template('admin/customers/customer1.html',
                           customers=customers, title="Customers")

def send_msg(name, number, id):
    # -*- coding: utf-8 -*-
    msg = "Hello "+name+", it's now your turn!. (Token Z"+str(id)+"). Please proceed to the counter.\n"

    
    mal = u'നമസ്കാരം '.encode("utf-8")
    mal1 = u'. താങ്കളുടെ ഊഴം ആയിരിക്കുന്നു. ദയവായി കൗണ്ടറിലേക്ക് സമീപിക്കുക.'.encode("utf-8")
    mallu = mal+name+mal1
    msg = msg + mallu
    #print(msg, file=sys.stderr)
    
    mobile = number
    sid = "ZugoTL"
    ura = "http://smshorizon.co.in/api/sendsms.php?user=zugo&apikey=G6gNVWxbBr4E5bsNd6fX&mobile="+mobile+"&message="+msg+"&senderid="+sid+"&type=uni"
    #ura= "http://bhashsms.com/api/sendmsg.php?user=success&pass=123456&sender=sppurt&phone="+mobile+"&text="+msg+"&priority=ndnd&stype=normal"
    resp = requests.get(ura)


def chknext():
    #pass
    current_id = CurrentId.query.get_or_404(1)
    a = current_id.current
    customer = Customer.query.get_or_404(a)
    if (customer.is_done):
        current_id.current = current_id.current +1
        db.session.commit()
        chknext()
    else:
        print("Done checking", file=sys.stderr)





@admin.route('/customers/next', methods=['GET', 'POST'])
@login_required
def next_customer():
    try:
        current_id = CurrentId.query.get_or_404(1)
        current_2 = CurrentId.query.get_or_404(2)
        a = current_2.current
        try:
            customer = Customer.query.get_or_404(a)
            if (a!=current_id.current):
                try:
                    if (customer.is_current):
                        print("Pushed is current", file=sys.stderr)
                        customer.is_done = 1
                        db.session.commit()

                    if ((current_id.current + 1)==a):
                        print("Pushed is next", file=sys.stderr)
                        current_id.current = current_id.current + 1
                        db.session.commit()
                except:
                    print("Error with pushed", file=sys.stderr)
        except:
            print("Pushed is wrong", file=sys.stderr)

        #chknext()

        try:
            #print("Current : "+str(current_id.current), file=sys.stderr)
            customer = Customer.query.get_or_404(current_id.current)
            customer.is_done = 1
            customer.is_current = 0
            db.session.commit()
        except:
            print("Before exec. curretn", file=sys.stderr)
        #print("Before exec", file=sys.stderr)
        try:
            current_id.current = current_id.current + 1
            customer = Customer.query.get_or_404(current_id.current)
            customer.is_current = 1
            name = customer.name
            #print("In exec name: "+name, file=sys.stderr)
            no = customer.phone_no
            db.session.commit()
        except:
            flash("No next customer")
            return redirect(url_for('admin.list_customers'))
        #print("After exec", file=sys.stderr)
        try:
            send_msg(name, no, current_id.current)
            flash(" Sent to customer: "+str(current_id.current))
        except:
            current_id.current = current_id.current - 1
            #customer = Customer.query.get_or_404(current_id.current)
            #customer.is_current = 0
            db.session.commit()
            flash("Couldn't send message to: "+str(no))
    except Exception as e:
        #raise e
        flash("Error in Queue")
        pass
    
    return redirect(url_for('admin.list_customers'))

@admin.route('/customers/reset', methods=['GET', 'POST'])
@login_required
def reset_customer():
    """
    Edit a department
    """
    print("In reset", file=sys.stderr)
    try:
        query = "TRUNCATE TABLE customers"
        sql = text(query)
        result = db.engine.execute(sql)

        current_id = CurrentId.query.get_or_404(1)
        current_id.current = 0
        db.session.commit()

        current_id = CurrentId.query.get_or_404(2)
        current_id.current = 0
        db.session.commit()

        flash("Customer list reset")
    except Exception as e:
        flash("Error in Queue")
        pass
    
    return redirect(url_for('admin.list_customers'))

