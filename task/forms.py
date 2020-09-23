# 2020-09-23 09:56:33 -0700 - Maged Bebawy - started working on forms and models files - lines:,2,3,4,5,6,7,8,9,10
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, PasswordField, SelectField, DateField
from wtforms.validators import DataRequired, EqualTo, email

class Task(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    due_date = DateField('Due date', validators=[DataRequired()])
    submit = SubmitField('Submit')
