################################################################################
# At this page, we will do the imports related to forms and users
#   - The new member of this section is filefield and fileallowed.
#       They will allow the user to update a png or jpeg file as profile picture
#
################################################################################

# Imports related to Forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# Imports related to Users
from flask_login import current_user
from project_1.models import User

# Now we create the login form where we inherit from FlaskForm
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

# Now we create our registrationform, where we also inherit from FlaskForm
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message = 'Passwords must match')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

# Now we will create a function that checks whether the email and username has
# already been used by another profile. The User, is what we import from models.
# In other words, we are checking if the email and username is unique
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has already been registered')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your username has already been registered')

# Now we will add in the ability to update the userform and have a profile picture
# we specify jpg and png, so they dont upload an excel sheet
class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('UserName', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
