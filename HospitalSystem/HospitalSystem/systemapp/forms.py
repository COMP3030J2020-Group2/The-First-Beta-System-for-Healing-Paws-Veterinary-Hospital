from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField
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