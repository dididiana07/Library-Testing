from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class AddBook(FlaskForm):
    """Create a class that inherits from FlaskForm to create some field to get a specific data."""
    title = StringField(name="Title", validators=[DataRequired()])
    author = StringField(name="Author", validators=[DataRequired()])
    rate = IntegerField(name="Rating", validators=[DataRequired(), NumberRange(min=0, max=5)])
    submit = SubmitField(name="Submit")
