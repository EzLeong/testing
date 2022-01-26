from asyncio.windows_events import NULL
from App import app
from flask import render_template, redirect, url_for, flash, request
from App.models import Report, User, Final, Emergency
from App.forms import RegisterForm, LoginForm, ReportForm, SearchForm
from App import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
import string
import random

def ran_gen(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form) 

@app.route('/')
@app.route('/home')
def home_Page():
    return render_template('home.html')

@app.route('/track')
def track_Page():
    track_User = current_user.Username
    items = Report.query.filter(Report.Username.like(track_User)).all()
    return render_template('track.html',items=items)

@app.route('/emergency')
def emergency_Page():
    items = Emergency.query.all()
    return render_template('emergency.html', items=items)

@app.route('/search', methods=['POST'])
def search_Page():
    form = SearchForm()
    items = Report.query.all()
    if form.validate_on_submit():

        if form.Searched.data != "":
            searched_Inputs = form.Searched.data
            searched_Items = "%{}%".format(searched_Inputs)
            Searched = Report.query.filter(Report.ID.like(searched_Items)).all()

            flash(f'Successfully searched for the report', category='success')
            return render_template("search.html", form=form, items=items, Searched=Searched)

        else:
            flash(f'Search Invalid! Please try again!', category='danger')

    return render_template("search.html", form=form, items=items)


@app.route('/report', methods=['GET','POST'])
@login_required
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
                              Status = status_Update,
                              Username = current_user.Username)
        db.session.add(report_to_create)
        db.session.commit()

        flash(f"You've submitted a report {report_to_create.ID}", category = "success")
        return redirect(url_for('report_Page'))

    return render_template('report.html', items=items, form=form)

@app.route('/admin')
@login_required
def admin_Page():
    if current_user.Username != "Admin123" :
        flash(f"You're not authorized to access the page!", category = "danger")
        return redirect(url_for('home_Page'))
    
    else:
        items = Report.query.all()
        return render_template('admin.html', items=items)


@app.route('/register', methods=['GET', 'POST'])
def register_Page():
    form = RegisterForm()
    Admin_Code = "CONFIRM"
    if form.validate_on_submit():
        if form.CODE.data == Admin_Code:
            user_to_create = User(Username = form.Username.data,
                                Email = form.Email.data,
                                Password = form.Password_1.data)
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
        if attempted_user.Password == form.Password.data:
            """ and attempted_user.check_password_correction(
                    attempted_password=form.Password.data
            ):"""
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.Username}', category='success')
            return redirect(url_for('home_Page'))

        else:
                flash('Failure in Login invalid!', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_Page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_Page"))

@app.route('/delete/<int:No>')
def delete_Item(No):
    items = Report.query.get_or_404(No)
    x = items.ID

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

        flash(f'Successfully deleted report: {x}', category='success')
        return redirect(url_for('admin_Page'))

    except:
        flash("There's a problem deleting that task", category='danger')

    return render_template('admin.html')

@app.route('/update/<int:No>', methods=['GET','POST'])
def update_Item(No):
    items = Report.query.get_or_404(No)
    form = ReportForm()


    if request.method == 'POST':
        items.Area = request.form['selected_Area']
        items.Category = request.form['selected_Category']
        items.Description = request.form['selected_Description']
        items.Status = request.form['selected_Status']

        try:
            db.session.commit()
            flash(f"You've updated report: {items.ID}", category = "success")
            return redirect(url_for('admin_Page'))

        except:
            flash("There's a problem updating that report", category='danger')

    else:
        return render_template('update.html', items=items)

    return render_template('admin.html',items=items, form=form)

<<<<<<< Updated upstream
<<<<<<< Updated upstream


@app.route('/graph', methods=['GET','POST'])
def graph():
    items = Report.query.all()
    form = ReportForm()

    return render_template('graph.html', items=items, form=form)
=======
=======
>>>>>>> Stashed changes
@app.route('/graph')
def graph():
    data = [
        ("01-01-2020",123),
        ("02-01-2020",456),
    ]

    labels = [row[0] for row in data]
    values = [row[1] for row in data]


<<<<<<< Updated upstream
    return render_template ('graph.html', labels=labels, values = values)
>>>>>>> Stashed changes
=======
    return render_template ('graph.html', labels=labels, values = values)
>>>>>>> Stashed changes
