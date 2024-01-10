from sequences import app, db
from flask import render_template, redirect, url_for, flash, request
from sequences.models import Item, User
from sequences.forms import RegisterForm, LoginForm, AddItemForm, RemoveItemForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/sequencing', methods=['GET', 'POST'])
@login_required
def sequencing_page():
    items = [
        {'id': 1, 'name': 'Childs Pose', 'sanskrit': 'Balasana', 'level': 'Beginner',
         'focus': 'Forward Bend, Hip-Opening, and Restorative', 'image': '../static/images/childs-pose.jpg'},
        {'id': 2, 'name': 'Cobra Pose', 'sanskrit': 'Bhujangasana', 'level': 'Beginner',
         'focus': 'Chest-Opening and Backbend', 'image': '../static/images/cobra-pose.jpg'},
        {'id': 3, 'name': 'Extended Side Angle', 'sanskrit': 'Utthita Parsvakonasana', 'level': 'Beginner',
         'focus': 'Standing and Strengthening', 'image': '../static/images/extended-side-angle.jpg'},
        {'id': 4, 'name': 'Forward Fold', 'sanskrit': 'Padangusthasana', 'level': 'Beginner',
         'focus': 'Forward Bend and Standing', 'image': '../static/images/forward-fold.jpg'},
        {'id': 5, 'name': 'Halfway Lift', 'sanskrit': 'Ardha Uttanasana', 'level': 'Beginner',
         'focus': 'Forward Bend and Standing', 'image': '../static/images/halfway-lift.jpg'},
        {'id': 6, 'name': 'Mountain Pose', 'sanskrit': 'Tadasana', 'level': 'Beginner',
         'focus': 'Standing', 'image': '../static/images/mountain-pose.jpg'},
        {'id': 7, 'name': 'Cat Pose', 'sanskrit': 'Marjaryasana', 'level': 'Beginner',
         'focus': 'Core', 'image': '../static/images/cat-pose.jpg'},
        {'id': 8, 'name': 'Triangle', 'sanskrit': 'Utthita Trikonasana', 'level': 'Beginner',
         'focus': 'Standing and Strengthening', 'image': '../static/images/triangle.jpg'},
        {'id': 9, 'name': 'Warrior I', 'sanskrit': 'Virabhadrasana I', 'level': 'Beginner',
         'focus': 'Standing and Strengthening', 'image': '../static/images/warrior-I.jpg'},
        {'id': 10, 'name': 'Warrior II', 'sanskrit': 'Virabhadrasana II', 'level': 'Beginner',
         'focus': 'Strengthening, Balancing, and Standing', 'image': '../static/images/warrior-II.jpg'}
    ]
    add_form = AddItemForm()
    remove_form = RemoveItemForm()
    if request.method == "POST":
        # Add Item Logic
        added_item = request.form.get('added_item')
        a_item_object = Item.query.filter_by(name=added_item).first()
        if a_item_object:
            flash(f"You have added {a_item_object.name} ",
                  category='success')

        # Remove Item Logic
        removed_item = request.form.get('removed_item')
        s_item_object = Item.query.filter_by(name=removed_item).first()
        if s_item_object:
            s_item_object.remove(current_user)
            flash(f"You have removed {s_item_object.name}", category='success')
        return redirect(url_for('sequencing_page'))

    return render_template('sequencing.html', items=items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('sequencing_page'))
    if form.errors != {}:  # If there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
