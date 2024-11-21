from sequences import app, db, auth0, login_manager
from flask import render_template, redirect, url_for, flash, request, session, jsonify
from sequences.models import Item, User, Sequence, SequenceItem
from sequences.forms import RegisterForm, LoginForm, AddItemForm, RemoveItemForm
from flask_login import login_user, logout_user, login_required, current_user
import jwt
from datetime import datetime, timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

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
            # Logic to add item to user's sequence
            flash(f"You have added {a_item_object.name} to your sequence", category='success')

        # Remove Item Logic
        removed_item = request.form.get('removed_item')
        s_item_object = Item.query.filter_by(name=removed_item).first()
        if s_item_object:
            # Logic to remove item from user's sequence
            flash(f"You have removed {s_item_object.name} from your sequence", category='success')
        return redirect(url_for('sequencing_page'))

    if request.method == "GET":
        items = Item.query.all()
        owned_items = Sequence.query.filter_by(user_id=current_user.id).all()
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
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('sequencing_page'))
    if form.errors != {}:  # If there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Limit login attempts to 5 per minute per IP
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            # Generate JWT token
            payload = {'user_id': attempted_user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)}
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
            # Store token in session
            session['token'] = token
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('sequencing_page'))
        else:
            flash('Username and password do not match', category='danger')
    return render_template('login.html', form=form)

@app.route('/auth0_login')
def auth0_login():
    return auth0.authorize_redirect(redirect_uri='http://127.0.0.1:5000/callback',
                                    audience='https://dev-b1chlna5prtx13oi.us.auth0.com/api/v2/')

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    user = User.query.filter_by(email_address=userinfo['email']).first()
    if not user:
        # Create a new user if not exists
        user = User(username=userinfo['name'], email_address=userinfo['email'])
        db.session.add(user)
        db.session.commit()

    login_user(user)
    flash(f'You are logged in as {user.username}', category='success')
    return redirect(url_for('sequencing_page'))

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

# Protected route that requires JWT token
@app.route('/protected', methods=['GET'])
def protected():
    # Verify JWT token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Missing token'}), 401

    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': 'Access granted', 'username': payload['username']}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/save_sequence', methods=['POST'])
@login_required
def save_sequence():
    sequence_data = request.json
    name = sequence_data['name']
    items = sequence_data['items']
    # Save sequence to the database, associating it with the current user
    sequence = Sequence(name=name, user_id=current_user.id)
    db.session.add(sequence)
    db.session.commit()

    for item_id in items:
        sequence_item = SequenceItem(sequence_id=sequence.id, item_id=item_id)
        db.session.add(sequence_item)

    db.session.commit()
    return jsonify({'message': 'Sequence saved successfully'})

@app.route('/saved_sequences')
@login_required
def saved_sequences():
    user_sequences = Sequence.query.filter_by(user_id=current_user.id).all()
    return render_template('saved_sequences.html', user_sequences=user_sequences)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/categorized_items')
def categorized_items():
    # Query all items
    items = Item.query.all()

    # Group items by level
    categorized_items = {}
    for item in items:
        if item.level not in categorized_items:
            categorized_items[item.level] = []
        categorized_items[item.level].append(item)
    
    return render_template('categorized_items.html', categorized_items=categorized_items)

