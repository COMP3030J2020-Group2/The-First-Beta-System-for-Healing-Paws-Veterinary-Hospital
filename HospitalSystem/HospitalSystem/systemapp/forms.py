from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, TextAreaField, IntegerField, SelectMultipleField, SelectField, RadioField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class PetSignUpForm(FlaskForm):
    petname = StringField('Pet Name', validators=[DataRequired()])
    type = SelectField('Type',coerce=int, choices=[(0, 'Please Choice'),(1, 'Cat'), (2, 'Dog')],default = 0)
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)
    submit = SubmitField('Sign In')


class AppointmentForm(FlaskForm):
    pets = SelectField('Choose Pet', validators=[DataRequired()], default=1, coerce=int)
    location = SelectField('Choose Pet', choices=[(1, 'Beijing'),(2, 'Shanghai'), (3, 'Chengdu')], default=1, coerce=int)
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmergencyAppointmentForm(FlaskForm):
    pets = SelectField('Choose Pet', validators=[DataRequired()], default=1, coerce=int)
    location = SelectField('Choose Location', choices=[(1, 'Beijing'),(2, 'Shanghai'), (3, 'Chengdu')], default=1, coerce=int)
    submit = SubmitField('Submit')


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class InformationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Register')

class StaffLoginForm(FlaskForm):
    staffname = StringField('Staff Name',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('remember me',default=False)
    submit = SubmitField('Sign in')

class QuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AnswerForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class StaffSignupForm(FlaskForm):
    staffname = StringField('Staff Name',validators=[DataRequired()])
    level = IntegerField('Level',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired()])
    submit = SubmitField('Sign up')
