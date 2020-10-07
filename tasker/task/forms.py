from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, PasswordField, SelectField, validators
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    due_date = DateField('Due date', validators=[DataRequired()])
    hour = SelectField('Hour', validators=[DataRequired()], choices=[
        ('0', '12 AM'),
        ('1', '1 AM'),
        ('2', '2 AM'),
        ('3', '3 AM'),
        ('4', '4 AM'),
        ('5', '5 AM'),
        ('6', '6 AM'),
        ('7', '7 AM'),
        ('8', '8 AM'),
        ('9', '9 AM'),
        ('10', '10 AM'),
        ('11', '11 AM'),
        ('12', '12 PM'),
        ('13', '1 PM'),
        ('14', '2 PM'),
        ('15', '3 PM'),
        ('16', '4 PM'),
        ('17', '5 PM'),
        ('18', '6 PM'),
        ('19', '7 PM'),
        ('20', '8 PM'),
        ('21', '9 PM'),
        ('22', '10 PM'),
        ('23', '11 PM'),
    ])
    submit = SubmitField('Submit')

class SnoozeTaskForm(FlaskForm):
    due_date = DateField('Due Date', validators=[DataRequired()])
    note = StringField('Note', [validators.Length(min=0, max=1000)])
    submit = SubmitField('Snooze')

class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Delete')
