from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from App.models import User

class RegisterForm(FlaskForm):
    def validate_Username(self, Username_to_check):
            user = User.query.filter_by(Username=Username_to_check.data).first()
            if user:
                raise ValidationError('Username already exists! Please try using a different Username')

    def validate_Email(self,Email_to_check):
            user = User.query.filter_by(Email=Email_to_check.data).first()
            if user:
                raise ValidationError('Email address already exists! Please try using a different Email address')


    Username = StringField(label='Username', validators=[Length(min=6, max=30), DataRequired()])
    Email = StringField(label='Email Address', validators=[Email(), DataRequired()])
    Password_1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    Password_2 = PasswordField(label='Confirm Password', validators=[EqualTo('Password_1'), DataRequired()])
    CODE = StringField(label='Admin Code', validators=[DataRequired()])
    Submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    Username = StringField(label='Username', validators=[DataRequired()])
    Password = PasswordField(label='Password', validators=[DataRequired()])
    Submit = SubmitField(label='Sign In')

class ReportForm(FlaskForm):
    Area = StringField(label='Area', validators=[DataRequired()])
    Category = StringField(label='Category', validators=[DataRequired()])
    Description = StringField(label='Description', validators=[DataRequired()])
    Submit = SubmitField(label='Submit')
    Status = StringField(label='Status', validators=[DataRequired()])

class SearchForm(FlaskForm):
    Searched = StringField(label='Searched', validators=[DataRequired()])
    Submit =  SubmitField(label='Submit')