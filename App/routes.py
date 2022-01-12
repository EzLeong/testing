from App import app
from flask import render_template, redirect, url_for, flash
from App.models import Report, User
from App.forms import RegisterForm, LoginForm
from App import db
from flask_login import login_user


@app.route('/')
@app.route('/home')
def home_Page():
    return render_template('home.html')

@app.route('/report')
def report_Page():
    items = Report.query.all()
    return render_template('report.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_Page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(Username = form.Username.data,
                              Email = form.Email.data,
                              password = form.Password_1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('report_Page'))
    if form.errors != {}: #if there are no errors from the validation
        for err_msg in form.errors.values():
            flash(f'There was an error with creating user account: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login_Page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(Username=form.Username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.Password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.Username}', category='success')
            return redirect(url_for('report_Page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)