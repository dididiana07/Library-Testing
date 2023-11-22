from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields import StringField, SubmitField, PasswordField, BooleanField

class SignIn(FlaskForm):
    """Create a class that inherits from FlaskForm to create a Sign In field."""
    username = StringField(name="Username", validators=[DataRequired()])
    password = PasswordField(name="Password", validators=[DataRequired()])
    session = BooleanField(name="Keep me logged in")
    submit = SubmitField(name="Sign In")


class Register(FlaskForm):
    """Create a class that inherits from FlaskForm to create a Register form."""
    username = StringField(name="Username", validators=[DataRequired()])
    email = StringField(name="Email", validators=[DataRequired()])
    password = PasswordField(name="Password", validators=[DataRequired()])
    submit = SubmitField(name="Register")
