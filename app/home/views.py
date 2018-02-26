
from flask_login import login_required
from flask import flash, redirect, render_template, url_for
from . import home

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    #return render_template('home/index.html', title="Welcome")
    return redirect(url_for('auth.register'))

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")