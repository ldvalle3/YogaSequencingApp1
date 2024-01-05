from run import app
from flask import render_template
from sequences.models import Item
from sequences.forms import RegisterForm


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/sequencing')
def sequencing_page():
    items = Item.query.all()
    return render_template('sequencing.html', items=items)


@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)
