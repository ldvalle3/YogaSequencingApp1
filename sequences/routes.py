from sequences import app, db
from flask import render_template, redirect, url_for, flash, request
from sequences.models import Item, User
<<<<<<< HEAD
from sequences.forms import RegisterForm, LoginForm, AddItemForm, RemoveItemForm
from flask_login import login_user, logout_user, login_required, current_user
=======
from sequences.forms import RegisterForm, LoginForm
from sequences import db
from flask_login import login_user, logout_user, login_required
>>>>>>> af18db9b4973e3b92beddf2c27a85823c9077924


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/sequencing', methods=['GET', 'POST'])
@login_required
def sequencing_page():
    add_form = AddItemForm()
    remove_form = RemoveItemForm()
    if request.method == "POST":
        # Add Item Logic
        added_item = request.form.get('added_item')
        a_item_object = Item.query.filter_by(name=added_item).first()
        if a_item_object:
            a_item_object.add(current_user)
            flash(f"You have added {a_item_object.name} ",
                  category='success')

        # Remove Item Logic
        removed_item = request.form.get('removed_item')
        s_item_object = Item.query.filter_by(name=removed_item).first()
        if s_item_object:
            s_item_object.remove(current_user)
            flash(f"You have removed {s_item_object.name}", category='success')
        return redirect(url_for('sequencing_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None).all()
        owned_items = Item.query.filter_by(owner=current_user.id).all()
        return render_template('sequencing.html', items=items, add_form=add_form, owned_items=owned_items,
                               remove_form=remove_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
<<<<<<< HEAD
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('sequencing_page'))
    if form.errors != {}:  # If there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

=======
        return redirect(url_for('sequencing_page'))
    if form.errors != {}:  # if there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}", category='danger')
>>>>>>> af18db9b4973e3b92beddf2c27a85823c9077924
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
<<<<<<< HEAD
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('sequencing_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

=======
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match! Please try again!', category='danger')
>>>>>>> af18db9b4973e3b92beddf2c27a85823c9077924
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
<<<<<<< HEAD
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
=======
    flash("You have been logged out.", category='info')
    return redirect(url_for('home_page'))
>>>>>>> af18db9b4973e3b92beddf2c27a85823c9077924
