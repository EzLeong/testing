from App import app
from flask import render_template, redirect, url_for, flash, request
from App.models import Report, User, Final
from App.forms import RegisterForm, LoginForm, ReportForm
from App import db
from flask_login import login_user, logout_user, login_required
from datetime import datetime
import string
import random

def ran_gen(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

@app.route('/')
@app.route('/home')
def home_Page():
    return render_template('home.html')

@app.route('/report', methods=['GET','POST'])
def report_Page():
    items = Report.query.all()
    form = ReportForm()
    if request.method == 'POST':

        ID_to_Add = ran_gen(8, "ABCDEFGHIJKLMNOPQRSTUVQXYZ1234567890")
        for item in items:
            if ID_to_Add == item.ID:
                ID_to_Add = ran_gen(8, "ABCDEFGHIJKLMNOPQRSTUVQXYZ1234567890")

        now = datetime.now()
        date_to_Add = now.strftime("%m/%d/%Y, %H:%M:%S")
        status_Update = "Pending"
        report_to_create = Report(Area = request.form['selected_Area'],
                              Category = request.form['selected_Category'],
                              Description = request.form['selected_Description'],
                              ID = ID_to_Add,
                              Date = date_to_Add,
                              Status = status_Update)
        db.session.add(report_to_create)
        db.session.commit()

        temp_items = Report.query.all()

        for item in temp_items:
            temp_to_create = Final(Area = item.Area,
                                Category = item.Category,
                                Description = item.Description,
                                ID = item.ID,
                                Date = item.Date,
                                Status = item.Status)
            db.session.add(temp_to_create)
            db.session.commit()


        new_items = Final.query.all()
        db.session.query(Report).delete()
        db.session.commit()

        for item in new_items:
            final_to_create = Report(Area = item.Area,
                                Category = item.Category,
                                Description = item.Description,
                                ID = item.ID,
                                Date = item.Date,
                                Status = item.Status)
            db.session.add(final_to_create)
            db.session.commit()
        

        db.session.query(Final).delete()
        db.session.commit()

        flash(f"You've submitted a report {final_to_create.ID}", category = "success")
        return redirect(url_for('report_Page'))

    return render_template('report.html', items=items, form=form)

@app.route('/admin')
@login_required
def admin_Page():
    items = Report.query.all()

    return render_template('admin.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_Page():
    form = RegisterForm()
    Admin_Code = "ADMIN123"
    if form.validate_on_submit():
        if form.CODE.data == Admin_Code:
            user_to_create = User(Username = form.Username.data,
                                Email = form.Email.data,
                                password = form.Password_1.data)
            db.session.add(user_to_create)
            db.session.commit()

            login_user(user_to_create)
            flash(f"Account created successfully! You're now logged in as {user_to_create.Username}", category = "success")

            return redirect(url_for('report_Page'))

        else:
            flash(f'CODE is invalid! Please try again', category="danger")


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
            return redirect(url_for('admin_Page'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_Page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_Page"))

@app.route('/delete/<int:No>')
def delete_Item(No):
    items = Report.query.get_or_404(No)

    try:
        db.session.delete(items)
        db.session.commit()

        temp_items = Report.query.all()
        
        for item in temp_items:
            temp_to_create = Final(Area = item.Area,
                                Category = item.Category,
                                Description = item.Description,
                                ID = item.ID,
                                Date = item.Date,
                                Status = item.Status)
            db.session.add(temp_to_create)
            db.session.commit()


        new_items = Final.query.all()
        db.session.query(Report).delete()
        db.session.commit()

        for item in new_items:
            final_to_create = Report(Area = item.Area,
                                Category = item.Category,
                                Description = item.Description,
                                ID = item.ID,
                                Date = item.Date,
                                Status = item.Status)
            db.session.add(final_to_create)
            db.session.commit()

        db.session.query(Final).delete()
        db.session.commit()

        flash("Successfully deleted", category='success')
        return redirect(url_for('admin_Page'))

    except:
        flash("There's a problem deleting that task", category='danger')

    return render_template('admin.html')

