# 2020-10-05 08:28:49 -0400 - ADM Wayne Bryan - Added form to create a single task, /add_task - lines:,13
# 2020-09-23 09:56:33 -0700 - Maged Bebawy - started working on forms and models files - lines:,8,12,14,15,16
# 2020-10-04 23:10:10 -0700 - Maged Bebawy - Added delete task - lines:,49,51
# 2020-10-04 12:16:06 -0700 - Emily Martens - finalize fields for form and template - lines:,9,47
# 2020-10-05 20:17:43 -0400 - ADM Wayne Bryan - Added hour for user to create a single task - lines:,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42
# 2020-10-04 23:13:36 -0700 - Maged Bebawy - Added delete task - lines:,50
# 2020-10-04 12:16:06 -0700 - Emily Martens - add Snooze form and template fields - lines:,10,11,43,44,45,46,48
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
