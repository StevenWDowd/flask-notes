from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class RegisterUserForm(FlaskForm):
    username = StringField("Username", 
                           validators=[InputRequired(), Length(20)])
    email = StringField("Email", 
                        validators=[InputRequired(), Email()])
    password = PasswordField("Password", 
                             validators=[InputRequired(), Length(8, 30)])
    first_name = StringField("First Name", 
                             validators=[InputRequired(), Length(30)])
    last_name = StringField("Last Name", 
                            validators=[InputRequired(), Length(30)])

class LoginUserForm(FlaskForm):
    username = StringField("Username", 
                           validators=[InputRequired(), Length(20)])
    password = PasswordField("Password", 
                             validators=[InputRequired(), Length(8, 30)])