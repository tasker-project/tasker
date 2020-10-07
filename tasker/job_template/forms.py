# 2020-10-04 14:14:23 -0700 - Emily Martens - cleaning up messy code. - lines:,53
# 2020-09-23 09:56:33 -0700 - Maged Bebawy - started working on forms and models files - lines:,6,9,10,17,46,54,55
# 2020-10-04 23:26:44 -0400 - Jeremy Axmacher - Add job template deletion - lines:,11,12,13,14,15
# 2020-09-29 16:36:00 -0400 - Jeremy Axmacher - Add initial job template form and creation logic - lines:,8,16,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,56,57,58,59,60,61,62
# 2020-09-29 16:36:00 -0400 - Jeremy Axmacher - Clean up job template form and job template detail field formatting - lines:,7,18
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, TextAreaField
from wtforms.fields.html5 import IntegerField, DateField
from wtforms.validators import DataRequired, EqualTo, email


class DeleteConfirmationForm(FlaskForm):
    submit = SubmitField('Delete')


class JobTemplateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
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
    #validators=[DataRequired()])
    repetition = IntegerField('Repetition', validators=[DataRequired()])
    interval = SelectField('Interval', validators=[DataRequired()], coerce=int, choices=[
        ('1', 'Day(s)'),
        ('2', 'Week(s)'),
        ('3', 'Month(s) (30 days)')
    ])
    #validators=[DataRequired()])
    starting_date = DateField('Starting', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_starting_date(form, field):
        print('Custom validator')
        print(field)
        print('Custom validator')
        return
        if len(field.data) > 50:
            raise ValidationError('Name must be less than 50 characters')
