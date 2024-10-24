import re
import bleach
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from sequences.models import User


class RegisterForm(FlaskForm):

    # Password complexity validation
    def validate_password1(self, password_to_check):
        password = password_to_check.data
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[@$!%*?&]", password):
            raise ValidationError("Password must contain at least one special character (@, $, !, %, *, ?, &).")
    
    def validate_username(self, username_to_check):
        # Sanitize the username input
        sanitized_username = bleach.clean(username_to_check.data)

        user = User.query.filter_by(username=sanitized_username).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

        # Set the sanitized data back to the form field
        self.username.data = sanitized_username

    def validate_email_address(self, email_address_to_check):
        # Sanitize the email address input
        sanitized_email = bleach.clean(email_address_to_check.data)

        email_address = User.query.filter_by(email_address=sanitized_email).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

        # Set the sanitized data back to the form field
        self.email_address.data = sanitized_email

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    
    def validate_username(self, username_to_check):
        # Sanitize the username input before processing
        sanitized_username = bleach.clean(username_to_check.data)
        self.username.data = sanitized_username

    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class AddItemForm(FlaskForm):
    submit = SubmitField(label='Add Pose')


class RemoveItemForm(FlaskForm):
    submit = SubmitField(label='Remove Pose')
