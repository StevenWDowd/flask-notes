from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class RegisterUserForm(FlaskForm):
    """Form for registering user."""
    username = StringField("Username",
                           validators=[InputRequired(), Length(6, 20)])
    email = StringField("Email",
                        validators=[InputRequired(), Email()])
    password = PasswordField("Password",
                             validators=[InputRequired(), Length(6, 30)])
    first_name = StringField("First Name",
                             validators=[InputRequired(), Length(1, 30)])
    last_name = StringField("Last Name",
                            validators=[InputRequired(), Length(1, 30)])

class LoginUserForm(FlaskForm):
    """Form for logging in user."""
    username = StringField("Username",
                           validators=[InputRequired(), Length(0, 20)])
    password = PasswordField("Password",
                             validators=[InputRequired(), Length(6, 30)])