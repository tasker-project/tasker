from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo, email

class JobTemplate(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    repetition = IntegerField('Repetition', validators=[DataRequired()])
    interval = IntegerField('Interval', validators=[DataRequired()])
    submit = SubmitField('Submit')





