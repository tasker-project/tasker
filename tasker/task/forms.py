from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, PasswordField, SelectField, validators
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    due_date = DateField('Due date', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SnoozeTaskForm(FlaskForm):
    due_date = DateField('Due Date', validators=[DataRequired()])
    note = StringField('Note', [validators.Length(min=0, max=1000)])
    submit = SubmitField('Snooze')
