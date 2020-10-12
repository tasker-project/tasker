# 2020-10-05 08:28:49 -0400 - ADM Wayne Bryan - Added form to create a single task, /add_task - lines:,14
# 2020-09-23 09:56:33 -0700 - Maged Bebawy - started working on forms and models files - lines:,9,13,15,16,17
# 2020-10-04 23:10:10 -0700 - Maged Bebawy - Added delete task - lines:,76,78
# 2020-10-04 12:16:06 -0700 - Emily Martens - finalize fields for form and template - lines:,10,74
# 2020-10-05 20:17:43 -0400 - ADM Wayne Bryan - Added hour for user to create a single task - lines:,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43
# 2020-10-07 20:15:53 -0700 - Emily Martens - fix snooze to work with template-based and one-time tasks, remove zip folder. - lines:,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73
# 2020-10-04 23:13:36 -0700 - Maged Bebawy - Added delete task - lines:,77
# 2020-10-04 12:16:06 -0700 - Emily Martens - add Snooze form and template fields - lines:,11,12,44,45,46,47,75
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
    note = StringField('Note', [validators.Length(min=0, max=1000)])
    submit = SubmitField('Snooze')

class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Delete')
