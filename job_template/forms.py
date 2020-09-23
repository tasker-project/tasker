# 2020-09-23 09:56:33 -0700 - Maged Bebawy - started working on forms and models files - lines:,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo, email

class JobTemplate(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    repetition = IntegerField('Repetition', validators=[DataRequired()])
    interval = IntegerField('Interval', validators=[DataRequired()])
    submit = SubmitField('Submit')
