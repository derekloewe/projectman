from datetime import datetime
import arrow
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Task

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name_first = StringField('First Name', validators=[DataRequired()])
    name_last = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    name_first = StringField('First Name', validators=[DataRequired()])
    name_last = StringField('Last Name', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    date_modified = DateTimeField(datetime.utcnow())
    password = PasswordField('Password', validators=[])
    password2 = PasswordField(
            'Repeat Password', validators=[])
    current_password = PasswordField('Current Password', validators=[])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username')

class TaskForm(FlaskForm):
    name = TextAreaField('Task Name', validators=[DataRequired(), Length(min=1, max=140)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=300)])
    submit = SubmitField('Submit')
    