# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.fields import HiddenField
from wtforms.validators import Optional


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class GoalForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])
    type = SelectField('Type', choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], validators=[DataRequired()])
    effort_points = IntegerField('Effort Points', validators=[DataRequired()])
    submit = SubmitField('Save')

class TaskForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    is_completed = BooleanField('Is Completed')
    completed_at = StringField('Completed At')
    submit = SubmitField('Save')

class TimeSlotForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired()])
    start_time = StringField('Start Time', validators=[DataRequired()])
    end_time = StringField('End Time', validators=[DataRequired()])
    submit = SubmitField('Save')
