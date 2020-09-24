from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, PasswordField, SelectField, DateField
from wtforms.validators import DataRequired, EqualTo, email

class Task(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    due_date = DateField('Due date', validators=[DataRequired()])
    submit = SubmitField('Submit')