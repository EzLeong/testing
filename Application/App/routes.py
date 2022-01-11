from App import app
from flask import render_template
from App.models import Item

@app.route('/')
@app.route('/home')
def home_Page():
    return render_template('home.html')

@app.route('/report')
def report_Page():
    items = Item.query.all()
    return render_template('report.html', items=items)